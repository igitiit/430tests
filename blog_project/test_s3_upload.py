import boto3
import pytest
from moto import mock_aws

# Mock the S3 service
@mock_aws
def test_upload_to_s3():
    # Initialize mock S3
    s3 = boto3.client('s3', region_name='us-east-1')
    bucket_name = 'coursera2025-bucket'

    # Create a mock bucket
    s3.create_bucket(Bucket=bucket_name)

    # Upload a file to the mock S3 bucket
    s3.put_object(Bucket=bucket_name, Key='testfile.txt', Body=b'Hello world!')

    # Retrieve the uploaded file
    response = s3.get_object(Bucket=bucket_name, Key='testfile.txt')
    data = response['Body'].read()

    # Assert that the data matches what was uploaded
    assert data == b'Hello world!'

# Run the test if this file is executed
if __name__ == "__main__":
    test_upload_to_s3()

