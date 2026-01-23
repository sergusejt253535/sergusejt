import streamlit as st
import pandas as pd
import requests
import plotly.graph_objects as go
from datetime import datetime, timedelta
from streamlit_autorefresh import st_autorefresh

# --- 1. AYARLAR ---
st.set_page_config(page_title="SDR PRESTIGE GLOBAL | V.5.9", layout="wide")
st_autorefresh(interval=10 * 1000, key="sdr_forced_black_v59")

# --- 2. ÖZEL TASARIM (CSS) ---
st.markdown("""
    <style>
    .stApp { background-color: #000000 !important; }
    .top-bar { 
        display: flex; justify-content: space-between; align-items: center; 
        padding: 20px; border-bottom: 3px solid #00f2ff; 
        margin-bottom: 25px; background: #050505; 
    }
    .main-title { 
        color: #00f2ff; text-align: center; font-family: 'Impact'; 
        font-size: 65px; text-shadow: 0px 0px 30px #00f2ff; 
        margin-bottom: 0px;
    }
    .sub-title { 
        color: #FFD700; text-align: center; font-family: 'Courier New'; 
        font-size: 24px; letter-spacing: 8px; margin-bottom: 35px; 
        font-weight: bold; text-shadow: 0px 0px 10px #FFD700;
    }
    .live-indicator {
        color: #00ffcc; font-weight: bold; font-size: 15px;
        animation: blinker 1.5s linear infinite;
    }
    @keyframes blinker { 50% { opacity: 0; } }
    
    /* Tabloyu Siyaha Zorla */
    div[data-testid="stDataFrame"] { border: 2px solid #00f2ff !important; background-color: black !important; }
    .info-box { 
        background: #080808; border: 2px solid #00f2ff; 
        padding: 35px; border-radius: 20px; color: white; 
    }
    .license-text { color: #555; font-size: 12px; text-align: left; font-family: monospace; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. ZAMAN VE TARİH ---
utc_now = datetime.utcnow()
tr_now = utc_now + timedelta(hours=3)

st.markdown(f"""
    <div class="top-bar">
        <div class="live-indicator">📡 LIVE BINANCE STREAM ACTIVE (10s)</div>
        <div style='color:white; font-family:monospace; font-size:16px;'>
            📅 {tr_now.strftime("%d.%m.%Y")} | 
            🌐 <b>UTC:</b> {utc_now.strftime("%H:%M:%S")} | 
            🇹🇷 <b>TR:</b> {tr_now.strftime("%H:%M:%S")}
        </div>
        <div style='color:#00f2ff; font-weight:bold; font-size:20px; letter-spacing:3px;'>SDR PRESTIGE</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="main-title">SDR PRESTIGE GLOBAL</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">SADRETTİN TURAN VIP ANALYTICS</div>', unsafe_allow_html=True)

# --- 4. VERİ MOTORU ---
def get_sdr_data():
    assets = "BTC,ETH,SOL,AVAX,XRP,BNB,ADA,DOGE,LINK,SUI,PEPE,FET,RENDER,MATIC"
    url = f"https://min-api.cryptocompare.com/data/pricemultifull?fsyms={assets}&tsyms=USD"
    rows = []
    try:
        r = requests.get(url, timeout=10).json()['RAW']
        for coin in r:
