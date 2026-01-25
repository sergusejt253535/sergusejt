import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta
import plotly.express as px
import random
from streamlit_autorefresh import st_autorefresh

# --- 1. AYARLAR (FULL SCREEN MODU) ---
st.set_page_config(page_title="SDR PRESTIGE GLOBAL | VIP", layout="wide", initial_sidebar_state="collapsed")

# --- 2. 15 SANİYELİK GÜNCELLEME MOTORU ---
st_autorefresh(interval=15 * 1000, key="datarefresh")

# --- 3. SDR ÖZEL SİBER TASARIM (EN GENİŞ HALİ) ---
st.markdown("""
    <style>
    .stApp { background-color: #000000 !important; }
    .top-bar { display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; padding: 10px 20px; background-color: #000000; border-bottom: 2px solid #FFD700; margin-bottom: 10px; }
    .main-title { color: #00d4ff; text-align: center; font-family: 'Arial Black'; font-size: 60px; margin-bottom: 0px; text-shadow: 0px 0px 30px #00d4ff; }
    .sub-title { color: #ffffff; text-align: center; font-family: 'Courier New'; font-size: 22px; letter-spacing: 7px; margin-bottom: 20px; text-transform: uppercase; }
    
    /* METRİK KARTLARI */
    [data-testid="stMetric"] {
        background-color: #050505 !important;
        border: 2px solid #FFD700 !important;
        border-radius: 12px;
        padding: 15px !important;
        box-shadow: 0px 0px 10px rgba(255, 215, 0, 0.1);
    }
    [data-testid="stMetricLabel"] { color: #ffffff !important; font-size: 16px !important; }
    [data-testid="stMetricValue"] { color: #FFD700 !important; font-size: 32px !important; }

    /* DEV TABLO TASARIMI */
    div[data-testid="stDataFrame"] { 
        background-color: #000000 !important; 
        border: 3px solid #FFD700 !important; 
        border-radius: 15px;
        padding: 10px;
    }
    .stDataFrame td, .stDataFrame th { font-size: 22px !important; font-weight: bold !important; color: #FFD700 !important; }
    
    /* BİLGİ KUTULARI */
    .info-box { background-color: #0a0a0a; border: 1px solid #FFD700; padding: 20px; border-radius: 12px; height: 100%; }
    .ticker-wrap { background: #FFD700; color: black; padding: 5px; font-weight: bold; font-family: monospace; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. ZAMAN VE ZİYARETÇİ AYARLARI ---
su_an_utc = datetime.utcnow()
su_an_tr = su_an_utc + timedelta(hours=3)

if 'fake_counter' not in st.session_state:
    st.session_state.fake_counter = random.randint(310, 390)
else:
    st.session_state.fake_counter += random.randint(-2, 3)

# --- 5. İNATÇI BİNANCE VERİ MOTORU ---
def get_sdr_master_data():
    # En geniş altcoin listesi
    assets = [
        'BTCUSDT', 'ETHUSDT', 'SOLUSDT', 'AVAXUSDT', 'XRPUSDT', 'BNBUSDT', 'ADAUSDT', 
        'DOGEUSDT', 'DOTUSDT', 'LINKUSDT', 'SUIUSDT', 'FETUSDT', 'RENDERUSDT', 'PEPEUSDT', 
        'SHIBUSDT', 'NEARUSDT', 'OPUSDT', 'ARBUSDT', 'TIAUSDT', 'LTCUSDT', 'BCHUSDT', 'APTUSDT'
    ]
    
    urls = [
        "https://api.binance.com/api/v3/ticker/24hr",
        "https://api1.binance.com/api/v3/ticker/24hr",
        "https://api2.binance.com/api/v3/ticker/24hr"
    ]
    
    data = None
    for url in urls:
        try:
            r = requests.get(url, timeout=5, headers={'User-Agent': 'Mozilla/5.0'})
            if r.status_code == 200:
                data = r.json()
                break
        except: continue
            
    if data:
        active = [i for i in data if i['symbol'] in assets]
        rows = []
        total_vol = 0
        for item in active:
            try:
                p, h, l = float(item['lastPrice']), float(item['highPrice']), float(item['lowPrice'])
                ch = float(item['priceChangePercent'])
                v_1h = (float(item['quoteVolume']) / 1_000_000) / 24
                total_vol += v_1h
                guc = int(((
