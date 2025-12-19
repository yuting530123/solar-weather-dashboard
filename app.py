import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

# ==================== 1. 基本頁面設定 ====================
st.set_page_config(page_title="台中氣象分析儀表板", layout="wide")

# 中文字體設定
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei', 'SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

# ==================== 2. 資料讀取函數 ====================
@st.cache_data # 快取資料，提升效能
def load_data(file_path):
    if not os.path.exists(file_path):
        return None
    
    # 讀取 CSV
    df = pd.read_csv(file_path, skipinitialspace=True)
    
    # 資料清理：處理雨跡 (-9.8 視為 0)
    df['PP01'] = df['PP01'].replace(-9.8, 0.0)
    
    # 時間轉換
    df['date'] = pd.to_datetime(df['yyyymmdd'], format='%Y%m%d')
    df = df.sort_values('date').reset_index(drop=True)
    df['month'] = df['date'].dt.month
    
    # --- 太陽能發電潛力計算 ---
    panel_area = 10         # 10 平方公尺
    panel_efficiency = 0.18 # 18% 效率
    df['UV_norm'] = df['UV01'] / (df['UV01'].max() if df['UV01'].max() != 0 else 1)
    df['solar_kwh'] = df['SS01'] * 1.0 * panel_area * panel_efficiency * df['UV_norm']
    
    return df

# 載入資料
DATA_FILE = 'weather_data.csv'
df = load_data(DATA_FILE)

# ==================== 3. 側邊欄與標題 ====================
st.title("🌤️ 台中市 多要素分析儀表板")
st.markdown("---")

if df is None:
    st.error(f"找不到檔案 `{DATA_FILE}`，請確保檔案已上傳至正確目錄。")
    st.stop()

st.sidebar.header("⚙️ 分析與控制")
primary_key = st.sidebar.selectbox(
    "主要分析要素",
    ['TX01', 'PP01', 'SS01', 'UV01'],
    format_func=lambda x: {'TX01':'平均氣溫(℃)', 'PP01':'降水量(mm)', 'SS01':'日照時數(小時)', 'UV01':'紫外線指數'}[x]
)

secondary_key = st.sidebar.selectbox(
    "對比要素 (雙軸)",
    [None, 'TX01', 'PP01', 'SS01', 'UV01'],
    format_func=lambda x: '無' if x is None else {'TX01':'平均氣溫(℃)', 'PP01':'降水量(mm)', 'SS01':'日照時數(小時)', 'UV01':'紫外線指數'}[x]
)

window = st.sidebar.slider("移動平均趨勢（天數）", 1, 14, 7)

# ==================== 4. 關鍵指標 (Metrics) ====================
col_info = {
    'TX01':('平均氣溫','℃'), 'PP01':('降水量','mm'), 
    'SS01':('日照時數','小時'), 'UV01':('紫外線指數','')
}

name, unit = col_info[primary_key]
avg_val = df[primary_key].mean()
max_val = df[primary_key].max()
max_date = df.loc[df[primary_key].idxmax(), 'date'].strftime('%Y-%m-%d')

st.subheader(f"📊 {name} 核心統計")
m1, m2, m3 = st.columns(3)
m1.metric("期間平均值", f"{avg_val:.2f} {unit}")
m2.metric("最大觀測值", f"{max_val:.2f} {unit}")
m3.metric("發生日期", max_date)

# ==================== 5. 圖表視覺化 ====================
st.markdown("### 📈 每日變化趨勢")
fig, ax1 = plt.subplots(figsize=(10, 4))

# 主軸
ax1.plot(df['date'], df[primary_key], color='#3498db', alpha=0.4, label=f"{name}")
ax1.plot(df['date'], df[primary_key].rolling(window).mean(), color='#2980b9', linewidth=2, label=f"{window}日移動平均")
ax1.set_ylabel(f"{name} ({unit})")
ax1.grid(True, linestyle='--', alpha=0.5)

# 雙軸設定
if secondary_key:
    ax2 = ax1.twinx()
    s_name, s_unit = col_info[secondary_key]
    ax2.plot(df['date'], df[secondary_key], color='#e74c3c', alpha=0.4, label=s_name)
    ax2.set_ylabel(f"{s_name} ({s_unit})", color='#e74c3c')

fig.legend(loc='upper right', bbox_to_anchor=(1, 1), bbox_transform=ax1.transAxes)
st.pyplot(fig)

# ==================== 6. 月份對比區塊 ====================
st.markdown("---")
c_left, c_right = st.columns(2)

with c_left:
    st.subheader("📅 月份數據對比")
    compare_df = df.groupby('month')[primary_key].agg(['mean', 'max', 'sum']).rename(index={10: '10月', 11: '11月'})
    st.table(compare_df.style.format("{:.2f}"))

with c_right:
    st.subheader("☀️ 太陽能發電潛力 (kWh)")
    solar_df = df.groupby('month')['solar_kwh'].agg(['mean', 'sum']).rename(index={10: '10月', 11: '11月'})
    solar_df.columns = ['平均每日', '月總量']
    st.table(solar_df.style.format("{:.1f}"))

# ==================== 7. 原始資料 ====================
with st.expander("🔍 展開查看原始數據表"):
    st.dataframe(df[['date', 'TX01', 'PP01', 'SS01', 'UV01', 'solar_kwh']], use_container_width=True)