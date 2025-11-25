# extractors.py
import re
from datetime import datetime
from typing import List, Dict, Any, Optional
from . import globals as g

REQ_KEYWORDS = [
    "сертификация", "опыт", "требования", "гарантия", "техническая поддержка",
    "warranty", "experience", "requirements", "certification", "technical support",
    "сертификаттау", "тәжірибе", "талаптар", "кепілдік"
]

DEADLINE_KEYWORDS = [
    "сроки", "deadline", "мерзімдер", "дата окончания", "final date"
]

DATE_RELATED_KEYWORDS = DEADLINE_KEYWORDS + [
    "дата публикации", "дата регистрации", "publication date", "registration date"
]

DATE_REGEX = r"\b\d{1,2}[-./]\d{1,2}[-./]\d{2,4}\b"

def extract_requirements(text: str) -> List[str]:
    paragraphs = text.splitlines()
    requirements = []

    IGNORE_ONLY_DATE_KWS = DEADLINE_KEYWORDS + ["дата публикации", "дата регистрации"]

    for p in paragraphs:
        sentences = re.split(r'(?<=[.!?])\s+', p)

        for s in sentences:
            s_strip = s.strip()
            if not s_strip:
                continue

            is_requirement = any(kw.lower() in s_strip.lower() for kw in REQ_KEYWORDS)

            if is_requirement:
                is_date_only = any(kw.lower() in s_strip.lower() for kw in IGNORE_ONLY_DATE_KWS) and len(
                    re.findall(DATE_REGEX, s_strip)) > 0 and len(s_strip) < 30

                if not is_date_only:
                    requirements.append(s_strip.rstrip('.'))

    return sorted(list(set(requirements)))


def extract_deadlines(text: str, keywords: Optional[List[str]] = None) -> List[str]:
    found_dates = []
    paragraphs = text.splitlines()

    search_keywords = keywords if keywords is not None else DATE_RELATED_KEYWORDS

    for p in paragraphs:
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
        if g.NER_PIPELINE:
            ner_results = g.NER_PIPELINE(text)
        else:
            ner_results = []

        for ent in ner_results:
            score = float(ent.get("score", 0))
            if score >= min_score:
                entity_group = ent.get("entity_group").upper()
                entities.append({
                    "entity_group": entity_group,
                    "word": ent.get("word"),
                    "score": score
                })

        roles_matches = re.findall(
            r"(?:заказчик|buyer|поставщик|supplier)\s*[:\-]\s*([A-Za-zА-Яа-я0-9\s]+)",
            text, flags=re.IGNORECASE
        )
        for r in roles_matches:
            role_type = "BUYER" if re.search(r"(заказчик|buyer)", r, flags=re.IGNORECASE) else "SUPPLIER"
            entities.append({"entity_group": role_type, "word": r.strip(), "score": 1.0})

        orgs = re.findall(r"Компания\s+([A-Za-zА-Яа-я0-9]+)", text)
        for o in orgs:
            entities.append({"entity_group": "ORG", "word": o.strip(), "score": 1.0})

        unique_entities = []
        seen = set()
        for ent in entities:
            ent_key = (ent["entity_group"], ent["word"])
            if ent_key not in seen:
                unique_entities.append(ent)
                seen.add(ent_key)
        entities = unique_entities

    except Exception as e:
        print(f"[ERROR] NER extraction failed: {e}")
        entities = []

    return entities

def extract_prices(text: str) -> List[Dict[str, Any]]:
    price_keywords = r"(?:цена|стоимость|price|cost|руб|kzt|usd|eur|тг|тенге|₸|₽|us\$)"

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

        price_str_normalized = price_str.replace(" ", "")
        price_str_normalized = price_str_normalized.replace(",", ".")

        if price_str_normalized.count('.') > 1:
            parts = price_str_normalized.split('.')
            price_str_normalized = "".join(parts[:-1]) + "." + parts[-1]

        elif price_str_normalized.count('.') == 1 and len(price_str_normalized.split('.')[-1]) > 2:
            price_str_normalized = price_str_normalized.replace('.', '')

        price_str_final = re.sub(r"[^\d.]", "", price_str_normalized)

        if not currency:
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
