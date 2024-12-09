import time
import logging
import boto3
from botocore.exceptions import ClientError

# Initialize the CloudWatch client
cloudwatch = boto3.client('logs')

LOG_GROUP_NAME = "DjangoBlogLogs2"
LOG_STREAM_NAME = "PostCreation2"

def ensure_log_group(log_group_name):
    """Ensure the log group exists."""
    try:
        cloudwatch.describe_log_groups(logGroupNamePrefix=log_group_name)
    except ClientError as e:
        logging.error(f"Failed to describe log groups: {e}")
        raise
 
def get_sequence_token(log_group_name, log_stream_name):
    """Retrieve the next sequence token from the log stream."""
    try:
        response = cloudwatch.describe_log_streams(
            logGroupName=log_group_name,
            logStreamNamePrefix=log_stream_name,
        )
        
        log_stream = next(
            (stream for stream in response['logStreams'] if stream['logStreamName'] == log_stream_name), None)
        
        if log_stream and 'uploadSequenceToken' in log_stream:
            return log_stream['uploadSequenceToken']
        return None
    except ClientError as e:
        logging.error(f"Error retrieving sequence token: {e}")
        return None

def log_to_cloudwatch(message, log_group_name=LOG_GROUP_NAME, log_stream_name=LOG_STREAM_NAME):
    """Log a message to CloudWatch."""
    try:
        # Ensure the log group exists
        ensure_log_group(log_group_name)

        # Ensure the log stream exists
        try:
            cloudwatch.create_log_stream(logGroupName=log_group_name, logStreamName=log_stream_name)
        except ClientError as e:
            if "ResourceAlreadyExistsException" not in str(e):
                raise

        # Get the sequence token for the stream
        sequence_token = get_sequence_token(log_group_name, log_stream_name)
        
        # Create the log event
        timestamp = int(time.time() * 1000)
        log_event = {
            "timestamp": timestamp,
            "message": message,
        }

        # If a sequence token exists, use it for the log post
        if sequence_token:
            response = cloudwatch.put_log_events(
                logGroupName=log_group_name,
                logStreamName=log_stream_name,
                logEvents=[log_event],
                sequenceToken=sequence_token  # Use the token if available
            )
        else:
            # If no token, it's the first post, so don't pass a sequence token
            response = cloudwatch.put_log_events(
                logGroupName=log_group_name,
                logStreamName=log_stream_name,
                logEvents=[log_event]
            )
        
        # Print out the next sequence token for logging purposes
        if 'nextSequenceToken' in response:
            print(f"Next sequence token: {response['nextSequenceToken']}")
            return response['nextSequenceToken']

        print(f"Log event successfully posted to {log_stream_name}.")
    except (ClientError, Exception) as e:
        logging.error(f"Failed to log to CloudWatch: {e}", exc_info=True)

# For testing the log posting manually, you can run this function as a standalone script
if __name__ == "__main__":
    log_to_cloudwatch("This is a test log message")
