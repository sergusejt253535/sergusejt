import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta
import plotly.express as px
from streamlit_autorefresh import st_autorefresh

# --- 1. AYARLAR ---
st.set_page_config(page_title="SDR PRESTIGE GLOBAL", layout="wide")

if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.markdown("<h1 style='color: #FFD700; text-align: center;'>🛡️ SDR PRESTIGE ACCESS</h1>", unsafe_allow_html=True)
    password = st.text_input("SDR GİZLİ ANAHTAR / ACCESS KEY:", type="password")
    if st.button("SİSTEME GİRİŞ YAP / LOGIN"):
        if password == "serguxy2026":
            st.session_state.authenticated = True
            st.rerun()
    st.stop()

st_autorefresh(interval=15 * 1000, key="datarefresh")

# --- 2. VERİ MOTORU (KESİN BİNANCE VERİSİ) ---
def get_sdr_data():
    assets = ['BTCUSDT', 'ETHUSDT', 'SOLUSDT', 'AVAXUSDT', 'XRPUSDT', 'BNBUSDT', 'ADAUSDT', 'DOGEUSDT', 'DOTUSDT', 'LINKUSDT', 'MATICUSDT', 'TRXUSDT', 'UNIUSDT', 'BCHUSDT', 'SUIUSDT', 'FETUSDT', 'RENDERUSDT', 'PEPEUSDT', 'SHIBUSDT']
    rows = []
    try:
        # Fiyat ve 24s Değişim verisini aynı anda alıyoruz
        r = requests.get("https://api.binance.com/api/v3/ticker/24hr", timeout=10)
        if r.status_code == 200:
            data = r.json()
            for sym in assets:
                item = next((i for i in data if i['symbol'] == sym), None)
                if item:
                    price = float(item['lastPrice'])
                    change = float(item['priceChangePercent'])
                    # Güç algoritmasını %50 baz alıp değişime göre (artı/eksi) hesaplıyoruz
                    power = int(50 + (change * 4))
                    power = max(min(power, 99), 1)
                    
                    if power > 80: sig, ana = "🛡️ SELL", "🚨 ZİRVE / PEAK (Take Profit)"
                    elif power < 25: sig, ana = "💰 BUY", "🔥 DİP / BOTTOM (Accumulate)"
                    else: sig, ana = "📈 FOLLOW", "💎 TREND İZLE / WATCH"
                    
                    rows.append({
                        "SDR SIGNAL": sig,
                        "VARLIK / ASSET": sym.replace("USDT", ""),
                        "FİYAT / PRICE": f"{price:,.2f} $",
                        "24H %": f"%{change:+.2f}",
                        "GÜÇ / POWER (%)": f"%{power}",
                        "POWER_VAL": power,
                        "ANALİZ / ANALYSIS": ana
                    })
    except: pass
    return pd.DataFrame(rows)

# --- 3. TASARIM ---
st.markdown("""
    <style>
    .stApp { background-color: #000000 !important; }
    .top-bar { display: flex; justify-content: space-between; align-items: center; padding: 15px; border-bottom: 3px solid #FFD700; margin-bottom: 15px; }
    .main-title { color: #00d4ff; text-align: center; font-family: 'Arial Black'; font-size: 55px; text-shadow: 0px 0px 20px #00d4ff; }
    div[data-testid="stDataFrame"] { border: 3px solid #FFD700 !important; border-radius: 10px; }
    .info-box { background-color: #111; border: 2px solid #FFD700; padding: 15px; border-radius: 10px; color: white; }
    </style>
    """, unsafe_allow_html=True)

su_an_utc = datetime.utcnow()
su_an_tr = su_an_utc + timedelta(hours=3)

# --- 4. PANEL ---
df = get_sdr_data()

st.markdown(f"""
    <div class="top-bar">
        <div style='color:#00ffcc;'>OFFICIAL BINANCE API | 15S UPDATE</div>
        <div style='text-align:center; color:white;'>
            <b>{su_an_tr.strftime('%d.%m.%Y')}</b> | 
            TR: <span style='color:#FFD700;'>{su_an_tr.strftime('%H:%M:%S')}</span> | 
            UTC: <span style='color:#00d4ff;'>{su_an_utc.strftime('%H:%M:%S')}</span>
        </div>
        <div style='color:#FFD700;'>SDR PRESTIGE VIP</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="main-title">SDR PRESTIGE GLOBAL</div>', unsafe_allow_html=True)

if not df.empty:
    # Tablo (Rakamlar Gerçek)
    st.dataframe(df[["SDR SIGNAL", "VARLIK / ASSET", "FİYAT / PRICE", "24H %", "GÜÇ / POWER (%)", "ANALİZ / ANALYSIS"]].style.set_properties(**{
        'background-color': '#000000', 'color': '#FFD700', 'font-weight': 'bold'
    }), use_container_width=True, hide_index=True, height=550)

    # Grafik
    fig = px.bar(df, x='VARLIK / ASSET', y='POWER_VAL', color='POWER_VAL', color_continuous_scale='YlOrRd')
    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color="white"))
    st.plotly_chart(fig, use_container_width=True)
else:
    st.error("API Bağlantı Hatası! Rakamlar yüklenemedi. Lütfen sayfayı yenileyin.")

# Alt Kutular
c1, c2 = st.columns(2)
with c1:
    st.markdown('<div class="info-box"><b>⚠️ YASAL UYARI / LEGAL DISCLAIMER</b><br>Veriler Binance API ile çekilir. Yatırım tavsiyesi değildir.</div>', unsafe_allow_html=True)
with c2:
    st.markdown('<div class="info-box"><b>🛡️ SDR STRATEJİ / STRATEGY</b><br>15 saniyede bir güncellenir. %80 üzeri satış, %25 altı alış bölgesidir.</div>', unsafe_allow_html=True)
