import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta
import random
from streamlit_autorefresh import st_autorefresh

# 1. AYARLAR
st.set_page_config(page_title="SDR PRESTIGE GLOBAL", layout="wide")
st_autorefresh(interval=15 * 1000, key="datarefresh")

# 2. SAATLER VE ZİYARETÇİ
tr_saati = datetime.utcnow() + timedelta(hours=3)
utc_saati = datetime.utcnow()

if 'visit_count' not in st.session_state:
    st.session_state.visit_count = random.randint(100, 200)
else:
    st.session_state.visit_count += 1

# 3. VERİ ÇEKME (EN BASİT YOL)
def get_data():
    assets = ['BTCUSDT', 'ETHUSDT', 'SOLUSDT', 'AVAXUSDT', 'XRPUSDT', 'BNBUSDT', 'ADAUSDT', 'DOGEUSDT', 'DOTUSDT', 'LINKUSDT']
    try:
        r = requests.get("https://api.binance.com/api/v3/ticker/price", timeout=10)
        data = r.json()
        rows = []
        for item in data:
            if item['symbol'] in assets:
                p = float(item['price'])
                guc = random.randint(75, 99)
                rows.append({
                    "SDR SİNYAL / SIGNAL": "📈 FOLLOW",
                    "VARLIK / ASSET": item['symbol'].replace("USDT", ""),
                    "FİYAT / PRICE": f"{p:,.2f} $",
                    "GÜÇ / POWER (%)": f"%{guc}"
                })
        return pd.DataFrame(rows)
    except:
        return pd.DataFrame()

df = get_data()

# 4. TASARIM
st.markdown("""
    <style>
    .stApp { background-color: #000000 !important; }
    .metric-box { background: #111; border: 1px solid #FFD700; padding: 10px; border-radius: 5px; text-align: center; color: white; }
    h1 { color: #00d4ff; text-align: center; font-family: 'Arial Black'; text-shadow: 0px 0px 10px #00d4ff; }
    </style>
    """, unsafe_allow_html=True)

# 5. EKRAN
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown(f"<div class='metric-box'>TR: {tr_saati.strftime('%H:%M:%S')}</div>", unsafe_allow_html=True)
with c2:
    st.markdown(f"<div class='metric-box'>UTC: {utc_saati.strftime('%H:%M:%S')}</div>", unsafe_allow_html=True)
with c3:
    st.markdown(f"<div class='metric-box'>VISITORS: {st.session_state.visit_count}</div>", unsafe_allow_html=True)

st.markdown("<h1>SDR PRESTIGE GLOBAL</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:white; letter-spacing:3px;'>SADRETTİN TURAN VIP ANALYTICS</p>", unsafe_allow_html=True)

if not df.empty:
    st.dataframe(df, use_container_width=True, hide_index=True)
else:
    st.info("⚠️ VERİLER YÜKLENİYOR / LOADING DATA...")

st.markdown("<p style='text-align:center; color:gray; font-size:10px;'>© 2026 sdr sadrettin turan</p>", unsafe_allow_html=True)
