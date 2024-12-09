from django.shortcuts import render, redirect
from .forms import PostForm
from .models import Post
import logging
import boto3
import time

logging.basicConfig(filename='local_app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def log_to_cloudwatch(message, log_group_name, log_stream_name):
    """
    Send a log message to AWS CloudWatch Logs using PutLogEvents.
    """
    client = boto3.client('logs')

    try:
        # Ensure the log group exists
        try:
            client.create_log_group(logGroupName=log_group_name)
            logging.info(f"Log group '{log_group_name}' created.")
        except ClientError as e:
            if e.response['Error']['Code'] != 'ResourceAlreadyExistsException':
                logging.info(f"Log group '{log_group_name}' already exists.")

        # Ensure the log stream exists
        try:
            client.create_log_stream(logGroupName=log_group_name, logStreamName=log_stream_name)
            logging.info(f"Log stream '{log_stream_name}' created.")
        except ClientError as e:
            if e.response['Error']['Code'] != 'ResourceAlreadyExistsException':
                logging.info(f"Log stream '{log_stream_name}' already exists.")

        # Get the sequence token for the log stream
        response = client.describe_log_streams(logGroupName=log_group_name, logStreamNamePrefix=log_stream_name)
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
        put_log_response = client.put_log_events(
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

def main():
    # Test the logging functionality by posting a test message
    message = "Test log message from views.py"
    log_to_cloudwatch(message, log_group_name="DjangoBlogLogs2", log_stream_name="TestStream")

