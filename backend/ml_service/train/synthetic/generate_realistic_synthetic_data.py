import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

NUM_SUPPLIERS = 100
NUM_LOTS = 150
NUM_CONTRACTS = 200

today = datetime.now()
random.seed(42)
np.random.seed(42)

# ---------------------------
# 1. Поставщики
# ---------------------------
suppliers = []
for i in range(1, NUM_SUPPLIERS + 1):
    regdate = today - timedelta(days=random.randint(365, 365*15))
    suppliers.append({
        "pid": i,
        "bin": f"{100000000000+i}",
        "name": f"Supplier {i}",
        "regdate": regdate.strftime("%Y-%m-%d")
    })
suppliers_df = pd.DataFrame(suppliers)

# ---------------------------
# 2. RNU (high risk)
# ---------------------------
rnu_ids = random.sample(list(suppliers_df["pid"]), k=15)

# ---------------------------
# 3. Лоты
# ---------------------------
lots = []
for i in range(1, NUM_LOTS + 1):
    start = today - timedelta(days=random.randint(30, 180))
    end = start + timedelta(days=random.randint(5, 60))
    lots.append({
        "id": i,
        "price": random.randint(300_000, 7_000_000),
        "description_length": random.randint(5, 60),
        "start": start,
        "end": end,
        "customer_id": random.choice(suppliers_df["pid"])
    })
lots_df = pd.DataFrame(lots)

# ---------------------------
# 4. Контракты
# ---------------------------
contracts = []
for i in range(1, NUM_CONTRACTS + 1):
    lot = random.choice(lots)
    supplier = random.choice(suppliers)
    contracts.append({
        "id": i,
        "lot_id": lot["id"],
        "supplier_id": supplier["pid"],
    })
contracts_df = pd.DataFrame(contracts)

# ---------------------------
# 5. Акт → штрафы / задержки
# ---------------------------
acts = []
for c in contracts:
    if random.random() < 0.4:  # 40% контрактов имеют нарушения
        for _ in range(random.randint(1,2)):
            acts.append({
                "supplier_id": c["supplier_id"],
                "fine": random.randint(1000, 80_000),
                "days_overdue": random.randint(1, 45)
            })
acts_df = pd.DataFrame(acts)

# ---------------------------
# 6. Формируем признаки + класс риска
# ---------------------------
rows = []

for _, lot in lots_df.iterrows():
    supplier_ids = contracts_df[contracts_df["lot_id"] == lot["id"]]["supplier_id"].tolist()
    for sid in supplier_ids:
        supplier = suppliers_df[suppliers_df["pid"] == sid].iloc[0]
        past_fines = acts_df[acts_df["supplier_id"] == sid]["fine"].sum()
        overdue_days = acts_df[acts_df["supplier_id"] == sid]["days_overdue"].sum()

        company_age = (today - datetime.strptime(supplier["regdate"], "%Y-%m-%d")).days
        deadline_days = (lot["end"] - lot["start"]).days

        # --- Риск классификация ---
        if sid in rnu_ids or past_fines > 50_000 or overdue_days > 30:
            risk_label = 2  # high
        elif past_fines > 10_000 or deadline_days < 15 or company_age < 400:
            risk_label = 1  # medium
        else:
            risk_label = 0  # low

        rows.append({
            "price": lot["price"],
            "deadline_days": deadline_days,
            "requirements_count": lot["description_length"],
            "is_rnu": 1 if sid in rnu_ids else 0,
            "past_violations": past_fines,
            "delivery_delay_sum": overdue_days,
            "company_age": company_age,
            "risk_label": risk_label
        })

risk_df = pd.DataFrame(rows)

# Балансировка (до 500 строк)
while len(risk_df) < 500:
    extra = risk_df.sample(n=500 - len(risk_df), replace=True).copy()
    risk_df = pd.concat([risk_df, extra], ignore_index=True)

risk_df.to_csv("risk_train.csv", index=False)
print("✔ Создан файл risk_train.csv")
print("Строк:", len(risk_df))
