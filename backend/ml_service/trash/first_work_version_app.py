from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from pathlib import Path
import pandas as pd
import re
from datetime import datetime
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer, util
from transformers import pipeline
import joblib
import numpy as np
import asyncio
from contextlib import asynccontextmanager
import re
from typing import List, Dict, Any, Optional
from datetime import datetime

# --- Настройки ---
APP_ROOT = Path(__file__).parent
DATA_DIR = APP_ROOT / "data"
DATA_DIR.mkdir(exist_ok=True)

SUPPLIERS_PATH = DATA_DIR / "synthetic_data" / "suppliers.csv"
RISK_MODEL_PATH = APP_ROOT / "risk_model.pkl"
RISK_SCALER_PATH = APP_ROOT / "risk_scaler.pkl"
RNU_PATH = DATA_DIR / "synthetic_data" / "rnu.csv"
RISK_TRAIN_PATH = APP_ROOT / "risk_train.csv"
AUTOUPDATE_INTERVAL = 600  # секунд

# --- Глобальные переменные ---
SUPPLIERS_DF: pd.DataFrame = pd.DataFrame()
SUPPLIER_EMBS: Any = None
TFIDF_VECT: Any = None
TFIDF_MATRIX: Any = None
RNU_LIST: List[Dict[str, Any]] = []
NER_PIPELINE: Any = None
EMBED_MODEL: Any = None
RISK_MODEL: LogisticRegression = None
SCALER: StandardScaler = None


# --- Pydantic модели ---
class ExtractInput(BaseModel):
    tender_id: str
    text: Optional[str] = ""


class MatchInput(BaseModel):
    tender_id: str
    title: Optional[str] = None
    subject: Optional[str] = None
    top_k: int = 5


class RiskInput(BaseModel):
    tender_id: str
    features: Dict[str, Any]


class RiskOutput(BaseModel):
    tender_id: str
    risk_score: float
    risk_label: int
    risk_reasons: List[str]


# --- Загрузка данных ---
def load_suppliers():
    global SUPPLIERS_DF
    if SUPPLIERS_PATH.exists():
        SUPPLIERS_DF = pd.read_csv(SUPPLIERS_PATH)
        print(f"[INFO] Loaded {len(SUPPLIERS_DF)} suppliers")
    else:
        raise HTTPException(status_code=500, detail="suppliers.csv not found")


def load_rnu():
    global RNU_LIST
    if RNU_PATH.exists():
        df = pd.read_csv(RNU_PATH)
        RNU_LIST = df.to_dict(orient="records")
        print(f"[INFO] Loaded {len(RNU_LIST)} RNU entries")
    else:
        RNU_LIST.clear()


def train_risk_model():
    global RISK_MODEL, SCALER
    if RISK_TRAIN_PATH.exists():
        df = pd.read_csv(RISK_TRAIN_PATH)
        X = df[['price', 'deadline_days', 'requirements_count', 'is_rnu', 'past_violations', 'company_age']]
        y = df['risk_label']

        SCALER = StandardScaler()
        X_scaled = SCALER.fit_transform(X)

        RISK_MODEL = LogisticRegression()
        RISK_MODEL.fit(X_scaled, y)

        joblib.dump(RISK_MODEL, RISK_MODEL_PATH)
        joblib.dump(SCALER, RISK_SCALER_PATH)
        print("[INFO] Risk model trained")
    else:
        print("[WARN] risk_train.csv not found, skipping ML model training")


def update_embeddings():
    global SUPPLIER_EMBS, TFIDF_VECT, TFIDF_MATRIX
    if not SUPPLIERS_DF.empty and EMBED_MODEL:
        SUPPLIER_EMBS = EMBED_MODEL.encode(
            SUPPLIERS_DF['name_ru'].astype(str).tolist(),
            convert_to_tensor=True
        )

        TFIDF_VECT = TfidfVectorizer()
        TFIDF_MATRIX = TFIDF_VECT.fit_transform(
            SUPPLIERS_DF['name_ru'].astype(str).tolist()
        )

        print("[INFO] Embeddings updated")


# --- Фоновая автоматическая переобучалка ---
async def auto_update():
    while True:
        try:
            load_suppliers()
            load_rnu()
            update_embeddings()
            train_risk_model()
        except Exception as e:
            print("[ERROR] Auto-update failed:", e)

        await asyncio.sleep(AUTOUPDATE_INTERVAL)


# --- FastAPI lifecycle ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    global EMBED_MODEL, NER_PIPELINE, RISK_MODEL, SCALER

    # SBERT
    EMBED_MODEL = SentenceTransformer('all-MiniLM-L6-v2')

    # === НОВАЯ мощная NER модель ===
    NER_PIPELINE = pipeline(
        "token-classification",
        model="Babelscape/wikineural-multilingual-ner",
        aggregation_strategy="simple"
    )

    # Данные
    load_suppliers()
    load_rnu()
    update_embeddings()

    # ML risk model
    if RISK_MODEL_PATH.exists() and RISK_SCALER_PATH.exists():
        RISK_MODEL = joblib.load(RISK_MODEL_PATH)
        SCALER = joblib.load(RISK_SCALER_PATH)
    else:
        train_risk_model()

    asyncio.create_task(auto_update())
    yield


app = FastAPI(title="AI-Procure ML Service", lifespan=lifespan)


# --- Health check ---
@app.get("/health")
def health():
    return {"status": "ok"}


# NOTE: Вам нужно определить ExtractInput, app.post, и NER_PIPELINE.

# --- Константы ---

REQ_KEYWORDS = [
    "сертификация", "опыт", "требования", "гарантия", "техническая поддержка",
    "warranty", "experience", "requirements", "certification", "technical support",
    "сертификаттау", "тәжірибе", "талаптар", "кепілдік"
]

DEADLINE_KEYWORDS = [
    "сроки", "deadline", "мерзімдер", "дата окончания", "final date"
]

# Расширение для захвата 'дата публикации', 'дата регистрации' для all_dates
DATE_RELATED_KEYWORDS = DEADLINE_KEYWORDS + [
    "дата публикации", "дата регистрации", "publication date", "registration date"
]

# Регулярка для поиска даты
DATE_REGEX = r"\b\d{1,2}[-./]\d{1,2}[-./]\d{2,4}\b"


# --- Функции извлечения ---

def extract_requirements(text: str) -> List[str]:
    # ИСПРАВЛЕНИЕ: Разбиваем только по новой строке, чтобы точка не ломала предложения
    paragraphs = text.splitlines()
    requirements = []

    IGNORE_ONLY_DATE_KWS = DEADLINE_KEYWORDS + ["дата публикации", "дата регистрации"]

    for p in paragraphs:
        # Разбиваем абзац на предложения по точке для более точного извлечения
        sentences = re.split(r'(?<=[.!?])\s+', p)

        for s in sentences:
            s_strip = s.strip()
            if not s_strip:
                continue

            # 1. Проверяем, есть ли ключевое слово требования
            is_requirement = any(kw.lower() in s_strip.lower() for kw in REQ_KEYWORDS)

            # 2. Если это требование, убеждаемся, что это не просто короткая фраза с ключевым словом даты
            if is_requirement:
                # Проверяем, содержит ли фраза ключевое слово даты И дату, и она очень короткая (например, < 30 символов)
                is_date_only = any(kw.lower() in s_strip.lower() for kw in IGNORE_ONLY_DATE_KWS) and len(
                    re.findall(DATE_REGEX, s_strip)) > 0 and len(s_strip) < 30

                if not is_date_only:
                    # ИСПРАВЛЕНИЕ: Удаляем завершающую точку
                    requirements.append(s_strip.rstrip('.'))

    return sorted(list(set(requirements)))


def extract_deadlines(text: str, keywords: Optional[List[str]] = None) -> List[str]:
    found_dates = []
    # ИСПРАВЛЕНИЕ: Разбиваем только по новой строке, чтобы точка не ломала даты
    paragraphs = text.splitlines()

    search_keywords = keywords if keywords is not None else DATE_RELATED_KEYWORDS

    for p in paragraphs:
        # Для извлечения дат проверяем всю строку
        if search_keywords and not any(kw.lower() in p.lower() for kw in search_keywords):
            continue

        for d in re.findall(DATE_REGEX, p):
            for fmt in ("%d.%m.%Y", "%d/%m/%Y", "%d-%m-%Y",
                        "%d.%m.%y", "%d/%m/%y", "%d-%m-%y"):
                try:
                    dt = datetime.strptime(d, fmt).date()
                    if dt.year < 100:
                        dt = dt.replace(year=(2000 + dt.year if dt.year < 50 else 1900 + dt.year))
                    if 1900 <= dt.year <= 2100:
                        found_dates.append(str(dt))
                        break
                except ValueError:
                    continue
    return sorted(list(set(found_dates)))


