"""
    Solution state manager module
        - implements Workflows that call AWS Vendor API's.
"""
from datetime import datetime
import sdc_helpers.utils as utils
import boto3
from sdc_engine_helpers.sagemaker.utils import \
    create_resource_name, build_resource_tags
from sdc_engine_helpers.sagemaker.utils import name_from_base
from sdc_engine_helpers.date_utils import DateUtils

class SolutionStateManager:
    """
        Given a database solution object,

        1. get_state
            - call vendor API's to check if solution needs to be updated
            OR
            - check if the solution status in the database needs to be refreshed.
        2. update_state
            - call vendor API's to execute update workflow for solution
            - update status of solution in database

    """
    date_utils = DateUtils()
    # default tag to dev environment
    resource_tags = [
        {
            'Key': 'environment',
            'Value': 'dev'
        },
    ]
    # slack_helper = SlackHelper()
    # set path to entities in vendor objects
    solution_status_path = 'TrainingJobStatus'
    # setup available status to look for
    job_statuses = {
        'inProgress':['InProgress'],
        'running': ['InProgress', 'Stopping'],
        'failed':['Failed'],
        'blocking':['InProgress', 'Stopping', 'Failed'],
        'stopped':['Stopped'],
        'success':['Completed', None, 'None']
    }

    required_new_job_fields = [
        "TrainingJobName",
        'AlgorithmSpecification',
        'HyperParameters',
        'InputDataConfig',
        'OutputDataConfig',
        'ResourceConfig',
        'EnableManagedSpotTraining',
        'RoleArn',
        'StoppingCondition'
    ]

    def __init__(self):
        """
            Init a new version of the solution state manager

            Args:
                solution_base_name (str): [description]
        """
        # get vendor api
        self.sagemaker = boto3.client('sagemaker')

    def sagemaker_create_solution(
            self,
            training_job_name: str,
            client_code: str,
            service_slug: str,
            engine_slug: str
    ) -> str:
        """Performs a create solution API execution to create new solution version job

            Args:
                training_job_name (str): name of previously successful training job
                new_solution_name (str): new training job name

            Returns:
                (str) : new training job name
        """
        new_solution_base_name = create_resource_name(
            context=service_slug,
            function=client_code, # to maintain order of resource name
            additional_details=[
                engine_slug, 'training'
            ]
        )
        # get current solution
        prev_training_job = self.sagemaker.describe_training_job(
            TrainingJobName=training_job_name
        )

        new_training_job_config = {}
        for key_, values_ in prev_training_job.items():
            if key_ in self.required_new_job_fields:
                new_training_job_config.update({
                    key_ : values_
                })

        # update fields
        # generate a unique name with timestamp
        new_training_job_name = name_from_base(
            new_solution_base_name,
            max_length=63,
            short=False
        )

        # add new resource tags
        resource_tags = build_resource_tags(
            current_tags=self.resource_tags,
            new_tags=[
                {
                    'Key': 'environment',
                    'Value': 'prod'
                },
                {
                    'Key': 'client',
                    'Value': client_code
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

        new_training_job_config.update({
            'TrainingJobName': new_training_job_name,
            'Tags': resource_tags
        })

        self.sagemaker.create_training_job(**new_training_job_config)

        return new_training_job_config['TrainingJobName']

    def get_vendor_version_status(self, *, vendor_solution: dict) -> str:
        """
            Get vendor solution version status

            args:
                vendor_solution (dict): Solution from vendor

            returns:
                status (str): vendor solution version status

        """

        return utils.dict_query(
            dictionary=vendor_solution,
            path=self.solution_status_path
        )

    def get_state(self, *, solution: dict) -> dict:
        """
            Get the current state of the solution from vendor API's.

            Args:
                solution (dict): database solution config
            Return:
                (dict): current state config

        """
        state = {
            'should_create_version': False,
            'should_refresh_version_status': False
        }

        # get vendor solution
        vendor_solution = self.sagemaker.describe_training_job(
            TrainingJobName=solution.get('arn')
        )
        # check if new solution should be updated
        state['should_create_version'] = self.should_create_solution_version(
            solution=solution,
            vendor_solution=vendor_solution
        )

        if state['should_create_version']:
            # update next creation time
            this_version_creation_time = solution.get('next_version_creation_time', None)
            version_creation_frequency = solution.get('version_creation_frequency', None)

            if version_creation_frequency:
                state['next_version_creation_time'] = self.date_utils.get_next_time(
                    this_time=this_version_creation_time,
                    frequency=version_creation_frequency
                )
        else:
            # Check if the database version status needs to be updated
            version_status = solution.get('version_status', None)
            vendor_solution_status = self.get_vendor_version_status(
                vendor_solution=vendor_solution
            )

            # only update database status if refresh is true
            if vendor_solution_status != version_status:
                state['should_refresh_version_status'] = True
                state['new_version_status'] = vendor_solution_status

        return state

    def should_create_solution_version(
            self, *,
            solution: dict,
            vendor_solution: dict
    ) -> bool:
        """
            Check whether a new solution version should be updated

            args:
                solution (dict): Solution from the database
                vendor_solution (dict): Solution from vendor

            returns:
                result (bool): Should create solution version

        """
        # If the latest solution version is still creating in Personalize, don't create
        vendor_solution_version_status = self.get_vendor_version_status(
            vendor_solution=vendor_solution
        )

        if vendor_solution_version_status in self.job_statuses['blocking']:
            return False

        # If solution create job == failed, do not update
        if vendor_solution_version_status in self.job_statuses['failed']:
            # FUTURE: trigger/log an issue
            return False

        version_creation_frequency = solution.get('version_creation_frequency', None)

        if version_creation_frequency:
            # check if it's time to update solution
            next_version_creation_time = solution.get('next_version_creation_time')
            if next_version_creation_time:
                if (
                        datetime.now() <
                        datetime.strptime(next_version_creation_time, "%Y-%m-%d %H:%M:%S")
                ):
                    return False

        return True

    def update_state(
            self,
            solution: dict,
            client_code: str,
            service_slug: str,
            engine_slug: str
    ):
        """
            Run the update workflow for solution

            Args:
                solution (dict): database solution config
                solution_base_name (str): base name for new solution
            Return:
                (dict): new solution config

        """
        new_solution = {
            'arn': None,
            'version_status': None,
            'version_last_created_at': None,
            'next_version_creation_time': None
        }

        new_solution_arn = self.sagemaker_create_solution(
            training_job_name=solution['arn'],
            client_code=client_code,
            service_slug=service_slug,
            engine_slug=engine_slug
        )
        # update the arn with the new arn
        new_solution.update({
            'arn': new_solution_arn
        })

        vendor_solution = self.sagemaker.describe_training_job(
            TrainingJobName=new_solution_arn
        )

        vendor_solution_version_status = self.get_vendor_version_status(
            vendor_solution=vendor_solution
        )
        # default to inProgress
        new_solution.update({
            'version_status': vendor_solution_version_status
        })

        new_solution.update({
            'version_last_created_at': datetime.strftime(
                datetime.now(),
                self.date_utils.get_mysql_date_format()
                )
        })

        version_creation_frequency = solution['version_creation_frequency']

        if version_creation_frequency:
            next_version_creation_time = solution.get('next_version_creation_time', None)
            new_solution.update({
                'next_version_creation_time': self.date_utils.get_next_time(
                    this_time=next_version_creation_time,
                    frequency=version_creation_frequency
                )
            })
        return new_solution
