import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
import joblib

# ---------------------------
# 1. Загружаем датасет
# ---------------------------
data = pd.read_csv('../app/risk_train.csv')

# ---------------------------
# 2. Разделяем признаки и метку
# ---------------------------
X = data[['price', 'deadline_days', 'requirements_count', 'is_rnu', 'past_violations', 'company_age']]
y = data['risk_label']

# ---------------------------
# 3. Train/test split
# ---------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# ---------------------------
# 4. Масштабирование
# ---------------------------
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# ---------------------------
# 5. RandomForest с балансировкой классов
# ---------------------------
model = RandomForestClassifier(n_estimators=200, random_state=42, class_weight='balanced')
model.fit(X_train_scaled, y_train)

# ---------------------------
# 6. Оценка модели
# ---------------------------
y_pred = model.predict(X_test_scaled)
y_proba = model.predict_proba(X_test_scaled)[:,1]

print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

print("\nROC-AUC Score:", roc_auc_score(y_test, y_proba))

# ---------------------------
# 7. Сохраняем модель и scaler
# ---------------------------
joblib.dump(model, 'risk_model.pkl')
joblib.dump(scaler, 'risk_scaler.pkl')
print("Модель и scaler сохранены!")
