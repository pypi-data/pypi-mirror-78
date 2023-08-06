"""
    Dataset state manager module
        - state managers have knowledge of state transition and meaning
        - state manager is called to check state
        - state manager is called to transition state
        - state manager only sends back True/False. Do something or don't.

        may want to:
        - add validation of complex types: Url, etc https://validators.readthedocs.io/en/latest/
"""
import io
import json
from datetime import datetime
import boto3
from botocore.exceptions import ClientError as botocore_clienterror
import sdc_helpers.utils as utils
from sdc_helpers.redis_helper import RedisHelper
from sdc_engine_helpers.sagemaker.utils import parse_s3_url
from sdc_engine_helpers.date_utils import DateUtils

# pylint: disable=too-few-public-methods
class DatasetStateManager:
    """
        Given a database dataset object,

        1. get_state
            - check whether dataset should be updated by
                call vendor API's to check if campaign solution
                version differs from dataset solution version
            OR
            - check if the dataset status in the database needs to be refreshed.
        2. update_state
            - call vendor API's to execute update workflow for dataset
            - update status of dataset in database

    """
    date_utils = DateUtils()
    redis_helper = None
    query_helper = None
    # vendor
    vendor_campaign_arn_path = 'EndpointName'
    vendor_campaign_status_path = 'EndpointStatus'
    # input data key in TrainingJob
    vendor_campaign_solution_arn_path = 'ProductionVariants.0.VariantName'

    campaign_statuses = {
        'running':['Creating', 'Updating', 'SystemUpdating', 'Deleting'],
        'failed':['Failed', 'RollingBack'],
        'danger':['Failed'],
        'blocking':[
            'Creating',
            'Updating',
            'SystemUpdating',
            'Deleting',
            'Failed',
            'RollingBack'],
        'stopped':['OutOfService'],
        'active':['InService', None, 'None']
    }

    solution_statuses = {
        'blocking':['InProgress', 'Stopping', 'Failed', 'Stopped'],
        'success':['Completed', None, 'None']
    }

    dataset_statuses = {
        'active': ['Active', None, 'None'],
        'blocking': ['Updating']
    }

    def __init__(self, **kwargs):
        self.sagemaker = boto3.client('sagemaker')
        self.s3_client = boto3.client('s3')
        redis_config = kwargs.get('redis_config', {})
        if not isinstance(redis_config, dict):
            raise TypeError('Only dict is supported for redis_config')
        self.redis_helper = RedisHelper(**redis_config)

    @staticmethod
    def get_vendor_solution_dataset_identifier(
            *,
            vendor_solution: dict,
            dataset_label: str,
            file_type: str
        ) -> str:
        """
            Get a Sagemaker Training job input dataset by channel name

            args:
                vendor_solution (dict): Solution from Personalize
                dataset_label (str): dataset label as stored in db

            returns:
                status (str): Sagemaker solution version status

        """
        input_configs = vendor_solution.get("InputDataConfig")
        if input_configs is not None:
            for d_configs in input_configs:
                channel_name = d_configs.get("ChannelName")

                if channel_name is None:
                    raise KeyError("ChannelName must be provided by vendor")

                if channel_name == dataset_label:
                    s3_folder_path = utils.dict_query(
                        dictionary=d_configs,
                        path='DataSource.S3DataSource.S3Uri'
                    )
                    return "{}/{}.{}".format(
                        s3_folder_path,
                        dataset_label,
                        file_type
                    )

        else:
            raise ValueError("InputDataConfig is missing, vendor should provide this.")

        raise KeyError((
            "Channel with name = {} was not"
            "found in vendor solution".format(dataset_label)
        ))

    def download_s3_blob(self, s3_url: str):
        """download blob from s3"""
        # parse s3 url -> bucket, file_path
        bucket, file_path = parse_s3_url(s3_url)
        # load data from s3 as byte steam
        data_stream = io.BytesIO()
        self.s3_client.download_fileobj(
            bucket,
            file_path,
            data_stream
        )
        data_stream.seek(0)
        return data_stream

    def upload_s3_blob(self, blob: io.BytesIO, s3_url: str):
        """download blob from s3"""
        # parse s3 url -> bucket, file_path
        bucket, file_path = parse_s3_url(s3_url)
        self.s3_client.upload_fileobj(
            blob, bucket, file_path
        )

    def execute_s3_versioning(self, data_stream: io.BytesIO, dst_url: str):
        """
            Streams data from source s3 url to a destination s3 url

            Args:
                src_url (str): source s3 url
                dst_url (str): destination s3 url
        """
        try:
            self.upload_s3_blob(
                blob=data_stream,
                s3_url=dst_url
            )
        except botocore_clienterror as exception:
            if exception.response['Error']['Code'] == "404":
                # The object does not exist.
                print((
                    "Unable to find object. Skipping the task, "
                    "the following exception was found = {}".format(exception)
                ))
            else:
                raise

    def cache_lookup(self, data_stream: io.BytesIO, cache_key: str):
        """cache lookup in elasticcache

        Args:
            cache_key (str): key to use when caching
            json_data (dict): data to cache which should be simple dictionary lookup
        """
        json_data = json.loads(
            data_stream.read().decode("UTF-8")
        )
        if not isinstance(json_data, dict):
            raise Exception("ClientError: Json data is not a dictionary")

        if self.redis_helper.redis_hexists(hashkey=cache_key) == 1:
            print("This cache already exists. Deleting before caching new data")
            self.redis_helper.redis_delete(keys=[cache_key])

        self.redis_helper.redis_hset(
            hashkey=cache_key,
            dict_obj=json_data
        )

    def get_vendor_campaign_solution_version_arn(self, vendor_campaign: dict):
        """
            Get vendor campaign solution version status

            args:
                vendor_campaign (dict): Solution from vendor campaign

            returns:
                status (str): vendor solution version status

        """

        return utils.dict_query(
            dictionary=vendor_campaign,
            path=self.vendor_campaign_solution_arn_path
        )

    def get_vendor_campaign_status(self, vendor_campaign: dict):
        """
            Get vendor campaign solution version status

            args:
                vendor_campaign (dict): Solution from vendor campaign

            returns:
                status (str): vendor solution version status

        """

        return utils.dict_query(
            dictionary=vendor_campaign,
            path=self.vendor_campaign_status_path
        )

    def get_state(
            self, *,
            dataset: dict,
            campaign: dict):
        """
            Get dataset state

            Args:
                dataset (dict): database dataset config
                campaign (dict): database campaign config
            Return:
                (dict): current state config
        """
        state = {
            'should_update': False
        }

        # get current campaign from vendor
        vendor_campaign = self.sagemaker.describe_endpoint(
            EndpointName=campaign.get('arn')
        )

        # check if should update
        state['should_update'] = self.should_update(
            dataset=dataset,
            vendor_campaign=vendor_campaign
        )

        if state['should_update']:
            # set a new version status as InProgress
            state.update(
                {
                    'new_version_status': 'Updating'
                }
            )

        return state

    def update_state(
            self, *,
            dataset: dict,
            campaign: dict,
            cache_key: str
    ):
        """
            This is where jobs to create datasets are run

            Args:
                dataset (dict): database dataset config
                campaign (dict): database campaign config
            Return:
                (dict): new dataset
        """

        new_dataset = {
            'data': None,
            'identifier': None,
            'solution_version_arn': None,
            'last_updated_at': None,
            'last_status': None
        }

        # get vendor solution
        vendor_campaign = self.sagemaker.describe_endpoint(
            EndpointName=campaign.get('arn')
        )

        # get vendor campaign
        latest_vendor_solution_version_arn = self.get_vendor_campaign_solution_version_arn(
            vendor_campaign
        )

        vendor_solution = self.sagemaker.describe_training_job(
            TrainingJobName=latest_vendor_solution_version_arn
        )

        # update solution arn
        new_dataset.update({
            'solution_version_arn': latest_vendor_solution_version_arn
        })

        # update identifier
        new_dataset.update({
            'identifier': self.get_vendor_solution_dataset_identifier(
                vendor_solution=vendor_solution,
                dataset_label=dataset['label'],
                file_type=dataset['file_type']
            )
        })

        if dataset.get('should_store'):
            # update data
            identifier = new_dataset.get('identifier', None)
            # get dataset from reference
            if isinstance(identifier, str):
                print("Build prod destination url")
                prod_url = identifier.replace("/train/", "/prod/")
                print("Build previous destination url")
                previous_url = identifier.replace("/train/", "/previous/")

                print("Download dataset from prod/ in s3")

                data_stream = self.download_s3_blob(s3_url=prod_url)

                print("Pushing to previous/ to s3")
                self.execute_s3_versioning(
                    data_stream=data_stream,
                    dst_url=previous_url
                )

                print("Download dataset from train/ from s3")
                # get data
                data_stream = self.download_s3_blob(s3_url=identifier)

                # cache to elastic cache
                print("Caching new prod dataset")
                self.cache_lookup(
                    data_stream=data_stream,
                    cache_key=cache_key
                )
                print("Pushing dataset to prod/ in s3")
                self.execute_s3_versioning(
                    data_stream=data_stream,
                    dst_url=prod_url
                )

        # date
        new_dataset.update({
            'last_updated_at': datetime.strftime(
                datetime.now(),
                self.date_utils.get_mysql_date_format()
                )
        })

        # update status
        new_dataset.update({
            'last_status': 'Active'
        })

        return new_dataset

    def should_update(
            self,
            *,
            dataset: dict,
            vendor_campaign: dict
    ) -> bool:
        """Check if dataset should update"""
        # (look at campaign state manager)
        latest_vendor_campaign_solution_version_arn = self.get_vendor_campaign_solution_version_arn(
            vendor_campaign
        )

        latest_vendor_campaign_status = self.get_vendor_campaign_status(
            vendor_campaign
        )

        # Don't update dataset if its on the latest solution version
        if (
                dataset.get('solution_version_arn') ==
                latest_vendor_campaign_solution_version_arn
        ):
            return False

        if latest_vendor_campaign_status not in self.campaign_statuses['active']:
            return False

        if dataset.get('last_status') not in self.dataset_statuses['active']:
            return False

        return True
