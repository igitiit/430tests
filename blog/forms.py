# blog/forms.py
from django import forms
from .models import BlogPost

class BlogPostForm(forms.ModelForm):
    image = forms.ImageField(required=False)

    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'image']
