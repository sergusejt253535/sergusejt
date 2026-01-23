import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta
import plotly.express as px
import random
from streamlit_autorefresh import st_autorefresh

# --- 1. AYARLAR (CRITICAL) ---
st.set_page_config(page_title="SDR PRESTIGE GLOBAL", layout="wide", initial_sidebar_state="collapsed")

# --- 2. GÜNCELLEME MOTORU (30 Saniye) ---
st_autorefresh(interval=30 * 1000, key="datarefresh")

# --- 3. CSS TASARIM (Zehra'nın Dokunuşu) ---
st.markdown("""
    <style>
    .stApp { background-color: #000000 !important; }
    .top-bar { display: flex; justify-content: space-between; align-items: center; padding: 15px; background-color: #000000; border-bottom: 3px solid #FFD700; margin-bottom: 15px; }
    .main-title { color: #00d4ff; text-align: center; font-family: 'Arial Black'; font-size: clamp(30px, 5vw, 55px); margin-bottom: 0px; text-shadow: 0px 0px 30px #00d4ff; }
    .sub-title { color: #ffffff; text-align: center; font-family: 'Courier New'; font-size: 18px; letter-spacing: 5px; margin-bottom: 20px; }
    
    /* Metric Kutuları */
    [data-testid="stMetric"] {
        background-color: #0c0c0c !important;
        border: 2px solid #FFD700 !important;
        border-radius: 15px;
        padding: 15px !important;
        text-align: center;
    }
    [data-testid="stMetricLabel"] { color: #ffffff !important; font-size: 16px !important; }
    [data-testid="stMetricValue"] { color: #FFD700 !important; font-size: 32px !important; }

    /* Tablo Tasarımı */
    .stDataFrame { border: 2px solid #FFD700 !important; border-radius: 10px; }
    
    .info-box { background-color: #0c0c0c; border: 1px solid #FFD700; padding: 20px; border-radius: 15px; height: 100%; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. ZAMAN VE ZİYARETÇİ ---
su_an_utc = datetime.utcnow()
su_an_tr = su_an_utc + timedelta(hours=3)

if 'fake_counter' not in st.session_state:
    st.session_state.fake_counter = random.randint(225, 275)
else:
    st.session_state.fake_counter += random.randint(-1, 2)

# --- 5. VERİ ÇEKME FONKSİYONU ---
def get_live_data():
    assets = ['BTCUSDT', 'ETHUSDT', 'SOLUSDT', 'AVAXUSDT', 'XRPUSDT', 'BNBUSDT', 'ADAUSDT', 
              'DOGEUSDT', 'DOTUSDT', 'LINKUSDT', 'MATICUSDT', 'TRXUSDT', 'UNIUSDT', 
              'BCHUSDT', 'SUIUSDT', 'FETUSDT', 'RENDERUSDT', 'PEPEUSDT', 'SHIBUSDT']
    try:
        r = requests.get("https://api.binance.com/api/v3/ticker/24hr", timeout=10)
        if r.status_code == 200:
            data = r.json()
            active = [i for i in data if i['symbol'] in assets]
            rows = []
            total_vol = 0
            for item in active:
                p = float(item.get('lastPrice', 0))
                h = float(item.get('highPrice', 0))
                l = float(item.get('lowPrice', 0))
                v_24h = float(item.get('quoteVolume', 0)) / 1_000_000
                v_1h = v_24h / 24 # Tahmini 1s hacim
                total_vol += v_1h
                
                # Güç Hesaplama (RSI mantığına yakın)
                guc = int(((p - l) / (h - l)) * 100) if (h - l) != 0 else 50
                
                if guc > 88: d, e = "🛡️ SELL", "🚨 ZİRVE: Kâr Al / PEAK"
                elif guc < 15: d, e = "💰 BUY", "🔥 DİP: Topla / BOTTOM"
                elif 15 <= guc < 45: d, e = "🥷 WAIT", "⌛ PUSU / AMBUSH"
                else: d, e = "📈 FOLLOW", "💎 TREND / WATCH"
                
                rows.append({
                    "SDR SİNYAL": d, 
                    "VARLIK/ASSET": item['symbol'].replace("USDT", ""),
                    "FİYAT/PRICE": f"{p:,.2f} $", 
                    "HACİM/VOL (1H)": f"${v_1h:,.2f} M",
                    "GÜÇ/POWER (%)": guc,
                    "SDR ANALİZ / ANALYSIS": e
                })
            return pd.DataFrame(rows), total_vol
        else:
            return pd.DataFrame(), 0
    except Exception as err:
        return pd.DataFrame(), 0

# --- 6. ARAYÜZ ---
st.markdown(f"""
    <div class="top-bar">
        <div style='color:#00ffcc; font-weight:bold;'>● BINANCE LIVE | 30S</div>
        <div style='text-align:center;'>
            <span style='color:#ffffff;'>👥 VISITORS:</span> <span style='color:#ff00ff; font-weight:bold;'>{st.session_state.fake_counter}</span>
            <span style='color:#00d4ff; margin-left:20px;'>🌍 UTC: {su_an_utc.strftime("%H:%M:%S")}</span>
            <span style='color:#00ffcc; margin-left:20px;'>🇹🇷 TR: {su_an_tr.strftime("%H:%M:%S")}</span>
        </div>
        <div style='color:#FFD700; font-weight:bold;'>SDR PRESTIGE</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="main-title">SDR PRESTIGE GLOBAL</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">SADRETTİN TURAN VIP ANALYTICS</div>', unsafe_allow_html=True)

df, t_vol = get_live_data()

if not df.empty:
    m1, m2, m3 = st.columns(3)
    m1.metric("💰 ALIM / BUY ZONE", len(df[df['SDR SİNYAL'] == "💰 BUY"]))
    m2.metric("🛡️ SATIŞ / SELL ZONE", len(df[df['SDR SİNYAL'] == "🛡️ SELL"]))
    m3.metric("📊 TOTAL VOL (1H)", f"${t_vol:,.2f} M")
    
    st.write("")
    
    # Tabloyu gösterirken stile dikkat
    st.dataframe(
        df[["SDR SİNYAL", "VARLIK/ASSET", "FİYAT/PRICE", "HACİM/VOL (1H)", "GÜÇ/POWER (%)", "SDR ANALİZ / ANALYSIS"]],
        use_container_width=True, 
        hide_index=True, 
        height=600
    )
    
    st.write("### 📊 GÜÇ ANALİZİ (%) / GLOBAL POWER")
    fig = px.bar(df, x='VARLIK/ASSET', y='GÜÇ/POWER (%)', color='GÜÇ/POWER (%)', 
                 color_continuous_scale='RdYlGn', range_y=[0,100])
    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color="white"))
    st.plotly_chart(fig, use_container_width=True)
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"""<div class="info-box" style="border-left: 10px solid #ff4b4b;">
            <h3 style='color:#ff4b4b; margin:0;'>⚠️ YASAL UYARI</h3>
            <p style='color:white;'>Yatırım danışmanlığı değildir. Sado'nun stratejisidir.</p>
            </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class="info-box" style="border-left: 10px solid #FFD700;">
            <h3 style='color:#FFD700; margin:0;'>🛡️ STRATEJİ</h3>
            <p style='color:white;'>%15 Altı: Topla | %88 Üstü: Çık.</p>
            </div>""", unsafe_allow_html=True)
else:
    st.warning("Veri bekleniyor... Binance API'ye bağlanıyorum aslanım, bekle!")

st.markdown("<br><p style='text-align:center; opacity: 0.5; color:white;'>© 2026 sdr sadrettin turan</p>", unsafe_allow_html=True)
