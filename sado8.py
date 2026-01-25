import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta
import plotly.express as px
from streamlit_autorefresh import st_autorefresh

# --- 1. AYARLAR (İLK SIRADA OLMALI) ---
st.set_page_config(page_title="SDR PRESTIGE GLOBAL VIP", layout="wide")

# --- 2. GÜNCELLEME MOTORU (30 SANİYEDE BİR TAZELEME) ---
st_autorefresh(interval=30 * 1000, key="datarefresh")

# --- 3. ÖZEL CSS TASARIMI (VIP DOKUNUŞ) ---
st.markdown("""
    <style>
    /* Ana Arka Plan */
    .stApp { background-color: #000000 !important; }
    
    /* Başlık ve Alt Başlık */
    .main-title { color: #00d4ff; text-align: center; font-family: 'Arial Black'; font-size: 50px; text-shadow: 0px 0px 25px #00d4ff; margin-bottom: 5px; }
    .sub-title { color: #ffffff; text-align: center; font-family: 'Courier New'; font-size: 18px; letter-spacing: 4px; margin-bottom: 30px; border-bottom: 2px solid #FFD700; padding-bottom: 10px; }
    
    /* Kart (Metric) Tasarımları */
    [data-testid="stMetric"] {
        background-color: #0a0a0a !important;
        border: 1px solid #FFD700 !important;
        border-radius: 12px;
        padding: 15px !important;
        box-shadow: 0px 4px 15px rgba(255, 215, 0, 0.1);
    }
    [data-testid="stMetricLabel"] { color: #ffffff !important; font-size: 16px !important; }
    [data-testid="stMetricValue"] { color: #FFD700 !important; font-size: 32px !important; }

    /* Tablo Tasarımı */
    div[data-testid="stDataFrame"] {
        border: 2px solid #FFD700 !important;
        border-radius: 10px;
        background-color: #000000 !important;
    }
    
    /* Yan Menü (Sidebar) */
    .css-1d391kg { background-color: #050505 !important; }
    
    /* Bilgi Kutuları */
    .info-box {
        background-color: #0a0a0a;
        border-left: 5px solid #FFD700;
        padding: 15px;
        border-radius: 5px;
        margin-top: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. YAN MENÜ (VIP PANEL & STRATEJİ) ---
with st.sidebar:
    st.markdown("<h2 style='color:#FFD700; text-align:center;'>👑 SDR VIP</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Pazarlama Adımı: 3 Günlük Ücretsiz Deneme Uyarısı
    st.info("🎁 DURUM: 3 Günlük Ücretsiz Deneme Süreniz Aktif!")
    
    st.markdown("### 🛡️ SDR STRATEJİ REHBERİ")
    st.markdown("""
    <div class='info-box'>
        <b style='color:#00ffcc;'>%0 - %15:</b> <span style='color:white;'>DİP (Mal Topla)</span><br>
        <b style='color:#FFD700;'>%15 - %40:</b> <span style='color:white;'>PUSU (Beklemede Kal)</span><br>
        <b style='color:#00d4ff;'>%40 - %88:</b> <span style='color:white;'>TREND (İzlemeye Devam)</span><br>
        <b style='color:#ff4b4b;'>%88 - %100:</b> <span style='color:white;'>ZİRVE (Kâr Al/Sat)</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("#### 💬 VIP ERİŞİM & SATIN ALMA")
    st.write("Süreniz dolduğunda veya özel analizler için bizimle iletişime geçin.")
    # Not: Buradaki linke kendi WP grubunun veya numaranın linkini koyabiliriz Sado'm.
    st.link_button("📱 WHATSAPP VIP HATTI", "https://wa.me/numaraniz")

# --- 5. VERİ ÇEKME FONKSİYONU ---
def get_live_data():
    assets = ['BTCUSDT', 'ETHUSDT', 'SOLUSDT', 'AVAXUSDT', 'XRPUSDT', 'BNBUSDT', 'ADAUSDT', 'DOGEUSDT', 'DOTUSDT', 'LINKUSDT', 'SUIUSDT', 'FETUSDT', 'PEPEUSDT']
    try:
        r = requests.get("https://api.binance.com/api/v3/ticker/24hr", timeout=10)
        data = r.json()
        active = [i for i in data if i['symbol'] in assets]
        rows = []
        total_vol = 0
        for item in active:
            try:
                p = float(item.get('lastPrice', 0))
                h = float(item.get('highPrice', 0))
                l = float(item.get('lowPrice', 0))
                v_1h = (float(item.get('quoteVolume', 0)) / 1_000_000) / 24
                total_vol += v_1h
                guc = int(((p - l) / (h - l)) * 100) if (h - l) != 0 else 0
                
                if guc > 88: s, a = "🛡️ SELL", "🚨 KÂR ALMA ZAMANI"
                elif guc < 15: s, a = "💰 BUY", "🔥 KADEMELİ TOPLA"
                elif 15 <= guc < 40: s, a = "⌛ WAIT", "💤 GÜÇ TOPLANIYOR"
                else:
