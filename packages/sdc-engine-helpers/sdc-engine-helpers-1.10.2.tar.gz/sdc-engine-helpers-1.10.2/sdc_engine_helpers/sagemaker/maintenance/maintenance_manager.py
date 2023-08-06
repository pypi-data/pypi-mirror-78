"""
    Maintenance manager module
        - performs maintenance on solution, campaign, datasets
        - calls solution, campaign, datasets which interact with AWS
        - gets current states in database
        - updates states in database

    Issues:
     - boto3 does not allow subclassing & builds internal classes at runtime:
        https://boto3.amazonaws.com/v1/documentation/api/latest/guide/events.html
"""
import boto3
from sqlalchemy.exc import InternalError
from botocore.exceptions import ClientError as botocore_clienterror
from sdc_helpers.slack_helper import SlackHelper
from sdc_helpers import decorators as global_decorators
from sdc_engine_helpers.sagemaker.utils import create_resource_name
from sdc_engine_helpers.models.subscription import Subscription
from sdc_engine_helpers.date_utils import DateUtils
from sdc_engine_helpers import decorators as engine_decorators
from sdc_engine_helpers.sagemaker.sagemaker_query_helpers import \
    SagemakerEngineHelpers
from sdc_engine_helpers.sagemaker.maintenance.campaign_state_manager import \
    CampaignStateManager
from sdc_engine_helpers.sagemaker.maintenance.solution_state_manager import \
    SolutionStateManager
from sdc_engine_helpers.sagemaker.maintenance.dataset_state_manager import \
    DatasetStateManager

