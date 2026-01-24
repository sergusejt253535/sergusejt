import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta
from streamlit_autorefresh import st_autorefresh

# --- 1. AYARLAR ---
st.set_page_config(page_title="SDR PRESTIGE GLOBAL | V.7.1", layout="wide")
st_autorefresh(interval=15 * 1000, key="sdr_final_fix")

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
    </style>
    """, unsafe_allow_html=True)

# --- 3. ÜST BAR ---
tr_now = datetime.utcnow() + timedelta(hours=3)
st.markdown(f"""
    <div class="top-bar">
        <div style='color:#00ffcc; font-weight:bold;'>📡 STRATEGIC LIVE FEED (BINANCE)</div>
        <div style='color:white; font-family:monospace;'>📅 {tr_now.strftime("%d.%m.%Y")} | 🇹🇷 TR: {tr_now.strftime("%H:%M:%S")}</div>
        <div style='color:#00f2ff; font-weight:bold;'>SADRETTİN TURAN EXECUTIVE</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="main-title">SDR PRESTIGE GLOBAL</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">SADRETTİN TURAN VIP ANALYTICS</div>', unsafe_allow_html=True)

# --- 4. VERİ MOTORU (EN SADE HALİ) ---
def get_sdr_data():
    coins = ["BTC","ETH","BNB","SOL","XRP","ADA","DOGE","AVAX","TRX","DOT","LINK","MATIC","NEAR","LTC","BCH","UNI","SHIB","SUI","PEPE","FET","RENDER","APT","STX","FIL","ARB","TIA","OP","INJ","KAS","LDO"]
    assets = ",".join(coins)
    url = f"https://min-api.cryptocompare.com/data/pricemultifull?fsyms={assets}&tsyms=USD&e=Binance"
    try:
        r = requests.get(url, timeout=15).json()['RAW']
        rows = []
        for coin in r:
            i = r[coin]['USD']
            p, h, l, c = i['PRICE'], i['HIGH24HOUR'], i['LOW24HOUR'], i['CHANGEPCT24HOUR']
            guc = int(((p - l) / (h - l)) * 100) if (h-l) != 0 else 50
            if guc > 85: ana = "🛡️ ZİRVE: Kâr Al"
            elif guc < 20: ana = "💰 DİP: Kademeli Al"
            else: ana = "📈 TREND TAKİBİ"
            rows.append({"ASSET": coin, "PRICE": f"{p:,.2f} $", "24H %": f"% {c:.2f}", "SDR POWER": f"% {guc}", "ANALYSIS": ana})
        return pd.DataFrame(rows)
    except: return pd.DataFrame()

df = get_sdr_data()

# --- 5. TABLO (HİÇBİR RİSK ALMADAN ÇİZİYORUZ) ---
if not df.empty:
    st.table(df) # En sağlam tablo komutu budur, asla sekmez!
else:
    st.error("Veri bekleniyor... Lütfen bekleyin paşam.")

st.markdown(f"<p style='text-align:right; color:#00ffcc;'>🕒 Sync: {tr_now.strftime('%H:%M:%S')}</p>", unsafe_allow_html=True)
