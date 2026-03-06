# MarketPulse · Fintech Analytics Platform

> End-to-end Machine Learning pipeline for stock price prediction with a professional financial dashboard — deployed on AWS with daily automated retraining.

![Python](https://img.shields.io/badge/Python-3.11-blue?style=flat-square&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32+-red?style=flat-square&logo=streamlit)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.4+-orange?style=flat-square&logo=scikit-learn)
![Plotly](https://img.shields.io/badge/Plotly-5.19+-purple?style=flat-square&logo=plotly)
![Docker](https://img.shields.io/badge/Docker-ready-blue?style=flat-square&logo=docker)
![AWS](https://img.shields.io/badge/AWS-Lambda%20%7C%20S3%20%7C%20ECR-orange?style=flat-square&logo=amazon-aws)

---

## What is this?

MarketPulse is a **full Data Science project** that downloads real stock market data, engineers features, trains a Machine Learning model, and presents everything in a professional fintech-style dashboard.

Built as a portfolio project to demonstrate end-to-end ML pipeline development — from raw data ingestion to cloud deployment with automated daily retraining.

---

## Live Demo

> Dashboard running locally on `https://marketpuls3.streamlit.app`  
> Tickers analyzed: **AAPL** (Apple) · **MSFT** (Microsoft)

## Dashboard Preview

![MarketPulse Dashboard](assets/dashboard.png)

---

## Features

- **Real-time data ingestion** via Yahoo Finance API
- **Feature engineering** — moving averages, volatility, momentum indicators
- **Random Forest Regressor** trained on 2 years of historical data
- **Next-day price prediction** with confidence scoring
- **Interactive candlestick chart** with MA20, MA50, RSI, Volatility Band toggles
- **15-day forecast** with uncertainty band
- **Monthly performance analysis** with best/worst day breakdown
- **Multi-ticker comparison** normalized to base 100
- **Model metrics panel** — MAE, MAPE, R² Score
- **KPI tooltips** — contextual explanations on hover
- **Automated daily retraining** via AWS Lambda + EventBridge

---

## Cloud Architecture

The pipeline runs automatically every day at 8:00 AM (Argentina time) using AWS serverless infrastructure — no manual intervention required.

```
EventBridge (cron scheduler)
        │
        │  every day at 8am ART
        ▼
Lambda Function (Docker container)
        │
        ├── 1. Downloads fresh data from Yahoo Finance
        ├── 2. Engineers features (MA, volatility, returns)
        ├── 3. Retrains Random Forest model
        │
        ▼
S3 Bucket (marketpulse-data-jbaigorria)
        ├── data/raw/          ← OHLCV price data
        ├── data/processed/    ← engineered features
        └── models/            ← trained .pkl models
```

### AWS Services

| Service | Purpose |
|---|---|
| S3 | Store data, features and trained models |
| ECR | Docker image registry |
| Lambda | Serverless pipeline execution |
| EventBridge | Daily cron scheduler (8am ART) |
| IAM | Security and permissions |
| CloudWatch | Execution logs and monitoring |

---

## Project Architecture

```
marketpulse/
├── Dockerfile                # Container definition for AWS Lambda
├── config.py                 # Central configuration (tickers, dates, paths)
├── src/
│   ├── ingestion.py          # Module 1: Data download from Yahoo Finance
│   ├── features.py           # Module 2: Feature engineering
│   ├── model.py              # Module 3: Random Forest training
│   └── lambda_handler.py     # Module 4: AWS Lambda entrypoint
├── dashboard/
│   └── app.py                # Module 5: Streamlit dashboard
├── data/
│   ├── raw/                  # Raw OHLCV data (CSV)
│   └── processed/            # Engineered features (CSV)
└── models/                   # Trained models (.pkl)
```

---

## ML Pipeline

### 1. Data Ingestion (`src/ingestion.py`)
Downloads 2 years of daily OHLCV data for each ticker using `yfinance`.

### 2. Feature Engineering (`src/features.py`)

| Feature | Description |
|---|---|
| `close` | Closing price |
| `return_1d` | Daily percentage return |
| `ma_7` | 7-day moving average |
| `ma_21` | 21-day moving average |
| `volatility_7` | 7-day rolling standard deviation |
| `dist_ma7` | Distance from price to MA7 |
| `dist_ma21` | Distance from price to MA21 |
| `target` | Next day's closing price (label) |

### 3. Model Training (`src/model.py`)

- **Algorithm:** Random Forest Regressor
- **Estimators:** 100 trees
- **Split:** 80% train / 20% test (chronological — no data leakage)
- **Metrics:** MAE · MAPE · R² Score
- **Confidence:** Based on inter-tree prediction variance

### 4. Dashboard (`dashboard/app.py`)
Built with Streamlit + Plotly. Bloomberg-style dark theme, fully interactive.

---

## Model Performance

| Ticker | MAE | MAPE | R² |
|--------|-----|------|----|
| AAPL | ~$15 | ~6% | varies |
| MSFT | ~$9 | ~2% | ~0.91 |

> Note: Financial price prediction is inherently uncertain. These metrics reflect pattern recognition on historical data, not guaranteed future performance.

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Data | yfinance, pandas |
| ML | scikit-learn (RandomForestRegressor) |
| Visualization | Plotly, Streamlit |
| Serialization | joblib |
| Containerization | Docker |
| Cloud | AWS S3, Lambda, ECR, EventBridge |
| Language | Python 3.11 |

---

## Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/Jbaigorria22/marketpulse.git
cd marketpulse
```

### 2. Create virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables
Create a `.env` file in the root directory:
```
MP_ACCESS_KEY_ID=your_aws_access_key
MP_SECRET_ACCESS_KEY=your_aws_secret_key
MP_REGION=sa-east-1
MP_S3_BUCKET=your_s3_bucket_name
```

### 5. Run the pipeline locally
```bash
# Step 1: Download data
python src/ingestion.py

# Step 2: Engineer features
python src/features.py

# Step 3: Train model
python src/model.py

# Step 4: Launch dashboard
streamlit run dashboard/app.py
```

### 6. Run with Docker
```bash
docker build -t marketpulse-pipeline .
docker run --env-file .env marketpulse-pipeline
```

---

## Configuration

Edit `config.py` to change tickers, date range, or forecast horizon:

```python
TICKERS       = ["AAPL", "MSFT"]   # Add any Yahoo Finance ticker
DATE_START    = "2023-01-01"
DATE_END      = "2025-01-01"
FORECAST_DAYS = 15
```

---

## What I Learned

- Building a **complete ML pipeline** from raw data to cloud deployment
- **Feature engineering** for time series — avoiding data leakage with chronological splits
- **Random Forest** internals — using tree variance as a confidence proxy
- **Docker** containerization for reproducible environments
- **AWS Lambda + ECR** serverless deployment with container images
- **EventBridge** cron scheduling for automated pipeline execution
- **Product thinking** — designing for the user, not just the data

---

## Roadmap

- [x] AWS deployment (S3 + Lambda + EventBridge for daily auto-update)
- [ ] Streamlit Cloud hosting
- [ ] Additional tickers support
- [ ] Email alerts when confidence score drops

---

## Author

Built by **Joaquin Baigorria** as part of a Data Science portfolio.  
Open to Data Analyst / Data Scientist roles.

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?style=flat-square&logo=linkedin)](https://linkedin.com/in/joaquinbaigorria/)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-black?style=flat-square&logo=github)](https://github.com/Jbaigorria22)

---

> *Not financial advice. Built for educational and portfolio purposes.*