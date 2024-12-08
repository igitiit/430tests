import boto3
import time
import logging
from botocore.exceptions import ClientError

LOG_GROUP_NAME = "DjangoBlogLogs2"
LOG_STREAM_NAME = "PostCreation3"

# Initialize CloudWatch client
client = boto3.client('logs', region_name='us-east-1')

def log_to_cloudwatch(message):
    """Log a message to AWS CloudWatch."""
    try:
        logging.info("Starting CloudWatch log process...")
        
        response = client.describe_log_streams(
            logGroupName=LOG_GROUP_NAME, 
            logStreamNamePrefix=LOG_STREAM_NAME
        )
        
        logging.info(f"Log stream description: {response}")

        log_stream = response['logStreams'][0]
        sequence_token = log_stream.get('uploadSequenceToken', None)
        
        log_event = {
            'logGroupName': LOG_GROUP_NAME,
            'logStreamName': LOG_STREAM_NAME,
            'logEvents': [
                {
                    'timestamp': int(time.time() * 1000),
                    'message': message,
                }
            ]
        }

        if sequence_token:
            log_event['sequenceToken'] = sequence_token

        response = client.put_log_events(**log_event)
        logging.info(f"Successfully logged to CloudWatch: {response}")

    except ClientError as e:
        logging.error(f"CloudWatch logging failed: {str(e)}")
