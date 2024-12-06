import logging
from django.shortcuts import render, redirect, get_object_or_404
from .forms import PostForm
from .models import Post
from .monitoring import log_to_cloudwatch

# Configure logging
logging.basicConfig(filename='local_app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def post_list(request):
    posts = Post.objects.all()
    return render(request, 'blog/post_list.html', {'posts': posts})

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

                # Test CloudWatch logging
                test_cloudwatch_logging()

                return redirect('post_detail', pk=post.pk)
        else:
            form = PostForm()
    except Exception as e:
        # Log the exception to both CloudWatch and local file
        error_message = f"Exception occurred: {str(e)}"
        log_to_cloudwatch(error_message, log_group_name="DjangoBlogLogs2", log_stream_name="PostExceptions", aws_profile="James")
        logging.error(error_message)  # Log to local file
        raise e

    return render(request, 'blog/create_post.html', {'form': form})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

def test_cloudwatch_logging():
    """Function to log a test message to CloudWatch."""
    try:
        test_message = "Test log message to verify CloudWatch integration."
        log_to_cloudwatch(test_message, log_group_name="DjangoBlogLogs2", log_stream_name="TestLogs", aws_profile="James")
        logging.info("CloudWatch test logging succeeded.")
    except Exception as e:
        logging.error(f"Failed to log test message to CloudWatch: {str(e)}")
