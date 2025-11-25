from pathlib import Path

APP_ROOT = Path(__file__).parent
DATA_DIR = APP_ROOT / "data"
DATA_DIR.mkdir(exist_ok=True)

SUPPLIERS_PATH = DATA_DIR / "synthetic_data" / "suppliers.csv"
RISK_MODEL_PATH = APP_ROOT / "risk_model.pkl"
RISK_SCALER_PATH = APP_ROOT / "risk_scaler.pkl"
RNU_PATH = DATA_DIR / "synthetic_data" / "rnu.csv"
RISK_TRAIN_PATH = APP_ROOT / "risk_train.csv"

AUTOUPDATE_INTERVAL = 600  # секунд
