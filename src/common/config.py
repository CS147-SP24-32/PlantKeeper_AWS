import datetime

import boto3
from boto3.dynamodb.conditions import Key, Attr
import os
from uuid import uuid4


class Config:
    def __init__(self):
        if os.environ.get('AWS_SAM_LOCAL', False):
            resource = boto3.resource('dynamodb', endpoint_url='http://host.docker.internal:8000')
        else:
            resource = boto3.resource('dynamodb')
        self.table = resource.Table(os.environ["CONFIG_TABLE"])
        self.table.load()

    def get(self, plant_id: str):
        dbresponse = self.table.get_item(Key={"plant_id": plant_id})
        if item := dbresponse.get('Item'):
            return item

    def put(self, item):
        self.table.put_item(Item=item)