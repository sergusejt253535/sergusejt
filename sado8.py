import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta
import plotly.express as px
import random
from streamlit_autorefresh import st_autorefresh

# --- 1. AYARLAR (İLK SIRADA OLMAK ZORUNDA) ---
st.set_page_config(page_title="SDR PRESTIGE GLOBAL", layout="wide")

# --- 2. GÜNCELLEME MOTORU ---
st_autorefresh(interval=30 * 1000, key="datarefresh")

# --- 3. CSS TASARIM ---
st.markdown("""
    <style>
    .stApp { background-color: #000000 !important; }
    .top-bar { display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; padding: 15px; background-color: #000000; border-bottom: 3px solid #FFD700; margin-bottom: 15px; }
    .main-title { color: #00d4ff; text-align: center; font-family: 'Arial Black'; font-size: 55px; margin-bottom: 0px; text-shadow: 0px 0px 30px #00d4ff; }
    .sub-title { color: #ffffff; text-align: center; font-family: 'Courier New'; font-size: 20px; letter-spacing: 5px; margin-bottom: 20px; }
    
    [data-testid="stMetric"] {
        background-color: #000000 !important;
        border: 2px solid #FFD700 !important;
        border-radius: 15px;
        padding: 20px !important;
    }
    [data-testid="stMetricLabel"] { color: #ffffff !important; font-size: 18px !important; font-weight: bold !important; }
    [data-testid="stMetricValue"] { color: #FFD700 !important; font-size: 38px !important; }

    div[data-testid="stDataFrame"] div[role="columnheader"] {
        background-color: #000000 !important;
        color: #FFD700 !important;
    }
    div[data-testid="stDataFrame"] { 
        background-color: #000000 !important; 
        border: 4px solid #FFD700 !important; 
        border-radius: 15px;
    }
    .stDataFrame td, .stDataFrame th { font-size: 28px !important; font-weight: bold !important; }
    .info-box { background-color: #000000; border: 2px solid #FFD700; padding: 25px; border-radius: 15px; height: 100%; margin-bottom: 15px; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. DEĞİŞKENLER ---
su_an_utc = datetime.utcnow()
su_an_tr = su_an_utc + timedelta(hours=3)

if 'fake_counter' not in st.session_state:
    st.session_state.fake_counter = random.randint(225, 275)
else:
    st.session_state.fake_counter += random.randint(-1, 2)
    if st.session_state.fake_counter > 300: st.session_state.fake_counter = 295

def get_live_data():
    assets = ['BTCUSDT', 'ETHUSDT', 'SOLUSDT', 'AVAXUSDT', 'XRPUSDT', 'BNBUSDT', 'ADAUSDT', 'DOGEUSDT', 'DOTUSDT', 'LINKUSDT', 'MATICUSDT', 'TRXUSDT', 'UNIUSDT', 'BCHUSDT', 'SUIUSDT', 'FETUSDT', 'RENDERUSDT', 'PEPEUSDT', 'SHIBUSDT']
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
                
                if guc > 88: d, e = "🛡️ SELL", "🚨 ZİRVE: Kâr Al & Nakde Geç / PEAK: Take Profit"
                elif guc < 15: d, e = "💰 BUY", "🔥 DİP: Kademeli Topla / BOTTOM: Buy Time"
                elif 15 <= guc < 40: d, e = "🥷 WAIT", "⌛ PUSU: Güç Toplanıyor / AMBUSH: Recovering"
                else: d, e = "📈 FOLLOW", "💎 TRENDİ İZLE / WATCHING THE TREND"
                
                rows.append({
                    "SDR SİNYAL": d, "VARLIK/ASSET": item['symbol'].replace("USDT", ""),
                    "FİYAT/PRICE": f"{p:,.2f} $", "HACİM/VOL (1H)": f"${v_1h:,.2f} M",
                    "GÜÇ/POWER (%)": f"%{guc}", "POWER_NUM": guc, "SDR ANALİZ / ANALYSIS": e
                })
            except: continue
        return pd.DataFrame(rows), total_vol
    except: return pd.DataFrame(), 0

# --- 5. EKRAN TASARIMI ---
st.markdown(f"""
    <div class="top-bar">
        <div style='color:#00ffcc; font-weight:bold;'>● OFFICIAL BINANCE API | UPDATE: 30S</div>
        <div style='text-align:center;'>
            <span style='color:#ffffff;'>👥 VISITORS:</span> <span style='color:#ff00ff; font-weight:bold;'>{st.session_state.fake_counter}</span>
            &nbsp;&nbsp;&nbsp;&nbsp;
            <span style='color:#00d4ff;'>🌍 UTC: {su_an_utc.strftime("%H:%M:%S")}</span>
            &nbsp;&nbsp;&nbsp;&nbsp;
            <span style='color:#00ffcc;'>🇹🇷 TR: {su_an_tr.strftime("%H:%M:%S")}</span>
        </div>
        <div style='color:#FFD700; font-weight:bold;'>SDR PRESTIGE</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="main-title">SDR PRESTIGE GLOBAL</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">SADRETTİN TURAN VIP ANALYTICS</div>', unsafe_allow_html=True)

df, t_vol = get_live_data()

if not df.empty:
    m1, m2, m3 = st.columns([1,1,2])
    m1.metric("💰 ALIM BÖLGESİ / BUY ZONE", len(df[df['SDR SİNYAL'] == "💰 BUY"]))
    m2.metric("🛡️ SATIŞ BÖLGESİ / SELL ZONE", len(df[df['SDR SİNYAL'] == "🛡️ SELL"]))
    m3.metric("📊 TOPLAM HACİM (1H) / TOTAL VOLUME", f"${t_vol:,.2f} M")
    
    st.write("---")
    
    st.dataframe(df[["SDR SİNYAL", "VARLIK/ASSET", "FİYAT/PRICE", "HACİM/VOL (1H)", "GÜÇ/POWER (%)", "SDR ANALİZ / ANALYSIS"]].style.set_properties(**{
        'background-color': '#000000', 'color': '#FFD700', 'border-color': '#FFD700', 'font-weight': 'bold'
    }), use_container_width=True, hide_index=True, height=750)
    
    st.write("---")
    
    st.write("### 📊 GÜÇ ANALİZİ (%) / GLOBAL POWER PERCENTAGE")
    fig = px.bar(df, x='VARLIK/ASSET', y='POWER_NUM', color='POWER_NUM', color_continuous_scale='Blues')
    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color="white"))
    st.plotly_chart(fig, use_container_width=True)
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""
        <div class="info-box" style="border-left: 10px solid #ff4b4b;">
            <h3 style='color:#ff4b4b; margin-top:0;'>⚠️ YASAL UYARI / LEGAL NOTICE</h3>
            <p style='color:#ffffff;'><b>YATIRIM DANIŞMANLIĞI DEĞİLDİR. / NOT AN INVESTMENT ADVICE.</b></p>
            <p style='color:#cccccc;'>Data source: Official Binance Public API. / Veri kaynağı: Resmi Binance API.</p>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="info-box" style="border-left: 10px solid #FFD700;">
            <h3 style='color:#FFD700; margin-top:0;'>🛡️ SDR STRATEJİ / STRATEGY</h3>
            <p style='color:#ffffff;'>🚀 <b>%88-100 POWER:</b> Take profit. / Kar al.</p>
            <p style='color:#ffffff;'>📉 <b>%0-15 POWER:</b> Accumulation zone. / Toplama bölgesi.</p>
            <p style='color:#00d4ff;'>⚡ 50% cash protection is advised. / %50 nakit koruması tavsiye edilir.</p>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br><p style='text-align:center; opacity: 0.5; color:white;'>© 2026 sdr sadrettin turan • binance public api data</p>", unsafe_allow_html=True)
