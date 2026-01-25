import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta
import plotly.express as px
from streamlit_autorefresh import st_autorefresh

# --- 1. AYARLAR (İLK SIRADA) ---
st.set_page_config(page_title="SDR PRESTIGE GLOBAL | VIP TERMINAL", layout="wide")

# --- 2. 15 SANİYELİK GÜNCELLEME MOTORU ---
st_autorefresh(interval=15 * 1000, key="datarefresh")

# --- 3. CSS TASARIM (SİBER SİYAH VE ALTIN SARISI) ---
st.markdown("""
    <style>
    .stApp { background-color: #000000 !important; }
    .main-title { color: #00d4ff; text-align: center; font-family: 'Arial Black'; font-size: 60px; text-shadow: 0px 0px 30px #00d4ff; margin-bottom: 0px; }
    .sub-title { color: #FFD700; text-align: center; font-family: 'Courier New'; font-size: 20px; letter-spacing: 5px; margin-bottom: 30px; }
    
    /* Metrik Kartları */
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, #050505 0%, #151515 100%) !important;
        border: 2px solid #FFD700 !important;
        border-radius: 15px;
        padding: 20px !important;
        box-shadow: 0px 0px 15px rgba(255, 215, 0, 0.2);
    }
    
    /* TABLO TASARIMI - PİYASADA YOK DEDİĞİN TABLO BURADA! */
    div[data-testid="stDataFrame"] {
        border: 4px solid #FFD700 !important;
        border-radius: 15px;
        background-color: #000000 !important;
        padding: 10px;
    }
    .stDataFrame td, .stDataFrame th { font-size: 18px !important; }

    /* Yasal Uyarı Kutusu */
    .legal-box {
        background-color: #0a0a0a;
        border: 2px solid #ff4b4b;
        padding: 20px;
        border-radius: 15px;
        color: #ffffff;
        font-family: 'Arial';
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. VERİ MOTORU (TR/EN DESTEKLİ + 30 ALTCOIN) ---
def get_sdr_data():
    assets = [
        'BTCUSDT', 'ETHUSDT', 'SOLUSDT', 'AVAXUSDT', 'XRPUSDT', 'BNBUSDT', 'ADAUSDT', 'DOGEUSDT', 
        'DOTUSDT', 'LINKUSDT', 'MATICUSDT', 'NEARUSDT', 'SUIUSDT', 'FETUSDT', 'OPUSDT', 'ARBUSDT', 
        'TIAUSDT', 'PEPEUSDT', 'SHIBUSDT', 'RENDERUSDT', 'LTCUSDT', 'BCHUSDT', 'APTUSDT', 'FILUSDT', 
        'ICPUSDT', 'STXUSDT', 'INJUSDT', 'GALAUSDT', 'TRXUSDT', 'ORDIUSDT'
    ]
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
            guc = int(((p - l) / (h - l)) * 100) if (h - l) != 0 else 0
            
            # TR/EN Sinyal ve Analiz
            if guc > 85: 
                s, a = "🛡️ SELL / SAT", "🚨 ZİRVE: KÂR AL / PEAK: TAKE PROFIT"
            elif guc < 15: 
                s, a = "💰 BUY / AL", "🔥 DİP: TOPLA / BOTTOM: ACCUMULATE"
            else: 
                s, a = "📈 FOLLOW / İZLE", "💎 TREND TAKİBİ / TRACKING TREND"

            rows.append({
                "SDR SİNYAL": s,
                "VARLIK / ASSET": item['symbol'].replace("USDT", ""),
                "FİYAT / PRICE": f"{p:,.2f} $",
                "24S DEĞİŞİM / 24H CHG": f"%{ch}",
                "HACİM / VOLUME": f"${v:,.1f} M",
                "GÜÇ / POWER (%)": f"%{guc}",
                "G_NUM": guc,
                "SDR ANALİZ / ANALYSIS": a
            })
        return pd.DataFrame(rows)
    except: return pd.DataFrame()

# --- 5. ÜST PANEL ---
st.markdown('<div class="main-title">SDR PRESTIGE GLOBAL</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">SADRETTİN TURAN VIP ANALYTICS</div>', unsafe_allow_html=True)

df = get_sdr_data()

if not df.empty:
    # 3'lü Metrik Kartları
    c1, c2, c3 = st.columns(3)
    with c1: st.metric("💰 ALIM BÖLGESİ / BUY ZONE", len(df[df['SDR SİNYAL'].str.contains("BUY")]))
    with c2: st.metric("🛡️ SATIŞ BÖLGESİ / SELL ZONE", len(df[df['SDR SİNYAL'].str.contains("SELL")]))
    with c3: st.metric("🌍 GÜNCELLEME / UPDATE", datetime.now().strftime("%H:%M:%S"))

    # --- 6. DEV TABLO (İŞTE BURADA PAŞAM!) ---
    st.markdown("### 📊 CANLI PİYASA TERMİNALİ / LIVE MARKET TERMINAL")
    st.dataframe(
        df[["SDR SİNYAL", "VARLIK / ASSET", "FİYAT / PRICE", "24S DEĞİŞİM / 24H CHG", "HACİM / VOLUME", "GÜÇ / POWER (%)", "SDR ANALİZ / ANALYSIS"]], 
        use_container_width=True, 
        hide_index=True, 
        height=800
    )

    # --- 7. GRAFİK PANELİ ---
    st.write("---")
    st.markdown("### 📈 GÜÇ ENDEKSİ / POWER INDEX")
    fig = px.bar(df, x='VARLIK / ASSET', y='G_NUM', color='G_NUM', color_continuous_scale='Turbo')
    fig.update_layout(plot_bgcolor='black', paper_bgcolor='black', font=dict(color="white"), margin=dict(l=0, r=0, t=0, b=0))
    st.plotly_chart(fig, use_container_width=True)

# --- 8. YASAL UYARI & VIP İLETİŞİM ---
st.write("---")
l1, l2 = st.columns([2, 1])

with l1:
    st.markdown("""
    <div class='legal-box'>
        <h3 style='color:#ff4b4b; margin:0;'>⚠️ YASAL UYARI / LEGAL NOTICE</h3>
        <p>Yatırım danışmanlığı değildir. Sadece Sadrettin Turan VIP algoritmasıdır. / Not an investment advice. SDR VIP Algorithm only.</p>
        <p style='font-size:12px; opacity:0.7;'>Data source: Binance Official API</p>
    </div>
    """, unsafe_allow_html=True)

with l2:
    st.sidebar.markdown("### 👤 SADRETTİN TURAN")
    st.sidebar.info("3 GÜNLÜK ÜCRETSİZ DENEME / 3 DAYS FREE TRIAL")
    if st.sidebar.button("🔓 VIP ERİŞİM AL / GET VIP ACCESS"):
        st.sidebar.write("WhatsApp: +90 XXX XXX XX XX") # Buraya numaranı yaz Sado'm

st.markdown("<br><p style='text-align:center; color:#555;'>© 2026 SDR PRESTIGE GLOBAL • ALL RIGHTS RESERVED</p>", unsafe_allow_html=True)
