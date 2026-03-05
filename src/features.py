# src/features.py
import pandas as pd
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from config import DATA_RAW_PATH, DATA_PROCESSED_PATH


def load_raw(ticker: str) -> pd.DataFrame:
    filepath = f"{DATA_RAW_PATH}{ticker}.csv"
    df = pd.read_csv(filepath, header=[0, 1], index_col=0, parse_dates=True)
    df.columns = df.columns.get_level_values(0)
    return df


def build_features(df: pd.DataFrame) -> pd.DataFrame:
    feat = pd.DataFrame(index=df.index)

    feat["close"] = df["Close"]

    # Retorno diario: cuánto subió o bajó el precio en % respecto a ayer
    # Ej: si ayer cerró en $100 y hoy en $103 → return_1d = 0.03 (3%)
    feat["return_1d"] = feat["close"].pct_change()

    # Media móvil 7 días: promedio del precio de los últimos 7 días
    # Suaviza el ruido diario y muestra la tendencia corta
    feat["ma_7"] = feat["close"].rolling(7).mean()

    # Media móvil 21 días: igual pero ventana más larga → tendencia larga
    feat["ma_21"] = feat["close"].rolling(21).mean()

    # Volatilidad: qué tan bruscos son los movimientos en los últimos 7 días
    # Alta volatilidad = precio saltando mucho = más riesgo
    feat["volatility_7"] = feat["return_1d"].rolling(7).std()

    # Target: el precio de MAÑANA — esto es lo que el modelo tiene que predecir
    # shift(-1) "mueve" la columna un día hacia atrás
    feat["target"] = feat["close"].shift(-1)

    # Distancia entre precio y sus medias (captura momentum)
    feat["dist_ma7"]  = (feat["close"] - feat["ma_7"])  / feat["ma_7"]
    feat["dist_ma21"] = (feat["close"] - feat["ma_21"]) / feat["ma_21"]

    feat = feat.dropna()
    return feat


def save_processed(df: pd.DataFrame, ticker: str) -> str:
    os.makedirs(DATA_PROCESSED_PATH, exist_ok=True)
    filepath = f"{DATA_PROCESSED_PATH}{ticker}_features.csv"
    df.to_csv(filepath)
    print(f"  💾 Features guardadas en {filepath}")
    return filepath


def run_features(tickers: list) -> dict:
    print("\n⚙️  Construyendo features MarketPulse\n")
    resultados = {}

    for ticker in tickers:
        print(f"  🔧 Procesando {ticker}...")
        df_raw  = load_raw(ticker)
        df_feat = build_features(df_raw)
        filepath = save_processed(df_feat, ticker)
        print(f"  ✅ {ticker}: {len(df_feat)} filas | columnas: {list(df_feat.columns)}")
        resultados[ticker] = df_feat

    print(f"\n✅ Features completas: {len(resultados)} tickers listos para el modelo")
    return resultados


if __name__ == "__main__":
    from config import TICKERS
    run_features(TICKERS)