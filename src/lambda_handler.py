import os
import sys
from datetime import datetime, timedelta
from dotenv import load_dotenv
import boto3

sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
load_dotenv()

from ingestion import download_ticker
from features  import build_features
from model     import train_model

import pandas as pd
import joblib

TICKERS = ["AAPL", "MSFT"]
TMP = "/tmp"

s3 = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("MP_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("MP_SECRET_ACCESS_KEY"),
    region_name=os.getenv("MP_REGION")
)

BUCKET = os.getenv("MP_S3_BUCKET")

def upload_file(local_path, s3_key):
    s3.upload_file(local_path, BUCKET, s3_key)
    print(f"  ✅ Subido: {s3_key}")

def handler(event=None, context=None):
    print("🚀 MarketPulse Pipeline iniciado")

    end   = datetime.today().strftime("%Y-%m-%d")
    start = (datetime.today() - timedelta(days=730)).strftime("%Y-%m-%d")
    print(f"📅 Período: {start} → {end}")

    for ticker in TICKERS:
        print(f"\n📊 Procesando {ticker}...")

        # 1. Ingestion → /tmp
        print("  → Descargando datos...")
        df_raw = download_ticker(ticker, start, end)
        raw_path = f"{TMP}/{ticker}_raw.csv"
        df_raw.to_csv(raw_path)
        upload_file(raw_path, f"data/raw/{ticker}.csv")

        # 2. Features → /tmp
        print("  → Engineerando features...")
        df_feat = build_features(df_raw)
        feat_path = f"{TMP}/{ticker}_features.csv"
        df_feat.to_csv(feat_path)
        upload_file(feat_path, f"data/processed/{ticker}_features.csv")

        # 3. Model → /tmp
        print("  → Entrenando modelo...")
        model = train_model(df_feat, ticker)
        model_path = f"{TMP}/{ticker}_model.pkl"
        joblib.dump(model, model_path)
        upload_file(model_path, f"models/{ticker}_model.pkl")

    print("\n✅ Pipeline completado exitosamente")
    return {"statusCode": 200, "body": "Pipeline ejecutado correctamente"}

if __name__ == "__main__":
    import tempfile
    TMP = tempfile.gettempdir()
    handler()