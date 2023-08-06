"""
    Personalize abstract manager module
"""
from sdc_helpers.models.client import Client
from sdc_helpers.redis_helper import RedisHelper
from sdc_engine_helpers.engine_query_helper import EngineQueryHelper

class Manager:
    """
        Abstract manager class to be inherited by various Personalize managers
    """
    service = None
    service_for_update = False
    engine_slug = None
    query_helper = None
    redis_helper = None
    parameters = None
    # flag to determine if maintenance was performed
    can_perform_maintenance = False

    def __init__(self, **kwargs):
        query_helper_kwargs = dict(filter(lambda item: item[0] == 'rds_config', kwargs.items()))
        redis_helper_kwargs = dict(filter(lambda item: item[0] == 'redis_config', kwargs.items()))
        self.query_helper = EngineQueryHelper(**query_helper_kwargs)
        self.redis_helper = RedisHelper(**redis_helper_kwargs)
        self.service_slug = kwargs.pop('service_slug', 'recommend')
        self.service = self.query_helper.get_service(
            slug=self.service_slug,
            for_update=self.service_for_update
        )
        self.engine_slug = kwargs.pop('engine_slug', 'personalize')
        self.parameters = kwargs

    def __del__(self):
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
        del self.redis_helper

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

    def get_client(self) -> Client:
        """
            Determine the client with the supplied parameters

            returns:
                client (Client): The determined client

        """
        client = None

        client_id = self.parameters.get('client_id', None)
        if client_id is not None:
            client = self.query_helper.get_client(client_id=client_id)
        else:
            api_key_id = self.parameters.get('api_key_id', None)
            if api_key_id is not None:
                client = self.query_helper.get_client(api_key_id=api_key_id)

        if client is None:
            raise Exception('ClientError: Could not determine client for this request')

        return client
