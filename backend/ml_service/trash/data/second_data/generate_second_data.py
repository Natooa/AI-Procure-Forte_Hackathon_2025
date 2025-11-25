import pandas as pd
import random
from faker import Faker
from datetime import datetime, timedelta

fake = Faker("ru_RU")

num_rows = 1200  # количество строк в каждой таблице

# ---------------------------------------------------------------------
# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# ---------------------------------------------------------------------
def rand_date():
    return fake.date_between(start_date="-3y", end_date="today")

def rand_datetime():
    return fake.date_time_between(start_date="-3y", end_date="now")

def rand_bin():
    return str(random.randint(100000000000, 999999999999))

def rand_iin():
    return str(random.randint(100000000000, 999999999999))


# ---------------------------------------------------------------------
# TRD BUY — полностью совпадает с API
# ---------------------------------------------------------------------
trd_buy = pd.DataFrame({
    "id": range(1, num_rows + 1),
    "number_anno": [fake.uuid4() for _ in range(num_rows)],
    "name_ru": [fake.sentence(nb_words=4) for _ in range(num_rows)],
    "name_kz": [fake.sentence(nb_words=4) for _ in range(num_rows)],
    "ref_trade_methods_id": [random.randint(1, 10) for _ in range(num_rows)],
    "publish_date": [rand_date() for _ in range(num_rows)],
    "start_date": [rand_date() for _ in range(num_rows)],
    "end_date": [rand_date() for _ in range(num_rows)],
    "total_sum": [round(random.uniform(10000, 10000000), 2) for _ in range(num_rows)],
    "ref_buy_status_id": [random.randint(1, 5) for _ in range(num_rows)],
    "org_bin": [rand_bin() for _ in range(num_rows)],
    "system_id": [3 for _ in range(num_rows)],
    "index_date": [rand_datetime() for _ in range(num_rows)],
})


# ---------------------------------------------------------------------
# LOTS — полностью совпадает с API
# ---------------------------------------------------------------------
lots = pd.DataFrame({
    "id": range(1, num_rows + 1),
    "lot_number": [random.randint(1, 99999) for _ in range(num_rows)],
    "ref_lot_status_id": [random.randint(1, 10) for _ in range(num_rows)],
    "last_update_date": [rand_datetime() for _ in range(num_rows)],
    "union_lots": [random.randint(0, 1) for _ in range(num_rows)],
    "count": [random.randint(1, 500) for _ in range(num_rows)],
    "amount": [round(random.uniform(5000, 5000000), 2) for _ in range(num_rows)],
    "name_ru": [fake.word() for _ in range(num_rows)],
    "name_kz": [fake.word() for _ in range(num_rows)],
    "description_ru": [fake.sentence() for _ in range(num_rows)],
    "description_kz": [fake.sentence() for _ in range(num_rows)],
    "customer_id": [random.randint(1, 500) for _ in range(num_rows)],
    "customer_bin": [rand_bin() for _ in range(num_rows)],
    "trd_buy_number_anno": [fake.uuid4() for _ in range(num_rows)],
    "trd_buy_id": [random.randint(1, num_rows) for _ in range(num_rows)],
    "dumping": [random.choice([0, 1]) for _ in range(num_rows)],
    "dumping_lot_price": [round(random.uniform(0, 100000), 2) for _ in range(num_rows)],
    "psd_sign": [random.randint(0, 1) for _ in range(num_rows)],
    "compl_exp": [random.randint(0, 1) for _ in range(num_rows)],
    "consulting_services": [random.randint(0, 1) for _ in range(num_rows)],
    "point_list": [fake.word() for _ in range(num_rows)],
    "index_date": [rand_datetime() for _ in range(num_rows)],
    "system_id": [3 for _ in range(num_rows)],
})


