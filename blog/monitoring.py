import boto3
import time
from botocore.exceptions import ClientError

def log_to_cloudwatch(message, log_group_name, log_stream_name, aws_profile):
    """
    Logs a message to the specified CloudWatch log group and stream.

    Args:
        message (str): The log message to be posted.
        log_group_name (str): The name of the CloudWatch log group.
        log_stream_name (str): The name of the CloudWatch log stream.
        aws_profile (str): The AWS CLI profile to use.
    """
    # Create a session using the specified AWS profile
    session = boto3.Session(profile_name=aws_profile)
    cloudwatch = session.client('logs')

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
    except ClientError as e:
        print(f"Failed to log to CloudWatch: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