def extract_entities(text: str, min_score: float = 0.5) -> List[Dict[str, Any]]:
    entities = []
    try:
        global NER_PIPELINE

        # --- Активация NER-пайплайна ---
        if NER_PIPELINE:
            # Вызов модели. Она возвращает список агрегированных сущностей.
            ner_results = NER_PIPELINE(text)
        else:
            ner_results = []
        # ------------------------------------

        for ent in ner_results:
            score = float(ent.get("score", 0))
            if score >= min_score:
                # 'entity_group' содержит тип сущности (ORG, LOC, PER)
                entity_group = ent.get("entity_group").upper()

                # 'word' - это уже агрегированная сущность благодаря "aggregation_strategy": "simple"
                entities.append({
                    "entity_group": entity_group,
                    "word": ent.get("word"),
                    "score": score
                })

        # Дополнительная логика извлечения (роли заказчик/поставщик)
        roles_matches = re.findall(
            r"(?:заказчик|buyer|поставщик|supplier)\s*[:\-]\s*([A-Za-zА-Яа-я0-9\s]+)",
            text, flags=re.IGNORECASE
        )
        for r in roles_matches:
            role_type = "BUYER" if re.search(r"(заказчик|buyer)", r, flags=re.IGNORECASE) else "SUPPLIER"
            entities.append({"entity_group": role_type, "word": r.strip(), "score": 1.0})

        # Компании, найденные по ключевому слову "Компания"
        orgs = re.findall(r"Компания\s+([A-Za-zА-Яа-я0-9]+)", text)
        for o in orgs:
            entities.append({"entity_group": "ORG", "word": o.strip(), "score": 1.0})

        # Уникализация: Удаляем дубликаты, которые могут возникнуть из-за NER и ручной логики.
        unique_entities = []
        seen = set()
        for ent in entities:
            # Для уникальности проверяем группу и слово
            ent_key = (ent["entity_group"], ent["word"])
            if ent_key not in seen:
                # Добавляем сущность, сохраняя ее оригинальный score
                unique_entities.append(ent)
                seen.add(ent_key)
        entities = unique_entities

    except Exception as e:
        print(f"[ERROR] NER extraction failed: {e}")
        entities = []

    return entities


def extract_prices(text: str) -> List[Dict[str, Any]]:
    price_keywords = r"(?:цена|стоимость|price|cost|руб|kzt|usd|eur|тг|тенге|₸|₽|us\$)"

    # Новый шаблон: Ищем число, которое может быть либо:
    # 1. С разделителями тысяч (пробел, запятая, точка)
    # 2. Простое число
    # (Число: group 1) (Валюта: group 2)
    # Используем lookbehind `(?<=...)` для ключевого слова, чтобы не включать его в `m.group(0)`,
    # или просто требуем, чтобы оно было перед числом.

    # Шаблон: (Optional Key/Context) + (The Actual Number/Value) + (Optional Currency)
    # Number part: \d{1,3}(?:[\s,.]\d{3})*(?:[.,]\d+)?|\d+
    # Это находит: 1 200 000, 1,200,000, 1.200.000, 1200000, 12.34
    pattern = re.compile(
        rf"(?:{price_keywords}[:\s]*|[\s]|^)?(\d{{1,3}}(?:[\s,.]\d{{3}})*(?:[.,]\d{{1,2}})?|\d+)\s*(KZT|USD|EUR|₸|₽|US\$|руб|тг)?",
        flags=re.IGNORECASE
    )

    prices = []
    for m in pattern.finditer(text):
        if not m.group(1):
            continue

        price_str = m.group(1).strip()
        currency = m.group(2)

        # 1. Удаляем пробелы (разделители тысяч)
        price_str_normalized = price_str.replace(" ", "")

        # 2. Заменяем запятые на точки
        price_str_normalized = price_str_normalized.replace(",", ".")

        # 3. Обработка множественных точек (разделитель тысяч vs десятичный):
        # Если точек > 1 (напр., 1.200.000), удаляем все точки, кроме последней
        if price_str_normalized.count('.') > 1:
            parts = price_str_normalized.split('.')
            # Соединяем все части, кроме последней (без точек), и добавляем последнюю часть через точку
            price_str_normalized = "".join(parts[:-1]) + "." + parts[-1]

        # 4. Если осталась одна точка, а после нее 3+ цифры (напр. 1.200), считаем это разделителем тысяч и удаляем точку
        elif price_str_normalized.count('.') == 1 and len(price_str_normalized.split('.')[-1]) > 2:
            price_str_normalized = price_str_normalized.replace('.', '')

        # Финальная очистка
        price_str_final = re.sub(r"[^\d.]", "", price_str_normalized)

        if not currency:
            # Пытаемся определить валюту по контексту всего совпадения (m.group(0))
            if re.search(r"(kzt|тг|тенге)", m.group(0), flags=re.IGNORECASE):
                currency = "KZT"
            else:
                currency = "KZT"

        try:
            price_val = float(price_str_final)
        except ValueError:
            continue

        if 1000 <= price_val <= 1_000_000_000:
            prices.append({"value": price_val, "currency": currency})

    unique = {f"{p['value']}_{p['currency']}": p for p in prices}
    return sorted(unique.values(), key=lambda x: x['value'])

