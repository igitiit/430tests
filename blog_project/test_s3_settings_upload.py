# test_s3_upload.py
import os
import django
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog_project.settings')
django.setup()

# Test uploading a file to S3
file_content = ContentFile(b'This is a test file for S3 upload')
file_name = 'test_s3_upload.txt'

file_path = default_storage.save(file_name, file_content)

print(f'File successfully uploaded to: {file_path}')