# ---------------------------------------------------------------------
# SUBJECT_ALL — ДОБАВЛЕНЫ ВСЕ ПРОПУЩЕННЫЕ ПОЛЯ API
# ---------------------------------------------------------------------
subject_all = pd.DataFrame({
    "pid": range(1, num_rows + 1),
    "bin": [rand_bin() for _ in range(num_rows)],
    "iin": [rand_iin() for _ in range(num_rows)],
    "inn": [rand_bin() for _ in range(num_rows)],
    "unp": [rand_bin() for _ in range(num_rows)],
    "regdate": [rand_date() for _ in range(num_rows)],
    "crdate": [rand_date() for _ in range(num_rows)],
    "index_date": [rand_datetime() for _ in range(num_rows)],
    "number_reg": [random.randint(10000, 99999) for _ in range(num_rows)],
    "series": [fake.word() for _ in range(num_rows)],
    "name_ru": [fake.company() for _ in range(num_rows)],
    "name_kz": [fake.company() for _ in range(num_rows)],
    "full_name_ru": [fake.company() for _ in range(num_rows)],
    "full_name_kz": [fake.company() for _ in range(num_rows)],
    "country_code": [random.choice(["KZ", "RU", "UZ", "KG"]) for _ in range(num_rows)],
    "customer": [random.randint(0, 1) for _ in range(num_rows)],
    "organizer": [random.randint(0, 1) for _ in range(num_rows)],
    "mark_national_company": [random.randint(0, 1) for _ in range(num_rows)],
    "ref_kopf_code": [random.randint(10, 999) for _ in range(num_rows)],
    "mark_assoc_with_disab": [random.randint(0, 1) for _ in range(num_rows)],
    "system_id": [3 for _ in range(num_rows)],
    "supplier": [random.randint(0, 1) for _ in range(num_rows)],
    "type_supplier": [random.randint(1, 3) for _ in range(num_rows)],
    "krp_code": [random.randint(10, 999) for _ in range(num_rows)],
    "oked_list": [fake.word() for _ in range(num_rows)],
    "kse_code": [random.randint(10, 999) for _ in range(num_rows)],
    "mark_world_company": [random.randint(0, 1) for _ in range(num_rows)],
    "mark_state_monopoly": [random.randint(0, 1) for _ in range(num_rows)],
    "mark_natural_monopoly": [random.randint(0, 1) for _ in range(num_rows)],
    "mark_patronymic_producer": [random.randint(0, 1) for _ in range(num_rows)],
    "mark_patronymic_supplyer": [random.randint(0, 1) for _ in range(num_rows)],
    "mark_small_employer": [random.randint(0, 1) for _ in range(num_rows)],
    "is_single_org": [random.randint(0, 1) for _ in range(num_rows)],
    "email": [fake.email() for _ in range(num_rows)],
    "phone": [fake.phone_number() for _ in range(num_rows)],
    "website": [fake.url() for _ in range(num_rows)],
    "last_update_date": [rand_datetime() for _ in range(num_rows)],
    "qvazi": [random.randint(0, 1) for _ in range(num_rows)],
    "year": [random.randint(2000, 2024) for _ in range(num_rows)],
    "mark_resident": [random.randint(0, 1) for _ in range(num_rows)],
})


# ---------------------------------------------------------------------
# RNU — совпадает
# ---------------------------------------------------------------------
rnu = pd.DataFrame({
    "pid": range(1, num_rows + 1),
    "supplier_biin": [rand_bin() for _ in range(num_rows)],
    "supplier_innunp": [rand_bin() for _ in range(num_rows)],
    "supplier_name_ru": [fake.company() for _ in range(num_rows)],
    "supplier_name_kz": [fake.company() for _ in range(num_rows)],
    "kato_list": [fake.word() for _ in range(num_rows)],
    "index_date": [rand_datetime() for _ in range(num_rows)],
    "system_id": [3 for _ in range(num_rows)],
})


# ---------------------------------------------------------------------
# CONTRACT — совпадает с API
# ---------------------------------------------------------------------
contract = pd.DataFrame({
    "id": range(1, num_rows + 1),
    "contract_number": [fake.uuid4() for _ in range(num_rows)],
    "contract_number_sys": [fake.uuid4() for _ in range(num_rows)],
    "trd_buy_id": [random.randint(1, num_rows) for _ in range(num_rows)],
    "trd_buy_number_anno": [fake.uuid4() for _ in range(num_rows)],
    "ref_contract_type_id": [random.randint(1, 5) for _ in range(num_rows)],
    "ref_contract_status_id": [random.randint(1, 10) for _ in range(num_rows)],
    "crdate": [rand_datetime() for _ in range(num_rows)],
    "contract_sum_wnds": [round(random.uniform(50000, 50000000), 2) for _ in range(num_rows)],
    "supplier_id": [random.randint(1, num_rows) for _ in range(num_rows)],
    "supplier_biin": [rand_bin() for _ in range(num_rows)],
    "customer_id": [random.randint(1, num_rows) for _ in range(num_rows)],
    "customer_bin": [rand_bin() for _ in range(num_rows)],
    "index_date": [rand_datetime() for _ in range(num_rows)],
    "system_id": [3 for _ in range(num_rows)],
})


# ---------------------------------------------------------------------
# CONTRACT DETAILS — ДОБАВЛЕНО ВСЕ, ЧТО ТЫ ПРОСИЛ
# ---------------------------------------------------------------------

