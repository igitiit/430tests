import boto3
import time
import logging
from botocore.exceptions import ClientError, NoCredentialsError, PartialCredentialsError
import requests

# AWS Configuration
LOG_GROUP_NAME = "DjangoBlogLogs2"
LOG_STREAM_NAME = "PostCreation2"

# Initialize CloudWatch client dynamically
def get_instance_region():
    try:
        response = requests.get("http://169.254.169.254/latest/meta-data/placement/region")
        return response.text
    except Exception:
        return "us-east-1"  # Default region if metadata fails

region_name = get_instance_region()
cloudwatch = boto3.client('logs', region_name=region_name)

# Configure logging
logging.basicConfig(filename="cloudwatch_errors.log", level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s")

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

def log_to_cloudwatch(message, log_group_name=LOG_GROUP_NAME, log_stream_name=LOG_STREAM_NAME):
    try:
        # Ensure the log group exists
        ensure_log_group(log_group_name)

        # Ensure the log stream exists
        try:
            cloudwatch.create_log_stream(logGroupName=log_group_name, logStreamName=log_stream_name)
        except ClientError as e:
            if "ResourceAlreadyExistsException" not in str(e):
                raise

        # Hardcoded sequence token
        sequence_token = "49039859612205958146379088404712293159822848430144983396"

        # Create the log event
        timestamp = int(time.time() * 1000)
        log_event = {
            "timestamp": timestamp,
            "message": message,
        }

        response = cloudwatch.put_log_events(
            logGroupName=log_group_name,
            logStreamName=log_stream_name,
            logEvents=[log_event],
            sequenceToken=sequence_token
        )
        print(f"Log event successfully posted to {log_stream_name}.")
    except (NoCredentialsError, PartialCredentialsError):
        logging.error("Error: Unable to locate or incomplete AWS credentials.")
    except ClientError as e:
        logging.error(f"Failed to log to CloudWatch: {e}", exc_info=True)
    except Exception as e:
        logging.error(f"Unexpected error: {e}", exc_info=True)


