import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta
import random
from streamlit_autorefresh import st_autorefresh

# --- 1. AYARLAR & 15 SANİYE GÜNCELLEME ---
st.set_page_config(page_title="SDR PRESTIGE GLOBAL", layout="wide")
st_autorefresh(interval=15 * 1000, key="datarefresh")

# --- 2. ZİYARETÇİ BOTU (SADECE 100-200 ARASI) ---
if 'visit_count' not in st.session_state:
    st.session_state.visit_count = random.randint(100, 200)
else:
    # Her yenilemede abartmadan 1-2 kişi artsın
    st.session_state.visit_count += random.randint(0, 1)

# --- 3. VERİ ÇEKME MOTORU (Bilingual & Hızlı) ---
def get_live_data():
    assets = ['BTCUSDT', 'ETHUSDT', 'SOLUSDT', 'AVAXUSDT', 'XRPUSDT', 'BNBUSDT', 'ADAUSDT', 'DOGEUSDT', 'DOTUSDT', 'LINKUSDT']
    try:
        # Daha hızlı sonuç veren price API'sini kullanıyoruz
        r = requests.get("https://api.binance.com/api/v3/ticker/price", timeout=15)
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

# Verileri çek
df = get_live_data()
su_an_tr = datetime.utcnow() + timedelta(hours=3)

# --- 4. CSS TASARIM ---
st.markdown("""
    <style>
    .stApp { background-color: #000000 !important; }
    .top-bar { display: flex; justify-content: space-between; padding: 10px; background-color: #000000; border-bottom: 2px solid #FFD700; margin-bottom: 20px; }
    .main-title { color: #00d4ff; text-align: center; font-family: 'Arial Black'; font-size: 40px; text-shadow: 0px 0px 15px #00d4ff; }
    .sub-title { color: #ffffff; text-align: center; font-family: 'Courier New'; font-size: 16px; letter-spacing: 4px; margin-bottom: 20px; }
    .metric-box { background: #111; border: 1px solid #FFD700; padding: 10px; border-radius: 8px; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- 5. ÜST PANEL (Ziyaretçi 100-200 arası) ---
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f"<div class='metric-box'><span style='color:gray; font-size:12px;'>ZİYARETÇİ / VISITORS</span><br><span style='color:#00ffcc; font-size:18px;'>{st.session_state.visit_count}</span></div>", unsafe_allow_html=True)
with col2:
    st.markdown(f"<div class='metric-box'><span style='color:gray; font-size:12px;'>SDR SAAT / TIME (TR)</span><br><span style='color:#FFD700; font-size:18px;'>{su_an_tr.strftime('%H:%M:%S')}</span></div>", unsafe_allow_html=True)
with col3:
    st.markdown(f"<div class='metric-box'><span style='color:gray; font-size:12px;'>DURUM / STATUS</span><br><span style='color:#00d4ff; font-size:18px;'>ONLINE</span></div>", unsafe_allow_html=True)

st.markdown('<div class="main-title">SDR PRESTIGE GLOBAL</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">SADRETTİN TURAN VIP ANALYTICS</div>', unsafe_allow_html=True)

# --- 6. TABLO ALANI ---
if not df.empty:
    st.dataframe(df, use_container_width=True, hide_index=True)
    st.markdown(f"<div style='color:#00ff00; text-align:center; font-size:12px; margin-top:10px;'>✓ VERİLER GÜNCEL / DATA IS UP TO DATE</div>", unsafe_allow_html=True)
else:
    st.warning("⚠️ BAĞLANTI BEKLENİYOR / WAITING FOR CONNECTION... (Binance API)")

st.markdown("<p style='text-align:center; color:gray; margin-top:40px; font-size:10px;'>© 2026 sdr sadrettin turan • Prestige Edition</p>", unsafe_allow_html=True)
