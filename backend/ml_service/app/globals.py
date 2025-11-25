# globals.py
"""Централизованное хранилище для всех глобальных переменных"""

import pandas as pd
from typing import Any, List, Dict

# Data
SUPPLIERS_DF: pd.DataFrame = pd.DataFrame()
RNU_LIST: List[Dict[str, Any]] = []

# ML Models
RISK_MODEL: Any = None
SCALER: Any = None
NER_PIPELINE: Any = None

# Embeddings
EMBED_MODEL: Any = None
SUPPLIER_EMBS: Any = None
TFIDF_VECT: Any = None
TFIDF_MATRIX: Any = None