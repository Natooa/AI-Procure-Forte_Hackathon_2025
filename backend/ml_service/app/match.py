# match.py
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import util
from . import globals as g

# ВАЖНО: Не импортируйте SUPPLIERS_DF напрямую!

def match(input):
    if g.SUPPLIERS_DF.empty:
        return {"tender_id": input.tender_id, "matches": []}

    query = " ".join(filter(None, [input.title, input.subject]))
    if not query.strip():
        return {"tender_id": input.tender_id, "matches": []}

    try:
        def normalize_scores(scores):
            min_s, max_s = scores.min(), scores.max()
            if max_s - min_s < 1e-6:
                return np.zeros_like(scores)
            return (scores - min_s) / (max_s - min_s)

        # SBERT
        sbert_scores = np.zeros(len(g.SUPPLIERS_DF))
        if g.EMBED_MODEL and g.SUPPLIER_EMBS is not None:
            query_emb = g.EMBED_MODEL.encode(query, convert_to_tensor=True)
            cos_scores = util.cos_sim(query_emb, g.SUPPLIER_EMBS)[0]
            sbert_scores = cos_scores.cpu().numpy().astype(float)
            sbert_scores = normalize_scores(sbert_scores)

        # TF-IDF
        tfidf_scores = np.zeros(len(g.SUPPLIERS_DF))
        if g.TFIDF_VECT and g.TFIDF_MATRIX is not None:
            query_vec = g.TFIDF_VECT.transform([query])
            tfidf_scores = cosine_similarity(query_vec, g.TFIDF_MATRIX)[0].astype(float)
            tfidf_scores = normalize_scores(tfidf_scores)

        # Weighted merge
        weight_sbert = 0.6
        final_scores = weight_sbert * sbert_scores + (1 - weight_sbert) * tfidf_scores

        top_k_idx = final_scores.argsort()[-input.top_k:][::-1]
        matches = [
            {
                "supplier_id": int(g.SUPPLIERS_DF.iloc[idx]['pid']),
                "name": g.SUPPLIERS_DF.iloc[idx]['name_ru'],
                "score": float(final_scores[idx])
            }
            for idx in top_k_idx if final_scores[idx] > 0.1
        ]

    except Exception as e:
        print("[ERROR] Match failed:", e)
        matches = []

    return {"tender_id": input.tender_id, "matches": matches}
