import os
import json
from common.sensor_data import SensorData
from common.config import Config
import boto3
import time

sns = boto3.client('sns')

last_notification_time = 0


def notify(message):
    global last_notification_time
    current_time = time.time()
    if current_time - last_notification_time >= 600:  # Check if 10 minutes have passed
        sns.publish(
            TopicArn=os.environ["ALERT_ARN"],
            Message=message,
            Subject='Plant Watering Alert'
        )
        last_notification_time = current_time


def lambda_handler(event, context):
    body = json.loads(event['body'])
    plant_id = "0" # TODO: make this part of the request
    needs_watering = False
    SensorData().new(body, plant_id)
    plant_config = Config().get(plant_id)
    watering_threshold = plant_config.get('watering_threshold', 50)
    alert_threshold = plant_config.get('water_alert_threshold', 40)
    if (moisture := body.get('moisture')) is not None:
        if moisture < watering_threshold > alert_threshold:
            message = "Soil moisture level is low. Pump should start."
            needs_watering = True
        elif moisture > 85:
            message = "Soil moisture level is high. Please check your watering system."
            notify(message)
        elif moisture < alert_threshold:
            message = "Soil moisture level is very low. Please check your watering system."
            notify(message)
            needs_watering = True
        else:
            message = "Soil moisture level is normal."
        return {
            'statusCode': 200,
            'body': json.dumps({"message": message,
                "needs_watering": needs_watering,})
        }
    return {
        'statusCode': 400,
        'body': json.dumps({"message": "missing moisture data",})
    }

