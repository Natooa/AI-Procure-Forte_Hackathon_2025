# data_loader.py
import pandas as pd
import joblib
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from fastapi import HTTPException
from transformers import pipeline

from .config import SUPPLIERS_PATH, RNU_PATH, RISK_TRAIN_PATH, RISK_MODEL_PATH, RISK_SCALER_PATH
from . import globals as g  # Импортируем модуль globals

def load_suppliers():
    if SUPPLIERS_PATH.exists():
        g.SUPPLIERS_DF = pd.read_csv(SUPPLIERS_PATH)
        print(f"[INFO] Loaded {len(g.SUPPLIERS_DF)} suppliers")
    else:
        raise HTTPException(status_code=500, detail="suppliers.csv not found")

def load_rnu():
    if RNU_PATH.exists():
        df = pd.read_csv(RNU_PATH)
        g.RNU_LIST = df.to_dict(orient="records")
        print(f"[INFO] Loaded {len(g.RNU_LIST)} RNU entries")
    else:
        g.RNU_LIST.clear()

def train_risk_model():
    if RISK_TRAIN_PATH.exists():
        df = pd.read_csv(RISK_TRAIN_PATH)
        X = df[['price', 'deadline_days', 'requirements_count', 'is_rnu', 'past_violations', 'company_age']]
        y = df['risk_label']

        g.SCALER = StandardScaler()
        X_scaled = g.SCALER.fit_transform(X)

        g.RISK_MODEL = LogisticRegression()
        g.RISK_MODEL.fit(X_scaled, y)

        joblib.dump(g.RISK_MODEL, RISK_MODEL_PATH)
        joblib.dump(g.SCALER, RISK_SCALER_PATH)
        print("[INFO] Risk model trained")
    else:
        print("[WARN] risk_train.csv not found, skipping ML model training")

def init_ner_pipeline():
    """Инициализация NER pipeline"""
    g.NER_PIPELINE = pipeline(
        "token-classification",
        model="Babelscape/wikineural-multilingual-ner",
        aggregation_strategy="simple"
    )
    print("[INFO] NER pipeline initialized")
