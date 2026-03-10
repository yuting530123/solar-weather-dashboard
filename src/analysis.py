import pandas as pd

taipei = pd.read_csv("data/processed/taipei_clean.csv")
taichung = pd.read_csv("data/processed/taichung_clean.csv")
kaohsiung = pd.read_csv("data/processed/kaohsiung_clean.csv")

taipei["city"] = "Taipei"
taichung["city"] = "Taichung"
kaohsiung["city"] = "Kaohsiung"

df = pd.concat([taipei, taichung, kaohsiung])

#城市總日照量分析
city_rank = df.groupby("city")["SS01"].mean().sort_values(ascending=False)
print(city_rank)

#城市/年份分析
city_year = df.groupby(["city","year"])["SS01"].mean()
print(city_year)

#城市/月份分析
df["month"] = df["yyyymm"].astype(str).str[4:6]
monthly = df.groupby("month")["SS01"].mean()
print(monthly)

# 城市 × 月份日照分析
city_month = df.groupby(["city","month"])["SS01"].mean()
print(city_month)