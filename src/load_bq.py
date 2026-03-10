import pandas as pd
from google.cloud import bigquery

# ===== 設定 =====
PROJECT_ID = "my-first-bigquery-483106"
DATASET_ID = "solar"
TABLE_ID = "weather_clean"

CSV_PATH = "data/processed/weather_clean.csv"

# ===== 讀取 CSV =====
df = pd.read_csv(CSV_PATH)

# 確保 date 是 datetime
df["date"] = pd.to_datetime(df["date"]).dt.date

client = bigquery.Client(project=PROJECT_ID)
table_ref = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}"

# ===== 1️⃣ 查詢 BigQuery 已存在的日期 =====
query = f"""
SELECT DISTINCT date
FROM `{table_ref}`
"""
try:
    existing_dates = client.query(query).to_dataframe()["date"].tolist()
except Exception:
    # 表還不存在時
    existing_dates = []

# ===== 2️⃣ 只保留 BigQuery 沒有的日期 =====
df_new = df[~df["date"].isin(existing_dates)]

if df_new.empty:
    print("ℹ️ 沒有新日期資料，跳過寫入")
else:
    # ===== 3️⃣ append 寫入 =====
    job_config = bigquery.LoadJobConfig(
        write_disposition="WRITE_APPEND"
    )

    job = client.load_table_from_dataframe(
        df_new,
        table_ref,
        job_config=job_config
    )
    job.result()

    print(f"✅ 成功寫入 {len(df_new)} 筆新資料到 BigQuery")
