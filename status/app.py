import json
import os
from sensor_data import SensorData
import boto3
import time

sns = boto3.client('sns')

last_notification_time = 0


def lambda_handler(event, context):
    global last_notification_time
    current_time = time.time()
    body = json.loads(event['body'])

    needs_watering = False
    SensorData().new(body, "0")
    if moisture := body.get('moisture'):
        if moisture < 44:
            message = "Soil moisture level is low. Please water your plant."
            needs_watering = True
        elif moisture > 70:
            message = "Soil moisture level is high. Please check your watering system."
        else:
            message = "Soil moisture level is normal."

        if current_time - last_notification_time >= 300 and needs_watering:  # Check if 5 minutes have passed
            sns.publish(
                TopicArn=os.environ["ALERT_ARN"],
                Message=message,
                Subject='Plant Watering Alert'
            )
            last_notification_time = current_time  # Update the last notification time
        return {
            'statusCode': 200,
            'body': json.dumps({"message": message,
                "needs_watering": needs_watering,})
        }
    return {
        'statusCode': 400,
        'body': json.dumps({"message": "missing moisture data",})
    }

