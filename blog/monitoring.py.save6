import boto3
import time
from botocore.exceptions import ClientError, NoCredentialsError, PartialCredentialsError

# AWS Configuration
LOG_GROUP_NAME = "DjangoBlogLogs2"
LOG_STREAM_NAME = "PostCreation2"  # Use the actual stream name you're targeting

# Initialize CloudWatch client
cloudwatch = boto3.client('logs', region_name='us-east-1')

def get_sequence_token(log_group_name, log_stream_name):
    try:
        response = cloudwatch.describe_log_streams(
            logGroupName=log_group_name,
            logStreamNamePrefix=log_stream_name,
        )
        log_stream = next(
            (stream for stream in response['logStreams'] if stream['logStreamName'] == log_stream_name), None)
        
        if log_stream:
            return log_stream.get('uploadSequenceToken')
    except ClientError as e:
        print(f"Error getting sequence token: {e}")
        return None

def log_to_cloudwatch(message, log_group_name=LOG_GROUP_NAME, log_stream_name=LOG_STREAM_NAME):
    try:
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

        if sequence_token:
            response = cloudwatch.put_log_events(
                logGroupName=log_group_name,
                logStreamName=log_stream_name,
                logEvents=[log_event],
                sequenceToken=sequence_token  # Pass the token if it's available
            )
        else:
            response = cloudwatch.put_log_events(
                logGroupName=log_group_name,
                logStreamName=log_stream_name,
                logEvents=[log_event]
            )
        
        print(f"Log event successfully posted to {log_stream_name}.")
    except (NoCredentialsError, PartialCredentialsError):
        print("Error: Unable to locate or incomplete AWS credentials.")
    except ClientError as e:
        print(f"Failed to log to CloudWatch: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

# Example usage
if __name__ == "__main__":
    test_message = "This is a test log message 2."
    log_to_cloudwatch(test_message)
