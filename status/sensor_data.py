import datetime

import boto3
import os
from uuid import uuid4


class SensorData:
    """Wrapper for DynamoDB sensor data table queries."""
    def __init__(self):
        if os.environ.get('AWS_SAM_LOCAL', False):
            resource = boto3.resource('dynamodb', endpoint_url='http://host.docker.internal:8000')
        else:
            resource = boto3.resource('dynamodb')
        self.table = resource.Table(os.environ["SENSOR_TABLE"])
        self.table.load()

    def new(self, readings, plant_id) -> None:
        """Log a set of sensor data."""
        self.table.put_item(
            Item={
                'plant_id': plant_id,
                'timestamp': datetime.datetime.utcnow().isoformat(),
                **readings,
            }
        )
