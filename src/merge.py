import pandas as pd

#台北
df_2024 = pd.read_csv("taipei_2024.csv")
df_2025 = pd.read_csv("taipei_2025.csv")

df = pd.concat([df_2024, df_2025], ignore_index=True)

print(df.head())

df.to_csv("data/raw/taipei_raw.csv", index=False)

#台中
df_2024 = pd.read_csv("taichung_2024.csv")
df_2025 = pd.read_csv("taichung_2025.csv")

df = pd.concat([df_2024, df_2025], ignore_index=True)

print(df.head())

df.to_csv("data/raw/taichung_raw.csv", index=False)

#高雄
df_2024 = pd.read_csv("kaohsiung_2024.csv")
df_2025 = pd.read_csv("kaohsiung_2025.csv")

df = pd.concat([df_2024, df_2025], ignore_index=True)

print(df.head())

df.to_csv("data/raw/kaohsiung_raw.csv", index=False)

