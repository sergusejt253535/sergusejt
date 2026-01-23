import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta
import random
from streamlit_autorefresh import st_autorefresh

# --- 1. AYARLAR ---
st.set_page_config(page_title="SDR PRESTIGE GLOBAL", layout="wide")

# Otomatik Yenileme (30 saniye)
st_autorefresh(interval=30 * 1000, key="datarefresh")

# --- 2. CSS TASARIM (Sado'nun Şanına Yakışır) ---
st.markdown("""
    <style>
    .stApp { background-color: #000000 !important; }
    .main-title { color: #00d4ff; text-align: center; font-family: 'Arial Black'; font-size: 45px; text-shadow: 0px 0px 20px #00d4ff; }
    .sub-title { color: #ffffff; text-align: center; font-family: 'Courier New'; font-size: 18px; letter-spacing: 5px; margin-bottom: 20px; }
    [data-testid="stMetric"] { background-color: #0c0c0c !important; border: 2px solid #FFD700 !important; border-radius: 10px; }
    [data-testid="stMetricValue"] { color: #FFD700 !important; }
    th { background-color: #111 !important; color: #00d4ff !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. VERİ ÇEKME MOTORU (GITHUB ÖZEL) ---
def get_live_data():
    assets = ['BTCUSDT', 'ETHUSDT', 'SOLUSDT', 'AVAXUSDT', 'XRPUSDT', 'BNBUSDT', 'ADAUSDT', 'DOGEUSDT', 'DOTUSDT', 'LINKUSDT']
    # GitHub üzerinden giderken tarayıcı gibi davranması için header ekledik
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    url = "https://api.binance.com/api/v3/ticker/24hr"
    
    try:
        r = requests.get(url, headers=headers, timeout=10)
        if r.status_code == 200:
            all_data = r.json()
            rows = []
            total_vol = 0
            for item in all_data:
                if item['symbol'] in assets:
                    p = float(item['lastPrice'])
                    h = float(item['highPrice'])
                    l = float(item['lowPrice'])
                    v = (float(item['quoteVolume']) / 1_000_000) / 24
                    total_vol += v
                    guc = int(((p - l) / (h - l)) * 100) if (h - l) != 0 else 50
                    
                    sig = "💰 BUY" if guc < 15 else ("🛡️ SELL" if guc > 88 else "📈 FOLLOW")
                    anlz = "🔥 DİP" if guc < 15 else ("🚨 ZİRVE" if guc > 88 else "💎 İZLE")
                    
                    rows.append({
                        "SİNYAL": sig,
                        "VARLIK": item['symbol'].replace("USDT", ""),
                        "FİYAT": f"{p:,.2f} $",
                        "GÜÇ (%)": f"%{guc}",
                        "ANALİZ": anlz
                    })
            return pd.DataFrame(rows), total_vol
    except:
        pass
    return pd.DataFrame(), 0

# --- 4. ARAYÜZ ---
su_an_tr = datetime.utcnow() + timedelta(hours=3)
st.markdown(f'<p style="text-align:right; color:#FFD700;">🇹🇷 TR: {su_an_tr.strftime("%H:%M:%S")}</p>', unsafe_allow_html=True)
st.markdown('<div class="main-title">SDR PRESTIGE GLOBAL</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">SADRETTİN TURAN VIP ANALYTICS</div>', unsafe_allow_html=True)

df, t_vol = get_live_data()

if not df.empty:
    m1, m2, m3 = st.columns(3)
    m1.metric("💰 ALIM BÖLGESİ", len(df[df['SİNYAL'] == "💰 BUY"]))
    m2.metric("🛡️ SATIŞ BÖLGESİ", len(df[df['SİNYAL'] == "🛡️ SELL"]))
    m3.metric("📊 HACİM (1H)", f"${t_vol:,.2f} M")
    
    st.write("---")
    st.table(df) # GitHub ortamında en sorunsuz çalışan tablo formatı
else:
    st.error("GitHub Bağlantısı Zorlanıyor... Sado'm, sayfayı bir kez yenile (Refresh) yaparsan mermi gibi gelecektir!")

st.markdown("<p style='text-align:center; opacity: 0.3; color:white; margin-top:50px;'>© 2026 sdr sadrettin turan</p>", unsafe_allow_html=True)
