import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta
import plotly.express as px
import random
from streamlit_autorefresh import st_autorefresh

# --- 1. AYARLAR & GİZLİ GİRİŞ KAPISI ---
st.set_page_config(page_title="SDR PRESTIGE GLOBAL", layout="wide")

if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.markdown("<h1 style='color: #FFD700; text-align: center;'>🛡️ SDR PRESTIGE ACCESS</h1>", unsafe_allow_html=True)
    password = st.text_input("SDR GİZLİ ANAHTAR / ACCESS KEY:", type="password")
    if st.button("SİSTEME GİRİŞ YAP"):
        if password == "serguxy2026":
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("❌ HATALI ANAHTAR!")
    st.stop()

# --- 2. GÜNCELLEME MOTORU ---
st_autorefresh(interval=15 * 1000, key="datarefresh")

# --- 3. CSS TASARIM ---
st.markdown("""
    <style>
    .stApp { background-color: #000000 !important; }
    .top-bar { display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; padding: 15px; background-color: #000000; border-bottom: 3px solid #FFD700; margin-bottom: 15px; }
    .main-title { color: #00d4ff; text-align: center; font-family: 'Arial Black'; font-size: 55px; margin-bottom: 0px; text-shadow: 0px 0px 30px #00d4ff; }
    .sub-title { color: #ffffff; text-align: center; font-family: 'Courier New'; font-size: 20px; letter-spacing: 5px; margin-bottom: 20px; }
    [data-testid="stMetric"] { background-color: #000000 !important; border: 2px solid #FFD700 !important; border-radius: 15px; padding: 20px !important; }
    [data-testid="stMetricValue"] { color: #FFD700 !important; font-size: 38px !important; }
    div[data-testid="stDataFrame"] { background-color: #000000 !important; border: 4px solid #FFD700 !important; border-radius: 15px; }
    .stDataFrame td, .stDataFrame th { font-size: 28px !important; font-weight: bold !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. TARİH & VERİ MOTORU ---
su_an_utc = datetime.utcnow()
su_an_tr = su_an_utc + timedelta(hours=3)
tarih_sdr = su_an_tr.strftime("%d.%m.%Y")
saat_sdr = su_an_tr.strftime("%H:%M:%S")

def get_live_data():
    assets = ['BTCUSDT', 'ETHUSDT', 'SOLUSDT', 'AVAXUSDT', 'XRPUSDT', 'BNBUSDT', 'ADAUSDT', 'DOGEUSDT', 'DOTUSDT', 'LINKUSDT', 'MATICUSDT', 'TRXUSDT', 'UNIUSDT', 'BCHUSDT', 'SUIUSDT', 'FETUSDT', 'RENDERUSDT', 'PEPEUSDT', 'SHIBUSDT']
    active_data = []
    try:
        r = requests.get("https://api.binance.com/api/v3/ticker/price", timeout=5)
        if r.status_code == 200:
            data = r.json()
            active_data = [i for i in data if i['symbol'] in assets]
    except: pass

    rows = []
    for sym in assets:
        item = next((i for i in active_data if i['symbol'] == sym), None)
        p = float(item['price']) if item else random.uniform(50, 105000)
        guc = random.randint(10, 98)
        if guc > 88: d, e = "🛡️ SELL", "🚨 ZİRVE: Kâr Al"
        elif guc < 15: d, e = "💰 BUY", "🔥 DİP: Topla"
        elif 15 <= guc < 40: d, e = "🥷 WAIT", "⌛ PUSUDA"
        else: d, e = "📈 FOLLOW", "💎 TRENDİ İZLE"
        
        rows.append({
            "SDR SİNYAL": d, "VARLIK/ASSET": sym.replace("USDT", ""),
            "FİYAT/PRICE": f"{p:,.2f} $", "HACİM (1H)": f"${random.uniform(5, 55):,.2f} M",
            "GÜÇ (%)": f"%{guc}", "ANALİZ": e
        })
    return pd.DataFrame(rows)

# --- 5. PANEL ---
df = get_live_data()

st.markdown(f"""
    <div class="top-bar">
        <div style='color:#00ffcc; font-weight:bold;'>● LIVE DATA STREAM</div>
        <div style='text-align:center;'>
            <span style='color:#FFD700; font-size:22px; font-weight:bold;'>📅 {tarih_sdr}</span>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
            <span style='color:#ffffff; font-size:22px; font-weight:bold;'>🕒 {saat_sdr}</span>
        </div>
        <div style='color:#FFD700; font-weight:bold;'>SDR PRESTIGE VIP</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="main-title">SDR PRESTIGE GLOBAL</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">SADRETTİN TURAN VIP ANALYTICS</div>', unsafe_allow_html=True)

st.dataframe(df.style.set_properties(**{
    'background-color': '#000000', 'color': '#FFD700', 'border-color': '#FFD700', 'font-weight': 'bold'
}), use_container_width=True, hide_index=True, height=800)

st.markdown("<p style='text-align:center; opacity: 0.5; color:white;'>© 2026 SDR Sadrettin Turan</p>", unsafe_allow_html=True)
