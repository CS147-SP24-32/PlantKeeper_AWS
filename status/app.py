import json
import os

import boto3
import time

sns = boto3.client('sns')

last_notification_time = 0


def lambda_handler(event, context):
    """Sample pure Lambda function

       Parameters
       ----------
       event: dict, required
           API Gateway Lambda Proxy Input Format

           Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

       context: object, required
           Lambda Context runtime methods and attributes

           Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

       Returns
       ------
       API Gateway Lambda Proxy Output Format: dict

           Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
       """

    # try:
    #     ip = requests.get("http://checkip.amazonaws.com/")
    # except requests.RequestException as e:
    #     # Send some context about this error to Lambda Logs
    #     print(e)

    #     raise e

    global last_notification_time
    current_time = time.time()
    moisture = int(event['queryStringParameters']['moisture'])
    needs_watering = False
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