class MaintenanceManager:
    """
        Manage AWS SDC Engine solutions and campaigns
    """
    # pylint: disable=too-many-instance-attributes, raise-missing-from
    # flag to determine if maintenance was performed
    current_client = None
    can_perform_maintenance = False
    # get helpers
    date_utils = DateUtils()
    slack_helper = SlackHelper()

    # set up states
    solution_job_status = {
        'active': ['Completed']
    }

    def __init__(self, **kwargs):
        # get service slug
        self.service_slug = kwargs.get('service_slug', 'recommend')
        # get rds config
        rds_config = kwargs.get('rds_config', {})
        if not isinstance(rds_config, dict):
            raise TypeError('Only dict is supported for rds_config')

        # get redis config
        redis_config = kwargs.get('redis_config', {})
        if not isinstance(redis_config, dict):
            raise TypeError('Only dict is supported for redis_config')

        self.engine_slug = kwargs.get('engine_slug', 'alice')
        # instantiate query helpers
        self.query_helper = SagemakerEngineHelpers(
            rds_config=rds_config,
            redis_config=redis_config
        )
        # get service config for service slug
        self.service = self.query_helper.get_service(
            slug=self.service_slug,
            for_update=True
        )
        # create instance of sagemaker
        self.sagemaker = boto3.client('sagemaker')
        # init state managers
        self.solution_state_manager = SolutionStateManager()
        self.campaign_state_manager = CampaignStateManager()
        self.dataset_state_manager = DatasetStateManager()
        process = self.query_helper.get_process(slug='sagemaker-maintenance')
        if process is not None:
            self.query_helper.process_id = process.id

    def __del__(self):
        # finally close query helper
        if self.can_perform_maintenance:
            # reset maintenance_in_progress
            self.service = self.query_helper.get_service(
                slug=self.service_slug,
                for_update=True
            )

            self.service.properties['maintenance_in_progress'] = None
            # update service
            self.query_helper.update(
                model=self.service,
                audit=False
            )
        del self.query_helper

    def check_maintenance_is_allowed(self) -> bool:
        """
            checks if maintenance is currently in progress for a given service.
            if not, returns True allowing the current manager to take ownership and run
            maintenance else returns False to exit gracefully.

            Returns:
                bool: Whether current manager can perform maintenance.
        """
        allow_maintenance = False

        if (
                isinstance(self.service.properties, dict) and
                self.service.properties.get('maintenance_in_progress', None) is None
        ):
            allow_maintenance = True
        elif (
                self.service.properties is None
        ):
            # setting empty properties field as a dict in python model
            self.service.properties = {}
            allow_maintenance = True

        if allow_maintenance:
            # no maintenance in progress
            # run maintenance
            self.service.properties['maintenance_in_progress'] = self.engine_slug

            self.query_helper.update(
                model=self.service,
                audit=False
            )

        return allow_maintenance

    def perform_maintenance(self):
        """
            Execute maintenance that performs a set of tasks for engines
            These are specifically Update, refresh or do nothing.

            Return:
                (bool) : the outcome of maintenance "updated", "not_updated", "blocked"
        """
        maintenance_outcome = "not_updated"

        # check if maintenance can be performed
        self.can_perform_maintenance = self.check_maintenance_is_allowed()

        if self.can_perform_maintenance:
            # start maintenance
            for client in self.query_helper.get_clients():
                maintenance_mode, _ = self.query_helper.get_engine_entity(
                    client_id=client.id,
                    service_id=self.service.id,
                    engine_slug=self.engine_slug,
                    entity_key='maintenance_mode',
                    from_cache=False
                )

                if maintenance_mode is None or maintenance_mode == 'off':
                    continue

                # get subscription for engine
                subscription = self.query_helper.get_subscription(
                    client_id=client.id,
                    service_id=self.service.id,
                    from_cache=False,
                    for_update=True
                )

                self.current_client = client
                solution_updated = self.perform_solution_maintenance(
                    client=client,
                    engine_slug=self.engine_slug,
                    maintenance_mode=maintenance_mode
                )

                campaign_updated = self.perform_campaign_maintenance(
                    client=client,
                    engine_slug=self.engine_slug,
                    maintenance_mode=maintenance_mode
                )

                datasets_updated = self.perform_dataset_maintenance(
                    client=client,
                    engine_slug=self.engine_slug,
                    maintenance_mode=maintenance_mode
                )

                if any([solution_updated, campaign_updated, datasets_updated]):
                    # when any of the above have been updated
                    maintenance_outcome = self.perform_session_update(
                        subscription=subscription
                    )
        else:
            maintenance_outcome = "blocked"

        return maintenance_outcome

    @engine_decorators.retry_handler(
        exceptions=(Exception, InternalError),
        total_tries=4,
        initial_wait=0.5,
        backoff_factor=2
    )
    def perform_session_update(self, subscription: Subscription) -> bool:
        """
            Perform the session update in the database to commit update to database

            Returns:
                updated (bool): whether the database session was updated
        """
        print("Updating subscription")
        self.query_helper.update(
            model=subscription
        )
        print("clearing cache")
        self.query_helper.flush_subscription_properties_cache(
            subscription=subscription
        )

        return "updated"


    @global_decorators.general_exception_handler(
        logger=slack_helper,
        exceptions=(botocore_clienterror, Exception),
        should_raise=False
    )
    def perform_dataset_maintenance(
            self, *,
            client: object,
            engine_slug: str,
            maintenance_mode: str
    ) -> dict:
        """
            Performs dataset update maintainence

            - get state
            - for each dataset, check state for vendor
        """
        datasets_updated = False
        curr_state = {}
        if maintenance_mode != 'off':
            # get datasets
            datasets, _ = self.query_helper.get_engine_entity(
                client_id=client.id,
                service_id=self.service.id,
                engine_slug=engine_slug,
                entity_key='datasets',
                from_cache=False,
                for_update=True
            )

            if datasets is None:
                return datasets_updated

            for _, dataset in enumerate(datasets):

                label = dataset.get('label', None)
                if label is None:
                    # skip this dataset
                    continue

                new_dataset = {}

                # get solution from db
                campaign, _ = self.query_helper.get_campaign(
                    client_id=client.id,
                    service_id=self.service.id,
                    engine_slug=engine_slug,
                    from_cache=False,
                    for_update=True,
                    recipe=dataset['recipe']
                )
                # get dataset
                curr_state = self.dataset_state_manager.get_state(
                    dataset=dataset,
                    campaign=campaign
                )

                if curr_state.get('should_update') is True:

                    print(
                        'Updating dataset version for client: {client_name}'
                        .format(client_name=client.name)
                    )

                    # build cache key
                    cache_key = create_resource_name(
                        context="recommendation",
                        function=dataset['label'],
                        additional_details=[
                            self.service.id, client.id, engine_slug
                        ]
                    )

                    new_dataset = self.dataset_state_manager.update_state(
                        dataset=dataset,
                        campaign=campaign,
                        cache_key=cache_key
                    )

                    # update dataset
                    self.query_helper.update_dataset(
                        client_id=client.id,
                        service_id=self.service.id,
                        engine_slug=engine_slug,
                        label=dataset['label'],
                        config=new_dataset
                    )

                    dataset_label = dataset['label']
                    print(
                        'Successfully updated dataset version: {dataset_label}'
                        .format(dataset_label=dataset_label)
                    )

                    datasets_updated = True

        return datasets_updated


    @global_decorators.general_exception_handler(
        logger=slack_helper,
        exceptions=(botocore_clienterror, Exception),
        should_raise=False
    )
    def perform_solution_maintenance(
            self,
            *,
            client: dict,
            engine_slug: str,
            maintenance_mode: str
    ) -> dict:
        """
            Perform the required maintenance on a list of solutions

            args:
                client (dict): The client this maintenance is being performed for
                engine_slug (str): Slug of the engine involved
                maintenance_mode (str): The maintenance mode of the subscription
                                        (full/database_only)

            returns:
                result (dict): A dictionary with an updated flag and resultant solutions

        """
        solutions_updated = False
        curr_state = {}
        # get solutions
        solutions, _ = self.query_helper.get_engine_entity(
            client_id=client.id,
            service_id=self.service.id,
            engine_slug=engine_slug,
            entity_key='solutions',
            from_cache=False,
            for_update=True
        )

        if solutions is None:
            return solutions_updated

        for _, solution in enumerate(solutions):

            # The solution arn is required to continue maintenance for this solution
            arn = solution.get('arn', None)

            if arn is None:
                continue

            # get current state
            curr_state = self.solution_state_manager.get_state(
                solution=solution
            )

            if maintenance_mode == 'full' and curr_state.get('should_create_version') is True:
                print(
                    'Building solution version for client: {client_name}'
                    .format(client_name=client.name)
                )

                # train a new model if should_create_version True
                new_solution = self.solution_state_manager.update_state(
                    solution=solution,
                    client_code=client.code,
                    service_slug=self.service.slug,
                    engine_slug=engine_slug,
                )

                # get solution arn
                solution_arn = new_solution.get('arn')
                print(
                    'Successfully started creation of solution version: {solution_version_arn}'
                    .format(solution_version_arn=solution_arn)
                )

                # update immedidately and change status
                self.query_helper.update_solution(
                    client_id=client.id,
                    service_id=self.service.id,
                    engine_slug=engine_slug,
                    recipe=solution['recipe'],
                    config=new_solution
                )

                solutions_updated = True

            elif curr_state.get('should_refresh_version_status') is True:
                # update state step >> solution manager
                solution_arn = curr_state.get('arn')
                new_version_status = curr_state.get('new_version_status')

                print(
                    'Refreshing version status on solution: {arn} for client: {client_name}'
                    ' to {status}'
                    .format(
                        arn=arn,
                        client_name=client.name,
                        status=new_version_status
                    )
                )
                # update immedidately and change status
                self.query_helper.update_solution(
                    client_id=client.id,
                    service_id=self.service.id,
                    engine_slug=engine_slug,
                    recipe=solution['recipe'],
                    config={
                        'version_status': new_version_status
                    }
                )

                solutions_updated = True

        return solutions_updated


    @global_decorators.general_exception_handler(
        logger=slack_helper,
        exceptions=(botocore_clienterror, Exception),
        should_raise=False
    )
    def perform_campaign_maintenance(
            self, *,
            client: dict,
            engine_slug: str,
            maintenance_mode: str
    ) -> dict:
        """
            Perform the required maintenance on a list of campaigns

            args:
                client (dict): The client this maintenance is being performed for
                engine_slug (str): Slug of the engine involved
                maintenance_mode (str): The maintenance mode of the subscription
                                        (full/database_only)

            returns:
                result (dict): Dictionary containing:
                               1) campaigns_updated
                               2) Resultant campaigns list

        """
        campaigns_updated = False
        curr_state = {}
        # get campaigns for this engine
        campaigns, _ = self.query_helper.get_engine_entity(
            client_id=client.id,
            service_id=self.service.id,
            engine_slug=engine_slug,
            entity_key='campaigns',
            from_cache=False,
            for_update=True
        )

        if campaigns is None:
            return campaigns_updated

        for _, campaign in enumerate(campaigns):
            # The campaign arn is required to continue maintenance for this campaign
            arn = campaign.get('arn', None)

            if arn is None:
                continue

            # get related-listings solution
            solution, _ = self.query_helper.get_solution(
                client_id=client.id,
                service_id=self.service.id,
                engine_slug=engine_slug,
                from_cache=False,
                for_update=True,
                recipe=campaign['recipe']
            )

            curr_state = self.campaign_state_manager.get_state(
                campaign=campaign,
                solution=solution
            )

            if maintenance_mode == 'full' and curr_state.get('should_update') is True:

                # update campaign state >> campaign_state_manager
                latest_solution_version_arn = curr_state.get(
                    'latest_solution_version_arn'
                )

                print(
                    'Updating campaign for client: {client_name} to solution version: {arn}'
                    .format(
                        client_name=client.name,
                        arn=latest_solution_version_arn
                    )
                )

                new_campaign = self.campaign_state_manager.update_state(
                    campaign=campaign,
                    solution=solution,
                    client_code=client.code,
                    service_slug=self.service.slug,
                    engine_slug=engine_slug
                )

                print('Successfully started updating campaign: {arn}'.format(arn=arn))

                # try and update else fail
                self.query_helper.update_campaign(
                    client_id=client.id,
                    service_id=self.service.id,
                    engine_slug=engine_slug,
                    recipe=campaign['recipe'],
                    config=new_campaign
                )

                campaigns_updated = True

            elif curr_state.get('should_refresh_status') is True:
                # get current version arn
                latest_solution_version_arn = curr_state.get(
                    'latest_solution_version_arn'
                )
                new_status = curr_state.get('new_status')
                last_refreshed_at = curr_state.get('last_refreshed_at')

                print(
                    'Refreshing status on campaign: {arn} for client: {client_name} to {status}'
                    .format(
                        arn=arn,
                        client_name=client.name,
                        status=new_status
                    )
                )
                new_status = curr_state.get('new_status')
                last_refreshed_at = curr_state.get('last_refreshed_at')

                # solution refresh to account for endpoint roll-back
                # when sagemaker endpoint update fails, it rolls back
                # as such campaign in db and vendor will differ
                # this is a roll back
                refresher_solution = {
                    'status':new_status,
                    'solution_version_arn':latest_solution_version_arn,
                    'last_updated_at': last_refreshed_at
                }
                # update status in db
                self.query_helper.update_campaign(
                    client_id=client.id,
                    service_id=self.service.id,
                    engine_slug=engine_slug,
                    recipe=campaign['recipe'],
                    config=refresher_solution
                )

                campaigns_updated = True

        return campaigns_updated
