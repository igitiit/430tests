import boto3
import time
from botocore.exceptions import ClientError, NoCredentialsError, PartialCredentialsError

# Initialize AWS session and CloudWatch client
AWS_PROFILE = "default"
LOG_GROUP_NAME = "DjangoBlogLogs2"
session = boto3.Session(profile_name=AWS_PROFILE)
cloudwatch = session.client('logs')

def log_to_cloudwatch(message, log_group_name=LOG_GROUP_NAME, log_stream_name="DjangoBlogLogs2", aws_profile=AWS_PROFILE):
    global cloudwatch
    
    # Create a new session and client if using a different profile
    if aws_profile != AWS_PROFILE:
        session = boto3.Session(profile_name="default")
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
    except (NoCredentialsError, PartialCredentialsError):
        print("Error: Unable to locate or incomplete AWS credentials.")
    except ClientError as e:
        print(f"Failed to log to CloudWatch: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
