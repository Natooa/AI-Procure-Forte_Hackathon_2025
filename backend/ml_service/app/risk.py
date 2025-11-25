# risk.py
import numpy as np
from .models import RiskOutput
from . import globals as g

# ВАЖНО: Не импортируйте SUPPLIERS_DF, RISK_MODEL, SCALER напрямую из data_loader!

def advanced_risk_analysis(features):
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
    if supplier_name and not g.SUPPLIERS_DF.empty:
        affiliated = g.SUPPLIERS_DF[
            g.SUPPLIERS_DF['name_ru'].str.contains(supplier_name, case=False, na=False)
        ]
        if len(affiliated) > 1:
            reasons.append("Potentially affiliated supplier")

    # Подозрительные цены
    median_price = features.get("median_price")
    if median_price and features.get("price", 0) > 2 * median_price:
        reasons.append("Price significantly above market median")

    return reasons

def calculate_risk(input):
    f = input.features or {}
    reasons = advanced_risk_analysis(f)

    ml_score = 0.0
    try:
        if g.RISK_MODEL and g.SCALER:
            feat_order = [
                'price', 'deadline_days', 'requirements_count',
                'is_rnu', 'past_violations', 'company_age'
            ]
            x = np.array([[f.get(feat, 0) for feat in feat_order]])
            x_scaled = g.SCALER.transform(x)
            ml_score = float(g.RISK_MODEL.predict_proba(x_scaled)[0][1])
    except Exception as e:
        print("[ERROR] ML risk prediction failed:", e)

    rule_score = len(reasons) / 5
    risk_score = min(1.0, 0.6 * ml_score + 0.4 * rule_score)

    # Градация риска
    if risk_score < 0.4:
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
