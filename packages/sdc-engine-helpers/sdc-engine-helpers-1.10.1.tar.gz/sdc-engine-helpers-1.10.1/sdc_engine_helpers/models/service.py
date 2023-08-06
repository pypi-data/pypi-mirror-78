"""
   SDC Engine service model module
"""
from sqlalchemy import func
from sqlalchemy.orm import query_expression
from sqlalchemy.sql.functions import _FunctionGenerator
from sdc_helpers.models.service import Service as BaseService


class Service(BaseService):
    """
       SDC Engine Service model class
    """
    # pylint: disable=too-few-public-methods
    extend_existing = True

    maintenance_in_progress = query_expression()

    @classmethod
    def maintenance_in_progress_expression(cls) -> _FunctionGenerator:
        """
            SQL expression to get the maintenance_in_progress from properties

            returns:
                function (_FunctionGenerator): The JSON_EXTRACT SQL function

            Example SQL expression:

                JSON_EXTRACT(
                    properties,
                    "$.maintenance_in_progress"
                )
        """
        return func.json_extract(
            Service.properties,
            '$.maintenance_in_progress'
        )
