import os
import django
from django.conf import settings
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Set up Django environment

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog_project.blog_project.settings')
django.setup()

def test_s3_settings():
    try:
        # Create a session using the credentials in the Django settings
        s3 = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_S3_REGION_NAME
        )

        # Attempt to list buckets or objects in the specified bucket
        response = s3.list_objects_v2(Bucket=settings.AWS_STORAGE_BUCKET_NAME)
        print(f"Successfully connected to S3. Bucket contains: {response.get('Contents', [])}")
    except NoCredentialsError:
        print("Credentials not available.")
    except PartialCredentialsError:
        print("Incomplete credentials provided.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    test_s3_settings()
