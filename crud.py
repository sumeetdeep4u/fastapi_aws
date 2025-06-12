import boto3
import os
from dotenv import load_dotenv
from botocore.exceptions import ClientError
import uuid

load_dotenv()

aws_config = {
    'aws_access_key_id': os.getenv("AWS_ACCESS_KEY_ID"),
    'aws_secret_access_key': os.getenv("AWS_SECRET_ACCESS_KEY"),
    'region_name': os.getenv("AWS_REGION")
}

dynamodb = boto3.resource('dynamodb', **aws_config)
s3 = boto3.client('s3', **aws_config)

table = dynamodb.Table(os.getenv("DYNAMODB_TABLE"))
bucket = os.getenv("S3_BUCKET_NAME")

def get_users(limit: int = 10):
    try:
        response = table.scan(Limit=limit)
        return response.get('Items', [])
    except ClientError as e:
        print("DynamoDB scan error:", e)
        raise Exception(f"Could not retrieve users: {e}")


def create_user(user: dict):
    table.put_item(Item=user)
    return user

def get_user(user_id: str):
    response = table.get_item(Key={'user_id': user_id})
    return response.get('Item')

def delete_user(user_id: str):
    try:
        response = table.delete_item(
            Key={'user_id': user_id}
        )
        return response
    except ClientError as e:
        print("DynamoDB delete error:", e)
        raise Exception(f"Could not delete user: {e}")

def upload_file_to_s3(file, filename):
    s3_key = f"uploads/{uuid.uuid4()}_{filename}"
    try:
        s3.upload_fileobj(file.file, bucket, s3_key)
        url = f"https://{bucket}.s3.{aws_config['region_name']}.amazonaws.com/{s3_key}"
        return url
    except ClientError as e:
        raise Exception(f"Upload failed: {e}")
