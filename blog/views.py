from django.shortcuts import render, redirect, get_object_or_404
from .forms import PostForm
from .models import Post
from .monitoring import log_to_cloudwatch  # Import the logging function

def post_list(request):
    posts = Post.objects.all()
    return render(request, 'blog/post_list.html', {'posts': posts})

def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()

            # Log the creation of a new post to CloudWatch
            log_to_cloudwatch(
                f"New post created: {post.title}",
                log_group_name="DjangoBlogLogs2",
                log_stream_name="PostCreation2",
                aws_profile="James"
            )
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/create_post.html', {'form': form})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})
