import logging
import boto3
import time
from botocore.exceptions import ClientError
from django.shortcuts import render, redirect, get_object_or_404
from .forms import PostForm
from .models import Post

# Configure local logging to file
logging.basicConfig(filename='local_app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# AWS CloudWatch logging configuration
LOG_GROUP_NAME = "DjangoBlogLogs2"
LOG_STREAM_NAME = "PostCreation2"

# Initialize CloudWatch client
cloudwatch = boto3.client('logs')

def log_to_cloudwatch(message, log_group_name=LOG_GROUP_NAME, log_stream_name=LOG_STREAM_NAME):
    """
    Send a log message to AWS CloudWatch Logs using PutLogEvents.
    """
    try:
        # Ensure the log group exists
        try:
            cloudwatch.create_log_group(logGroupName=log_group_name)
            logging.info(f"Log group '{log_group_name}' created.")
        except ClientError as e:
            if e.response['Error']['Code'] != 'ResourceAlreadyExistsException':
                logging.error(f"Failed to create log group '{log_group_name}': {e}", exc_info=True)

        # Ensure the log stream exists
        try:
            cloudwatch.create_log_stream(logGroupName=log_group_name, logStreamName=log_stream_name)
            logging.info(f"Log stream '{log_stream_name}' created.")
        except ClientError as e:
            if e.response['Error']['Code'] != 'ResourceAlreadyExistsException':
                logging.error(f"Failed to create log stream '{log_stream_name}': {e}", exc_info=True)

        # Hardcoded sequence token
        sequence_token = "49039859612205958146379088404712293159822848430144983396"

        # Prepare the log event
        timestamp = int(time.time() * 1000)  # Current time in milliseconds
        log_event = {
            'timestamp': timestamp,
            'message': message
        }

        # Send the log event
        put_log_response = cloudwatch.put_log_events(
            logGroupName=log_group_name,
            logStreamName=log_stream_name,
            logEvents=[log_event],
            sequenceToken=sequence_token
        )
        logging.info(f"Log sent to CloudWatch: {put_log_response}")
        return put_log_response
    except ClientError as e:
        logging.error(f"Failed to send log to CloudWatch: {e}", exc_info=True)
        raise
    except Exception as e:
        logging.error(f"Unexpected error: {e}", exc_info=True)
        raise

# View for listing posts
def post_list(request):
    posts = Post.objects.all()  # Get all posts from the database
    return render(request, 'blog/post_list.html', {'posts': posts})

# View for creating a new post
def create_post(request):
    logging.debug("Reached create_post function")  # Debug message to verify logging
    try:
        if request.method == 'POST':
            form = PostForm(request.POST, request.FILES)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.save()
                # Log the creation of a new post to both CloudWatch and local file
                message = f"New post created: {post.title}"
                log_to_cloudwatch(message, log_group_name="DjangoBlogLogs2", log_stream_name="PostCreation2")
                logging.info(message)  # Log to local file
                return redirect('post_detail', pk=post.pk)
        else:
            form = PostForm()
    except Exception as e:
        # Log the exception to both CloudWatch and local file
        error_message = f"Exception occurred: {str(e)}"
        log_to_cloudwatch(error_message, log_group_name="DjangoBlogLogs2", log_stream_name="PostExceptions")
        logging.error(error_message)  # Log to local file
        raise e
    return render(request, 'blog/create_post.html', {'form': form})

# View for displaying a post detail
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

# Function to test CloudWatch logging
def test_cloudwatch_logging(message):
    """
    Function to log a test message to CloudWatch.
    """
    try:
        log_to_cloudwatch(message, log_group_name="DjangoBlogLogs2", log_stream_name="TestLogs")
        logging.info("CloudWatch test logging succeeded.")
    except Exception as e:
        logging.error(f"Failed to log test message to CloudWatch: {str(e)}", exc_info=True)
