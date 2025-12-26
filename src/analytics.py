import pandas as pd

def build_analytics():
    # 1. 讀 processed 資料
    df = pd.read_csv("data/processed/weather_clean.csv")

    # 2. 太陽能計算
    panel_area = 10         # 平方公尺
    panel_efficiency = 0.18 # 18% 效率

    df['UV_norm'] = df['UV01'] / (df['UV01'].max() if df['UV01'].max() != 0 else 1)
    df['solar_kwh'] = df['SS01'] * panel_area * panel_efficiency * df['UV_norm']

    # 3. 存 analytics 層
    df.to_csv("data/analytics/weather_solar.csv", index=False)

if __name__ == "__main__":
    build_analytics()
