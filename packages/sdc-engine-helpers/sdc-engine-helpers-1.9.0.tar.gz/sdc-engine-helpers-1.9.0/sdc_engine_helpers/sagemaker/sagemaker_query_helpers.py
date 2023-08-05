"""
    Sagemaker Engine Helpers module used to manage
    and get information on client subscription
"""
import json
from sdc_engine_helpers.engine_query_helper import EngineQueryHelper
from sdc_engine_helpers.models.subscription import Subscription

class SagemakerEngineHelpers(EngineQueryHelper):
    """Extension on the EngineQueryHelper"""

    def get_solution(
            self,
            *,
            client_id: int,
            service_id: int,
            engine_slug: str,
            from_cache: bool = True,
            for_update: bool = False,
            **kwargs
    ):

        # get solution
        solution, index = super().get_solution(
            client_id=client_id,
            service_id=service_id,
            engine_slug=engine_slug,
            from_cache=from_cache,
            for_update=for_update,
            **kwargs
        )

        if not solution:
            raise IndexError(
                (
                    'ClientError: No Solution matching {} '
                    'found for Engine = "{}" '
                    'And client = "{}" '.format(json.dumps(kwargs), engine_slug, client_id)
                )
            )

        return solution, index

    def get_dataset(
            self,
            *,
            client_id: int,
            service_id: int,
            engine_slug: str,
            from_cache: bool = True,
            for_update: bool = False,
            **kwargs
    ):
        dataset, index = super().get_dataset(
            client_id=client_id,
            service_id=service_id,
            engine_slug=engine_slug,
            from_cache=from_cache,
            for_update=for_update,
            **kwargs
        )

        if not dataset:
            raise IndexError(
                (
                    "ClientError: No Dataset matching {} "
                    "found in Engine = '{}' "
                    "for client = '{}'".format(json.dumps(kwargs), engine_slug, client_id)
                )
            )

        return dataset, index

    def get_item_from_lookup(
            self,
            *,
            client_id: int,
            service_id: int,
            engine: str,
            from_cache: bool = True,
            for_update: bool = False,
            label: str,
            key: str
    ):
        """
            Get a specific item from lookup

            args:
                client_id (int): The client id of the subscription
                service_id (int): The service id of the subscription
                engine (str): Subscription property engine
                from_cache (bool): Retrieve the datasets from cache - Default True
                label (str): Label describing what the dataset is for
                key (str): Dataset key to lookup

            returns:
                result (dict): The result of the lookup
        """
        dataset_kwargs = {'label': label}

        dataset, _ = self.get_dataset(
            client_id=client_id,
            service_id=service_id,
            engine_slug=engine,
            from_cache=from_cache,
            for_update=for_update,
            **dataset_kwargs
        )

        return dataset.get("data", {}).get(str(key))

    def get_campaign(
            self,
            *,
            client_id: int,
            service_id: int,
            engine_slug: str,
            from_cache: bool = True,
            for_update: bool = False,
            **kwargs
    ):
        campaign, index = super().get_campaign(
            client_id=client_id,
            service_id=service_id,
            engine_slug=engine_slug,
            from_cache=from_cache,
            for_update=for_update,
            **kwargs
        )

        if not campaign:
            raise IndexError(
                (
                    "ClientError: No Campaign matching {} "
                    "found for Engine = '{}' "
                    "And client = '{}' ".format(json.dumps(kwargs), engine_slug, client_id)
                )
            )

        return campaign, index

    @staticmethod
    def update_engine_entity_on_index(
            *,
            subscription: Subscription,
            engine_index: int,
            entity_key: str,
            entity_index: int,
            value
    ):
        """
            Update a specific entity in a specific engine in a subscription

            args:
                subscription (Subscription): The subscription model to update
                engine_index (str): The engine index in the Subscription model properties
                entity_key (str): The key of the entity in the engine
                value: The data to set the entity key node to
        """
        subscription.properties['engines'][engine_index][entity_key][entity_index] = value

    def update_dataset(
            self,
            *,
            client_id: int,
            service_id: int,
            engine_slug: str,
            config: dict,
            from_cache: bool = True,
            **kwargs
    ):
        """
            Update specific dataset in a specific engine in a subscription

            args:
                subscription (Subscription): The subscription model to update
                engine_index (str): The engine index in the Subscription model properties
                value: The data to set the entity key node to
        """

        # get subscription for engine
        subscription = self.get_subscription(
            client_id=client_id,
            service_id=service_id,
            from_cache=False,
            for_update=True
        )

        # get dataset index
        dataset, dataset_index = self.get_dataset(
            client_id=client_id,
            service_id=service_id,
            engine_slug=engine_slug,
            from_cache=from_cache,
            for_update=False,
            **kwargs
        )
        # update config
        dataset.update(config)

        # get engine_index
        _, engine_index = self.get_engine_entity(
            client_id=client_id,
            service_id=service_id,
            engine_slug=engine_slug,
            entity_key='datasets',
            from_cache=False,
            for_update=False
        )

        # update entity
        self.update_engine_entity_on_index(
            subscription=subscription,
            engine_index=engine_index,
            entity_key='datasets',
            entity_index=dataset_index,
            value=dataset
        )

    def update_campaign(
            self,
            *,
            client_id: int,
            service_id: int,
            engine_slug: str,
            config: dict,
            from_cache: bool = True,
            **kwargs
    ):
        """
            Update specific campaign in a specific engine in a subscription

            args:
                subscription (Subscription): The subscription model to update
                engine_index (str): The engine index in the Subscription model properties
                value: The data to set the entity key node to
        """
        # get subscription for engine
        subscription = self.get_subscription(
            client_id=client_id,
            service_id=service_id,
            from_cache=False,
            for_update=True
        )

        # get campaign index
        campaign, campaign_index = self.get_campaign(
            client_id=client_id,
            service_id=service_id,
            engine_slug=engine_slug,
            from_cache=from_cache,
            for_update=False,
            **kwargs
        )

        campaign.update(config)

        # get engine_index
        _, engine_index = self.get_engine_entity(
            client_id=client_id,
            service_id=service_id,
            engine_slug=engine_slug,
            entity_key='campaigns',
            from_cache=False,
            for_update=False
        )
        # update the engine campaign
        self.update_engine_entity_on_index(
            subscription=subscription,
            engine_index=engine_index,
            entity_key='campaigns',
            entity_index=campaign_index,
            value=campaign
        )

    def update_solution(
            self,
            *,
            client_id: int,
            service_id: int,
            engine_slug: str,
            config: dict,
            from_cache: bool = True,
            **kwargs
    ):
        """
            Update specific solution in a specific engine in a subscription

            args:
                subscription (Subscription): The subscription model to update
                engine_index (str): The engine index in the Subscription model properties
                value (dict): dataset configs to set the entity key node to
        """
        # get subscription for engine
        subscription = self.get_subscription(
            client_id=client_id,
            service_id=service_id,
            from_cache=False,
            for_update=True
        )

        solution, solution_index = self.get_solution(
            client_id=client_id,
            service_id=service_id,
            engine_slug=engine_slug,
            from_cache=from_cache,
            for_update=False,
            **kwargs
        )
        solution.update(config)
        # get engine_index
        _, engine_index = self.get_engine_entity(
            client_id=client_id,
            service_id=service_id,
            engine_slug=engine_slug,
            entity_key='solutions',
            from_cache=False,
            for_update=False
        )
        # update the engine solution
        self.update_engine_entity_on_index(
            subscription=subscription,
            engine_index=engine_index,
            entity_key='solutions',
            entity_index=solution_index,
            value=solution
        )
