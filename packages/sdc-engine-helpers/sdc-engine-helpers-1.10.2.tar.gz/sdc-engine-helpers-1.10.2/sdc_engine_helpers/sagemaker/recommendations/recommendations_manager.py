"""
    Sagemaker recommendations manager module
"""
import json
from sdc_helpers.models.client import Client
from sdc_helpers.redis_helper import RedisHelper
import boto3
from sdc_engine_helpers.sagemaker.utils import create_resource_name
from sdc_engine_helpers.sagemaker.sagemaker_query_helpers import \
    SagemakerEngineHelpers

class RecommendationsManager:
    """
        Manages retrieval of Sagemaker recommendations for a given set of parameters
    """
    # pylint: disable=raise-missing-from
    client = {}
    engine = None

    def __init__(self, **kwargs):
        """
            kwargs:
                service_slug (str): slug of service to use
                rds_config (dict): config for mysql database
                redis_config (dict): config for redis cache database
                item_ids (str): name of item id lookup in mysql db
                item_codes (str): name of item code lookup in mysql db
        """
        # get rds config
        rds_config = kwargs.get('rds_config', {})
        if not isinstance(rds_config, dict):
            raise TypeError('Only dict is supported for rds_config')

        # get redis config
        redis_config = kwargs.get('redis_config', {})
        if not isinstance(redis_config, dict):
            raise TypeError('Only dict is supported for redis_config')

        # instantiate query helpers
        self.query_helper = SagemakerEngineHelpers(
            rds_config=rds_config,
            redis_config=redis_config
        )

        self.redis_helper = RedisHelper(**redis_config)
        # service slug is the same for all engines
        service_slug = kwargs.pop('service_slug', 'recommend')

        # get name of lookups
        self.item_id_identifier = kwargs.pop('item_id_identifier', 'item_id_lookup')
        self.item_code_identifier = kwargs.pop('item_code_identifier', 'item_code_lookup')

        # load service details from service table
        self.service = self.query_helper.get_service(slug=service_slug)

    def __del__(self):
        """
            Close connections on delete
        """
        del self.query_helper
        del self.redis_helper

    def get_recommendations(
            self,
            *,
            client_id: id,
            item_id: str,
            engine: str,
            **kwargs
    ):
        """
            Get the recommendations for the specified parameters

            parameters:
                - dictionary of parameter arguments
            returns:
                results (dict): Results from the Sagemaker invocation
        """
        results = None
        self.client = self.get_client(client_id=client_id)
        self.engine = engine
        # recipe is set by client config
        recipe = kwargs.get('recipe', 'related_items')
        num_results = kwargs.get('num_results', 25)
        from_cache = kwargs.get('from_cache', True)

        cache_key = (
            'recommendation-request-'\
            '{item_id}-{service_id}-'\
            '{client_id}-{engine_slug}'.format(
                item_id=item_id,
                service_id=self.service.id,
                client_id=self.client.id,
                engine_slug=self.engine
            )
        )

        if from_cache:
            results = self.redis_helper.redis_get(key=cache_key)

        if not results:
            campaign = self.get_campaign(
                client_id=self.client.id,
                engine=self.engine,
                recipe=recipe
            )

            if not campaign:
                raise Exception('ServerError: Could not determine campaign for this client')

            # changed campaign_arn to be campaign_name
            endpoint_name = campaign['arn']

            results = self.get_results(
                item_id=item_id,
                endpoint_name=endpoint_name,
                num_results=num_results
            )
            self.redis_helper.redis_set(
                key=cache_key,
                value=json.dumps(results),
                expiry=7200
            )
        else:
            results = json.loads(results)

        return results

    def get_client(
            self, *,
            client_id: int = None,
            api_key_id: str = None
    ) -> Client:
        """
            Determine the client with the supplied parameters

            Expects either client_id or api_key_id
            args:
                client_id (int): client id to fetch
                api_key_id (int): api_key_id to fetch client_id

            returns:
                client (Client): The determined client

        """
        client = None

        if client_id is not None:
            client = self.query_helper.get_client(client_id=client_id)
        else:
            if api_key_id is not None:
                client = self.query_helper.get_client(api_key_id=api_key_id)

        if client is None:
            raise Exception('ClientError: Could not determine client for this request')

        return client

    def get_campaign(
            self, *,
            client_id: int,
            engine: str,
            recipe='related_items'
    ) -> dict:
        """
            Determine the campaign with the supplied parameters
            note:
                - Currently: Campaign arn = (Sagemaker Engpoint Name)

            args:
                client_id (int): client id
                engine (str): engine slug
                recipe (str): recipe name

            returns:
                campaign (dict): Campaign from the database

        """
        campaign_kwargs = {'recipe': recipe}

        campaign, _ = self.query_helper.get_campaign(
            client_id=client_id,
            service_id=self.service.id,
            engine_slug=engine,
            from_cache=True,
            **campaign_kwargs
        )

        return campaign

    def encode_item_code(
            self,
            *,
            item_ids: list,
            from_cache: bool = True
    ):
        """
            Lookup a list of item codes

            args:
                 item_ids (list) : list of item id's
                 from_cache (bool) : Get lookup from cache first
            return:
                item_codes (list) : list of item codes
        """
        item_codes = []

        cache_key = create_resource_name(
            context='recommendation',
            function=self.item_code_identifier,
            additional_details=[
                self.service.id, self.client.id, self.engine
            ]
        )

        # check that key exists
        key_exists = self.redis_helper.redis_hexists(
            hashkey=cache_key
        )
        print("Cached Key = {}".format(cache_key))
        print("keys found = {}".format(key_exists))
        if key_exists == 0:
            print("Falling back to clone")
            tmp_cache_clone = "{}-tmp-clone".format(cache_key)
            # check that key exists
            key_exists = self.redis_helper.redis_hexists(
                hashkey=cache_key
            )
            if key_exists == 0:
                raise Exception((
                    "ServerError: Item Code lookup could "
                    "not be found in cache. Both main and clone missing."
                ))
            # use clone as lookup
            cache_key = tmp_cache_clone

        if from_cache:
            # encode item_id -> item_code
            item_codes = self.redis_helper.redis_hmget(
                hashkey=cache_key,
                keys=item_ids
            )

        results = []
        for item_code in item_codes:
            # decode item_ids bytes -> str
            if isinstance(item_code, bytes):
                item_code = item_code.decode("utf-8")

            # check if item_id is none
            if item_code is not None:
                results.append(item_code)

        return results

    def decode_item_code(
            self,
            *,
            item_codes: list,
            from_cache: bool = True
    ):
        """"
            Lookup a list of item ids

            args:
                 item_codes (list) : list of item codes
                 from_cache (bool) : Get lookup from cache first
            return:
                item_ids (list) : list of item id
        """
        item_ids = []

        cache_key = create_resource_name(
            context='recommendation',
            function=self.item_id_identifier,
            additional_details=[self.service.id, self.client.id, self.engine]
        )
        # check that key exists
        key_exists = self.redis_helper.redis_hexists(
            hashkey=cache_key
        )
        print("Cached Key = {}".format(cache_key))
        print("keys found = {}".format(key_exists))
        if key_exists == 0:
            print("Falling back to clone")
            tmp_cache_clone = "{}-tmp-clone".format(cache_key)
            # check that key exists
            key_exists = self.redis_helper.redis_hexists(
                hashkey=cache_key
            )

            if key_exists == 0:
                raise Exception((
                    "ServerError: Item ID lookup could "
                    "not be found in cache. Both main and clone missing."
                ))
            # use clone as lookup
            cache_key = tmp_cache_clone

        if from_cache:
            # decode item_codes -> item_ids
            item_ids = self.redis_helper.redis_hmget(
                hashkey=cache_key,
                keys=item_codes
            )

        results = []
        for item_id in item_ids:
            if isinstance(item_id, bytes):
                # decode item_ids bytes -> str
                item_id = item_id.decode("utf-8")

            # check if item_id is none
            if item_id is not None:
                results.append(item_id)

        return results

    def get_results(
            self,
            *,
            item_id: str,
            endpoint_name: str,
            num_results: int = 25
    ) -> list:
        """
            Determine the results for this request

            args:
                item_id (str): The client requesting the recommendation
                endpoint_name (str): The AWS Sagemaker endpoint_name
                num_results (int) : Number of recommendation results to return

            returns:
                results (list): Sagemaker invocation results

        """
        results = []
        # lookup item code
        item_codes = self.encode_item_code(item_ids=[item_id])
        # test that item_code is valid
        if len(item_codes) == 0:
            raise Exception('ClientError: item_id was not found in lookup')

        try:
            request_item = int(item_codes[0])
            sagemaker_runtime = boto3.client('sagemaker-runtime')
            # make the recommender ignore self recommendation
            event = {
                'item_code': request_item,
                'args': {
                    'n_similar': num_results,
                    'exclude': [
                        request_item
                    ]
                }
            }
            payload = json.dumps(event)

            # get recommendations
            response = sagemaker_runtime.invoke_endpoint(
                EndpointName=endpoint_name,
                ContentType='application/json',
                Body=payload
            )

            # decode application/json response
            response_decoded = json.loads(response['Body'].read().decode())


            if isinstance(response_decoded, str):
                # if decorded response still string
                # assume error and raise
                raise Exception(response_decoded)

            #extract itemcodes
            recommendations = [r['item_code'] for r in response_decoded]

        except sagemaker_runtime.exceptions.ModelError:
            # insure model errors are returned as 500
            msg = "ServerError: 500 Internal Server Error"
            raise Exception(msg)

        # decode recommendations bytes -> str
        results = self.decode_item_code(item_codes=recommendations)
        # check list of item_ids are not all None
        if len(results) == 0:
            raise Exception('ClientError: Unable to decode recommendations to item_id')

        return results
