import streamlit as st
import pandas as pd
import requests
import plotly.graph_objects as go
from datetime import datetime, timedelta
from streamlit_autorefresh import st_autorefresh

# --- 1. AYARLAR & HIZ ---
st.set_page_config(page_title="SDR PRESTIGE GLOBAL | V.6.2", layout="wide")
st_autorefresh(interval=10 * 1000, key="sdr_prestige_v62")

# --- 2. ÜST DÜZEY GÖRSEL TASARIM (CSS) ---
st.markdown("""
    <style>
    .stApp { background-color: #000000 !important; }
    .top-bar { 
        display: flex; justify-content: space-between; align-items: center; 
        padding: 15px; border-bottom: 2px solid #00f2ff; 
        background: linear-gradient(90deg, #050505 0%, #001a1a 100%); 
    }
    /* Balina Takip Bandı Animasyonu */
    .whale-alert {
        background: #001a1a; color: #00f2ff; padding: 5px;
        font-family: monospace; overflow: hidden; white-space: nowrap;
        border-bottom: 1px solid #00f2ff; margin-bottom: 20px;
    }
    .main-title { 
        color: #00f2ff; text-align: center; font-family: 'Impact'; 
        font-size: 70px; text-shadow: 0px 0px 35px #00f2ff; margin-bottom: -10px;
    }
    .sub-title { 
        color: #FFD700; text-align: center; font-family: 'Courier New'; 
        font-size: 26px; letter-spacing: 10px; margin-bottom: 30px; 
        font-weight: bold; text-shadow: 0px 0px 15px #FFD700;
    }
    div[data-testid="stDataFrame"] { border: 2px solid #00f2ff !important; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. WHALE TRACKER & ZAMAN ---
tr_now = datetime.utcnow() + timedelta(hours=3)
st.markdown(f"""
    <div class="whale-alert">
        <marquee scrollamount="5">📡 [SDR WHALE ALERT]: LARGE BUY ORDER DETECTED ON BTC/USDT | LIQUIDITY FLOWING INTO SUI | PRESTIGE TERMINAL ACTIVE...</marquee>
    </div>
    <div class="top-bar">
        <div style='color:#00f2ff; font-weight:bold;'>🔐 VIP SECURE ACCESS</div>
        <div style='color:white; font-family:monospace;'>🇹🇷 {tr_now.strftime("%H:%M:%S")}</div>
        <div style='color:#FFD700; font-weight:bold;'>SADRETTİN TURAN EDITION</div>
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
            
            if guc > 85: ana, sig = "🛡️ ZİRVE: Kâr Al / TAKE PROFIT", "🔴 SELL"
            elif guc < 20: ana, sig = "💰 DİP: Kademeli Al / ACCUMULATE", "🟢 BUY"
            else: ana, sig = "📈 TREND TAKİBİ: Bekle / HOLDING", "🥷 WAIT"

            rows.append({
                "STATUS": sig, "ASSET": coin, "PRICE": p, 
                "24H %": c, "SDR POWER %": guc, "SDR VIP ANALYSIS": ana
            })
    except: return pd.DataFrame()
    return pd.DataFrame(rows)

df = get_sdr_data()

# --- 5. LİKİDİTE RADARI (GAUGE) ---
if not df.empty:
    avg_power = df['SDR POWER %'].mean()
    fig_gauge = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = avg_power,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "SDR MARKET LIQUIDITY RADAR", 'font': {'color': "#00f2ff", 'size': 20}},
        gauge = {
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "white"},
            'bar': {'color': "#00f2ff"},
            'bgcolor': "black",
            'borderwidth': 2,
            'bordercolor': "#00f2ff",
            'steps': [
                {'range': [0, 25], 'color': 'rgba(0, 255, 0, 0.3)'},
                {'range': [75, 100], 'color': 'rgba(255, 0, 0, 0.3)'}
            ],
            'threshold': {'line': {'color': "yellow", 'width': 4}, 'thickness': 0.75, 'value': avg_power}
        }
    ))
    fig_gauge.update_layout(paper_bgcolor = 'black', font = {'color': "white", 'family': "Arial"}, height=300)
    st.plotly_chart(fig_gauge, use_container_width=True)

    # --- TABLO ---
    def style_table(styler):
        styler.set_properties(**{'background-color': 'black', 'color': '#00f2ff', 'font-weight': 'bold'})
        def color_analysis(val):
            if "ZİRVE" in val: color = '#FF4B4B'
            elif "DİP" in val: color = '#00FF00'
            else: color = '#FFD700'
            return f'color: {color}; background-color: black;'
        styler.map(color_analysis, subset=['SDR VIP ANALYSIS'])
        return styler

    styled_df = df.style.pipe(style_table).format({"PRICE": "{:,.2f} $", "24H %": "% {:,.2f}", "SDR POWER %": "% {}"})
    st.dataframe(styled_df, use_container_width=True, hide_index=True)

else:
    st.info("📡 Connecting to Sadrettin Turan's Hub...")

# --- ALT BİLGİ ---
st.markdown("<p style='text-align:center; color:#00f2ff; opacity:0.6;'>SDR PRESTIGE • ARCHITECT: SADRETTİN TURAN • V6.2</p>", unsafe_allow_html=True)
