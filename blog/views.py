import logging
import boto3
import time
from botocore.exceptions import ClientError
from django.shortcuts import render, redirect, get_object_or_404
from .forms import PostForm
from .models import Post

# Configure local logging to file
logging.basicConfig(filename='local_app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# AWS CloudWatch logging configuration
LOG_GROUP_NAME = "DjangoBlogLogs2"
LOG_STREAM_NAME = "PostCreation2"

# Initialize CloudWatch client
cloudwatch = boto3.client('logs')

def log_to_cloudwatch(message, log_group_name=LOG_GROUP_NAME, log_stream_name=LOG_STREAM_NAME):
    """
    Send a log message to AWS CloudWatch Logs using PutLogEvents.
    """
    try:
        # Ensure the log group exists
        try:
            cloudwatch.describe_log_groups(logGroupNamePrefix=log_group_name)
        except ClientError as e:
            if 'ResourceNotFoundException' in str(e):
                cloudwatch.create_log_group(logGroupName=log_group_name)
                logging.info(f"Log group '{log_group_name}' created.")
            else:
                logging.error(f"Error checking log group: {e}", exc_info=True)

        # Ensure the log stream exists
        try:
            cloudwatch.describe_log_streams(logGroupName=log_group_name, logStreamNamePrefix=log_stream_name)
        except ClientError as e:
            if 'ResourceNotFoundException' in str(e):
                cloudwatch.create_log_stream(logGroupName=log_group_name, logStreamName=log_stream_name)
                logging.info(f"Log stream '{log_stream_name}' created.")
            else:
                logging.error(f"Error checking log stream: {e}", exc_info=True)

        # Get the sequence token for the log stream
        response = cloudwatch.describe_log_streams(logGroupName=log_group_name, logStreamNamePrefix=log_stream_name)
        log_streams = response.get('logStreams', [])
        if not log_streams:
            raise Exception(f"Log stream '{log_stream_name}' not found in log group '{log_group_name}'.")
        sequence_token = log_streams[0].get('uploadSequenceToken', None)

        # Prepare the log event
        timestamp = int(time.time() * 1000)  # Current time in milliseconds
        log_event = {
            'timestamp': timestamp,
            'message': message
        }

        # Send the log event
        put_log_response = cloudwatch.put_log_events(
            logGroupName=log_group_name,
            logStreamName=log_stream_name,
            logEvents=[log_event],
            sequenceToken=sequence_token  # Include token if required
        )
        logging.info(f"Log sent to CloudWatch: {put_log_response}")
        return put_log_response

    except ClientError as e:
        logging.error(f"Failed to send log to CloudWatch: {e}", exc_info=True)
        raise
    except Exception as e:
        logging.error(f"Unexpected error: {e}", exc_info=True)
        raise
