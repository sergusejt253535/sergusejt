import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from streamlit_autorefresh import st_autorefresh

# --- 1. AYARLAR ---
st.set_page_config(page_title="SDR PRESTIGE GLOBAL | VIP TERMINAL", layout="wide")

# --- 2. GÜNCELLEME MOTORU (15 SANİYEYE DÜŞÜRDÜM, DAHA AKICI) ---
st_autorefresh(interval=15 * 1000, key="datarefresh")

# --- 3. CSS TASARIM (SİYAH, ALTIN VE SİBER MAVİ) ---
st.markdown("""
    <style>
    .stApp { background-color: #000000 !important; }
    .main-title { color: #00d4ff; text-align: center; font-family: 'Arial Black'; font-size: 60px; text-shadow: 0px 0px 30px #00d4ff; margin-bottom: 0px; }
    .sub-title { color: #FFD700; text-align: center; font-family: 'Courier New'; font-size: 22px; letter-spacing: 5px; margin-bottom: 30px; }
    
    /* VIP Kartlar */
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, #050505 0%, #1a1a1a 100%) !important;
        border: 2px solid #FFD700 !important;
        border-radius: 20px;
        padding: 25px !important;
        box-shadow: 0px 10px 30px rgba(255, 215, 0, 0.15);
    }
    
    /* Kayan Yazı (Ticker) */
    .ticker-wrap { background: #FFD700; color: black; padding: 5px; font-weight: bold; overflow: hidden; white-space: nowrap; }
    .ticker { display: inline-block; animation: ticker 30s linear infinite; }
    @keyframes ticker { 0% { transform: translateX(100%); } 100% { transform: translateX(-100%); } }

    /* Bilgi Kutusu */
    .legal-box {
        background-color: #0a0a0a;
        border: 1px solid #ff4b4b;
        padding: 20px;
        border-radius: 15px;
        color: #cccccc;
        font-size: 13px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. VERİ MOTORU (30+ COIN) ---
def get_crypto_data():
    # Listeyi genişlettim Sado'm, ekran dolsun!
    assets = ['BTCUSDT', 'ETHUSDT', 'SOLUSDT', 'AVAXUSDT', 'XRPUSDT', 'BNBUSDT', 'ADAUSDT', 'DOGEUSDT', 'DOTUSDT', 'LINKUSDT', 
              'MATICUSDT', 'NEARUSDT', 'SUIUSDT', 'FETUSDT', 'OPUSDT', 'ARBUSDT', 'TIAUSDT', 'PEPEUSDT', 'SHIBUSDT', 'RNDRUSDT',
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
            guc = int(((p - l) / (h - l)) * 100) if (h - l) != 0 else 0
            
            if guc > 85: status = "🚨 ZİRVE / PEAK"
            elif guc < 15: status = "💰 DİP / BOTTOM"
            else: status = "📈 ANALİZDE / TRACKING"

            rows.append({
                "SİNYAL": status,
                "COIN": item['symbol'].replace("USDT", ""),
                "FİYAT": p,
                "DEĞİŞİM (%)": ch,
                "HACİM (24S)": f"${v:,.1f}M",
                "GÜÇ (%)": guc
            })
        return pd.DataFrame(rows)
    except: return pd.DataFrame()

# --- 5. ÜST BİLGİ VE KAYAN YAZI ---
df = get_crypto_data()
ticker_text = " • ".join([f"{row['COIN']}: {row['FİYAT']}$ (%{row['DEĞİŞİM (%)']})" for _, row in df.iterrows()])
st.markdown(f"<div class='ticker-wrap'><div class='ticker'>{ticker_text}</div></div>", unsafe_allow_html=True)

st.markdown('<div class="main-title">SDR PRESTIGE GLOBAL</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">SADRETTİN TURAN VIP ANALYTICS SYSTEM</div>', unsafe_allow_html=True)

# --- 6. METRİKLER (ÖZET PANELİ) ---
if not df.empty:
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("💎 TOPLAM VARLIK", len(df))
    m2.metric("🔥 EN ÇOK ARTAN", f"{df.iloc[df['DEĞİŞİM (%)'].idxmax()]['COIN']}", f"%{df['DEĞİŞİM (%)'].max()}")
    m3.metric("📉 EN ÇOK DÜŞEN", f"{df.iloc[df['DEĞİŞİM (%)'].idxmin()]['COIN']}", f"%{df['DEĞİŞİM (%)'].min()}")
    m4.metric("📊 MARKET GÜCÜ", f"%{int(df['GÜÇ (%)'].mean())}")

    # --- 7. ANA TABLO VE GRAFİKLER ---
    tab1, tab2 = st.tabs(["📊 CANLI ANALİZ TABLOSU", "📈 TEKNİK GRAFİKLER"])
    
    with tab1:
        st.dataframe(df.sort_values(by="GÜÇ (%)", ascending=False), use_container_width=True, hide_index=True)
    
    with tab2:
        c1, c2 = st.columns(2)
        with c1:
            fig_guc = px.bar(df, x='COIN', y='GÜÇ (%)', color='GÜÇ (%)', color_continuous_scale='Turbo', title="COIN GÜÇ ENDEKSİ")
            fig_guc.update_layout(plot_bgcolor='black', paper_bgcolor='black', font=dict(color="white"))
            st.plotly_chart(fig_guc, use_container_width=True)
        with c2:
            fig_hacim = px.pie(df.head(10), values='GÜÇ (%)', names='COIN', title="DOMİNANS ANALİZİ (TOP 10)", hole=0.4)
            fig_hacim.update_layout(plot_bgcolor='black', paper_bgcolor='black', font=dict(color="white"))
            st.plotly_chart(fig_hacim, use_container_width=True)

# --- 8. YASAL UYARI VE STRATEJİ (ALT PANEL) ---
st.write("---")
l1, l2 = st.columns([2, 1])

with l1:
    st.markdown("""
    <div class='legal-box'>
        <h4 style='color:#ff4b4b; margin:0;'>⚠️ YASAL BİLGİLENDİRME / LEGAL DISCLAIMER</h4>
        Bu platformda yer alan bilgiler, grafikler ve sinyaller Sadrettin Turan VIP algoritması tarafından 
        üretilmektedir. <b>Kesinlikle yatırım danışmanlığı kapsamında değildir.</b> Kripto paralar yüksek risk 
        içerir; sadece kaybetmeyi göze aldığınız sermaye ile işlem yapınız. Veriler Binance API üzerinden 
        anlık çekilmektedir.
    </div>
    """, unsafe_allow_html=True)

with l2:
    st.markdown("""
    <div style='border:1px solid #FFD700; padding:15px; border-radius:15px;'>
        <h4 style='color:#FFD700; margin:0;'>👑 SDR VIP STRATEJİ</h4>
        <li><b>%85 Üstü:</b> Kar realizasyonu önerilir.</li>
        <li><b>%15 Altı:</b> Kademeli alım bölgesidir.</li>
        <li><b>Sinyal Takibi:</b> Trend yönünde kalın.</li>
    </div>
    """, unsafe_allow_html=True)

st.sidebar.markdown("### 👤 SADRETTİN TURAN VIP")
st.sidebar.write("Hoş geldin Paşam! Bugün piyasa senin kontrolünde.")
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2583/2583344.png", width=100)
st.sidebar.markdown("---")
st.sidebar.button("🔓 VIP ERİŞİMİ UZAT")
st.sidebar.write("© 2026 SDR GLOBAL PRESTIGE")
