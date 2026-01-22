import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta
import random
import time
from streamlit_autorefresh import st_autorefresh

# --- 1. AYARLAR & 15 SANİYE GÜNCELLEME ---
st.set_page_config(page_title="SDR PRESTIGE GLOBAL", layout="wide")
st_autorefresh(interval=15 * 1000, key="datarefresh")

# --- 2. ZİYARETÇİ BOTU (100-200 ARASI) ---
if 'visit_count' not in st.session_state:
    st.session_state.visit_count = random.randint(100, 200)
st.session_state.visit_count += random.randint(1, 2)

# 1 Saatte bir hacim güncelleme simülasyonu
if 'hourly_vol' not in st.session_state or time.time() % 3600 < 15:
    st.session_state.hourly_vol = f"{random.uniform(1.2, 2.5):.2f}B $"

# --- 3. VERİ ÇEKME MOTORU (Bilingual) ---
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
                guc = random.randint(75, 99) 
                rows.append({
                    "SDR SİNYAL / SIGNAL": "📈 FOLLOW", 
                    "VARLIK / ASSET": item['symbol'].replace("USDT", ""),
                    "FİYAT / PRICE": f"{p:,.2f} $",
                    "GÜÇ / POWER (%)": f"%{guc}",
                    "DURUM / STATUS": "AKTİF / ACTIVE"
                })
            return pd.DataFrame(rows)
        return pd.DataFrame()
    except:
        return pd.DataFrame()

df = get_live_data()
su_an_tr = datetime.utcnow() + timedelta(hours=3)

# --- 4. CSS TASARIM ---
st.markdown("""
    <style>
    .stApp { background-color: #000000 !important; }
    .top-bar { display: flex; justify-content: space-between; padding: 15px; background-color: #000000; border-bottom: 3px solid #FFD700; }
    .main-title { color: #00d4ff; text-align: center; font-family: 'Arial Black'; font-size: 45px; text-shadow: 0px 0px 20px #00d4ff; margin-top:10px; }
    .sub-title { color: #ffffff; text-align: center; font-family: 'Courier New'; font-size: 18px; letter-spacing: 5px; }
    .metric-box { background: #111; border: 1px solid #FFD700; padding: 15px; border-radius: 10px; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- 5. ÜST PANEL (Bilingual) ---
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f"<div class='metric-box'><span style='color:gray;'>ZİYARETÇİ / VISITORS</span><br><span style='color:#00ffcc; font-size:20px;'>{st.session_state.visit_count}</span></div>", unsafe_allow_html=True)
with col2:
    st.markdown(f"<div class='metric-box'><span style='color:gray;'>SDR SAAT / TIME (TR)</span><br><span style='color:#FFD700; font-size:20px;'>{su_an_tr.strftime('%H:%M:%S')}</span></div>", unsafe_allow_html=True)
with col3:
    st.markdown(f"<div class='metric-box'><span style='color:gray;'>1S HACİM / 1H VOLUME</span><br><span style='color:#00d4ff; font-size:20px;'>{st.session_state.hourly_vol}</span></div>", unsafe_allow_html=True)

st.markdown('<div class="main-title">SDR PRESTIGE GLOBAL</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">SADRETTİN TURAN VIP ANALYTICS</div>', unsafe_allow_html=True)

# --- 6. UYARI VE TABLO (Bilingual) ---
st.info(f"🚀 SİSTEM AKTİF / SYSTEM ACTIVE: 15s Update | Binance API Live")

if not df.empty:
    st.dataframe(df, use_container_width=True, hide_index=True)
    st.success("✅ ANALİZ TAMAMLANDI / ANALYSIS COMPLETED")
else:
    st.error("⚠️ BAĞLANTI BEKLENİYOR / WAITING FOR CONNECTION...")

st.markdown("<p style='text-align:center; color:gray; margin-top:50px;'>© 2026 sdr sadrettin turan • Prestige Edition</p>", unsafe_allow_html=True)
