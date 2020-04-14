import boto3
import constants


def _configure_s3_client():
    s3_client = boto3.client(
        "s3", aws_access_key_id=constants.S3_ACCESS_KEY, aws_secret_access_key=constants.S3_SECRET_KEY
    )
    return s3_client