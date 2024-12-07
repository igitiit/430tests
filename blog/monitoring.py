import boto3
import time
from botocore.exceptions import ClientError, NoCredentialsError, PartialCredentialsError

# AWS Configuration
LOG_GROUP_NAME = "DjangoBlogLogs2"
LOG_STREAM_NAME = "DjangoBlogLogs2"

# Initialize CloudWatch client
cloudwatch = boto3.client('logs', region_name='us-east-1')

def log_to_cloudwatch(message, log_group_name=LOG_GROUP_NAME, log_stream_name=LOG_STREAM_NAME):
    try:
        # Ensure the log stream exists
        try:
            cloudwatch.create_log_stream(logGroupName=log_group_name, logStreamName=log_stream_name)
        except ClientError as e:
            if "ResourceAlreadyExistsException" not in str(e):
                raise

        # Create the log event
        timestamp = int(time.time() * 1000)
        response = cloudwatch.put_log_events(
            logGroupName=log_group_name,
            logStreamName=log_stream_name,
            logEvents=[
                {
                    "timestamp": timestamp,
                    "message": message,
                }
            ]
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
