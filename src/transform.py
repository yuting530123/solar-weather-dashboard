import pandas as pd

def transform_weather():
    # 1. 讀 raw 資料
    df = pd.read_csv("data/raw/weather_raw.csv")

    # 2. 清洗資料
    df['PP01'] = df['PP01'].replace(-9.8, 0.0)

    # 3. 時間處理
    df['date'] = pd.to_datetime(df['yyyymmdd'], format='%Y%m%d')
    df = df.sort_values('date').reset_index(drop=True)
    df['month'] = df['date'].dt.month

    # 4. 存 processed
    df.to_csv("data/processed/weather_clean.csv", index=False)

if __name__ == "__main__":
    transform_weather()
