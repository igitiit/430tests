import boto3
import time
import logging
from botocore.exceptions import ClientError

# AWS Configuration
LOG_GROUP_NAME = "DjangoBlogLogs2"
LOG_STREAM_NAME = "PostCreation2"

# Initialize CloudWatch client dynamically
cloudwatch = boto3.client('logs', region_name="us-east-1")

# Ensure log group exists
def ensure_log_group(log_group_name):
    try:
        cloudwatch.create_log_group(logGroupName=log_group_name)
        print(f"Log group '{log_group_name}' created.")
    except ClientError as e:
        if "ResourceAlreadyExistsException" in str(e):
            print(f"Log group '{log_group_name}' already exists.")
        else:
            logging.error(f"Failed to create log group: {e}")
            raise

# Fetch and return sequence token
def get_sequence_token(log_group_name, log_stream_name):
    try:
        response = cloudwatch.describe_log_streams(
            logGroupName=log_group_name,
            logStreamNamePrefix=log_stream_name,
        )
        log_stream = next(
            (stream for stream in response['logStreams'] if stream['logStreamName'] == log_stream_name), None)
        
        if log_stream:
            token = log_stream.get('uploadSequenceToken')
            print(f"Fetched sequence token: {token}")  # Debugging line
            return token
        else:
            print(f"No log stream found for {log_stream_name}")  # Debugging line
    except ClientError as e:
        logging.error(f"Error getting sequence token: {e}")
        return None

# Log to CloudWatch
def log_to_cloudwatch(message, log_group_name=LOG_GROUP_NAME, log_stream_name=LOG_STREAM_NAME):
    try:
        ensure_log_group(log_group_name)
        
        try:
            cloudwatch.create_log_stream(logGroupName=log_group_name, logStreamName=log_stream_name)
        except ClientError as e:
            if "ResourceAlreadyExistsException" not in str(e):
                raise
        
        sequence_token = get_sequence_token(log_group_name, log_stream_name)
        
        timestamp = int(time.time() * 1000)
        log_event = {
            "timestamp": timestamp,
            "message": message,
        }
        
        if sequence_token:
            response = cloudwatch.put_log_events(
                logGroupName=log_group_name,
                logStreamName=log_stream_name,
                logEvents=[log_event],
                sequenceToken=sequence_token
            )
        else:
            response = cloudwatch.put_log_events(
                logGroupName=log_group_name,
                logStreamName=log_stream_name,
                logEvents=[log_event]
            )
        
        print(f"Log event successfully posted to {log_stream_name}.")
    except Exception as e:
        logging.error(f"Unexpected error: {e}", exc_info=True)
