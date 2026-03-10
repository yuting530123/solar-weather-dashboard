import pandas as pd
station_map = {
    466920: "Taipei",   # 北部
    467490: "Taichung", # 中部
    467441: "Kaohsiung"    # 南部
}
#台北
def transform_taipei():
    # 讀 raw 資料
    df = pd.read_csv("data/raw/taipei_raw.csv")
    df["yyyymm"] = df["yyyymm"].astype(str)  # 字串
    df["year"] = df["yyyymm"].str[:4].astype(int)  # ✓ 正確，取前4個字元
    df["city"] = df["stno"].map(station_map)

    df.to_csv("data/processed/taipei_clean.csv", index=False)

if __name__ == "__main__":
    transform_taipei()

#台中
def transform_taichung():
    # 讀 raw 資料
    df = pd.read_csv("data/raw/taichung_raw.csv")
    df["yyyymm"] = df["yyyymm"].astype(str)  # 字串
    df["year"] = df["yyyymm"].str[:4].astype(int)  # ✓ 正確，取前4個字元
    df["city"] = df["stno"].map(station_map)
    df.to_csv("data/processed/taichung_clean.csv", index=False)

if __name__ == "__main__":
    transform_taichung()


#高雄
def transform_kaohsiung():
    # 讀 raw 資料
    df = pd.read_csv("data/raw/kaohsiung_raw.csv")
    df["yyyymm"] = df["yyyymm"].astype(str)  # 字串
    df["year"] = df["yyyymm"].str[:4].astype(int)  # ✓ 正確，取前4個字元
    df["city"] = df["stno"].map(station_map)
    df.to_csv("data/processed/kaohsiung_clean.csv", index=False)

if __name__ == "__main__":
    transform_kaohsiung()