"""
    Queue utilities module
"""
import os
import uuid
from datetime import datetime
import json
import boto3
from sdc_helpers import utils
from sdc_helpers.models.client import Client


def queue_s3_store(
        *,
        content: str,
        file_path: str,
):
    """
       Queue storage into S3

           args:
               content (str): The file content of the file in S3
               file_path (str): The S3 file path
    """
    sqs = boto3.client('sqs')
    queue_url = os.getenv('QUEUE_URL')
    if queue_url is None:
        raise Exception('Please set up the QUEUE_URL environment variable')
    s3_storer_lambda = os.getenv('S3_STORER_LAMBDA')
    if s3_storer_lambda is None:
        raise Exception('Please set up the S3_STORER_LAMBDA environment variable')

    sqs_body = {
        'bucket': 'base-lambda-requests',
        'file_path': file_path,
        'content': content
    }

    sqs_message_attributes = {
        'lambda_function': {
            'DataType': 'String',
            'StringValue': s3_storer_lambda
        }
    }

    sqs.send_message(
        QueueUrl=queue_url,
        MessageBody=json.dumps(sqs_body, indent=2),
        MessageAttributes=sqs_message_attributes
    )


def queue_s3_recommendations_store(
        *,
        client: Client,
        engine: str,
        results: list,
        item_id: int,
        context: dict
):
    """
        Queue recommendation results storage into S3

            args:
                client (Client): The client model involved
                engine (str): The engine that made the recommendations
                results (list): A results of the recommendation
                item_id (int): The item id of the requested recommendation
                context (dict): Additional information of the request
    """
    file_path = '{client}/recommendations/{uuid}.txt'.format(
        client=client.name,
        uuid=str(uuid.uuid4())
    )

    domain = utils.dict_query(
        dictionary=context,
        path='domain'
    )

    session_hash = utils.dict_query(
        dictionary=context,
        path='sessionHash'
    )

    content = {
        'engine': engine,
        'domain': domain,
        'item_id': item_id,
        'session_hash': session_hash,
        'results': results,
        'timestamp': datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
    }

    queue_s3_store(
        content=json.dumps(content, indent=2),
        file_path=file_path
    )
