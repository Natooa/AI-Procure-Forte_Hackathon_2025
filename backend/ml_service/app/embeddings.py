# embeddings.py
import asyncio
from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import TfidfVectorizer

from .config import AUTOUPDATE_INTERVAL
from .data_loader import load_rnu, load_suppliers, train_risk_model
from . import globals as g

def update_embeddings():
    if not g.SUPPLIERS_DF.empty and g.EMBED_MODEL:
        g.SUPPLIER_EMBS = g.EMBED_MODEL.encode(
            g.SUPPLIERS_DF['name_ru'].astype(str).tolist(),
            convert_to_tensor=True
        )

        g.TFIDF_VECT = TfidfVectorizer()
        g.TFIDF_MATRIX = g.TFIDF_VECT.fit_transform(
            g.SUPPLIERS_DF['name_ru'].astype(str).tolist()
        )

        print("[INFO] Embeddings updated")

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

def init_embed_model():
    """Инициализация embedding модели"""
    g.EMBED_MODEL = SentenceTransformer('all-MiniLM-L6-v2')
    print("[INFO] Embedding model initialized")
