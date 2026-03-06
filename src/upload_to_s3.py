# src/upload_to_s3.py
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

BUCKET = os.getenv("S3_BUCKET")

FILES = [
    # (archivo local,                destino en S3)
    ("data/raw/AAPL.csv",            "data/raw/AAPL.csv"),
    ("data/raw/MSFT.csv",            "data/raw/MSFT.csv"),
    ("data/processed/AAPL_features.csv", "data/processed/AAPL_features.csv"),
    ("data/processed/MSFT_features.csv", "data/processed/MSFT_features.csv"),
    ("models/AAPL_model.pkl",        "models/AAPL_model.pkl"),
    ("models/MSFT_model.pkl",        "models/MSFT_model.pkl"),
]

def upload_all():
    print(f"📤 Subiendo archivos a s3://{BUCKET}\n")
    success = 0
    for local_path, s3_key in FILES:
        if os.path.exists(local_path):
            s3.upload_file(local_path, BUCKET, s3_key)
            print(f"  ✅ {local_path} → s3://{BUCKET}/{s3_key}")
            success += 1
        else:
            print(f"  ⚠️  No encontrado: {local_path}")
    print(f"\n📦 {success}/{len(FILES)} archivos subidos correctamente.")

if __name__ == "__main__":
    upload_all()