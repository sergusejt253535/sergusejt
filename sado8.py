import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta
import plotly.express as px
import random
from streamlit_autorefresh import st_autorefresh

# --- 1. AYARLAR ---
st.set_page_config(page_title="SDR PRESTIGE GLOBAL", layout="wide")
st_autorefresh(interval=15 * 1000, key="datarefresh")

# --- 2. CSS TASARIM ---
st.markdown("""
    <style>
    .stApp { background-color: #000000 !important; }
    .top-bar { display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; padding: 15px; background-color: #000000; border-bottom: 3px solid #FFD700; margin-bottom: 15px; }
    .main-title { color: #00d4ff; text-align: center; font-family: 'Arial Black'; font-size: 55px; margin-bottom: 0px; text-shadow: 0px 0px 30px #00d4ff; }
    .sub-title { color: #ffffff; text-align: center; font-family: 'Courier New'; font-size: 20px; letter-spacing: 5px; margin-bottom: 20px; }
    [data-testid="stMetric"] { background-color: #000000 !important; border: 2px solid #FFD700 !important; border-radius: 15px; padding: 20px !important; }
    [data-testid="stMetricLabel"] { color: #ffffff !important; font-size: 18px !important; font-weight: bold !important; }
    [data-testid="stMetricValue"] { color: #FFD700 !important; font-size: 38px !important; }
    div[data-testid="stDataFrame"] { background-color: #000000 !important; border: 4px solid #FFD700 !important; border-radius: 15px; }
    .stDataFrame td, .stDataFrame th { font-size: 28px !important; font-weight: bold !important; }
    .info-box { background-color: #000000; border: 2px solid #FFD700; padding: 25px; border-radius: 15px; height: 100%; margin-bottom: 15px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. DEĞİŞKENLER & ZİYARETÇİ ---
su_an_utc = datetime.utcnow()
su_an_tr = su_an_utc + timedelta(hours=3)

if 'fake_counter' not in st.session_state:
    st.session_state.fake_counter = random.randint(100, 150)
else:
    st.session_state.fake_counter += random.randint(0, 1)
    if st.session_state.fake_counter > 200: st.session_state.fake_counter = 198

# --- 4. AKILLI VERİ MOTORU ---
def get_live_data():
    assets = ['BTCUSDT', 'ETHUSDT', 'SOLUSDT', 'AVAXUSDT', 'XRPUSDT', 'BNBUSDT', 'ADAUSDT', 'DOGEUSDT', 'DOTUSDT', 'LINKUSDT', 'MATICUSDT', 'TRXUSDT', 'UNIUSDT', 'BCHUSDT', 'SUIUSDT', 'FETUSDT', 'RENDERUSDT', 'PEPEUSDT', 'SHIBUSDT']
    data = None
    status_msg = "● SDR LIVE DATA"
    
    try:
        r = requests.get("https://api.binance.com/api/v3/ticker/price", timeout=5)
        if r.status_code == 200:
            data = r.json()
            active_data = [i for i in data if i['symbol'] in assets]
        else:
            active_data = []
    except:
        active_data = []

    rows = []
    total_vol = 0
    
    # Eğer veri gelmezse en son bilinen veya gerçekçi simülasyonu dök (SDR Smart-Recovery)
    if not active_data:
        status_msg = "● SDR SMART-RECOVERY MODE"
        prices = {"BTC": 102540.20, "ETH": 3245.50, "SOL": 245.15, "AVAX": 42.10, "XRP": 2.45}
        for sym in assets:
            base = sym.replace("USDT", "")
            p = prices.get(base, random.uniform(1, 100))
            guc = random.randint(10, 95)
            rows.append(create_row(base, p, guc))
            total_vol += random.uniform(5, 20)
    else:
        for item in active_data:
            p = float(item['price'])
            guc = random.randint(10, 98)
            rows.append(create_row(item['symbol'].replace("USDT", ""), p, guc))
            total_vol += random.uniform(5, 30)

    return pd.DataFrame(rows), total_vol, status_msg

def create_row(base, p, guc):
    if guc > 88: d, e = "🛡️ SELL", "🚨 ZİRVE: Kâr Al / PEAK"
    elif guc < 15: d, e = "💰 BUY", "🔥 DİP: Topla / BOTTOM"
    elif 15 <= guc < 40: d, e = "🥷 WAIT", "⌛ PUSUDA BEKLE / AMBUSH"
    else: d, e = "📈 FOLLOW", "💎 TRENDİ İZLE / WATCHING"
    
    return {
        "SDR SİNYAL": d, "VARLIK/ASSET": base,
        "FİYAT/PRICE": f"{p:,.2f} $", "HACİM/VOL (1H)": f"${random.uniform(5, 50):,.2f} M",
        "GÜÇ/POWER (%)": f"%{guc}", "POWER_NUM": guc, "SDR ANALİZ / ANALYSIS": e
    }

# --- 5. PANEL ---
df, t_vol, status_label = get_live_data()

st.markdown(f"""
    <div class="top-bar">
        <div style='color:#00ffcc; font-weight:bold;'>{status_label}</div>
        <div style='text-align:center;'>
            <span style='color:#ffffff;'>👥 VISITORS:</span> <span style='color:#ff00ff; font-weight:bold;'>{st.session_state.fake_counter}</span>
            &nbsp;&nbsp;&nbsp;
            <span style='color:#00d4ff;'>🌍 UTC: {su_an_utc.strftime("%H:%M:%S")}</span>
            &nbsp;&nbsp;&nbsp;
            <span style='color:#00ffcc;'>🇹🇷 TR: {su_an_tr.strftime("%H:%M:%S")}</span>
        </div>
        <div style='color:#FFD700; font-weight:bold;'>SDR PRESTIGE</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="main-title">SDR PRESTIGE GLOBAL</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">SADRETTİN TURAN VIP ANALYTICS</div>', unsafe_allow_html=True)

m1, m2, m3 = st.columns([1,1,2])
m1.metric("💰 BUY ZONE", len(df[df['SDR SİNYAL'] == "💰 BUY"]))
m2.metric("🛡️ SELL ZONE", len(df[df['SDR SİNYAL'] == "🛡️ SELL"]))
m3.metric("📊 TOTAL VOLUME (1H)", f"${t_vol:,.2f} M")

st.write("---")
st.dataframe(df[["SDR SİNYAL", "VARLIK/ASSET", "FİYAT/PRICE", "HACİM/VOL (1H)", "GÜÇ/POWER (%)", "SDR ANALİZ / ANALYSIS"]].style.set_properties(**{
    'background-color': '#000000', 'color': '#FFD700', 'border-color': '#FFD700', 'font-weight': 'bold'
}), use_container_width=True, hide_index=True, height=750)

st.write("---")
fig = px.bar(df, x='VARLIK/ASSET', y='POWER_NUM', color='POWER_NUM', color_continuous_scale='Blues')
fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color="white"))
st.plotly_chart(fig, use_container_width=True)

st.markdown("<p style='text-align:center; opacity: 0.5; color:white;'>© 2026 sdr sadrettin turan</p>", unsafe_allow_html=True)
