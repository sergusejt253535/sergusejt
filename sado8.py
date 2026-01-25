import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta
import plotly.express as px
from streamlit_autorefresh import st_autorefresh

# --- 1. AYARLAR ---
st.set_page_config(page_title="SDR PRESTIGE GLOBAL | VIP", layout="wide")

# --- 2. 15 SANİYELİK GÜNCELLEME ---
st_autorefresh(interval=15 * 1000, key="datarefresh")

# --- 3. SDR ÖZEL SİBER TASARIM ---
st.markdown("""
    <style>
    .stApp { background-color: #000000 !important; }
    .main-title { color: #00d4ff; text-align: center; font-family: 'Arial Black'; font-size: 55px; text-shadow: 0px 0px 30px #00d4ff; margin-bottom: 0px; }
    .sub-title { color: #FFD700; text-align: center; font-family: 'Courier New'; font-size: 20px; letter-spacing: 5px; margin-bottom: 20px; }
    
    /* DEV TABLO TASARIMI */
    div[data-testid="stDataFrame"] {
        border: 4px solid #FFD700 !important;
        border-radius: 15px;
        background-color: #000000 !important;
    }
    .stDataFrame td, .stDataFrame th { font-size: 18px !important; color: #FFD700 !important; }

    /* Yasal Uyarı */
    .legal-box {
        background-color: #0a0a0a;
        border: 2px solid #ff4b4b;
        padding: 20px;
        border-radius: 15px;
        color: #ffffff;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. BİNANCE VERİ ÇEKME MOTORU (GÜÇLENDİRİLMİŞ) ---
def get_sdr_data():
    assets = [
        'BTCUSDT', 'ETHUSDT', 'SOLUSDT', 'AVAXUSDT', 'XRPUSDT', 'BNBUSDT', 'ADAUSDT', 'DOGEUSDT', 
        'DOTUSDT', 'LINKUSDT', 'MATICUSDT', 'NEARUSDT', 'SUIUSDT', 'FETUSDT', 'OPUSDT', 'ARBUSDT', 
        'TIAUSDT', 'PEPEUSDT', 'SHIBUSDT', 'RENDERUSDT', 'LTCUSDT', 'BCHUSDT', 'APTUSDT', 'FILUSDT'
    ]
    try:
        # Binance API bağlantısı
        url = "https://api.binance.com/api/v3/ticker/24hr"
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            data = r.json()
            active = [i for i in data if i['symbol'] in assets]
            rows = []
            for item in active:
                p = float(item['lastPrice'])
                h = float(item['highPrice'])
                l = float(item['lowPrice'])
                ch = float(item['priceChangePercent'])
                v = float(item['quoteVolume']) / 1_000_000
                
                # SDR GÜÇ ENDEKSİ
                guc = int(((p - l) / (h - l)) * 100) if (h - l) != 0 else 0
                
                if guc > 85: s, a = "🛡️ SELL / SAT", "🚨 ZİRVE / PEAK: KÂR AL"
                elif guc < 15: s, a = "💰 BUY / AL", "🔥 DİP / BOTTOM: TOPLA"
                else: s, a = "📈 FOLLOW / İZLE", "💎 TREND TAKİBİ / TRACKING"

                rows.append({
                    "SDR SİNYAL": s,
                    "VARLIK / ASSET": item['symbol'].replace("USDT", ""),
                    "FİYAT / PRICE": f"{p:,.2f} $",
                    "DEĞİŞİM / CHG": f"%{ch}",
                    "HACİM / VOL": f"${v:,.1f} M",
                    "GÜÇ / POWER (%)": f"%{guc}",
                    "G_NUM": guc,
                    "ANALİZ / ANALYSIS": a
                })
            return pd.DataFrame(rows)
        else:
            return pd.DataFrame()
    except:
        return pd.DataFrame()

# --- 5. EKRAN DÜZENİ ---
st.markdown('<div class="main-title">SDR PRESTIGE GLOBAL</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">SADRETTİN TURAN VIP ANALYTICS</div>', unsafe_allow_html=True)

df = get_sdr_data()

if not df.empty:
    # Üst Özet Kartları
    c1, c2, c3 = st.columns(3)
    c1.metric("💰 BUY ZONE / ALIM", len(df[df['SDR SİNYAL'].str.contains("BUY")]))
    c2.metric("🛡️ SELL ZONE / SATIM", len(df[df['SDR SİNYAL'].str.contains("SELL")]))
    c3.metric("🌍 LAST UPDATE / GÜNCEL", datetime.now().strftime("%H:%M:%S"))

    # ANA TABLO - İŞTE O AKIŞ BURADA!
    st.write("### 📊 LIVE MARKET TERMINAL / CANLI PİYASA TERMİNALİ")
    st.dataframe(df[["SDR SİNYAL", "VARLIK / ASSET", "FİYAT / PRICE", "DEĞİŞİM / CHG", "HACİM / VOL", "GÜÇ / POWER (%)", "ANALİZ / ANALYSIS"]], 
                 use_container_width=True, hide_index=True, height=600)

    # GRAFİKLER
    st.write("---")
    st.write("### 📈 POWER INDEX / GÜÇ ENDEKSİ")
    fig = px.bar(df, x='VARLIK / ASSET', y='G_NUM', color='G_NUM', color_continuous_scale='Blues')
    fig.update_layout(plot_bgcolor='black', paper_bgcolor='black', font=dict(color="white"))
    st.plotly_chart(fig, use_container_width=True)

else:
    st.error("⚠️ Veri bağlantısı kurulamadı. Lütfen internet bağlantınızı veya API durumunu kontrol edin.")

# --- 6. YASAL UYARI ---
st.markdown("""
<div class='legal-box'>
    <h4 style='color:#ff4b4b; margin:0;'>⚠️ YASAL UYARI / LEGAL NOTICE</h4>
    Yatırım danışmanlığı değildir. Sadrettin Turan VIP algoritmasıdır. / Not an investment advice.
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("### 👤 SDR VIP ACCESS")
st.sidebar.info("3 DAYS FREE TRIAL / 3 GÜNLÜK DENEME")
st.sidebar.button("UNLOCK FULL ACCESS / KİLİDİ AÇ")
