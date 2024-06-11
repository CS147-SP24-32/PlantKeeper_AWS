import datetime
import common.packages.simplejson as json
import os
from common.sensor_data import SensorData
import boto3
import time

sns = boto3.client('sns')

last_notification_time = 0

def _cors_headers(content_type):
    return {
        'Content-Type': content_type,
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': '*'}

def lambda_handler(event, context):
    return {
        'statusCode': 200,
        'headers': _cors_headers('application/json'),
        'body': json.dumps(SensorData().get(event['queryStringParameters']['plantId'],
                           event['queryStringParameters']['startTime'],
                           event['queryStringParameters']['endTime']))
    }
