import boto3
from config.config import S3_BUCKET_Name, AWS_ENDPOINT

s3 = boto3.client("s3", endpoint_url=AWS_ENDPOINT)


def upload_image_to_s3(key, data):
    s3.put_object(
        Bucket=S3_BUCKET_Name,
        Key=key,
        Body=data
    )


def generate_download_url(key):
    url = s3.generate_presigned_url(
        "get_object",
        Params={
            "Bucket": S3_BUCKET_Name,
            "Key": key
        },
        ExpiresIn=3600
    )

    return url


def delete_image(key):
    s3.delete_object(
        Bucket=S3_BUCKET_Name,
        Key=key
    )
