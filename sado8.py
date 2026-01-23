import streamlit as st
import pandas as pd
import requests
import plotly.graph_objects as go
from datetime import datetime, timedelta
from streamlit_autorefresh import st_autorefresh

# --- 1. AYARLAR & TİCARİ KİMLİK ---
st.set_page_config(page_title="SDR PRESTIGE GLOBAL | V.4.5", layout="wide")
st_autorefresh(interval=15 * 1000, key="sdr_commercial_engine")

# --- 2. ÜST DÜZEY TASARIM (CSS) ---
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
    /* Lisans Yazısı */
    .license-text { color: #555; font-size: 12px; text-align: left; font-family: monospace; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. ZAMAN, TARİH VE LİSANS DURUMU ---
utc_now = datetime.utcnow()
tr_now = utc_now + timedelta(hours=3)

st.markdown(f"""
    <div class="top-bar">
        <div style='color:#00ffcc; font-weight:bold; font-size:20px;'>📡 SDR COMMERCIAL CORE V4.5</div>
        <div style='color:white; font-family:monospace; font-size:18px;'>
            📅 <b>DATE:</b> {tr_now.strftime("%d.%m.%Y")} | 
            <b>TR:</b> {tr_now.strftime("%H:%M:%S")}
        </div>
        <div style='color:#00f2ff; font-weight:bold; font-size:20px; letter-spacing:3px;'>SDR PRESTIGE</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="main-title">SDR PRESTIGE GLOBAL</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">SADRETTİN TURAN VIP ANALYTICS</div>', unsafe_allow_html=True)

# --- 4. SDR ÖZEL VERİ MOTORU ---
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
            
            # TİCARİ ANALİZ MODÜLÜ
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

if not df.empty:
    st.dataframe(df.style.format({"PRICE": "{:,.2f} $", "24H %": "% {:,.2f}", "SDR POWER %": "% {}"}).set_properties(**{
        'background-color': '#000', 'color': '#00f2ff', 'font-weight': 'bold'
    }), use_container_width=True, hide_index=True, height=500)

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
    st.info("📡 Initializing SDR Commercial Hub...")

# --- 5. LİSANS & UYARI ---
st.write("---")
st.markdown('<p class="license-text">LICENSE KEY: SDR-VIP-777-2026 | ACCESS: AUTHORIZED FOR SADRETTIN TURAN</p>', unsafe_allow_html=True)
c1, c2 = st.columns(2)
with c1:
    st.markdown("""<div class="info-box" style="border-left: 15px solid #ff4b4b;">
        <h3 style='color:#ff4b4b;'>⚠️ LEGAL DISCLAIMER</h3>
        <p>This software is a proprietary algorithmic trading terminal. Data provided is not financial advice. Past performance does not guarantee future results.</p>
    </div>""", unsafe_allow_html=True)
with c2:
    st.markdown("""<div class="info-box" style="border-left: 15px solid #00f2ff;">
        <h3 style='color:#00f2ff;'>🛡️ SDR METHODOLOGY</h3>
        <p>Proprietary logic monitors liquidity positioning and price displacement. Sell targets triggered above 88% displacement.</p>
    </div>""", unsafe_allow_html=True)
