from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Post
from .forms import PostForm
from .monitoring import log_to_cloudwatch  # Import the function to log to CloudWatch

def post_list(request):
    """Display a list of all blog posts."""
    posts = Post.objects.all()  # Get all posts from the database
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    """Display a single post's detail."""
    post = get_object_or_404(Post, pk=pk)  # Get the post by primary key (pk)
    return render(request, 'blog/post_detail.html', {'post': post})

def create_post(request):
    """Handle the creation of a new post."""
    if request.method == 'POST':
        form = PostForm(request.POST)  # Get the data from the form submission
        if form.is_valid():
            post = form.save()  # Save the new post to the database
            # Log the post creation to CloudWatch
            log_to_cloudwatch(f"New post created: {post.title}")
            return redirect('post_list')  # Redirect to the post list view
    else:
        form = PostForm()  # If it's a GET request, display the empty form

    return render(request, 'blog/post_form.html', {'form': form})

def post_edit(request, pk):
    """Handle editing an existing post."""
    post = get_object_or_404(Post, pk=pk)  # Get the post by primary key
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)  # Pre-fill the form with the current post data
        if form.is_valid():
            post = form.save()  # Save the updated post
            # Log the post update to CloudWatch
            log_to_cloudwatch(f"Post updated: {post.title}")
            return redirect('post_list')  # Redirect to the post list view
    else:
        form = PostForm(instance=post)  # Pre-fill the form with the current post data

    return render(request, 'blog/post_form.html', {'form': form})

def post_delete(request, pk):
    """Handle deleting a post."""
    post = get_object_or_404(Post, pk=pk)  # Get the post by primary key
    post.delete()  # Delete the post from the database
    # Log the post deletion to CloudWatch
    log_to_cloudwatch(f"Post deleted: {post.title}")
    return redirect('post_list')  # Redirect to the post list view
