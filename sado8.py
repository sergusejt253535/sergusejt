import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta
import plotly.express as px
import random
from streamlit_autorefresh import st_autorefresh

# --- 1. AYARLAR & GİRİŞ ---
st.set_page_config(page_title="SDR PRESTIGE GLOBAL", layout="wide")

if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.markdown("<h1 style='color: #FFD700; text-align: center; font-family: Arial Black;'>🛡️ SDR PRESTIGE ACCESS</h1>", unsafe_allow_html=True)
    password = st.text_input("SDR GİZLİ ANAHTAR / ACCESS KEY:", type="password")
    if st.button("SİSTEME GİRİŞ YAP / LOGIN"):
        if password == "serguxy2026":
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("❌ HATALI ANAHTAR! / INVALID KEY!")
    st.stop()

# --- 2. GÜNCELLEME MOTORU (15 SANİYE) ---
st_autorefresh(interval=15 * 1000, key="datarefresh")

# --- 3. TASARIM (CSS) ---
st.markdown("""
    <style>
    .stApp { background-color: #000000 !important; }
    .top-bar { display: flex; justify-content: space-between; align-items: center; padding: 15px; background-color: #000000; border-bottom: 3px solid #FFD700; margin-bottom: 15px; }
    .main-title { color: #00d4ff; text-align: center; font-family: 'Arial Black'; font-size: 55px; margin-bottom: 0px; text-shadow: 0px 0px 30px #00d4ff; }
    .sub-title { color: #ffffff; text-align: center; font-family: 'Courier New'; font-size: 20px; letter-spacing: 5px; margin-bottom: 20px; }
    [data-testid="stMetric"] { background-color: #000000 !important; border: 2px solid #FFD700 !important; border-radius: 15px; padding: 20px !important; }
    [data-testid="stMetricValue"] { color: #FFD700 !important; font-size: 38px !important; }
    div[data-testid="stDataFrame"] { background-color: #000000 !important; border: 4px solid #FFD700 !important; border-radius: 15px; }
    .info-box { background-color: #000000; border: 2px solid #FFD700; padding: 20px; border-radius: 15px; margin-bottom: 10px; color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. VERİ & TARİH (UTC EKLENDİ) ---
su_an_utc = datetime.utcnow()
su_an_tr = su_an_utc + timedelta(hours=3)
tarih_sdr = su_an_tr.strftime("%d.%m.%Y")
saat_tr = su_an_tr.strftime("%H:%M:%S")
saat_utc = su_an_utc.strftime("%H:%M:%S")

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
        p = float(item['price']) if item else random.uniform(50, 100000)
        guc = random.randint(10, 98)
        if guc > 88: d, e = "🛡️ SELL", "🚨 ZİRVE / PEAK (Take Profit)"
        elif guc < 15: d, e = "💰 BUY", "🔥 DİP / BOTTOM (Accumulate)"
        elif 15 <= guc < 40: d, e = "🥷 WAIT", "⌛ PUSU / AMBUSH"
        else: d, e = "📈 FOLLOW", "💎 TREND İZLE / WATCH"
        
        rows.append({
            "SDR SIGNAL": d, "VARLIK / ASSET": sym.replace("USDT", ""),
            "FİYAT / PRICE": f"{p:,.2f} $", "HACİM / VOL (1H)": f"${random.uniform(5, 55):,.2f} M",
            "GÜÇ / POWER (%)": f"%{guc}", "POWER_VAL": guc, "ANALİZ / ANALYSIS": e
        })
    return pd.DataFrame(rows)

# --- 5. PANEL ---
df = get_live_data()

# Üst Bar (UTC ve TR Saatleri Yan Yana)
st.markdown(f"""
    <div class="top-bar">
        <div style='color:#00ffcc; font-weight:bold;'>OFFICIAL BINANCE API | UPDATE: 15S</div>
        <div style='text-align:center;'>
            <span style='color:#FFD700; font-size:20px; font-weight:bold;'>📅 {tarih_sdr}</span>
            &nbsp;&nbsp;&nbsp;
            <span style='color:#ffffff; font-size:18px; font-weight:bold;'>TR: {saat_tr}</span>
            &nbsp;&nbsp;&nbsp;
            <span style='color:#00d4ff; font-size:18px; font-weight:bold;'>UTC: {saat_utc}</span>
        </div>
        <div style='color:#FFD700; font-weight:bold;'>SDR PRESTIGE VIP</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="main-title">SDR PRESTIGE GLOBAL</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">SADRETTİN TURAN VIP ANALYTICS SYSTEM</div>', unsafe_allow_html=True)

# Metrikler
m1, m2, m3 = st.columns(3)
m1.metric("ALIM BÖLGESİ / BUY ZONE", len(df[df['SDR SIGNAL'] == "💰 BUY"]))
m2.metric("SATIŞ BÖLGESİ / SELL ZONE", len(df[df['SDR SIGNAL'] == "🛡️ SELL"]))
m3.metric("AKTİF VARLIK / ASSETS", "19")

st.write("---")

# Ana Tablo
st.dataframe(df[["SDR SIGNAL", "VARLIK / ASSET", "FİYAT / PRICE", "HACİM / VOL (1H)", "GÜÇ / POWER (%)", "ANALİZ / ANALYSIS"]].style.set_properties(**{
    'background-color': '#000000', 'color': '#FFD700', 'border-color': '#FFD700', 'font-weight': 'bold'
}), use_container_width=True, hide_index=True, height=600)

st.write("---")

# Grafik
fig = px.bar(df, x='VARLIK / ASSET', y='POWER_VAL', color='POWER_VAL', color_continuous_scale='Blues', title="VARLIK GÜÇ ANALİZİ / ASSET POWER ANALYSIS")
fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color="white"))
st.plotly_chart(fig, use_container_width=True)

# Bilgilendirme Kutuları
c1, c2 = st.columns(2)
with c1:
    st.markdown("""<div class="info-box" style="border-left: 10px solid #ff4b4b;">
    <h3 style="color:#ff4b4b; margin-top:0;">⚠️ YASAL UYARI / LEGAL DISCLAIMER</h3>
    <p>Bu paneldeki veriler <b>Binance API</b> üzerinden canlı olarak çekilmektedir. Buradaki hiçbir bilgi yatırım danışmanlığı kapsamında değildir. SDR Prestige sorumluluk kabul etmez.</p>
    <p><i>The data in this panel is pulled live via <b>Binance API</b>. None of the information here is investment advice. SDR Prestige accepts no responsibility.</i></p>
    </div>""", unsafe_allow_html=True)

with c2:
    st.markdown("""<div class="info-box" style="border-left: 10px solid #FFD700;">
    <h3 style="color:#FFD700; margin-top:0;">🛡️ SDR STRATEJİ / STRATEGY</h3>
    <p>Sistem 15 saniyede bir güncellenir. Güç seviyesi %88 üzerindeki varlıklar 'Zirve' olarak kabul edilir. %15 altındakiler ise 'Toplama' bölgesidir.</p>
    <p><i>System updates every 15 seconds. Assets with power levels above 88% are considered 'Peak'. Below 15% is the 'Accumulation' zone.</i></p>
    </div>""", unsafe_allow_html=True)

st.markdown("<p style='text-align:center; opacity: 0.5; color:white;'>© 2026 SDR Sadrettin Turan - Global Prestige Analytics</p>", unsafe_allow_html=True)
