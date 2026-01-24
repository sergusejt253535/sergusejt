import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta
from streamlit_autorefresh import st_autorefresh

# --- 1. AYARLAR ---
st.set_page_config(page_title="SDR PRESTIGE GLOBAL | V.7.0", layout="wide")
# Hızı tam 15 saniye yaptık
st_autorefresh(interval=15 * 1000, key="sdr_vizyon_v7")

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
    .info-box { 
        background: #080808; border: 1px solid #333; 
        padding: 25px; border-radius: 10px; color: white; min-height: 220px;
    }
    .vizyon-header { color: #00f2ff; font-weight: bold; border-bottom: 1px solid #00f2ff; margin-bottom: 10px; padding-bottom: 5px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. ÜST BAR ---
utc_now = datetime.utcnow()
tr_now = utc_now + timedelta(hours=3)

st.markdown(f"""
    <div class="top-bar">
        <div style='color:#00ffcc; font-weight:bold;'>📡 STRATEGIC LIVE FEED (BINANCE)</div>
        <div style='color:white; font-family:monospace; font-size:14px;'>
            📅 {tr_now.strftime("%d.%m.%Y")} | 🌐 UTC: {utc_now.strftime("%H:%M:%S")} | 🇹🇷 TR: {tr_now.strftime("%H:%M:%S")}
        </div>
        <div style='color:#00f2ff; font-weight:bold;'>SADRETTİN TURAN EXECUTIVE</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="main-title">SDR PRESTIGE GLOBAL</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">SADRETTİN TURAN VIP ANALYTICS</div>', unsafe_allow_html=True)

# --- 4. VERİ MOTORU (HAFIZA TEMİZLEME EKLENDİ) ---
@st.cache_data(ttl=10) # Veriyi sadece 10 saniye sakla, sonra çöpe at ve yenisini çek!
def get_sdr_data():
    coins = ["BTC","ETH","BNB","SOL","XRP","ADA","DOGE","AVAX","TRX","DOT","LINK","MATIC","NEAR","LTC","BCH","UNI","SHIB","SUI","PEPE","FET","RENDER","APT","STX","FIL","ARB","TIA","OP","INJ","KAS","LDO"]
    assets = ",".join(coins)
    # URL'ye zaman damgası ekledim ki her seferinde farklı bir istek sanıp taze veri versin
    url = f"https://min-api.cryptocompare.com/data/pricemultifull?fsyms={assets}&tsyms=USD&e=Binance&t={int(datetime.now().timestamp())}"
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
            rows.append({"STATUS": sig, "ASSET": coin, "PRICE": p, "24H %": c, "SDR POWER %": guc, "SDR VIP ANALYSIS": ana})
    except: return pd.DataFrame()
    return pd.DataFrame(rows)

df = get_sdr_data()

# --- 5. TABLO ---
if not df.empty:
    def style_table(styler):
        styler.set_properties(**{'background-color': 'black', 'color': '#00f2ff', 'font-weight': 'bold'})
        styler.map(lambda v: f"color: {'#FF4B4B' if 'ZİRVE' in v else '#00FF00' if 'DİP' in v else '#FFD700'}; background-color: black; font-weight: bold;", subset=['SDR VIP ANALYSIS'])
        return styler
    
    st.dataframe(df.style.pipe(style_table).format({"PRICE": "{:,.2f} $", "24H %": "% {:,.2f}", "SDR POWER %": "% {}"}), use_container_width=True, hide_index=True, height=600)
    st.markdown(f"<p style='color:#00ffcc; font-size:12px; text-align:right;'>🕒 Son Veri Güncelleme (TR): {datetime.now().strftime('%H:%M:%S')}</p>", unsafe_allow_html=True)

st.write("---")

# --- 6. VİZYONER BİLGİLENDİRME ---
inf1, inf2 = st.columns(2)
with inf1:
    st.markdown("""<div class="info-box" style="border-top: 4px solid #ff4b4b;">
        <div class="vizyon-header">⚠️ YASAL UYARI & LEGAL DISCLAIMER</div>
        <p style='font-size:13px; color:#ccc;'>
        <b>[TR]:</b> Bu terminal, Binance Global verilerini görselleştiren profesyonel bir takip aracıdır. Yatırım tavsiyesi değildir.<br><br>
        <b>[EN]:</b> This terminal tracks Binance Global data for professional visualization. Not financial advice.
        </p>
    </div>""", unsafe_allow_html=True)

with inf2:
    st.markdown("""<div class="info-box" style="border-top: 4px solid #00f2ff;">
        <div class="vizyon-header">🛡️ STRATEJİK VİZYON & METHODOLOGY</div>
        <p style='font-size:13px; color:#ccc;'>
        <b>[TR]:</b> SDR PRESTIGE METODOLOJİSİ; Binance Global verileriyle analiz yapar. Saf piyasa gücünü Sadrettin Turan standartlarında sunar.<br><br>
        <b>[EN]:</b> THE SDR PRESTIGE METHODOLOGY analyzes Binance Global data to deliver pure market power through Sadrettin Turan's standards.
        </p>
    </div>""", unsafe_allow_html=True)

st.markdown("<p style='text-align:center; color:#00f2ff; opacity:0.4; margin-top:30px; font-family:monospace;'>SADRETTİN TURAN EXCLUSIVE GLOBAL TERMINAL • SOURCE: BINANCE • EST. 2026</p>", unsafe_allow_html=True)