# --- API endpoint ---
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

    # Title
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    title = lines[0].rstrip(".").strip() if lines else text.strip().rstrip(".")

    # Extract
    requirements = extract_requirements(text)
    deadlines = extract_deadlines(text, keywords=DEADLINE_KEYWORDS)
    all_dates = extract_deadlines(text, keywords=DATE_RELATED_KEYWORDS)
    prices = extract_prices(text)
    entities = extract_entities(text)

    # Confidence
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


# --- /match ---
@app.post("/match")
def match(input: MatchInput):
    if SUPPLIERS_DF.empty:
        return {"tender_id": input.tender_id, "matches": []}

    query = " ".join(filter(None, [input.title, input.subject]))
    if not query.strip():
        return {"tender_id": input.tender_id, "matches": []}

    try:
        # --- НОРМАЛИЗАЦИЯ И ВЕСОВОЕ ОБЪЕДИНЕНИЕ ---
        def normalize_scores(scores):
            min_s, max_s = scores.min(), scores.max()
            if max_s - min_s < 1e-6:
                return np.zeros_like(scores)
            return (scores - min_s) / (max_s - min_s)

        # SBERT
        sbert_scores = np.zeros(len(SUPPLIERS_DF))
        if EMBED_MODEL and SUPPLIER_EMBS is not None:
            query_emb = EMBED_MODEL.encode(query, convert_to_tensor=True)
            cos_scores = util.cos_sim(query_emb, SUPPLIER_EMBS)[0]
            sbert_scores = cos_scores.cpu().numpy().astype(float)
            sbert_scores = normalize_scores(sbert_scores)

        # TF-IDF
        tfidf_scores = np.zeros(len(SUPPLIERS_DF))
        if TFIDF_VECT and TFIDF_MATRIX is not None:
            query_vec = TFIDF_VECT.transform([query])
            tfidf_scores = cosine_similarity(query_vec, TFIDF_MATRIX)[0].astype(float)
            tfidf_scores = normalize_scores(tfidf_scores)

        # Weighted merge
        weight_sbert = 0.6
        final_scores = weight_sbert * sbert_scores + (1 - weight_sbert) * tfidf_scores

        top_k_idx = final_scores.argsort()[-input.top_k:][::-1]
        matches = [
            {
                "supplier_id": int(SUPPLIERS_DF.iloc[idx]['pid']),
                "name": SUPPLIERS_DF.iloc[idx]['name_ru'],
                "score": float(final_scores[idx])
            }
            for idx in top_k_idx if final_scores[idx] > 0.1  # фильтр низких скор
        ]

    except Exception as e:
        print("[ERROR] Match failed:", e)
        matches = []

    return {"tender_id": input.tender_id, "matches": matches}


# --- /risk ---
def advanced_risk_analysis(features: Dict[str, Any]) -> List[str]:
    reasons = []

    if features.get("is_rnu", 0):
        reasons.append("Supplier is in RNU")
    if features.get("past_violations", 0):
        reasons.append("Supplier has past violations")
    if features.get("price", 0) > 1_000_000:
        reasons.append("Price unusually high")
    if features.get("deadline_days", 9999) < 5:
        reasons.append("Deadline is very short")
    if features.get("requirements_count", 0) == 0:
        reasons.append("No requirements specified")

    # Аффилированные компании
    supplier_name = features.get("supplier_name")
    if supplier_name and not SUPPLIERS_DF.empty:
        affiliated = SUPPLIERS_DF[
            SUPPLIERS_DF['name_ru'].str.contains(supplier_name, case=False, na=False)
        ]
        if len(affiliated) > 1:
            reasons.append("Potentially affiliated supplier")

    # Подозрительные цены
    median_price = features.get("median_price")
    if median_price and features.get("price", 0) > 2 * median_price:
        reasons.append("Price significantly above market median")

    return reasons


@app.post("/risk", response_model=RiskOutput)
def calculate_risk(input: RiskInput):
    f = input.features or {}
    reasons = advanced_risk_analysis(f)

    ml_score = 0.0
    try:
        if RISK_MODEL and SCALER:
            feat_order = [
                'price', 'deadline_days', 'requirements_count',
                'is_rnu', 'past_violations', 'company_age'
            ]
            x = np.array([[f.get(feat, 0) for feat in feat_order]])
            x_scaled = SCALER.transform(x)
            ml_score = float(RISK_MODEL.predict_proba(x_scaled)[0][1])
    except Exception as e:
        print("[ERROR] ML risk prediction failed:", e)

    rule_score = len(reasons) / 5
    risk_score = min(1.0, 0.6 * ml_score + 0.4 * rule_score)

    # --- Градация риска ---
    if risk_score < 0.3:
        risk_label = 0  # Low
    elif risk_score < 0.7:
        risk_label = 1  # Medium
    else:
        risk_label = 2  # High

    return RiskOutput(
        tender_id=input.tender_id,
        risk_score=round(risk_score, 2),
        risk_label=risk_label,
        risk_reasons=reasons
    )
