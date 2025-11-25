import pandas as pd
import numpy as np

# Количество примеров
num_samples = 100

# Генерация признаков
np.random.seed(42)
data = pd.DataFrame({
    'price': np.random.randint(100000, 10000000, size=num_samples),
    'deadline_days': np.random.randint(0, 600, size=num_samples),
    'requirements_count': np.random.randint(10, 60, size=num_samples),
    'is_rnu': np.random.choice([0, 1], size=num_samples, p=[0.7, 0.3]),
    'past_violations': np.random.randint(0, 10000000, size=num_samples),
    'delivery_delay_sum': np.random.randint(0, 1000, size=num_samples),
    'company_age': np.random.randint(1, 50, size=num_samples)
})

# Простая логика для генерации риска
def compute_risk(row):
    score = 0
    if row['price'] > 5000000:
        score += 1
    if row['deadline_days'] < 30:
        score += 1
    if row['requirements_count'] > 40:
        score += 1
    if row['is_rnu'] == 1:
        score += 1
    if row['past_violations'] > 1000000:
        score += 1
    if row['delivery_delay_sum'] > 500:
        score += 1
    # Присваиваем метку риска от 0 до 2
    if score <= 2:
        return 0
    elif score <= 4:
        return 1
    else:
        return 2

data['risk_label'] = data.apply(compute_risk, axis=1)

# Сохраняем в CSV
data.to_csv('risk_train.csv', index=False, sep='\t')

print("Синтетический датасет создан!")
print(data.head())







# import os
#
# import pandas as pd
# from sklearn.model_selection import train_test_split
# from sklearn.preprocessing import StandardScaler
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
# import joblib
#
# # ---------------------------
# # 1. Загружаем датасет
# # ---------------------------
#
# BASE_DIR = os.path.dirname(__file__)
# data_path = os.path.join(BASE_DIR, 'risk_train.csv')
# data = pd.read_csv(data_path)
#
# print("Распределение классов:")
# print(data['risk_label'].value_counts())
#
# # ---------------------------
# # 2. Разделяем признаки и метку
# # ---------------------------
# features = ['price', 'deadline_days', 'requirements_count', 'is_rnu', 'past_violations', 'company_age']
# X = data[features].fillna(0)
# y = data['risk_label']
#
# # ---------------------------
# # 3. Train/test split
# # ---------------------------
# X_train, X_test, y_train, y_test = train_test_split(
#     X, y, test_size=0.2, random_state=42, stratify=y
# )
#
# # ---------------------------
# # 4. Масштабирование
# # ---------------------------
# scaler = StandardScaler()
# X_train_scaled = scaler.fit_transform(X_train)
# X_test_scaled = scaler.transform(X_test)
#
# # ---------------------------
# # 5. RandomForest с балансировкой классов
# # ---------------------------
# model = RandomForestClassifier(
#     n_estimators=200, random_state=42, class_weight='balanced'
# )
# model.fit(X_train_scaled, y_train)
#
# # ---------------------------
# # 6. Оценка модели
# # ---------------------------
# y_pred = model.predict(X_test_scaled)
# y_proba = model.predict_proba(X_test_scaled)
#
# print("Confusion Matrix:")
# print(confusion_matrix(y_test, y_pred))
#
# print("\nClassification Report:")
# print(classification_report(y_test, y_pred))
#
# # ROC-AUC для многоклассовой задачи
# roc_auc = roc_auc_score(y_test, y_proba, multi_class='ovr')
# print("\nMulticlass ROC-AUC Score:", roc_auc)
#
# # ---------------------------
# # 7. Сохраняем модель и scaler
# # ---------------------------
# joblib.dump(model, 'risk_model.pkl')
# joblib.dump(scaler, 'risk_scaler.pkl')
# print("Модель и scaler сохранены!")
