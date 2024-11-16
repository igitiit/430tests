from django.shortcuts import render

# Create your views here.

from django.shortcuts import render,redirect
from .forms import BlogPostForm
from .models import Post

<<<<<<< HEAD
'''prev'''
def post_list(request):
    posts = Post.objects.all()
    return render(request, 'blog/post_list.html', {'posts': posts})

=======
'''
def post_list(request):
    posts = Post.objects.all()
    return render(request, 'blog/post_list.html', {'posts': posts})
'''
>>>>>>> f122cb548384acb51ad855a2dc74c575d5524ae0
def create_post(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = BlogPostForm()
    return render(request, 'blog/create_post.html', {'form': form})

