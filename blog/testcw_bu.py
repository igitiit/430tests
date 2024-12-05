import boto3
import time
from botocore.exceptions import ClientError, NoCredentialsError, PartialCredentialsError

# Initialize a session with the 'James' profile
session = boto3.Session(profile_name='default')
cloudwatch = session.client('logs')

# Constants
LOG_GROUP_NAME = "DjangoBlogLogs2"
LOG_STREAM_NAME = "PostCreation2"

try:
    # 1. Create a Log Stream
    print(f"Creating log stream '{LOG_STREAM_NAME}' in log group '{LOG_GROUP_NAME}'...")
    try:
        cloudwatch.create_log_stream(logGroupName=LOG_GROUP_NAME, logStreamName=LOG_STREAM_NAME)
        print(f"Log stream '{LOG_STREAM_NAME}' created successfully.")
    except ClientError as e:
        if "ResourceAlreadyExistsException" in str(e):
            print(f"Log stream '{LOG_STREAM_NAME}' already exists.")
        else:
            raise e

    # 2. Post a Log Event
    timestamp = int(time.time() * 1000)  # Current time in milliseconds
    log_event_message = "This is a test log entry for PostCreation2."

    print(f"Posting a log event to '{LOG_STREAM_NAME}'...")
    response = cloudwatch.put_log_events(
        logGroupName=LOG_GROUP_NAME,
        logStreamName=LOG_STREAM_NAME,
        logEvents=[
            {
                "timestamp": timestamp,
                "message": log_event_message,
            }
        ]
    )

    print("Log event posted successfully.")
    print("Response:", response)

except NoCredentialsError:
    print("Error: Unable to locate credentials. Ensure AWS credentials are set up correctly.")
except PartialCredentialsError:
    print("Error: Incomplete credentials configuration. Check your AWS credentials.")
except ClientError as e:
    print(f"ClientError: {e}")
except Exception as e:
    print(f"Error: {e}")

