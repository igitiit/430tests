import boto3
import os

def log_to_cloudwatch(log_group_name, log_stream_name, message):
    client = boto3.client(
        'logs',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        region_name=os.getenv('AWS_REGION')
    )

    # Ensure log group exists
    try:
        client.create_log_group(logGroupName=log_group_name)
    except client.exceptions.ResourceAlreadyExistsException:
        pass

    # Ensure log stream exists
    try:
        client.create_log_stream(logGroupName=log_group_name, logStreamName=log_stream_name)
    except client.exceptions.ResourceAlreadyExistsException:
        pass

    # Fetch sequence token
    response = client.describe_log_streams(
        logGroupName=log_group_name,
        logStreamNamePrefix=log_stream_name
    )
    token = response['logStreams'][0].get('uploadSequenceToken')

    # Send log event
    log_event = {
        'logGroupName': log_group_name,
        'logStreamName': log_stream_name,
        'logEvents': [
            {'timestamp': int(time.time() * 1000), 'message': message},
        ],
    }
    if token:
        log_event['sequenceToken'] = token

    client.put_log_events(**log_event)
