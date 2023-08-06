"""
    Campaign state manager module
"""
from datetime import datetime
import boto3
from botocore.exceptions import ClientError as botocore_clienterror
import sdc_helpers.utils as utils
from sdc_engine_helpers.sagemaker.utils import \
    build_resource_tags
from sdc_engine_helpers.date_utils import DateUtils
from sdc_engine_helpers.sagemaker.utils import name_from_base

class CampaignStateManager:
    """
        Given a database campaign object,

        1. get_state
            - call vendor API's to check if campaign needs to be updated
            OR
            - check if the campaign status in the database needs to be refreshed.
        2. update_state
            - call vendor API's to execute update workflow for campaign
            - update status of campaign in database

    """
    # pylint: disable=raise-missing-from
    # default tag to dev environment
    resource_tags = [
        {
            'Key': 'environment',
            'Value': 'dev'
        }
    ]
    date_utils = DateUtils()
    # vendor
    vendor_solution_arn_path = 'TrainingJobName'
    vendor_campaign_arn_path = 'EndpointName'
    vendor_campaign_status_path = 'EndpointStatus'
    vendor_solution_status_path = 'TrainingJobStatus'
    # input data key in TrainingJob
    vendor_campaign_solution_arn_path = 'ProductionVariants.0.VariantName'

    campaign_statuses = {
        'running':['Creating', 'Updating', 'SystemUpdating', 'Deleting'],
        'updating': ['Updating'],
        'failed':['Failed', 'RollingBack'],
        'danger':['Failed'],
        'blocking':[
            'Creating',
            'Updating',
            'SystemUpdating',
            'Deleting',
            'Failed',
            'RollingBack'
        ],
        'stopped':['OutOfService'],
        'active':['InService', None, 'None']
    }

    solution_statuses = {
        'blocking': ['InProgress', 'Stopping', 'Failed', 'Stopped'],
        'success': ['Completed', None, 'None']
    }

    dataset_statuses = {
        'active': ['Active', None, 'None'],
        'blocking': ['Updating']
    }

    def __init__(self):
        self.sagemaker = boto3.client('sagemaker')

    def sagemaker_create_model(
            self,
            training_job_name: str,
            container_image: str = None,
            resource_tags: list = None
    ) -> str:
        """
            Create model from a trained model job using Sagemaker API.
            if model exists, creation is skipped.

            note:
                - Model name is the training job name

            Args:
                TrainingJobName (str): Naming of sagemaker training job

            Returns:
                str: model name
        """
        model_name = training_job_name

        training_job_config = self.sagemaker.describe_training_job(
            TrainingJobName=training_job_name
        )

        primary_container = {
            'Image': training_job_config['AlgorithmSpecification']['TrainingImage'],
            'Mode': 'SingleModel',
            'ModelDataUrl': training_job_config['ModelArtifacts']['S3ModelArtifacts']
        }

        if container_image is not None:
            # override Image with provided image
            print((
                "Updating serving image to provided "
                "container image, {}".format(container_image)
            ))
            primary_container.update(
                {
                    'Image': container_image
                }
            )

        try:
            _ = self.sagemaker.create_model(
                ModelName=model_name,
                ExecutionRoleArn=training_job_config['RoleArn'],
                PrimaryContainer=primary_container,
                Tags=resource_tags
            )

        except botocore_clienterror as exception:
            if exception.response['Error']['Code'] == 'ValidationException':
                # handle no
                if 'Cannot create already existing model' in exception.response['Error']['Message']:
                    print((
                        "This Model already exists, "
                        "with name = {}. Using the already created model."
                        .format(model_name)
                    ))
                else:
                    # re-throw error
                    raise botocore_clienterror(
                        error_response=exception.operation_name,
                        operation_name=exception.response
                    )

        return model_name

    def sagemaker_update_campaign(
            self,
            endpoint_name: str,
            training_job_name: str,
            container_image: str = None,
            **kwargs
    ):
        """
            (Call vendor API) Creates a endpoint config
            and updates endpoint with this config

            Args:
                EndpointName (str): name of sagemaker endpoint
                TrainingJobName (str): name of sagemaker training job

            Returns:
                dict: contains names of new created resources
        """
        client_code = kwargs.get("client_code", None)
        service_slug = kwargs.get("service_slug", None)
        engine_slug = kwargs.get("engine_slug", None)
        # each endpoint configuration needs unique name
        endpoint_config_name = name_from_base(
            endpoint_name,
            max_length=63,
            short=False
        )
        resource_tags = build_resource_tags(
            current_tags=self.resource_tags,
            new_tags=[
                {
                    'Key': 'client',
                    'Value': client_code
                },
                {
                    'Key': 'environment',
                    'Value': 'prod'
                },
                {
                    'Key': 'engine',
                    'Value': engine_slug
                },
                {
                    'Key': 'service',
                    'Value': service_slug
                }
            ]
        )
        endpoint = self.sagemaker.describe_endpoint(
            EndpointName=endpoint_name
        )

        model_name = self.sagemaker_create_model(
            training_job_name=training_job_name,
            container_image=container_image,
            resource_tags=resource_tags
        )

        previous_endpoint_config = self.sagemaker.describe_endpoint_config(
            EndpointConfigName=endpoint['EndpointConfigName']
        )

        production_varients = previous_endpoint_config['ProductionVariants']
        # update the model name in production varients
        production_varients[0]['ModelName'] = model_name
        production_varients[0]['VariantName'] = model_name

        _ = self.sagemaker.create_endpoint_config(
            EndpointConfigName=endpoint_config_name,
            ProductionVariants=production_varients
        )

        _ = self.sagemaker.update_endpoint(
            EndpointName=endpoint_name,
            EndpointConfigName=endpoint_config_name
        )

        return {
            'EndpointName': endpoint_name,
            'TrainingJobName': training_job_name,
            'ModelName': model_name
        }

    def get_vendor_solution_version_arn(self, vendor_solution: dict):
        """
            Get vendor solution version status

            args:
                vendor_solution (dict): Solution from vendor

            returns:
                status (str): vendor solution version status

        """

        return utils.dict_query(
            dictionary=vendor_solution,
            path=self.vendor_solution_arn_path
        )

    def get_vendor_campaign_solution_version_arn(self, vendor_campaign: dict):
        """
            Get vendor campaign version status

            args:
                vendor_campaign (dict): Campaign from vendor

            returns:
                status (str): vendor campaign version status

        """

        return utils.dict_query(
            dictionary=vendor_campaign,
            path=self.vendor_campaign_solution_arn_path
        )

    def get_vendor_solution_status(self, vendor_solution: dict):
        """
            Get vendor solution version status

            args:
                vendor_solution (dict): Solution from vendor

            returns:
                status (str): vendor solution version status

        """

        return utils.dict_query(
            dictionary=vendor_solution,
            path=self.vendor_solution_status_path
        )

    def get_vendor_campaign_status(self, vendor_campaign: dict):
        """
            Get vendor campaign version status

            args:
                vendor_campaign (dict): Campaign from vendor

            returns:
                status (str): vendor campaign version status

        """

        return utils.dict_query(
            dictionary=vendor_campaign,
            path=self.vendor_campaign_status_path
        )

    def get_state(self, *, campaign: dict, solution: dict) -> dict:
        """
            Get the current state to action an update, refresh or do nothing
            set of actions.

            Args:
                campaign (dict): database campaign config
                solution (dict): database solution config
            Return:
                (dict): current state config

        """
        state = {
            'should_update': False,
            'should_refresh_status': False
        }

        # get vendor campaign
        vendor_campaign = self.sagemaker.describe_endpoint(
            EndpointName=campaign.get('arn')
        )
        # get vendor solution
        vendor_solution = self.sagemaker.describe_training_job(
            TrainingJobName=solution.get('arn')
        )

        vendor_solution_arn = self.get_vendor_solution_version_arn(
            vendor_solution=vendor_solution
        )

        state['should_update'] = self.should_update(
            campaign=campaign,
            vendor_campaign=vendor_campaign,
            vendor_solution=vendor_solution
        )

        if state['should_update']:
            state.update({
                'latest_solution_version_arn': vendor_solution_arn
            })

        else:
            # Check if the database arn needs to be updated
            arn = campaign.get('solution_version_arn', None)

            vendor_campaign_solution_version_arn = self.get_vendor_campaign_solution_version_arn(
                vendor_campaign=vendor_campaign
            )
            # Check if the database status needs to be updated
            status = campaign.get('status', None)

            vendor_campaign_status = self.get_vendor_campaign_status(
                vendor_campaign=vendor_campaign
            )

            if (
                    (vendor_campaign_status != status) &
                    (vendor_campaign_status not in self.campaign_statuses['blocking'])
            ):
                # update status, when it differs from vendor during updating/blocking status
                # get current refresh time, for keeping track
                current_time_at_update = datetime.strftime(
                    datetime.now(),
                    self.date_utils.get_mysql_date_format()
                )
                state['should_refresh_status'] = True
                state['new_status'] = vendor_campaign_status
                state['latest_solution_version_arn'] = vendor_campaign_solution_version_arn
                state['last_refreshed_at'] = current_time_at_update
            elif (
                    (vendor_campaign_solution_version_arn != arn) &
                    (vendor_campaign_status not in self.campaign_statuses['blocking'])
            ):
                # when not in updating/blocking status, and db solution arn is mismatched
                # with vendor solution arn
                # get current refresh time, for keeping track
                current_time_at_update = datetime.strftime(
                    datetime.now(),
                    self.date_utils.get_mysql_date_format()
                )
                state['should_refresh_status'] = True
                state['new_status'] = vendor_campaign_status
                state['latest_solution_version_arn'] = vendor_campaign_solution_version_arn
                state['last_refreshed_at'] = current_time_at_update

        return state

    def should_update(
            self,
            *,
            campaign: dict,
            vendor_campaign: dict,
            vendor_solution: dict
    ) -> bool:
        """
            Check whether a campaign should be updated when all of the following are true

            args:
                vendor_campaign(dict): Campaign from Vendor
                vendor_solution (dict): solution from vendor

            returns:
                result (bool): Should update campaign
        """

        # get solution_version_arn from vendor campaign
        vendor_campaign_solution_version_arn = self.get_vendor_campaign_solution_version_arn(
            vendor_campaign=vendor_campaign
        )

        # get solution version arn in database
        database_campaign_solution_version_arn = campaign['solution_version_arn']

        # get solution arn from vendor solution
        vendor_solution_version_arn = self.get_vendor_solution_version_arn(
            vendor_solution=vendor_solution
        )

        # get campaign status from vendor campaign
        vendor_campaign_status = self.get_vendor_campaign_status(
            vendor_campaign=vendor_campaign
        )

        # get solution status from vendor campaign
        latest_vendor_solution_version_status = self.get_vendor_solution_status(
            vendor_solution=vendor_solution
        )

        # don't update if mismatch in vendor and database solution version arns
        if (
                database_campaign_solution_version_arn !=
                vendor_campaign_solution_version_arn
        ):
            return False

        # Don't update campaign if its on the latest solution version
        if (
                vendor_solution_version_arn ==
                vendor_campaign_solution_version_arn
        ):
            return False

        if vendor_campaign_status in self.campaign_statuses['blocking']:
            return False

        # If the current campaign state == failed, update immediately
        if vendor_campaign_status in self.campaign_statuses['danger']:
            return True

        # Don't update campaign if the vendor solution version is not active
        if latest_vendor_solution_version_status not in self.solution_statuses['success']:
            return False

        return True

    def update_state(
            self,
            campaign: dict,
            solution: dict,
            **kwargs
    ):
        """
            Run the update workflow for campaigns

            Args:
                campaign (dict): database campaign config
                solution (dict): database solution config
            Return:
                (dict): new campaign config

        """
        client_code = kwargs.get("client_code", None)
        service_slug = kwargs.get("service_slug", None)
        engine_slug = kwargs.get("engine_slug", None)
        new_campaign = {
            'arn': None,
            'solution_version_arn': None,
            'status': None,
            'last_updated_at': None
        }

        # run vendor campaign update workflow
        response = self.sagemaker_update_campaign(
            endpoint_name=campaign.get('arn'),
            training_job_name=solution.get('arn'),
            container_image=campaign.get('container_image', None),
            client_code=client_code,
            service_slug=service_slug,
            engine_slug=engine_slug
        )

        new_campaign['arn'] = response.get('EndpointName')
        new_campaign['solution_version_arn'] = response.get('TrainingJobName')

        # get the current time as last updated at time
        current_time_at_update = datetime.strftime(
            datetime.now(),
            self.date_utils.get_mysql_date_format()
        )
        new_campaign.update({
            'last_updated_at': current_time_at_update
        })

        # set new campaign status as updating status
        new_campaign.update({
            'status': self.campaign_statuses['updating'][0]
        })

        # get next update time, this is not a required trigger here
        # deprecate this going forward
        next_update_time = new_campaign.get('next_update_time', None)
        if next_update_time is not None:
            # next update time not implemented
            new_campaign.update({
                'next_update_time': None
            })

        return new_campaign
