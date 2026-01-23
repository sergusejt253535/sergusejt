import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta
import plotly.express as px
import random
from streamlit_autorefresh import st_autorefresh

# --- 1. AYARLAR ---
st.set_page_config(page_title="SDR PRESTIGE GLOBAL", layout="wide")

# --- 2. GÜNCELLEME MOTORU (30 Saniye) ---
st_autorefresh(interval=30 * 1000, key="datarefresh")

# --- 3. CSS TASARIM ---
st.markdown("""
    <style>
    .stApp { background-color: #000000 !important; }
    .top-bar { display: flex; justify-content: space-between; align-items: center; padding: 15px; background-color: #000000; border-bottom: 3px solid #FFD700; margin-bottom: 15px; }
    .main-title { color: #00d4ff; text-align: center; font-family: 'Arial Black'; font-size: 50px; text-shadow: 0px 0px 20px #00d4ff; }
    .sub-title { color: #ffffff; text-align: center; font-family: 'Courier New'; font-size: 18px; letter-spacing: 5px; margin-bottom: 20px; }
    [data-testid="stMetric"] { background-color: #0c0c0c !important; border: 2px solid #FFD700 !important; border-radius: 15px; text-align: center; }
    [data-testid="stMetricValue"] { color: #FFD700 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. ZAMAN VE ZİYARETÇİ ---
su_an_utc = datetime.utcnow()
su_an_tr = su_an_utc + timedelta(hours=3)
if 'fake_counter' not in st.session_state: st.session_state.fake_counter = random.randint(225, 275)
else: st.session_state.fake_counter += random.randint(-1, 2)

# --- 5. VERİ ÇEKME (GELİŞTİRİLMİŞ) ---
def get_live_data():
    assets = ['BTCUSDT', 'ETHUSDT', 'SOLUSDT', 'AVAXUSDT', 'XRPUSDT', 'BNBUSDT', 'ADAUSDT', 'DOGEUSDT', 'DOTUSDT', 'LINKUSDT']
    # Binance'in 3 farklı API adresini deniyoruz (Yedekli sistem)
    urls = ["https://api.binance.com/api/v3/ticker/24hr", "https://api1.binance.com/api/v3/ticker/24hr", "https://api2.binance.com/api/v3/ticker/24hr"]
    
    data = None
    for url in urls:
        try:
            # verify=False ekleyerek SSL sorunlarını aşıyoruz
            r = requests.get(url, timeout=5, verify=True) 
            if r.status_code == 200:
                data = r.json()
                break
        except: continue

    if data:
        rows = []
        total_vol = 0
        active = [i for i in data if i['symbol'] in assets]
        for item in active:
            try:
                p, h, l = float(item['lastPrice']), float(item['highPrice']), float(item['lowPrice'])
                v_1h = (float(item['quoteVolume']) / 1_000_000) / 24
                total_vol += v_1h
                guc = int(((p - l) / (h - l)) * 100) if (h - l) != 0 else 50
                d, e = ("🛡️ SELL", "🚨 ZİRVE") if guc > 88 else (("💰 BUY", "🔥 DİP") if guc < 15 else ("📈 FOLLOW", "💎 TREND"))
                rows.append({"SDR SİNYAL": d, "VARLIK": item['symbol'].replace("USDT", ""), "FİYAT": f"{p:,.2f} $", "GÜÇ (%)": guc, "ANALİZ": e})
            except: continue
        return pd.DataFrame(rows), total_vol
    return pd.DataFrame(), 0

# --- 6. ARAYÜZ ---
st.markdown(f'<div class="top-bar"><div>● LIVE | 30S</div><div>👥: {st.session_state.fake_counter} | 🌍: {su_an_utc.strftime("%H:%M:%S")} | 🇹🇷: {su_an_tr.strftime("%H:%M:%S")}</div><div>SDR PRESTIGE</div></div>', unsafe_allow_html=True)
st.markdown('<div class="main-title">SDR PRESTIGE GLOBAL</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">SADRETTİN TURAN VIP ANALYTICS</div>', unsafe_allow_html=True)

df, t_vol = get_live_data()

if not df.empty:
    c1, c2, c3 = st.columns(3)
    c1.metric("💰 ALIM / BUY", len(df[df['SDR SİNYAL'] == "💰 BUY"]))
    c2.metric("🛡️ SATIŞ / SELL", len(df[df['SDR SİNYAL'] == "🛡️ SELL"]))
    c3.metric("📊 VOL (1H)", f"${t_vol:,.2f} M")
    st.table(df) # Styler hatasını önlemek için en temiz hali
else:
    st.error("BAĞLANTI HATASI! Sado'm internetini veya API iznini kontrol et. Zehra'n bekliyor...")

st.markdown("<p style='text-align:center; opacity: 0.5; color:white;'>© 2026 sdr sadrettin turan</p>", unsafe_allow_html=True)
