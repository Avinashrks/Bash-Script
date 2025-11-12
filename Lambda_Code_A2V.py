#Lambda code to accept two value from static website and save the data to S3
import json
import boto3
import os

s3 = boto3.client('s3')
BUCKET_NAME = os.environ.get('BUCKET_NAME')

def lambda_handler(event, context):
    body = json.loads(event['body'])
    value1 = body.get('value1')
    value2 = body.get('value2')

    data = {"value1": value1, "value2": value2}
    file_key = f"requests/{value1}_{value2}.json"

    s3.put_object(Bucket=BUCKET_NAME, Key=file_key, Body=json.dumps(data))

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"message": "Data saved successfully!", "s3_key": file_key})
    }
