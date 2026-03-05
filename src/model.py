# src/model.py
import pandas as pd
import numpy as np
import os, sys, joblib

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from config import DATA_PROCESSED_PATH, MODEL_PATH, TICKERS

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score


def load_features(ticker: str) -> pd.DataFrame:
    """Carga el CSV de features generado por features.py"""
    filepath = f"{DATA_PROCESSED_PATH}{ticker}_features.csv"
    df = pd.read_csv(filepath, index_col=0, parse_dates=True)
    return df


def train_model(df: pd.DataFrame, ticker: str):
    """
    Entrena un RandomForest para predecir el precio de mañana.
    Retorna el modelo entrenado y las métricas de evaluación.
    """
    # Separamos features (X) del target (y)
    # X = las "pistas" que el modelo usa para aprender
    # y = lo que tiene que predecir (precio de mañana)
    FEATURES = ["close", "return_1d", "ma_7", "ma_21", "volatility_7", "dist_ma7", "dist_ma21"]
    X = df[FEATURES]
    y = df["target"]

    # Dividimos en 80% entrenamiento y 20% prueba
    # shuffle=False es CRÍTICO en series de tiempo
    # — no podemos mezclar el pasado con el futuro
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, shuffle=False
    )

    print(f"  📊 Train: {len(X_train)} días | Test: {len(X_test)} días")

    # Entrenamos el modelo
    model = RandomForestRegressor(
        n_estimators=100,   # 100 árboles de decisión
        random_state=42,    # semilla para reproducibilidad
        n_jobs=-1           # usa todos los núcleos del CPU
    )
    model.fit(X_train, y_train)

    # Evaluamos sobre el set de prueba
    y_pred = model.predict(X_test)

    mae = mean_absolute_error(y_test, y_pred)
    r2  = r2_score(y_test, y_pred)

    print(f"  📈 MAE  : ${mae:.2f}  (error promedio en dólares)")
    print(f"  📈 R²   : {r2:.4f}  (1.0 = perfecto, >0.90 = muy bueno)")

    return model, {"mae": mae, "r2": r2, "y_test": y_test, "y_pred": y_pred}


def save_model(model, ticker: str) -> str:
    """Guarda el modelo entrenado en disco"""
    os.makedirs(MODEL_PATH, exist_ok=True)
    filepath = f"{MODEL_PATH}{ticker}_model.pkl"
    joblib.dump(model, filepath)
    print(f"  💾 Modelo guardado en {filepath}")
    return filepath


def run_models(tickers: list) -> dict:
    """Función principal: entrena y guarda modelos para todos los tickers"""
    print("\n🤖 Entrenando modelos MarketPulse\n")
    resultados = {}

    for ticker in tickers:
        print(f"  🔧 Entrenando {ticker}...")
        df = load_features(ticker)
        model, metrics = train_model(df, ticker)
        save_model(model, ticker)
        resultados[ticker] = {"model": model, "metrics": metrics}
        print(f"  ✅ {ticker} listo\n")

    print("✅ Todos los modelos entrenados y guardados")
    return resultados


if __name__ == "__main__":
    run_models(TICKERS)