#Lambda Code for excel file to S3
import json
import boto3
import os
from datetime import datetime

s3 = boto3.client('s3')
BUCKET_NAME = os.environ.get('BUCKET_NAME')

def lambda_handler(event, context):
    try:
        # Parse incoming JSON body
        body = json.loads(event['body'])

        # Validate that body is an array
        if not isinstance(body, list):
            return {
                "statusCode": 400,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({"error": "Expected an array of objects"})
            }

        # Prepare response details
        saved_files = []

        # Loop through each row and save as separate file
        for idx, row in enumerate(body, start=1):
            timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
            file_key = f"requests/row_{idx}_{timestamp}.json"

            s3.put_object(
                Bucket=BUCKET_NAME,
                Key=file_key,
                Body=json.dumps(row),
                ContentType="application/json"
            )

            saved_files.append(file_key)

        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({
                "message": "Data saved successfully!",
                "rows_received": len(body),
                "files": saved_files
            })
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": str(e)})
        }
