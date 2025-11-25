# main.py
from fastapi import FastAPI
from contextlib import asynccontextmanager
import asyncio
import joblib

from .data_loader import load_suppliers, load_rnu, train_risk_model, init_ner_pipeline
from .embeddings import update_embeddings, auto_update, init_embed_model
from .extractors import extract_requirements, extract_deadlines, extract_entities, extract_prices
from .extractors import DEADLINE_KEYWORDS, DATE_RELATED_KEYWORDS
from .match import match as match_func
from .risk import calculate_risk
from .models import ExtractInput, MatchInput, RiskInput
from .config import RISK_MODEL_PATH, RISK_SCALER_PATH
from . import globals as g


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Инициализация моделей
    init_embed_model()
    init_ner_pipeline()

    # Загрузка данных
    load_suppliers()
    load_rnu()
    update_embeddings()

    # Загрузка или обучение risk модели
    if RISK_MODEL_PATH.exists() and RISK_SCALER_PATH.exists():
        g.RISK_MODEL = joblib.load(RISK_MODEL_PATH)
        g.SCALER = joblib.load(RISK_SCALER_PATH)
        print("[INFO] Risk model loaded from disk")
    else:
        train_risk_model()

    # Запуск фоновой задачи
    asyncio.create_task(auto_update())
    yield


app = FastAPI(title="AI-Procure ML Service", lifespan=lifespan)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/extract")
def extract(input: ExtractInput):
    text = input.text or ""
    if not text.strip():
        return {
            "tender_id": input.tender_id,
            "extracted": {
                "title": {"value": "", "confidence": 0.0},
                "prices": [],
                "deadlines": [],
                "requirements": [],
                "entities": [],
                "all_dates": [],
                "confidence_fields": {}
            }
        }

    lines = [l.strip() for l in text.splitlines() if l.strip()]
    title = lines[0].rstrip(".").strip() if lines else text.strip().rstrip(".")

    requirements = extract_requirements(text)
    deadlines = extract_deadlines(text, keywords=DEADLINE_KEYWORDS)
    all_dates = extract_deadlines(text, keywords=DATE_RELATED_KEYWORDS)
    prices = extract_prices(text)
    entities = extract_entities(text)

    confidence = {
        "title": 0.95,
        "prices": 0.9 if prices else 0.0,
        "deadlines": 0.9 if deadlines else 0.0,
        "requirements": 0.9 if requirements else 0.0,
        "entities": 0.9 if entities else 0.0
    }

    return {
        "tender_id": input.tender_id,
        "extracted": {
            "title": {"value": title, "confidence": confidence["title"]},
            "prices": prices,
            "deadlines": deadlines,
            "requirements": requirements,
            "entities": entities,
            "all_dates": all_dates,
            "confidence_fields": confidence
        }
    }


@app.post("/match")
def match(input: MatchInput):
    return match_func(input)


@app.post("/risk")
def risk(input: RiskInput):
    return calculate_risk(input)


