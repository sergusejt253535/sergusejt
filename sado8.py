import streamlit as st
import pandas as pd
import requests
import plotly.graph_objects as go
from datetime import datetime, timedelta
from streamlit_autorefresh import st_autorefresh

# --- 1. AYARLAR ---
st.set_page_config(page_title="SDR PRESTIGE GLOBAL | V.6.4", layout="wide")
st_autorefresh(interval=10 * 1000, key="sdr_refined_v64")

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
    div[data-testid="stDataFrame"] { border: 2px solid #00f2ff !important; background-color: black !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. ÜST BAR ---
tr_now = datetime.utcnow() + timedelta(hours=3)
st.markdown(f"""
    <div class="top-bar">
        <div style='color:#00ffcc; font-weight:bold;'>📡 BINANCE LIVE STREAM</div>
        <div style='color:white; font-family:monospace;'>📅 {tr_now.strftime("%d.%m.%Y")} | 🇹🇷 {tr_now.strftime("%H:%M:%S")}</div>
        <div style='color:#00f2ff; font-weight:bold;'>SADRETTİN TURAN EDITION</div>
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

# --- 5. ANA TABLO STİLİ ---
def style_table(styler):
    styler.set_properties(**{'background-color': 'black', 'color': '#00f2ff', 'font-weight': 'bold'})
    def color_analysis(val):
        if "ZİRVE" in val: color = '#FF4B4B'
        elif "DİP" in val: color = '#00FF00'
        else: color = '#FFD700'
        return f'color: {color}; background-color: black; font-weight: bold;'
    styler.map(color_analysis, subset=['SDR VIP ANALYSIS'])
    return styler

if not df.empty:
    # Hatalı olan kısım burasıydı, şimdi kusursuz:
    styled_df = df.style.pipe(style_table).format({
        "PRICE": "{:,.2f} $", 
        "24H %": "% {:,.2f}", 
        "SDR POWER %": "% {}"
    })
    st.dataframe(styled_df, use_container_width=True, hide_index=True, height=450)

    st.write("---")
    
    # --- 6. ALT ANALİZ PANELİ (ÜÇLÜ) ---
    c1, c2, c3 = st.columns(3)
    
    with c1:
        fig1 = go.Figure(go.Bar(x=df['ASSET'], y=df['24H %'], marker_color='#00f2ff'))
        fig1.update_layout(title="Market Momentum (%)", template="plotly_dark", height=300, plot_bgcolor='black', paper_bgcolor='black', margin=dict(l=10, r=10, t=40, b=10))
        st.plotly_chart(fig1, use_container_width=True)
        
    with c2:
        avg_p = df['SDR POWER %'].mean()
        fig_g = go.Figure(go.Indicator(
            mode = "gauge+number", value = avg_p,
            gauge = {'axis': {'range': [0, 100], 'tickcolor': "white"}, 'bar': {'color': "#00f2ff"}, 'bgcolor': "black",
                     'steps': [{'range': [0, 20], 'color': "rgba(0, 255, 0, 0.3)"}, {'range': [80, 100], 'color': "rgba(255, 0, 0, 0.3)"}]},
            title = {'text': "MARKET POWER RADAR", 'font': {'size': 16, 'color': '#00f2ff'}}
        ))
        fig_g.update_layout(paper_bgcolor='black', height=300, font={'color': "white"}, margin=dict(l=10, r=10, t=40, b=10))
        st.plotly_chart(fig_g, use_container_width=True)
        
    with c3:
        fig2 = go.Figure(go.Scatter(x=df['ASSET'], y=df['SDR POWER %'], mode='lines+markers', line=dict(color='#FFD700', width=2)))
        fig2.update_layout(title="SDR Power Index", template="plotly_dark", height=300, plot_bgcolor='black', paper_bgcolor='black', margin=dict(l=10, r=10, t=40, b=10))
        st.plotly_chart(fig2, use_container_width=True)

# --- 7. FOOTER ---
st.write("---")
st.markdown("<p style='text-align:center; color:#00f2ff; opacity:0.5;'>© 2026 SADRETTİN TURAN • PRESTIGE GLOBAL TERMINAL</p>", unsafe_allow_html=True)
