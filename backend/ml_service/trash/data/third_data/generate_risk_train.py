import pandas as pd
import numpy as np

# Количество примеров
num_samples = 50

np.random.seed(42)

data = pd.DataFrame({
    'price': np.random.randint(100000, 10000000, size=num_samples),          # похожие на твои цены
    'deadline_days': np.random.randint(0, 600, size=num_samples),            # до ~600 дней
    'requirements_count': np.random.randint(18, 55, size=num_samples),       # похожие на твои требования
    'is_rnu': np.random.choice([0, 1], size=num_samples, p=[0.7, 0.3]),      # RNU 0/1
    'past_violations': np.random.randint(0, 8000000, size=num_samples),      # похожие на твои прошлые нарушения
    'delivery_delay_sum': np.random.randint(0, 1000, size=num_samples),      # как в твоём примере
    'company_age': np.random.randint(10, 50, size=num_samples)               # возраст компании
})

# Генерация риска с учётом признаков
def compute_risk(row):
    score = 0
    if row['price'] > 5000000:
        score += 1
    if row['deadline_days'] < 50:
        score += 1
    if row['requirements_count'] > 40:
        score += 1
    if row['is_rnu'] == 1:
        score += 1
    if row['past_violations'] > 1000000:
        score += 1
    if row['delivery_delay_sum'] > 400:
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

# Проверка распределения классов
print("\nРаспределение классов риска:")
print(data['risk_label'].value_counts())





# import pandas as pd
# from datetime import datetime
#
# today = datetime.now()
#
# # ------------------------
# # 1. Загружаем файлы
# # ------------------------
# suppliers_df = pd.read_csv("subject_all.csv")  # новый файл поставщиков
# lots_df = pd.read_csv("lots.csv")
# contracts_df = pd.read_csv("contract.csv")
# contract_details_df = pd.read_csv("contract_details.csv")
# rnu_df = pd.read_csv("rnu.csv")
# trd_buy_df = pd.read_csv("trd_buy.csv")
#
# # ------------------------
# # 2. Подготовка RNU и маппинг BIN
# # ------------------------
# # mapping: supplier_id -> bin
# supplier_bins = dict(zip(suppliers_df['pid'], suppliers_df['bin']))
# # set RNU BINов
# rnu_bins = set(rnu_df['supplier_biin'].tolist())
#
# # ------------------------
# # 3. Генерация признаков
# # ------------------------
# rows = []
#
# for _, lot in lots_df.iterrows():
#     lot_contracts = contracts_df[contracts_df['trd_buy_id'] == lot['trd_buy_id']]
#
#     # даты лота
#     trd_row = trd_buy_df[trd_buy_df['id'] == lot['trd_buy_id']]
#     if len(trd_row) == 0:
#         continue
#     start_date = pd.to_datetime(trd_row.iloc[0]['start_date'])
#     end_date = pd.to_datetime(trd_row.iloc[0]['end_date'])
#     deadline_days = max(0, (end_date - start_date).days)
#
#     for _, contract in lot_contracts.iterrows():
#         supplier_id = contract['supplier_id']
#
#         # берем supplier bin
#         supplier_bin = supplier_bins.get(supplier_id, None)
#
#         # штрафы и задержки
#         details = contract_details_df[contract_details_df['supplier_id'] == supplier_id]
#         past_fines = details['fakt_sum_wnds'].sum() if 'fakt_sum_wnds' in details else 0
#
#         if 'ec_end_date' in details and 'fakt_exec_date' in details:
#             overdue_days = (pd.to_datetime(details['ec_end_date']) - pd.to_datetime(
#                 details['fakt_exec_date'])).dt.days.sum()
#             overdue_days = max(0, overdue_days)
#         else:
#             overdue_days = 0
#
#         # признаки
#         price = lot['amount'] if 'amount' in lot else 0
#         requirements_count = len(str(lot['point_list'])) if 'point_list' in lot else 0
#         company_age = today.year - int(suppliers_df.iloc[0]['year']) if 'year' in suppliers_df.columns else 2
#
#         # пропускаем некорректные строки
#         if price <= 0 or requirements_count <= 0:
#             continue
#
#         # классификация риска
#         if supplier_bin in rnu_bins or past_fines > 50000 or overdue_days > 30:
#             risk_label = 2
#         elif past_fines > 10000 or deadline_days < 15 or company_age < 2:
#             risk_label = 1
#         else:
#             risk_label = 0
#
#         rows.append({
#             "price": price,
#             "deadline_days": deadline_days,
#             "requirements_count": requirements_count,
#             "is_rnu": 1 if supplier_bin in rnu_bins else 0,
#             "past_violations": past_fines,
#             "delivery_delay_sum": overdue_days,
#             "company_age": company_age,
#             "risk_label": risk_label
#         })
#
# # ------------------------
# # 4. Сохраняем risk_train.csv
# # ------------------------
# risk_df = pd.DataFrame(rows)
# risk_df.to_csv("risk_train.csv", index=False)
# print("✔ risk_train.csv создан, строк:", len(risk_df))
