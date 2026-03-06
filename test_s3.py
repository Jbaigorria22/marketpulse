import boto3
from dotenv import load_dotenv
import os

load_dotenv()

s3 = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION")
)

bucket = os.getenv("S3_BUCKET")

# Listar carpetas del bucket
response = s3.list_objects_v2(Bucket=bucket, Delimiter="/")

print(f"✅ Conexión exitosa al bucket: {bucket}")
print("Carpetas encontradas:")
for prefix in response.get("CommonPrefixes", []):
    print(f"  📁 {prefix['Prefix']}")