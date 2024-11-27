# blog/forms.py
from django import forms
from .models import Post
#from .models import BlogPost

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'image']


'''
class BlogPostForm(forms.ModelForm):
    image = forms.ImageField(required=False)

    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'image']
'''
