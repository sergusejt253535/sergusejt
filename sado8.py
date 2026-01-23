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
    .top-bar { display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; padding: 15px; border-bottom: 3px solid #FFD700; margin-bottom: 15px; }
    .main-title { color: #00d4ff; text-align: center; font-family: 'Arial Black'; font-size: 55px; text-shadow: 0px 0px 30px #00d4ff; }
    .sub-title { color: #ffffff; text-align: center; font-family: 'Courier New'; font-size: 20px; letter-spacing: 5px; margin-bottom: 20px; }
    div[data-testid="stDataFrame"] { background-color: #000000 !important; border: 4px solid #FFD700 !important; border-radius: 15px; }
    .stDataFrame td { color: #FFD700 !important; font-weight: bold !important; font-size: 20px !important; }
    .info-box { background-color: #000000; border: 2px solid #FFD700; padding: 20px; border-radius: 15px; color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. VERİ MOTORU (SÜPER GARANTİ) ---
def get_live_data():
    assets = ['BTCUSDT', 'ETHUSDT', 'SOLUSDT', 'AVAXUSDT', 'XRPUSDT', 'BNBUSDT', 'ADAUSDT', 'DOGEUSDT', 'DOTUSDT', 'LINKUSDT', 'MATICUSDT', 'TRXUSDT', 'UNIUSDT', 'BCHUSDT', 'SUIUSDT', 'FETUSDT', 'RENDERUSDT', 'PEPEUSDT', 'SHIBUSDT']
    rows = []
    total_vol = 0
    
    try:
        # YÖNTEM 1: Toplu Veri Çekimi
        r = requests.get("https://api.binance.com/api/v3/ticker/24hr", timeout=5)
        if r.status_code == 200:
            data = r.json()
            active_data = [d for d in data if d['symbol'] in assets]
            for item in active_data:
                p = float(item['lastPrice'])
                h = float(item['highPrice'])
                l = float(item['lowPrice'])
                v = (float(item['quoteVolume']) / 1_000_000) / 24
                total_vol += v
                guc = int(((p - l) / (h - l)) * 100) if (h - l) != 0 else 50
                guc = max(min(guc, 99), 1)
                
                sig, ana = ("🛡️ SELL", "🚨 ZİRVE / PEAK") if guc > 88 else (("💰 BUY", "🔥 DİP / BOTTOM") if guc < 15 else ("📈 FOLLOW", "💎 TREND"))
                
                rows.append({
                    "SDR SİNYAL": sig, "VARLIK / ASSET": item['symbol'].replace("USDT", ""),
                    "FİYAT / PRICE": f"{p:,.2f} $", "HACİM / VOL (1H)": f"${v:,.2f} M",
                    "GÜÇ / POWER (%)": f"%{guc}", "POWER_NUM": guc, "ANALİZ / ANALYSIS": ana
                })
        
        # YÖNTEM 2: Eğer toplu veri başarısızsa tek tek fiyatları al (Failsafe)
        if not rows:
            r = requests.get("https://api.binance.com/api/v3/ticker/price", timeout=5)
            prices = r.json()
            for sym in assets:
                item = next((i for i in prices if i['symbol'] == sym), None)
                if item:
                    p = float(item['price'])
                    rows.append({
                        "SDR SİNYAL": "📈 FOLLOW", "VARLIK / ASSET": sym.replace("USDT", ""),
                        "FİYAT / PRICE": f"{p:,.2f} $", "HACİM / VOL (1H)": "--",
                        "GÜÇ / POWER (%)": "%50", "POWER_NUM": 50, "ANALİZ / ANALYSIS": "BAĞLANTI KISITLI"
                    })
    except: pass
    return pd.DataFrame(rows), total_vol

# --- 4. PANEL ---
su_an_utc = datetime.utcnow()
su_an_tr = su_an_utc + timedelta(hours=3)

st.markdown(f"""
    <div class="top-bar">
        <div style='color:#00ffcc;'>OFFICIAL BINANCE API | 15S</div>
        <div style='color:white;'>📅 {su_an_tr.strftime("%d.%m.%Y")} | 🌍 UTC: {su_an_utc.strftime("%H:%M:%S")} | 🇹🇷 TR: {su_an_tr.strftime("%H:%M:%S")}</div>
        <div style='color:#FFD700;'>SDR PRESTIGE</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="main-title">SDR PRESTIGE GLOBAL</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">SADRETTİN TURAN VIP ANALYTICS</div>', unsafe_allow_html=True)

df, t_vol = get_live_data()

if not df.empty:
    st.dataframe(df[["SDR SİNYAL", "VARLIK / ASSET", "FİYAT / PRICE", "HACİM / VOL (1H)", "GÜÇ / POWER (%)", "ANALİZ / ANALYSIS"]].style.set_properties(**{
        'background-color': '#000000', 'color': '#FFD700', 'font-weight': 'bold'
    }), use_container_width=True, hide_index=True, height=600)
    
    fig = px.bar(df, x='VARLIK / ASSET', y='POWER_NUM', color='POWER_NUM', color_continuous_scale='Blues')
    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color="white"))
    st.plotly_chart(fig, use_container_width=True)
else:
    st.error("🚨 API BLOKLANDI! Sayfayı yenileyin veya biraz bekleyin.")

# --- 5. ALT KUTULAR ---
c1, c2 = st.columns(2)
with c1:
    st.markdown('<div class="info-box"><b>⚠️ YASAL UYARI / LEGAL NOTICE</b><br>Veriler Binance API ile çekilir. Yatırım tavsiyesi değildir.</div>', unsafe_allow_html=True)
with c2:
    st.markdown('<div class="info-box"><b>🛡️ SDR STRATEJİ / STRATEGY</b><br>%88+ Kar Al, %15- Topla. Sistem 15s güncellenir.</div>', unsafe_allow_html=True)

st.markdown("<p style='text-align:center; opacity: 0.5; color:white;'>© 2026 SDR SADRETTİN TURAN</p>", unsafe_allow_html=True)
