import os
import boto3

def upload_file_to_s3(bucket_name, file_name, object_name):
    # Initialize a session using your AWS credentials
    s3 = boto3.client('s3')

    # Upload the file
    s3.upload_file(file_name, bucket_name, object_name)
    print(f"File {file_name} uploaded to bucket {bucket_name} as {object_name}")

def download_file_from_s3(bucket_name, object_name, file_name):
    # Initialize a session using your AWS credentials
    s3 = boto3.client('s3')

    # Download the file
    s3.download_file(bucket_name, object_name, file_name)
    print(f"File {object_name} downloaded from bucket {bucket_name} as {file_name}")

if __name__ == "__main__":
    bucket_name = 'coursera2025-bucket'  # replace with your actual bucket name
    file_name = os.path.join(os.path.dirname(__file__), 'testfile.txt')
    object_name = 's3dir/testfile.txt'
    
    # Assuming 'testfile.txt' is in the same directory as this script
    upload_file_to_s3(bucket_name, file_name, object_name)
    download_file_from_s3(bucket_name, object_name, 'downloaded_testfile.txt')
