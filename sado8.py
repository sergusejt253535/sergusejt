import streamlit as st
import pandas as pd
import requests
import plotly.graph_objects as go
from datetime import datetime, timedelta
from streamlit_autorefresh import st_autorefresh

# --- 1. AYARLAR ---
st.set_page_config(page_title="SDR PRESTIGE GLOBAL | V.5.5", layout="wide")
st_autorefresh(interval=15 * 1000, key="sdr_smart_colors_v55")

# --- 2. ÖZEL TASARIM (CSS) ---
st.markdown("""
    <style>
    .stApp { background-color: #000000 !important; }
    .top-bar { 
        display: flex; justify-content: space-between; align-items: center; 
        padding: 20px; border-bottom: 3px solid #00f2ff; 
        margin-bottom: 25px; background: #050505; 
    }
    .main-title { 
        color: #00f2ff; text-align: center; font-family: 'Impact'; 
        font-size: 65px; text-shadow: 0px 0px 30px #00f2ff; 
        margin-bottom: 0px;
    }
    .sub-title { 
        color: #FFD700; text-align: center; font-family: 'Courier New'; 
        font-size: 24px; letter-spacing: 8px; margin-bottom: 35px; 
        font-weight: bold; text-shadow: 0px 0px 10px #FFD700;
    }
    div[data-testid="stDataFrame"] { border: 2px solid #00f2ff !important; border-radius: 15px; }
    .info-box { 
        background: #080808; border: 2px solid #00f2ff; 
        padding: 35px; border-radius: 20px; color: white; 
    }
    .license-text { color: #555; font-size: 12px; text-align: left; font-family: monospace; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. ZAMAN VE TARİH ---
utc_now = datetime.utcnow()
tr_now = utc_now + timedelta(hours=3)

st.markdown(f"""
    <div class="top-bar">
        <div style='color:#00ffcc; font-weight:bold; font-size:20px;'>📡 SDR COMMERCIAL CORE V5.5</div>
        <div style='color:white; font-family:monospace; font-size:16px;'>
            📅 {tr_now.strftime("%d.%m.%Y")} | 
            🌐 <b>UTC:</b> {utc_now.strftime("%H:%M:%S")} | 
            🇹🇷 <b>TR:</b> {tr_now.strftime("%H:%M:%S")}
        </div>
        <div style='color:#00f2ff; font-weight:bold; font-size:20px; letter-spacing:3px;'>SDR PRESTIGE</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="main-title">SDR PRESTIGE GLOBAL</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">SADRETTİN TURAN VIP ANALYTICS</div>', unsafe_allow_html=True)

# --- 4. VERİ MOTORU ---
def get_sdr_data():
    assets = "BTC,ETH,SOL,AVAX,XRP,BNB,ADA,DOGE,LINK,SUI,PEPE,FET,RENDER,MATIC"
    url = f"https://min-api.cryptocompare.com/data/pricemultifull?fsyms={assets}&tsyms=USD"
    rows = []
    try:
        r = requests.get(url, timeout=10).json()['RAW']
        for coin in r:
            i = r[coin]['USD']
            p, h, l, c = i['PRICE'], i['HIGH24HOUR'], i['LOW24HOUR'], i['CHANGEPCT24HOUR']
            guc = int(((p - l) / (h - l)) * 100) if (h-l) != 0 else 50
            guc = max(min(guc, 99), 1)
            
            if guc > 88: ana, sig = "🛡️ ZİRVE: Kâr Al / PEAK: Take Profit", "🔴 SELL"
            elif guc < 15: ana, sig = "💰 DİP: Kademeli Al / BOTTOM: Accumulate", "🟢 BUY"
            else: ana, sig = "📈 TREND TAKİBİ: Bekle / TREND WATCH: Wait", "🥷 WAIT"

            rows.append({
                "STATUS": sig, "ASSET": coin, "PRICE": p, 
                "24H %": c, "SDR POWER %": guc, "SDR VIP ANALYSIS": ana
            })
    except: return pd.DataFrame()
    return pd.DataFrame(rows)

df = get_sdr_data()

# Dinamik Renklendirme Fonksiyonu
def apply_analysis_colors(val):
    if "ZİRVE" in val: color = '#FF4B4B'  # Kırmızı
    elif "DİP" in val: color = '#00FF00'   # Yeşil
    else: color = '#FFD700'                # Altın Sarısı
    return f'color: {color}; font-weight: bold; background-color: #000;'

if not df.empty:
    styled_df = df.style.format({
        "PRICE": "{:,.2f} $", "24H %": "% {:,.2f}", "SDR POWER %": "% {}"
    }).set_properties(**{
        'background-color': '#000', 'color': '#00f2ff', 'font-weight': 'bold'
    }, subset=['STATUS', 'ASSET', 'PRICE', '24H %', 'SDR POWER %']).map(
        apply_analysis_colors, subset=['SDR VIP ANALYSIS']
    )

    st.dataframe(styled_df, use_container_width=True, hide_index=True, height=500)

    st.write("---")
    g1, g2 = st.columns(2)
    with g1:
        fig1 = go.Figure(go.Bar(x=df['ASSET'], y=df['24H %'], marker_color='#00f2ff'))
        fig1.update_layout(title="Market Momentum (%)", template="plotly_dark", plot_bgcolor='black', paper_bgcolor='black')
        st.plotly_chart(fig1, use_container_width=True)
    with g2:
        fig2 = go.Figure(go.Scatter(x=df['ASSET'], y=df['SDR POWER %'], mode='lines+markers', line=dict(color='#00f2ff', width=3)))
        fig2.update_layout(title="SDR Algorithmic Power Index", template="plotly_dark", plot_bgcolor='black', paper_bgcolor='black')
        st.plotly_chart(fig2, use_container_width=True)
else:
    st.info("📡 Refreshing Smart Analysis...")

# --- 5. BİLGİLENDİRME ---
st.write("---")
st.markdown('<p class="license-text">LICENSE KEY: SDR-VIP-777-2026 | ACCESS: AUTHORIZED FOR SADRETTIN TURAN</p>', unsafe_allow_html=True)
c1, c2 = st.columns(2)
with c1:
    st.markdown("""<div class="info-box" style="border-left: 15px solid #ff4b4b;">
        <h3 style='color:#ff4b4b;'>⚠️ YASAL UYARI / LEGAL NOTICE</h3>
        <p><b>[TR]:</b> Sunulan veriler yatırım tavsiyesi değildir.</p>
        <hr style='border: 0.1px solid #333;'>
        <p><i><b>[EN]:</b> Data provided is not financial advice.</i></p>
    </div>""", unsafe_allow_html=True)
with c2:
    st.markdown("""<div class="info-box" style="border-left: 15px solid #00f2ff;">
        <h3 style='color:#00f2ff;'>🛡️ SDR METODOLOJİ / METHODOLOGY</h3>
        <p><b>[TR]:</b> SDR modeli, <b>Binance Global</b> verilerini analiz eder. Renk kodları risk bölgelerini temsil eder.</p>
        <hr style='border: 0.1px solid #333;'>
        <p><i><b>[EN]:</b> The SDR model analyzes <b>Binance Global</b> data. Color codes represent risk zones.</i></p>
    </div>""", unsafe_allow_html=True)

st.markdown("<p style='text-align:center; opacity: 0.5; color:#00f2ff;'>© 2026 SDR SADRETTİN TURAN • PRESTIGE GLOBAL TERMINAL</p>", unsafe_allow_html=True)
