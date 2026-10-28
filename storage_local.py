import sys
import boto3
from boto3.s3.transfer import TransferConfig
from botocore.config import Config

BUCKET = "files"
MB = 1024 * 1024

s3 = boto3.client(
    "s3",
    endpoint_url="http://localhost:9000",
    aws_access_key_id="admin",
    aws_secret_access_key="admin12345",
    region_name="us-east-1",
    config=Config(signature_version="s3v4"),
)
# файлы больше 64 МБ загружаются частями, поэтому размер не ограничен
cfg = TransferConfig(multipart_threshold=64 * MB, multipart_chunksize=64 * MB)

cmd = sys.argv[1] if len(sys.argv) > 1 else ""

if cmd == "upload":      # python storage_local.py upload файл ключ
    s3.upload_file(sys.argv[2], BUCKET, sys.argv[3], Config=cfg)
    print("Загружено:", sys.argv[3])
elif cmd == "download":  # python storage_local.py download ключ файл
    s3.download_file(BUCKET, sys.argv[2], sys.argv[3], Config=cfg)
    print("Скачано:", sys.argv[3])
elif cmd == "url":       # python storage_local.py url ключ
    print(s3.generate_presigned_url(
        "get_object", Params={"Bucket": BUCKET, "Key": sys.argv[2]}, ExpiresIn=900))
elif cmd == "list":
    for o in s3.list_objects_v2(Bucket=BUCKET).get("Contents", []):
        print(o["Key"], o["Size"])
else:
    print("Команды: upload, download, url, list")
