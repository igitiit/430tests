from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Post
#from .models import BlogPost

#admin.site.register(BlogPost)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    list_filter = ('title','created_at')
    search_fields = ('title', 'content')
