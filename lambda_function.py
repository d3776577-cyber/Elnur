import json
import os
import boto3
from botocore.config import Config

BUCKET = os.environ.get("S3_BUCKET", "my-bucket")
s3 = boto3.client("s3", config=Config(signature_version="s3v4"))


def lambda_handler(event, context):
    body = json.loads(event.get("body") or "{}")
    action = body.get("action")  # "upload" или "download"
    key = body.get("key")        # имя файла в бакете

    if not action or not key:
        return _resp(400, {"error": "нужны action и key"})

    if action == "upload":
        url = s3.generate_presigned_url(
            "put_object",
            Params={"Bucket": BUCKET, "Key": key, "ServerSideEncryption": "AES256"},
            ExpiresIn=900,
        )
    elif action == "download":
        url = s3.generate_presigned_url(
            "get_object", Params={"Bucket": BUCKET, "Key": key}, ExpiresIn=900
        )
    else:
        return _resp(400, {"error": "action: upload или download"})

    return _resp(200, {"url": url, "expires_in": 900})


def _resp(code, data):
    return {
        "statusCode": code,
        "headers": {"Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*"},
        "body": json.dumps(data),
    }
