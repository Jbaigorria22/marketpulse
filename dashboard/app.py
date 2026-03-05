# dashboard/app.py
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import joblib
import numpy as np
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from config import TICKERS, DATA_PROCESSED_PATH, MODEL_PATH, FORECAST_DAYS

st.set_page_config(
    page_title="MarketPulse · Fintech Analytics Platform",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================================
# CUSTOM CSS - DISEÑO PROFESIONAL FINTECH
# ============================================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* Reset y estilos base */
* {
    font-family: 'Inter', sans-serif !important;
    box-sizing: border-box;
}

.stApp {
    background: #0B0E14;
    color: #E5E9F0;
}

[data-testid="collapsedControl"], 
#MainMenu, 
footer, 
header {
    display: none !important;
    visibility: hidden !important;
}

.block-container {
    padding: 0 !important;
    max-width: 100% !important;
}

/* ===== HEADER CON GLASSMORPHISM ===== */
.mp-header {
    background: rgba(11, 14, 20, 0.95);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border-bottom: 1px solid rgba(45, 55, 72, 0.3);
    padding: 1rem 2.5rem;
    display: flex;
    align-items: center;
    gap: 2.5rem;
    position: sticky;
    top: 0;
    z-index: 1000;
}

.mp-logo {
    font-size: 1.5rem;
    font-weight: 800;
    letter-spacing: -0.02em;
    background: linear-gradient(135deg, #FFFFFF 0%, #94A3B8 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.mp-logo span {
    background: linear-gradient(135deg, #3B82F6, #8B5CF6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.mp-badge {
    font-size: 0.7rem;
    background: linear-gradient(135deg, #3B82F6, #8B5CF6);
    padding: 0.25rem 1rem;
    border-radius: 20px;
    color: white;
    font-weight: 600;
    letter-spacing: 0.03em;
    margin-left: 1rem;
}

/* ===== CARDS PRINCIPALES ===== */
.mp-card {
    background: #14181F;
    border: 1px solid #252F3A;
    border-radius: 20px;
    padding: 1.5rem;
    transition: all 0.25s ease;
    box-shadow: 0 8px 16px -4px rgba(0, 0, 0, 0.3);
    height: 100%;
    position: relative;
    overflow: hidden;
}

.mp-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: linear-gradient(90deg, #3B82F6, #8B5CF6);
    opacity: 0;
    transition: opacity 0.25s ease;
}

.mp-card:hover {
    border-color: #3B82F6;
    transform: translateY(-4px);
    box-shadow: 0 16px 24px -8px rgba(59, 130, 246, 0.25);
}

.mp-card:hover::before {
    opacity: 1;
}

.mp-card-label {
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #6B7A8F;
    margin-bottom: 0.75rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.mp-card-value {
    font-size: 2rem;
    font-weight: 700;
    color: #FFFFFF;
    line-height: 1.2;
    letter-spacing: -0.02em;
    margin-bottom: 0.25rem;
}

.mp-card-sub {
    font-size: 0.85rem;
    font-weight: 500;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

/* ===== MODEL INFO CARD ===== */
.mp-model-card {
    background: #14181F;
    border: 1px solid #252F3A;
    border-radius: 20px;
    padding: 1.75rem;
    height: 100%;
    box-shadow: 0 8px 16px -4px rgba(0, 0, 0, 0.3);
}

.mp-model-title {
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #6B7A8F;
    margin-bottom: 1.25rem;
    padding-bottom: 0.75rem;
    border-bottom: 1px solid #252F3A;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.mp-model-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.6rem 0;
    border-bottom: 1px solid rgba(37, 47, 58, 0.5);
    font-size: 0.9rem;
}

.mp-model-key {
    color: #6B7A8F;
    font-weight: 500;
}

.mp-model-val {
    color: #E5E9F0;
    font-weight: 600;
}

/* ===== TABS PERSONALIZADAS ===== */
.stTabs [data-baseweb="tab-list"] {
    background: transparent !important;
    border-bottom: 1px solid #252F3A !important;
    gap: 0.75rem;
    padding: 0;
}

.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: #6B7A8F !important;
    font-size: 0.85rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.03em !important;
    padding: 0.75rem 1.75rem !important;
    border: none !important;
    border-bottom: 2px solid transparent !important;
    transition: all 0.2s !important;
    border-radius: 0 !important;
}

.stTabs [aria-selected="true"] {
    color: #FFFFFF !important;
    border-bottom: 2px solid #3B82F6 !important;
    background: linear-gradient(to top, rgba(59, 130, 246, 0.1), transparent) !important;
}

/* ===== SELECTBOX MEJORADO ===== */
div[data-baseweb="select"] > div {
    background: #14181F !important;
    border: 1px solid #252F3A !important;
    border-radius: 30px !important;
    color: #FFFFFF !important;
    font-size: 0.95rem !important;
    font-weight: 600 !important;
    padding: 0.5rem 1rem !important;
    transition: border-color 0.2s !important;
}

div[data-baseweb="select"] > div:hover {
    border-color: #3B82F6 !important;
}

/* ===== BOTONES DE PERÍODO ===== */
.stButton > button {
    background: transparent !important;
    border: 1px solid #252F3A !important;
    color: #6B7A8F !important;
    border-radius: 30px !important;
    font-size: 0.8rem !important;
    font-weight: 600 !important;
    padding: 0.4rem 1.25rem !important;
    transition: all 0.2s !important;
}

.stButton > button:hover {
    border-color: #3B82F6 !important;
    color: #FFFFFF !important;
    background: rgba(59, 130, 246, 0.1) !important;
}

.stButton > button:focus {
    border-color: #3B82F6 !important;
    color: #FFFFFF !important;
    background: rgba(59, 130, 246, 0.15) !important;
}

/* ===== CHECKBOXES ===== */
div[data-baseweb="checkbox"] {
    background: #14181F !important;
    border: 1px solid #252F3A !important;
    border-radius: 30px !important;
    padding: 0.3rem 1.25rem 0.3rem 0.75rem !important;
    transition: all 0.2s !important;
}

div[data-baseweb="checkbox"]:hover {
    border-color: #3B82F6 !important;
}

/* ===== TABLA DE PERFORMANCE ===== */
.mp-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.9rem;
}

.mp-table th {
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #6B7A8F;
    padding: 0.75rem 1rem;
    border-bottom: 1px solid #252F3A;
    text-align: left;
}

.mp-table td {
    padding: 0.7rem 1rem;
    border-bottom: 1px solid rgba(37, 47, 58, 0.3);
    color: #A0B0C3;
}

.mp-table tr:hover td {
    background: rgba(20, 24, 31, 0.8);
}

/* ===== SECTION TITLES ===== */
.mp-section {
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #3B4A5C;
    margin: 2rem 0 1.25rem 0;
    padding-left: 0.5rem;
    display: flex;
    align-items: center;
    gap: 0.75rem;
}

.mp-section::before {
    content: '';
    width: 20px;
    height: 2px;
    background: linear-gradient(90deg, #3B82F6, #8B5CF6);
    border-radius: 2px;
}

/* ===== CONFIDENCE BAR ===== */
.conf-track {
    height: 4px;
    background: #252F3A;
    border-radius: 4px;
    margin-top: 0.75rem;
    overflow: hidden;
}

.conf-fill {
    height: 4px;
    border-radius: 4px;
    transition: width 0.4s ease;
}

/* ===== COLORES ===== */
.green { color: #10B981; }
.red { color: #EF4444; }
.blue { color: #3B82F6; }
.purple { color: #8B5CF6; }
.yellow { color: #F59E0B; }
.muted { color: #6B7A8F; }

/* ===== CONTENT WRAPPER ===== */
.mp-content {
    padding: 0 2.5rem 2.5rem 2.5rem;
}

/* ===== DIVIDER ===== */
.mp-divider {
    border: none;
    border-top: 1px solid #252F3A;
    margin: 0;
}

/* ===== FOOTER ===== */
.mp-footer {
    border-top: 1px solid #252F3A;
    padding: 1rem 2.5rem;
    margin-top: 2.5rem;
    display: flex;
    justify-content: space-between;
    font-size: 0.65rem;
    color: #3B4A5C;
    letter-spacing: 0.05em;
}
            
/* ===== TOOLTIPS KPI CARDS ===== */
.mp-card {
    position: relative;
    overflow: visible !important;
}

.mp-tooltip {
    display: none;
    position: absolute;
    bottom: calc(100% + 10px);
    left: 50%;
    transform: translateX(-50%);
    background: #1E293B;
    border: 1px solid #3B82F6;
    border-radius: 8px;
    padding: 0.65rem 0.9rem;
    font-size: 0.72rem;
    color: #94A3B8;
    width: 210px;
    line-height: 1.6;
    z-index: 9999;
    box-shadow: 0 8px 24px rgba(0,0,0,0.5);
    pointer-events: none;
}

.mp-tooltip::after {
    content: '';
    position: absolute;
    top: 100%;
    left: 50%;
    transform: translateX(-50%);
    border: 6px solid transparent;
    border-top-color: #3B82F6;
}

.mp-card:hover .mp-tooltip {
    display: block;
}
</style>
""", unsafe_allow_html=True)

# ============================================================================
# FUNCIONES HELPER
# ============================================================================

@st.cache_data(ttl=3600)
def load_data(ticker):
    """Carga los datos con caché de 1 hora"""
    try:
        feat = pd.read_csv(f"{DATA_PROCESSED_PATH}{ticker}_features.csv",
                          index_col=0, parse_dates=True)
        raw = pd.read_csv(f"data/raw/{ticker}.csv",
                         header=[0, 1], index_col=0, parse_dates=True)
        raw.columns = raw.columns.get_level_values(0)
        return feat, raw
    except Exception as e:
        st.error(f"Error loading data for {ticker}: {str(e)}")
        return None, None

@st.cache_resource
def load_model(ticker):
    """Carga el modelo con caché"""
    try:
        return joblib.load(f"{MODEL_PATH}{ticker}_model.pkl")
    except Exception as e:
        st.error(f"Error loading model for {ticker}: {str(e)}")
        return None

def confidence_score(model, X):
    """Calcula el score de confianza basado en la dispersión de los árboles"""
    try:
        preds = np.array([tree.predict(X)[0] for tree in model.estimators_])
        cv = preds.std() / (np.abs(preds.mean()) + 1e-9)
        return float(np.clip(1 - cv * 8, 0.30, 0.98))  # Ajustado para mejor sensibilidad
    except:
        return 0.75  # Valor por defecto

def calculate_mape(y_true, y_pred):
    """Mean Absolute Percentage Error"""
    return np.mean(np.abs((y_true - y_pred) / (y_true + 1e-9))) * 100

def format_volume(vol):
    """Formatea el volumen de manera profesional"""
    if vol >= 1e9:
        return f"{vol/1e9:.2f}B"
    elif vol >= 1e6:
        return f"{vol/1e6:.2f}M"
    elif vol >= 1e3:
        return f"{vol/1e3:.0f}K"
    else:
        return str(vol)

def get_signal_icon(signal):
    """Retorna icono para la señal"""
    return "▲" if signal == "Bullish" else "▼"

# ============================================================================
# CONFIGURACIÓN INICIAL
# ============================================================================

FEATURES = ["close", "return_1d", "ma_7", "ma_21", "volatility_7", "dist_ma7", "dist_ma21"]
PERIODS = {
    "1W": 5,
    "1M": 21,
    "3M": 63,
    "6M": 126,
    "1Y": 252,
    "MAX": 9999
}

# Inicializar session state
if "period" not in st.session_state:
    st.session_state["period"] = "6M"
if "show_ma20" not in st.session_state:
    st.session_state["show_ma20"] = True
if "show_ma50" not in st.session_state:
    st.session_state["show_ma50"] = True
if "show_vol" not in st.session_state:
    st.session_state["show_vol"] = False
if "show_rsi" not in st.session_state:
    st.session_state["show_rsi"] = False

# Colores del tema
BG = "#0B0E14"
CARD_BG = "#14181F"
GRID = "#252F3A"
TEXT = "#E5E9F0"
MUTED = "#6B7A8F"

# ============================================================================
# HEADER
# ============================================================================

col1, col2, col3, col4, col5, col6, col7 = st.columns([2, 1.5, 0.5, 0.5, 0.5, 0.5, 5])

with col1:
    st.markdown("""
    <div class="mp-logo">
        Market<span>Pulse</span>
        <span class="mp-badge">FINANCIAL ANALYTICS</span>
    </div>
    """, unsafe_allow_html=True)

with col2:
    ticker = st.selectbox("", TICKERS, label_visibility="collapsed", key="ticker_selector")

# Botones de período
with col3:
    if st.button("1W", key="btn_1w"):
        st.session_state["period"] = "1W"
with col4:
    if st.button("1M", key="btn_1m"):
        st.session_state["period"] = "1M"
with col5:
    if st.button("3M", key="btn_3m"):
        st.session_state["period"] = "3M"
with col6:
    if st.button("6M", key="btn_6m"):
        st.session_state["period"] = "6M"
with col7:
    if st.button("1Y", key="btn_1y"):
        st.session_state["period"] = "1Y"

st.markdown('<hr class="mp-divider"/>', unsafe_allow_html=True)

# ============================================================================
# CARGA DE DATOS
# ============================================================================

n_days = PERIODS[st.session_state["period"]]
df, raw = load_data(ticker)
model = load_model(ticker)

if df is None or raw is None or model is None:
    st.error("Error loading data. Please check your data files.")
    st.stop()

df_v = df.iloc[-n_days:].copy()
raw_v = raw.iloc[-n_days:].copy()

# ============================================================================
# CÁLCULO DE MÉTRICAS
# ============================================================================

# Precios y cambios
last_price = df["close"].iloc[-1]
prev_price = df["close"].iloc[-2]
price_change_pct = (last_price - prev_price) / prev_price * 100
price_change_abs = last_price - prev_price

# Volumen
volume_today = int(raw["Volume"].iloc[-1])

# Predicción
X_last = df[FEATURES].iloc[-1:]
pred_price = model.predict(X_last)[0]
pred_change_pct = (pred_price - last_price) / last_price * 100

# Confianza
confidence = confidence_score(model, X_last)
confidence_pct = int(confidence * 100)

# Señal MA
ma7 = df["ma_7"].iloc[-1]
ma21 = df["ma_21"].iloc[-1]
signal = "Bullish" if ma7 > ma21 else "Bearish"

# Colores dinámicos
price_color = "green" if price_change_pct >= 0 else "red"
pred_color = "green" if pred_change_pct >= 0 else "red"
signal_color = "green" if signal == "Bullish" else "red"
confidence_color = "#10B981" if confidence_pct >= 70 else "#F59E0B" if confidence_pct >= 50 else "#EF4444"

# ============================================================================
# MÉTRICAS DEL MODELO
# ============================================================================

from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score

X_all = df[FEATURES]
y_all = df["target"]
X_train, X_test, y_train, y_test = train_test_split(X_all, y_all, test_size=0.2, shuffle=False)

y_pred_test = model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred_test)
mape = calculate_mape(y_test.values, y_pred_test)
r2 = r2_score(y_test, y_pred_test)

# ============================================================================
# CONTENIDO PRINCIPAL
# ============================================================================

st.markdown('<div class="mp-content">', unsafe_allow_html=True)

# ----------------------------------------------------------------------------
# KPI CARDS - FILA SUPERIOR
# ----------------------------------------------------------------------------

st.markdown('<div class="mp-section">MARKET SNAPSHOT</div>', unsafe_allow_html=True)

kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)

with kpi1:
    st.markdown(f"""
    <div class="mp-card">
        <div class="mp-tooltip">
            Último precio de cierre registrado para {ticker} en Yahoo Finance.
            Se actualiza al correr la ingesta de datos.
        </div>
        <div class="mp-card-label"><span>💰</span> LAST PRICE</div>
        <div class="mp-card-value">${last_price:,.2f}</div>
        <div class="mp-card-sub muted">
            <span>{ticker}</span> · <span>NASDAQ</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with kpi2:
    st.markdown(f"""
    <div class="mp-card">
        <div class="mp-tooltip">
            Variación del precio respecto al cierre anterior.
            Verde = subió · Rojo = bajó.
            Alto volumen confirma la dirección.
        </div>
        <div class="mp-card-label"><span>📊</span> DAILY CHANGE</div>
        <div class="mp-card-value {price_color}">{price_change_pct:+.2f}%</div>
        <div class="mp-card-sub {price_color}">
            {price_change_abs:+.2f} USD
        </div>
    </div>
    """, unsafe_allow_html=True)

with kpi3:
    st.markdown(f"""
    <div class="mp-card">
        <div class="mp-tooltip">
            Cantidad de acciones operadas en el día.
            Volumen alto con precio subiendo = señal fuerte.
            Volumen bajo = movimiento poco confiable.
        </div>
        <div class="mp-card-label"><span>📦</span> VOLUME</div>
        <div class="mp-card-value">{format_volume(volume_today)}</div>
        <div class="mp-card-sub muted">24h trading volume</div>
    </div>
    """, unsafe_allow_html=True)

with kpi4:
    st.markdown(f"""
    <div class="mp-card">
        <div class="mp-tooltip">
            Precio estimado para el próximo día hábil.
            Generado por Random Forest con 7 variables:
            precio, retornos, medias móviles y volatilidad.
        </div>
        <div class="mp-card-label"><span>🔮</span> FORECAST (D+1)</div>
        <div class="mp-card-value">${pred_price:,.2f}</div>
        <div class="mp-card-sub {pred_color}">
            {pred_change_pct:+.2f}% expected
        </div>
    </div>
    """, unsafe_allow_html=True)

with kpi5:
    st.markdown(f"""
    <div class="mp-card">
        <div class="mp-tooltip">
            Acuerdo entre los 100 árboles del modelo.
            +70% = alta confianza en la predicción.
            -50% = usar con precaución.
        </div>
        <div class="mp-card-label"><span>⚡</span> MODEL CONFIDENCE</div>
        <div class="mp-card-value" style="color:{confidence_color}">
            {confidence_pct}%
        </div>
        <div class="conf-track">
            <div class="conf-fill"
                 style="width:{confidence_pct}%;background:{confidence_color}">
            </div>
        </div>
        <div class="mp-card-sub" style="margin-top:0.75rem;">
            <span style="color:{signal_color};">
                {get_signal_icon(signal)} {signal} SIGNAL
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ----------------------------------------------------------------------------
# CONTROLES DE INDICADORES
# ----------------------------------------------------------------------------

st.markdown('<div class="mp-section">CHART INDICATORS</div>', unsafe_allow_html=True)

ind1, ind2, ind3, ind4, ind5 = st.columns([1, 1, 1, 1, 6])

with ind1:
    show_ma20 = st.checkbox("MA 20", value=st.session_state["show_ma20"], key="ma20")
    st.session_state["show_ma20"] = show_ma20

with ind2:
    show_ma50 = st.checkbox("MA 50", value=st.session_state["show_ma50"], key="ma50")
    st.session_state["show_ma50"] = show_ma50

with ind3:
    show_vol = st.checkbox("Volatility Band", value=st.session_state["show_vol"], key="vol")
    st.session_state["show_vol"] = show_vol

with ind4:
    show_rsi = st.checkbox("RSI (14)", value=st.session_state["show_rsi"], key="rsi")
    st.session_state["show_rsi"] = show_rsi

# ----------------------------------------------------------------------------
# CÁLCULO DE INDICADORES ADICIONALES
# ----------------------------------------------------------------------------

# Moving Averages
df_v["ma_20"] = df["close"].rolling(20).mean().iloc[-n_days:]
df_v["ma_50"] = df["close"].rolling(50).mean().iloc[-n_days:]

# RSI
delta = df["close"].diff()
gain = delta.clip(lower=0).rolling(14).mean()
loss = (-delta.clip(upper=0)).rolling(14).mean()
rs = gain / (loss + 1e-9)
df_v["rsi"] = (100 - 100 / (1 + rs)).iloc[-n_days:]

# ----------------------------------------------------------------------------
# CANDLESTICK CHART PRINCIPAL
# ----------------------------------------------------------------------------

st.markdown('<div class="mp-section">PRICE ACTION & VOLUME</div>', unsafe_allow_html=True)

# Configuración de subplots
if show_vol and show_rsi:
    n_rows = 3
    row_heights = [0.6, 0.2, 0.2]
elif show_vol or show_rsi:
    n_rows = 3
    row_heights = [0.65, 0.17, 0.18]
else:
    n_rows = 2
    row_heights = [0.72, 0.28]

fig = make_subplots(
    rows=n_rows, 
    cols=1,
    shared_xaxes=True,
    vertical_spacing=0.03,
    row_heights=row_heights
)

# Candlestick principal
fig.add_trace(
    go.Candlestick(
        x=raw_v.index,
        open=raw_v["Open"],
        high=raw_v["High"],
        low=raw_v["Low"],
        close=raw_v["Close"],
        name=ticker,
        increasing_line_color="#10B981",
        decreasing_line_color="#EF4444",
        increasing_fillcolor="#10B981",
        decreasing_fillcolor="#EF4444",
        line=dict(width=0.8),
        whiskerwidth=0.8,
        hoverlabel=dict(bgcolor=CARD_BG, font_size=12),
    ),
    row=1, col=1
)

# Moving Averages
if show_ma20:
    fig.add_trace(
        go.Scatter(
            x=df_v.index,
            y=df_v["ma_20"],
            name="MA 20",
            line=dict(color="#3B82F6", width=1.8),
            opacity=0.9,
            hovertemplate="MA20: $%{y:.2f}<extra></extra>"
        ),
        row=1, col=1
    )

if show_ma50:
    fig.add_trace(
        go.Scatter(
            x=df_v.index,
            y=df_v["ma_50"],
            name="MA 50",
            line=dict(color="#F59E0B", width=1.8),
            opacity=0.9,
            hovertemplate="MA50: $%{y:.2f}<extra></extra>"
        ),
        row=1, col=1
    )

# Volatility Band
if show_vol:
    vol_upper = df_v["close"] * (1 + df_v["volatility_7"])
    vol_lower = df_v["close"] * (1 - df_v["volatility_7"])
    
    fig.add_trace(
        go.Scatter(
            x=df_v.index.tolist() + df_v.index.tolist()[::-1],
            y=vol_upper.tolist() + vol_lower.tolist()[::-1],
            fill="toself",
            fillcolor="rgba(59, 130, 246, 0.05)",
            line=dict(color="rgba(0,0,0,0)"),
            name="Volatility Band",
            hoverinfo="skip",
            showlegend=True
        ),
        row=1, col=1
    )

# Volumen
vol_colors = ["#10B981" if raw_v["Close"].iloc[i] >= raw_v["Open"].iloc[i] else "#EF4444" 
              for i in range(len(raw_v))]

fig.add_trace(
    go.Bar(
        x=raw_v.index,
        y=raw_v["Volume"],
        name="Volume",
        marker_color=vol_colors,
        opacity=0.5,
        hovertemplate="Volume: %{y:,.0f}<extra></extra>"
    ),
    row=2, col=1
)

# RSI
if show_rsi:
    rsi_row = 3
    fig.add_trace(
        go.Scatter(
            x=df_v.index,
            y=df_v["rsi"],
            name="RSI 14",
            line=dict(color="#8B5CF6", width=1.8),
            hovertemplate="RSI: %{y:.1f}<extra></extra>"
        ),
        row=rsi_row, col=1
    )
    
    # Líneas de sobrecompra/sobreventa
    fig.add_hline(
        y=70,
        line=dict(color="#EF4444", width=1, dash="dot"),
        row=rsi_row, col=1
    )
    fig.add_hline(
        y=30,
        line=dict(color="#10B981", width=1, dash="dot"),
        row=rsi_row, col=1
    )

# Layout del chart
fig.update_layout(
    template="plotly_dark",
    paper_bgcolor=BG,
    plot_bgcolor=BG,
    height=600,
    margin=dict(l=0, r=20, t=20, b=0),
    xaxis_rangeslider_visible=False,
    legend=dict(
        orientation="h",
        y=1.02,
        x=0,
        font=dict(size=11, color=MUTED),
        bgcolor="rgba(0,0,0,0)",
        bordercolor=GRID,
        borderwidth=1
    ),
    hoverlabel=dict(
        bgcolor=CARD_BG,
        font_size=12,
        font_color=TEXT,
        bordercolor=GRID
    ),
    hovermode="x unified",
)

# Configuración de ejes
for i in range(1, n_rows + 1):
    yaxis_key = f"yaxis{i}" if i > 1 else "yaxis"
    xaxis_key = f"xaxis{i}" if i > 1 else "xaxis"
    
    fig.update_layout(**{
        yaxis_key: dict(
            gridcolor=GRID,
            tickfont=dict(size=11, color=MUTED),
            side="right",
            showgrid=True,
            zeroline=False
        ),
        xaxis_key: dict(
            gridcolor=GRID,
            tickfont=dict(size=11, color=MUTED),
            showgrid=False
        )
    })

# Títulos de ejes específicos
fig.update_yaxes(title_text="Volume", row=2, col=1, tickfont=dict(size=10))

if show_rsi:
    fig.update_yaxes(title_text="RSI", row=3, col=1, tickfont=dict(size=10))

st.plotly_chart(fig, use_container_width=True, config={
    'displayModeBar': True,
    'modeBarButtonsToAdd': ['drawline', 'drawrect'],
    'displaylogo': False
})

# ----------------------------------------------------------------------------
# FORECAST Y MODEL INFO
# ----------------------------------------------------------------------------

st.markdown('<div class="mp-section">MODEL FORECAST & METRICS</div>', unsafe_allow_html=True)

forecast_col, model_col = st.columns([2.2, 1])

# ── Forecast ─────────────────────────────────────────────────────────────────
st.markdown('<div class="mp-section">MODEL FORECAST & METRICS</div>',
            unsafe_allow_html=True)

prices_forecast = []
current_row = df[FEATURES].iloc[-1:].copy()

for _ in range(FORECAST_DAYS):
    p = model.predict(current_row)[0]
    prices_forecast.append(p)
    current_row["close"]     = p
    current_row["return_1d"] = 0
    current_row["ma_7"]      = p
    current_row["ma_21"]     = p
    current_row["dist_ma7"]  = 0
    current_row["dist_ma21"] = 0

forecast_dates = pd.date_range(
    start=df.index[-1], periods=FORECAST_DAYS + 1, freq="B"
)[1:]

uncertainty = (1 - confidence) * 0.04
upper_band = [p * (1 + uncertainty * (i+1)) for i, p in enumerate(prices_forecast)]
lower_band = [p * (1 - uncertainty * (i+1)) for i, p in enumerate(prices_forecast)]

forecast_col, model_col = st.columns([2.2, 1])

with forecast_col:
    hist_data = df["close"].iloc[-45:]
    fig2 = go.Figure()

    fig2.add_trace(go.Scatter(
        x=hist_data.index, y=hist_data,
        name="Historical",
        line=dict(color="#4B5563", width=2),
        hovertemplate="$%{y:.2f}<extra>Historical</extra>"
    ))

    fig2.add_trace(go.Scatter(
        x=list(forecast_dates) + list(forecast_dates[::-1]),
        y=upper_band + lower_band[::-1],
        fill="toself",
        fillcolor="rgba(59,130,246,0.08)",
        line=dict(color="rgba(0,0,0,0)"),
        name="Confidence Band",
        hoverinfo="skip"
    ))

    fig2.add_trace(go.Scatter(
        x=[df.index[-1]] + list(forecast_dates),
        y=[last_price] + prices_forecast,
        name="Forecast",
        line=dict(color="#3B82F6", width=2.5, dash="dot"),
        mode="lines+markers",
        marker=dict(size=6, color="#3B82F6", symbol="diamond"),
        hovertemplate="$%{y:.2f}<extra>Forecast</extra>"
    ))

    fig2.update_layout(
        template="plotly_dark",
        paper_bgcolor=BG, plot_bgcolor=BG,
        height=320,
        margin=dict(l=0, r=20, t=20, b=0),
        legend=dict(orientation="h", y=1.1, x=0,
                    font=dict(size=11, color=MUTED),
                    bgcolor="rgba(0,0,0,0)"),
        hoverlabel=dict(bgcolor=CARD_BG, font_size=12,
                        font_color=TEXT, bordercolor=GRID),
        hovermode="x unified",
        yaxis=dict(gridcolor=GRID, tickfont=dict(size=11, color=MUTED),
                   side="right", title="Price (USD)"),
        xaxis=dict(gridcolor=GRID, tickfont=dict(size=11, color=MUTED),
                   showgrid=False),
    )
    st.plotly_chart(fig2, use_container_width=True,
                    config={"displayModeBar": True, "displaylogo": False})

    # Tabla de forecast detallada
    st.markdown('<div class="mp-section">FORECAST DETAIL</div>',
                unsafe_allow_html=True)
    prev_p = last_price
    rows_fc = ""
    for i, (fecha, precio) in enumerate(zip(forecast_dates, prices_forecast)):
        chg     = (precio - prev_p) / prev_p * 100
        cls     = "green" if chg >= 0 else "red"
        sign    = "+" if chg >= 0 else ""
        arrow   = "▲" if chg >= 0 else "▼"
        rows_fc += f"""<tr>
            <td>Day {i+1} · {fecha.strftime('%b %d')}</td>
            <td>${precio:,.2f}</td>
            <td class="{cls}">{arrow} {sign}{chg:.2f}%</td>
            <td>${upper_band[i]:,.2f} / ${lower_band[i]:,.2f}</td>
        </tr>"""
        prev_p = precio

    st.markdown(f"""
    <table class="mp-table">
        <thead><tr>
            <th>Date</th>
            <th>Predicted Price</th>
            <th>Change</th>
            <th>Range (High / Low)</th>
        </tr></thead>
        <tbody>{rows_fc}</tbody>
    </table>
    """, unsafe_allow_html=True)

with model_col:
    st.markdown(f"""
    <div class="mp-model-card">
        <div class="mp-model-title">
            MODEL SPECIFICATIONS
        </div>
        <div class="mp-model-row">
            <span class="mp-model-key">Algorithm</span>
            <span class="mp-model-val">Random Forest</span>
        </div>
        <div class="mp-model-row">
            <span class="mp-model-key">Estimators</span>
            <span class="mp-model-val">100 trees</span>
        </div>
        <div class="mp-model-row">
            <span class="mp-model-key">Target</span>
            <span class="mp-model-val">Next-day close</span>
        </div>
        <div class="mp-model-row">
            <span class="mp-model-key">Features</span>
            <span class="mp-model-val">7 predictors</span>
        </div>
        <div class="mp-model-row">
            <span class="mp-model-key">Training days</span>
            <span class="mp-model-val">{len(df)} days</span>
        </div>
        <div class="mp-model-row">
            <span class="mp-model-key">Train / Test</span>
            <span class="mp-model-val">80% / 20%</span>
        </div>
        <div class="mp-model-row">
            <span class="mp-model-key">MAE</span>
            <span class="mp-model-val" style="color:#10B981">${mae:.2f}</span>
        </div>
        <div class="mp-model-row">
            <span class="mp-model-key">MAPE</span>
            <span class="mp-model-val" style="color:#10B981">{mape:.2f}%</span>
        </div>
        <div class="mp-model-row">
            <span class="mp-model-key">R² Score</span>
            <span class="mp-model-val" style="color:#10B981">{r2:.3f}</span>
        </div>
        <div class="mp-model-row">
            <span class="mp-model-key">Confidence</span>
            <span class="mp-model-val" style="color:{confidence_color}">
                {confidence_pct}%
            </span>
        </div>
        <div class="mp-model-row" style="border-bottom:none">
            <span class="mp-model-key">MA Signal</span>
            <span class="mp-model-val" style="color:{signal_color}">
                {signal}
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ----------------------------------------------------------------------------
# FOOTER
# ----------------------------------------------------------------------------

st.markdown("""
<div class="mp-logo">
    MARKET<span>PULSE</span>
    <span class="mp-badge">FINANCIAL ANALYTICS</span>
</div>
""", unsafe_allow_html=True)