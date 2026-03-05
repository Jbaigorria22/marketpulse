# src/ingestion.py
import yfinance as yf
import pandas as pd
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from config import TICKERS, DATE_START, DATE_END, DATA_RAW_PATH


def download_ticker(ticker: str, start: str, end: str) -> pd.DataFrame:
    print(f"  📥 Descargando {ticker}...")

    df = yf.download(ticker, start=start, end=end)

    if df.empty:
        print(f"  ⚠️  No se encontraron datos para {ticker}")
        return None

    print(f"  ✅ {ticker}: {len(df)} registros ({start} → {end})")
    return df


def save_raw_data(df: pd.DataFrame, ticker: str) -> str:
    os.makedirs(DATA_RAW_PATH, exist_ok=True)
    filepath = f"{DATA_RAW_PATH}{ticker}.csv"
    df.to_csv(filepath)
    print(f"  💾 Guardado en {filepath}")
    return filepath


def run_ingestion():
    print("\n🚀 Iniciando ingesta de datos MarketPulse")
    print(f"   Tickers : {TICKERS}")
    print(f"   Período : {DATE_START} → {DATE_END}\n")

    resultados = {}
    for ticker in TICKERS:
        df = download_ticker(ticker, DATE_START, DATE_END)
        if df is not None:
            filepath = save_raw_data(df, ticker)
            resultados[ticker] = filepath

    print(f"\n✅ Ingesta completa: {len(resultados)}/{len(TICKERS)} tickers descargados")
    return resultados


if __name__ == "__main__":
    run_ingestion()