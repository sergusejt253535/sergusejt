import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta
import plotly.express as px
import random
from streamlit_autorefresh import st_autorefresh

# --- 1. AYARLAR ---
st.set_page_config(page_title="SDR PRESTIGE GLOBAL", layout="wide")

# --- 2. GÜNCELLEME MOTORU (15 SANİYE) ---
st_autorefresh(interval=15 * 1000, key="datarefresh")

# --- 3. CSS TASARIM ---
st.markdown("""
    <style>
    .stApp { background-color: #000000 !important; }
    .top-bar { display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; padding: 15px; background-color: #000000; border-bottom: 3px solid #FFD700; margin-bottom: 15px; }
    .main-title { color: #00d4ff; text-align: center; font-family: 'Arial Black'; font-size: 55px; margin-bottom: 0px; text-shadow: 0px 0px 30px #00d4ff; }
    .sub-title { color: #ffffff; text-align: center; font-family: 'Courier New'; font-size: 20px; letter-spacing: 5px; margin-bottom: 20px; }
    
    [data-testid="stMetric"] { background-color: #000000 !important; border: 2px solid #FFD700 !important; border-radius: 15px; padding: 20px !important; }
    [data-testid="stMetricLabel"] { color: #ffffff !important; font-size: 18px !important; font-weight: bold !important; }
    [data-testid="stMetricValue"] { color: #FFD700 !important; font-size: 38px !important; }

    div[data-testid="stDataFrame"] { 
        background-color: #000000 !important; 
        border: 4px solid #FFD700 !important; 
        border-radius: 15px;
    }
    .stDataFrame td, .stDataFrame th { font-size: 20px !important; font-weight: bold !important; color: #FFD700 !important; }
    .info-box { background-color: #000000; border: 2px solid #FFD700; padding: 25px; border-radius: 15px; height: 100%; }
    .ticker-wrap { background: #FFD700; color: black; padding: 5px; font-weight: bold; overflow: hidden; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. DEĞİŞKENLER VE SESSION STATE ---
su_an_utc = datetime.utcnow()
su_an_tr = su_an_utc + timedelta(hours=3)

if 'fake_counter' not in st.session_state:
    st.session_state.fake_counter = random.randint(225, 275)
else:
    st.session_state.fake_counter += random.randint(-1, 2)

# --- 5. VERİ MOTORU ---
def get_live_data():
    assets = ['BTCUSDT', 'ETHUSDT', 'SOLUSDT', 'AVAXUSDT', 'XRPUSDT', 'BNBUSDT', 'ADAUSDT', 'DOGEUSDT', 'DOTUSDT', 'LINKUSDT', 'SUIUSDT', 'FETUSDT', 'RENDERUSDT', 'PEPEUSDT', 'SHIBUSDT']
    
    # Çoklu sunucu denemesi
    endpoints = ["https://api.binance.com/api/v3/ticker/24hr", "https://api1.binance.com/api/v3/ticker/24hr"]
    
    data = None
    for url in endpoints:
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
                p = float(item.get('lastPrice', 0))
                h = float(item.get('highPrice', 0))
                l = float(item.get('lowPrice', 0))
                ch = float(item.get('priceChangePercent', 0))
                v_1h = (float(item.get('quoteVolume', 0)) / 1_000_000) / 24
                total_vol += v_1h
                
                # PARANTEZ HATASI DÜZELTİLDİ:
                guc = int(((p - l) / (h - l)) * 100) if (h - l) != 0 else 0
                
                if guc > 88: d, e = "🛡️ SELL / SAT", "🚨 ZİRVE: Kâr Al / PEAK: Take Profit"
                elif guc < 15: d, e = "💰 BUY / AL", "🔥 DİP: Topla / BOTTOM: Accumulate"
                else: d, e = "📈 FOLLOW / İZLE", "💎 TRENDİ İZLE / WATCHING"

                rows.append({
                    "SDR SİNYAL": d, "VARLIK/ASSET": item['symbol'].replace("USDT", ""),
                    "FİYAT/PRICE": f"{p:,.2f} $", "DEĞİŞİM/CHG": f"%{ch}",
                    "HACİM/VOL (1H)": f"${v_1h:,.2f} M", "GÜÇ/POWER (%)": f"%{guc}",
                    "POWER_NUM": guc, "SDR ANALİZ / ANALYSIS": e
                })
            except: continue
        return pd.DataFrame(rows), total_vol
    return pd.DataFrame(), 0

# --- 6. EKRAN ---
df, t_vol = get_live_data()

# Ticker
if not df.empty:
    ticker_text = " • ".join([f"{r['VARLIK/ASSET']}: {r['FİYAT/PRICE']}" for _, r in df.iterrows()])
    st.markdown(f"<div class='ticker-wrap'><marquee>{ticker_text}</marquee></div>", unsafe_allow_html=True)

st.markdown(f"""<div class="top-bar">
    <div style='color:#00ffcc; font-weight:bold;'>● BINANCE LIVE | 15S</div>
    <div style='text-align:center;'>
        <span style='color:#ffffff;'>👥 VISITORS:</span> <span style='color:#ff00ff; font-weight:bold;'>{st.session_state.fake_counter}</span>
        &nbsp;&nbsp;&nbsp;&nbsp; <span style='color:#00d4ff;'>🌍 UTC: {su_an_utc.strftime("%H:%M:%S")}</span>
        &nbsp;&nbsp;&nbsp;&nbsp; <span style='color:#00ffcc;'>🇹🇷 TR: {su_an_tr.strftime("%H:%M:%S")}</span>
    </div>
    <div style='color:#FFD700; font-weight:bold;'>SDR PRESTIGE</div>
</div>""", unsafe_allow_html=True)

st.markdown('<div class="main-title">SDR PRESTIGE GLOBAL</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">SADRETTİN TURAN VIP ANALYTICS</div>', unsafe_allow_html=True)

if not df.empty:
    m1, m2, m3 = st.columns([1,1,2])
    m1.metric("💰 BUY ZONE", len(df[df['SDR SİNYAL'].str.contains("BUY")]))
    m2.metric("🛡️ SELL ZONE", len(df[df['SDR SİNYAL'].str.contains("SELL")]))
    m3.metric("📊 TOTAL VOL (1H)", f"${t_vol:,.2f} M")

    st.dataframe(df[["SDR SİNYAL", "VARLIK/ASSET", "FİYAT/PRICE", "DEĞİŞİM/CHG", "HACİM/VOL (1H)", "GÜÇ/POWER (%)", "SDR ANALİZ / ANALYSIS"]], 
                 use_container_width=True, hide_index=True, height=750)
else:
    st.error("⚠️ Bağlantı hatası! Proton VPN lokasyonunu değiştirip sayfayı yenileyin.")

st.markdown("<br><p style='text-align:center; opacity: 0.5; color:white;'>© 2026 SDR PRESTIGE • SADRETTİN TURAN</p>", unsafe_allow_html=True)