# ---------------------------------------------------------------------
# CONTRACT DETAILS — contract/all — 100% совпадает с API
# ---------------------------------------------------------------------
contract_details = pd.DataFrame({
    "id": range(1, num_rows + 1),
    "parent_id": [random.randint(1, num_rows) for _ in range(num_rows)],
    "root_id": [random.randint(1, num_rows) for _ in range(num_rows)],

    "trd_buy_id": [random.randint(1, num_rows) for _ in range(num_rows)],
    "trd_buy_number_anno": [fake.uuid4() for _ in range(num_rows)],

    "ref_amendm_agreem_justif_id": [random.randint(1, 5) for _ in range(num_rows)],
    "ref_contract_status_id": [random.randint(1, 10) for _ in range(num_rows)],
    "deleted": [random.randint(0, 1) for _ in range(num_rows)],

    "crdate": [rand_datetime() for _ in range(num_rows)],
    "last_update_date": [rand_datetime() for _ in range(num_rows)],

    "supplier_id": [random.randint(1, num_rows) for _ in range(num_rows)],
    "supplier_biin": [rand_bin() for _ in range(num_rows)],
    "supplier_bik": [fake.swift() for _ in range(num_rows)],
    "supplier_iik": [fake.bban() for _ in range(num_rows)],
    "supplier_bank_name_kz": [fake.company() for _ in range(num_rows)],
    "supplier_bank_name_ru": [fake.company() for _ in range(num_rows)],

    "customer_id": [random.randint(1, num_rows) for _ in range(num_rows)],
    "customer_bin": [rand_bin() for _ in range(num_rows)],
    "customer_bik": [fake.swift() for _ in range(num_rows)],
    "customer_iik": [fake.bban() for _ in range(num_rows)],
    "customer_bank_name_kz": [fake.company() for _ in range(num_rows)],
    "customer_bank_name_ru": [fake.company() for _ in range(num_rows)],

    "contract_number": [fake.uuid4() for _ in range(num_rows)],
    "contract_number_sys": [fake.uuid4() for _ in range(num_rows)],

    "fin_year": [random.randint(2015, 2025) for _ in range(num_rows)],
    "ref_contract_agr_form_id": [random.randint(1, 5) for _ in range(num_rows)],
    "ref_contract_year_type_id": [random.randint(1, 5) for _ in range(num_rows)],
    "ref_finsource_id": [random.randint(1, 5) for _ in range(num_rows)],
    "ref_currency_code": [random.choice(["KZT", "USD", "EUR"]) for _ in range(num_rows)],

    "contract_sum_wnds": [round(random.uniform(50000, 50000000), 2) for _ in range(num_rows)],

    "sign_date": [rand_date() for _ in range(num_rows)],
    "ec_end_date": [rand_date() for _ in range(num_rows)],
    "plan_exec_date": [rand_date() for _ in range(num_rows)],
    "fakt_exec_date": [rand_date() for _ in range(num_rows)],

    "fakt_sum_wnds": [round(random.uniform(10000, 10000000), 2) for _ in range(num_rows)],
    "contract_end_date": [rand_date() for _ in range(num_rows)],
    "ref_contract_cancel_id": [random.randint(0, 5) for _ in range(num_rows)],

    "description_kz": [fake.sentence() for _ in range(num_rows)],
    "description_ru": [fake.sentence() for _ in range(num_rows)],
    "sign_reason_doc_name": [fake.word() for _ in range(num_rows)],
    "sign_reason_doc_date": [rand_date() for _ in range(num_rows)],
    "trd_buy_itogi_date_public": [rand_date() for _ in range(num_rows)],

    "fakt_trade_methods_id": [random.randint(1, 10) for _ in range(num_rows)],
    "ec_customer_approve": [random.randint(0, 1) for _ in range(num_rows)],
    "ec_supplier_approve": [random.randint(0, 1) for _ in range(num_rows)],

    "contract_ms": [round(random.uniform(0, 100), 2) for _ in range(num_rows)],
    "supplier_legal_address": [fake.address() for _ in range(num_rows)],
    "customer_legal_address": [fake.address() for _ in range(num_rows)],

    "payments_terms_ru": [fake.sentence() for _ in range(num_rows)],
    "payments_terms_kz": [fake.sentence() for _ in range(num_rows)],
    "is_gu": [random.randint(0, 1) for _ in range(num_rows)],
    "exchange_rate": [round(random.uniform(400, 600), 2) for _ in range(num_rows)],

    "system_id": [3 for _ in range(num_rows)],
    "index_date": [rand_datetime() for _ in range(num_rows)],
})


# ---------------------------------------------------------------------
# СОХРАНЕНИЕ В CSV
# ---------------------------------------------------------------------
trd_buy.to_csv("trd_buy.csv", index=False)
lots.to_csv("lots.csv", index=False)
subject_all.to_csv("subject_all.csv", index=False)
rnu.to_csv("rnu.csv", index=False)
contract.to_csv("contract.csv", index=False)
contract_details.to_csv("contract_details.csv", index=False)

# ---------------------------------------------------------------------
# СОХРАНЕНИЕ ВСЕГО В EXCEL (1 файл, много листов)
# ---------------------------------------------------------------------
with pd.ExcelWriter("all_tables.xlsx") as writer:
    trd_buy.to_excel(writer, sheet_name="trd_buy", index=False)
    lots.to_excel(writer, sheet_name="lots", index=False)
    subject_all.to_excel(writer, sheet_name="subject_all", index=False)
    rnu.to_excel(writer, sheet_name="rnu", index=False)
    contract.to_excel(writer, sheet_name="contract", index=False)
    contract_details.to_excel(writer, sheet_name="contract_details", index=False)

print("Готово! Все таблицы полностью соответствуют API.")