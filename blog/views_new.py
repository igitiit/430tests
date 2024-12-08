import logging
import boto3
from botocore.exceptions import ClientError
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Post
import time

from .log_util import log_to_cloudwatch  # Import the log function

# AWS CloudWatch Configuration
LOG_GROUP_NAME = "DjangoBlogLogs"
LOG_STREAM_NAME = "PostCreation"

# Initialize AWS CloudWatch Logs client
client = boto3.client('logs', region_name='us-east-1')

# Create a logger instance
logger = logging.getLogger('mylogger')  # Use 'mylogger' defined in settings.py

def some_view(request):
    logger.debug('This is a debug message')
    logger.info('This is an info message')
    logger.warning('This is a warning message')

    return HttpResponse('Logging test complete!')

# Local Logging Setup
logging.basicConfig(
    filename='local_app.log', 
    level=logging.DEBUG, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Ensure the CloudWatch log stream exists
def ensure_log_stream():
    """Ensure CloudWatch log stream exists."""
    try:
        client.create_log_stream(
            logGroupName=LOG_GROUP_NAME, 
            logStreamName=LOG_STREAM_NAME
        )
        logging.info(f"Log stream '{LOG_STREAM_NAME}' created.")
    except client.exceptions.ResourceAlreadyExistsException:
        logging.info(f"Log stream '{LOG_STREAM_NAME}' already exists.")
    except ClientError as e:
        logging.error(f"Error creating log stream: {str(e)}")


# Log to CloudWatch
def log_to_cloudwatch(message):
    try:
        response = client.describe_log_streams(
            logGroupName=LOG_GROUP_NAME, 
            logStreamNamePrefix=LOG_STREAM_NAME
        )

        log_stream = response['logStreams'][0]
        sequence_token = log_stream.get('uploadSequenceToken', None)

        log_event = {
            'logGroupName': LOG_GROUP_NAME,
            'logStreamName': LOG_STREAM_NAME,
            'logEvents': [
                {
                    'timestamp': int(time.time() * 1000),
                    'message': message,
                }
            ]
        }

        if sequence_token:
            log_event['sequenceToken'] = sequence_token

        response = client.put_log_events(**log_event)
        logging.info(f"Successfully logged to CloudWatch: {message}")

    except ClientError as e:
        logging.error(f"CloudWatch logging failed: {str(e)}")

# Create Post View
def create_post(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")

        # Create the post in the database
        post = Post.objects.create(title=title, content=content)

        # Log to AWS CloudWatch
        log_message = f"New post created: {title}"
        log_to_cloudwatch(log_message)

        return JsonResponse({'message': 'Post created successfully!'})

    return JsonResponse({'error': 'Invalid request'}, status=400)

# Post Detail View
def post_detail(request, pk):
    """Display post details."""
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})


# Post List View
def post_list(request):
    """Simple post list."""
    return HttpResponse("This is the post list view.")


# Test Logging View
def test_log(request):
    """Test CloudWatch logging."""
    log_to_cloudwatch("Test log from Django")
    return JsonResponse({'message': 'Log sent!'})


# Ensure CloudWatch log stream at server startup
ensure_log_stream()
