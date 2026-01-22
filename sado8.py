import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta
import random
from streamlit_autorefresh import st_autorefresh

# --- 1. AYARLAR ---
st.set_page_config(page_title="SDR PRESTIGE GLOBAL", layout="wide")

# --- 2. GÜNCELLEME MOTORU (20 Saniyede bir yeniler) ---
st_autorefresh(interval=20 * 1000, key="datarefresh")

# --- 3. VERİ ÇEKME MOTORU ---
def get_live_data():
    assets = ['BTCUSDT', 'ETHUSDT', 'SOLUSDT', 'AVAXUSDT', 'XRPUSDT', 'BNBUSDT', 'ADAUSDT', 'DOGEUSDT', 'DOTUSDT', 'LINKUSDT']
    try:
        r = requests.get("https://api.binance.com/api/v3/ticker/price", timeout=30)
        if r.status_code == 200:
            data = r.json()
            active = [i for i in data if i['symbol'] in assets]
            rows = []
            for item in active:
                p = float(item['price'])
                guc = random.randint(70, 99) 
                rows.append({
                    "SDR SİNYAL": "📈 FOLLOW", 
                    "VARLIK/ASSET": item['symbol'].replace("USDT", ""),
                    "FİYAT/PRICE": f"{p:,.2f} $",
                    "GÜÇ/POWER (%)": f"%{guc}",
                    "POWER_NUM": guc
                })
            return pd.DataFrame(rows), 0 
        return pd.DataFrame(), 0
    except:
        return pd.DataFrame(), 0

# Zamanı tanımlıyoruz
su_an_tr = datetime.utcnow() + timedelta(hours=3)

# --- 4. CSS TASARIM ---
st.markdown("""
    <style>
    .stApp { background-color: #000000 !important; }
    .top-bar { display: flex; justify-content: space-between; padding: 15px; background-color: #000000; border-bottom: 3px solid #FFD700; }
    .main-title { color: #00d4ff; text-align: center; font-family: 'Arial Black'; font-size: 50px; text-shadow: 0px 0px 20px #00d4ff; }
    .sub-title { color: #ffffff; text-align: center; font-family: 'Courier New'; font-size: 18px; letter-spacing: 5px; }
    </style>
    """, unsafe_allow_html=True)

# --- 5. EKRAN ÜST KISIM ---
st.markdown(f"""
    <div class="top-bar">
        <div style='color:#00ffcc;'>● SDR LIVE ACTIVE | {su_an_tr.strftime("%S")}s</div>
        <div style='color:#FFD700; font-weight:bold;'>SDR PRESTIGE GLOBAL</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="main-title">SDR PRESTIGE GLOBAL</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">SADRETTİN TURAN VIP ANALYTICS</div>', unsafe_allow_html=True)

# --- 6. TABLOYU ÇALIŞTIR ---
df, t_vol = get_live_data()

if not df.empty:
    st.dataframe(df, use_container_width=True, hide_index=True)
else:
    st.warning("Veriler şu an yükleniyor, lütfen bekleyin...")

st.markdown("<p style='text-align:center; color:gray;'>© 2026 sdr sadrettin turan</p>", unsafe_allow_html=True)
