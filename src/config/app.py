import datetime
import common.packages.simplejson as json
import os
from common.config import Config
import boto3
import time


def _cors_headers(content_type):
    return {
        'Content-Type': content_type,
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': '*'}


def lambda_handler(event, context):
    if event['queryStringParameters']['action'] == 'get':
        return {
            'statusCode': 200,
            'headers': _cors_headers('application/json'),
            'body': json.dumps(Config().get(event['queryStringParameters']['plantId']))
        }
    elif event['queryStringParameters']['action'] == 'put':
        body = json.loads(event['body'])
        Config().put(body)
        return {
            'statusCode': 200,
            'headers': _cors_headers('application/json'),
            'body': "{}"
        }