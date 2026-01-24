import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta
from streamlit_autorefresh import st_autorefresh

# --- 1. AYARLAR ---
st.set_page_config(page_title="SDR PRESTIGE GLOBAL | V.8.0", layout="wide")
# 15 saniyede bir sayfayı yeniler, taze kan pompalar
st_autorefresh(interval=15 * 1000, key="sdr_final_fortress")

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
    /* Tablonun içindeki yazıları beyaz ve okunur yapar */
    div[data-testid="stTable"] { 
        background-color: #000000; 
        color: #00f2ff;
        border: 1px solid #333;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. ÜST BAR ---
tr_now = datetime.utcnow() + timedelta(hours=3)
st.markdown(f"""
    <div class="top-bar">
        <div style='color:#00ffcc; font-weight:bold;'>📡 STRATEGIC LIVE FEED (BINANCE SOURCE)</div>
        <div style='color:white; font-family:monospace;'>📅 {tr_now.strftime("%d.%m.%Y")} | 🇹🇷 TR: {tr_now.strftime("%H:%M:%S")}</div>
        <div style='color:#00f2ff; font-weight:bold;'>SADRETTİN TURAN EXECUTIVE</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="main-title">SDR PRESTIGE GLOBAL</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">SADRETTİN TURAN VIP ANALYTICS</div>', unsafe_allow_html=True)

# --- 4. VERİ MOTORU ---
def get_sdr_data():
    coins = ["BTC","ETH","BNB","SOL","XRP","ADA","DOGE","AVAX","TRX","DOT","LINK","MATIC","NEAR","LTC","BCH","UNI","SHIB","SUI","PEPE","FET","RENDER","APT","STX","FIL","ARB","TIA","OP","INJ","KAS","LDO"]
    assets = ",".join(coins)
    # URL'ye zaman damgası ekledik ki her seferinde yeni veri gelsin
    url = f"https://min-api.cryptocompare.com/data/pricemultifull?fsyms={assets}&tsyms=USD&e=Binance&t={int(datetime.now().timestamp())}"
    try:
        response = requests.get(url, timeout=15)
        data = response.json()
        if 'RAW' in data:
            r = data['RAW']
            rows = []
            for coin in r:
                i = r[coin]['USD']
                p, h, l, c = i['PRICE'], i['HIGH24HOUR'], i['LOW24HOUR'], i['CHANGEPCT24HOUR']
                # SDR Güç Endeksi Hesaplama
                guc = int(((p - l) / (h - l)) * 100) if (h-l) != 0 else 50
                guc = max(min(guc, 99), 1)
                
                if guc > 85: ana = "🛡️ ZİRVE: Kâr Al / TAKE PROFIT"
                elif guc < 20: ana = "💰 DİP: Kademeli Al / BUY"
                else: ana = "📈 TREND TAKİBİ: HOLD"
                
                rows.append({
                    "ASSET": f"💎 {coin}",
                    "PRICE": f"{p:,.2f} $",
                    "24H %": f"{c:+.2f}%",
                    "SDR POWER": f"% {guc}",
                    "ANALYSIS": ana
                })
            return pd.DataFrame(rows)
        return pd.DataFrame()
    except Exception as e:
        return pd.DataFrame()

df = get_sdr_data()

# --- 5. TABLO VE GÖSTERİM ---
if not df.empty:
    # Bu sefer en sağlam ve okunur olan st.table kullanıyoruz
    st.table(df)
else:
    st.warning("📡 Veri senkronize ediliyor... Lütfen bekleyin paşam.")

st.markdown(f"<p style='text-align:right; color:#00ffcc; font-size:12px;'>🕒 Live Sync: {tr_now.strftime('%H:%M:%S')}</p>", unsafe_allow_html=True)

st.write("---")

# --- 6. BİLGİLENDİRME ---
inf1, inf2 = st.columns(2)
with inf1:
    st.markdown('<div style="background:#080808; padding:15px; border-radius:10px; border-top: 3px solid #ff4b4b; color:white;">'
                '<b>⚠️ LEGAL DISCLAIMER:</b> Bu terminal Binance verilerini izler. Yatırım tavsiyesi içermez.</div>', unsafe_allow_html=True)
with inf2:
    st.markdown('<div style="background:#080808; padding:15px; border-radius:10px; border-top: 3px solid #00f2ff; color:white;">'
                '<b>🛡️ SDR METHODOLOGY:</b> Saf piyasa gücü Sadrettin Turan standartlarında analiz edilir.</div>', unsafe_allow_html=True)
