import logging
from django.shortcuts import render, redirect, get_object_or_404
from .forms import PostForm
from .models import Post
from .monitoring import log_to_cloudwatch  # Import the log_to_cloudwatch function from monitoring.py

# Configure local logging
logging.basicConfig(filename='local_app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def create_post(request):
    """
    View to create a new blog post and log its creation to CloudWatch and locally.
    """
    logging.debug("Reached create_post function")  # Debug message to verify logging
    try:
        if request.method == 'POST':
            form = PostForm(request.POST, request.FILES)
            if form.is_valid():
                # Create and save the post object
                post = form.save(commit=False)
                post.author = request.user
                post.save()

                # Log the creation of a new post to both CloudWatch and local file
                message = f"New post created: {post.title}"
                
                # Send log to CloudWatch using the log_to_cloudwatch function from monitoring.py
                log_to_cloudwatch(message, log_group_name="DjangoBlogLogs2", log_stream_name="PostCreation2")

                # Log the same message locally for debugging
                logging.info(message)

                # Redirect to the post's detail page after successful creation
                return redirect('post_detail', pk=post.pk)
        else:
            form = PostForm()

    except Exception as e:
        # Log any exceptions that occur to CloudWatch and locally
        error_message = f"Exception occurred while creating a post: {str(e)}"
        log_to_cloudwatch(error_message, log_group_name="DjangoBlogLogs2", log_stream_name="PostExceptions")
        logging.error(error_message)  # Log to local file
        raise e  # Reraise exception to be handled by Django error handling

    return render(request, 'blog/create_post.html', {'form': form})

def post_list(request):
    """
    View for listing all blog posts.
    """
    posts = Post.objects.all()
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    """
    View for displaying the details of a specific post.
    """
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

# Function to test CloudWatch logging (can be called during debugging if necessary)
def test_cloudwatch_logging(message):
    """
    Function to log a test message to CloudWatch for debugging purposes.
    """
    try:
        log_to_cloudwatch(message, log_group_name="DjangoBlogLogs2", log_stream_name="TestLogs")
        logging.info("CloudWatch test logging succeeded.")
    except Exception as e:
        logging.error(f"Failed to log test message to CloudWatch: {str(e)}", exc_info=True)
