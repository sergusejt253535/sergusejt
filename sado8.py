import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta
import plotly.express as px
from streamlit_autorefresh import st_autorefresh

# --- 1. AYARLAR ---
st.set_page_config(page_title="SDR PRESTIGE GLOBAL | CANLI TERMİNAL", layout="wide")

# --- 2. 15 SANİYELİK GÜNCELLEME MOTORU ---
st_autorefresh(interval=15 * 1000, key="datarefresh")

# --- 3. SDR ÖZEL TASARIM (SİYAH & ALTIN) ---
st.markdown("""
    <style>
    .stApp { background-color: #000000 !important; }
    .main-title { color: #00d4ff; text-align: center; font-family: 'Arial Black'; font-size: 55px; text-shadow: 0px 0px 30px #00d4ff; margin-bottom: 0px; }
    .sub-title { color: #FFD700; text-align: center; font-family: 'Courier New'; font-size: 20px; letter-spacing: 5px; margin-bottom: 20px; }
    
    /* Tablo Stilini Sertleştirelim */
    div[data-testid="stDataFrame"] {
        border: 3px solid #FFD700 !important;
        border-radius: 15px;
        background-color: #000000 !important;
    }
    
    /* Metrik Kartları */
    [data-testid="stMetric"] {
        background: #0a0a0a !important;
        border: 1px solid #FFD700 !important;
        border-radius: 15px;
        padding: 20px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. BİNANCE VERİ MOTORU (30+ ALT COIN) ---
def get_binance_data():
    # Paşam listeyi senin için en popüler alt coinlerle doldurdum
    assets = ['BTCUSDT', 'ETHUSDT', 'SOLUSDT', 'AVAXUSDT', 'XRPUSDT', 'BNBUSDT', 'ADAUSDT', 'DOGEUSDT', 'DOTUSDT', 'LINKUSDT', 
              'MATICUSDT', 'NEARUSDT', 'SUIUSDT', 'FETUSDT', 'OPUSDT', 'ARBUSDT', 'TIAUSDT', 'PEPEUSDT', 'SHIBUSDT', 'RENDERUSDT',
              'LTCUSDT', 'BCHUSDT', 'APTUSDT', 'FILUSDT', 'ICPUSDT', 'STXUSDT', 'INJUSDT', 'GALAUSDT', 'TRXUSDT', 'ORDIUSDT']
    try:
        r = requests.get("https://api.binance.com/api/v3/ticker/24hr", timeout=10)
        data = r.json()
        active = [i for i in data if i['symbol'] in assets]
        rows = []
        for item in active:
            p = float(item.get('lastPrice', 0))
            ch = float(item.get('priceChangePercent', 0))
            h = float(item.get('highPrice', 0))
            l = float(item.get('lowPrice', 0))
            v = float(item.get('quoteVolume', 0)) / 1_000_000
            # SDR GÜÇ ALGORİTMASI
            guc = int(((p - l) / (h - l)) * 100) if (h - l) != 0 else 0
            
            if guc > 85: s, an = "🛡️ SELL (SAT)", "🚨 ZİRVE: KÂR AL!"
            elif guc < 15: s, an = "💰 BUY (AL)", "🔥 DİP: TOPLA!"
            else: s, an = "📈 FOLLOW", "💎 TREND TAKİBİ"

            rows.append({
                "SDR SİNYAL": s,
                "COIN": item['symbol'].replace("USDT", ""),
                "FİYAT": f"{p:,.2f} $",
                "24S DEĞİŞİM": f"%{ch}",
                "HACİM (24S)": f"${v:,.1f}M",
                "GÜÇ (%)": f"%{guc}",
                "ANALİZ": an
            })
        return pd.DataFrame(rows)
    except: return pd.DataFrame()

# --- 5. EKRAN DÜZENİ ---
st.markdown('<div class="main-title">SDR PRESTIGE GLOBAL</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">SADRETTİN TURAN VIP ANALYTICS</div>', unsafe_allow_html=True)

df = get_binance_data()

if not df.empty:
    # Üst Özet Kartları
    c1, c2, c3 = st.columns(3)
    c1.metric("💰 ALIM BÖLGESİ", len(df[df['SDR SİNYAL'] == "💰 BUY (AL)"]))
    c2.metric("🛡️ SATIŞ BÖLGESİ", len(df[df['SDR SİNYAL'] == "🛡️ SELL (SAT)"]))
    c3.metric("🌍 GÜNCELLEME", datetime.now().strftime("%H:%M:%S"))

    st.write("### 📊 CANLI ALT COİN TERMİNALİ (15S GÜNCEL)")
    # İŞTE O TABLO SADO'M! 30 COIN BURADA AKIYOR
    st.dataframe(df, use_container_width=True, hide_index=True, height=800)

    # Görsel Destek
    st.write("---")
    fig = px.bar(df, x='COIN', y='GÜÇ (%)', color='GÜÇ (%)', color_continuous_scale='Blues', title="GLOBAL GÜÇ ENDEKSİ")
    fig.update_layout(plot_bgcolor='black', paper_bgcolor='black', font=dict(color="white"))
    st.plotly_chart(fig, use_container_width=True)

# --- YASAL UYARI ---
st.markdown("""
<div style='background-color:#1a1a1a; border-left: 10px solid #ff4b4b; padding:15px; border-radius:10px;'>
    <h4 style='color:#ff4b4b; margin:0;'>⚠️ YASAL UYARI</h4>
    Buradaki veriler Sadrettin Turan VIP algoritmasıdır. Yatırım tavsiyesi değildir.
</div>
""", unsafe_allow_html=True)
