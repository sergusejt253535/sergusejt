import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px
from streamlit_autorefresh import st_autorefresh
import streamlit.components.v1 as components

# --- 1. AYARLAR ---
st.set_page_config(page_title="SDR PRESTIGE GLOBAL", layout="wide")
st_autorefresh(interval=20 * 1000, key="sdr_js_engine")

# --- 2. CSS TASARIM ---
st.markdown("""
    <style>
    .stApp { background-color: #000000 !important; }
    .top-bar { display: flex; justify-content: space-between; align-items: center; padding: 15px; border-bottom: 3px solid #FFD700; margin-bottom: 15px; }
    .main-title { color: #00d4ff; text-align: center; font-family: 'Arial Black'; font-size: 55px; text-shadow: 0px 0px 30px #00d4ff; }
    .sub-title { color: #ffffff; text-align: center; font-family: 'Courier New'; font-size: 20px; letter-spacing: 5px; margin-bottom: 20px; }
    div[data-testid="stDataFrame"] { background-color: #000000 !important; border: 4px solid #FFD700 !important; border-radius: 15px; }
    .stDataFrame td { color: #FFD700 !important; font-weight: bold !important; font-size: 18px !important; }
    .info-box { background-color: #111; border: 2px solid #FFD700; padding: 25px; border-radius: 15px; color: white; min-height: 250px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. VERİ MOTORU (BROWSER-SIDE FETCH) ---
@st.cache_data(ttl=15)
def get_data_via_python():
    # Sunucu üzerinden deneme (eğer çalışırsa)
    assets = ['BTCUSDT', 'ETHUSDT', 'SOLUSDT', 'AVAXUSDT', 'XRPUSDT', 'BNBUSDT', 'ADAUSDT', 'DOGEUSDT', 'DOTUSDT', 'LINKUSDT', 'MATICUSDT', 'TRXUSDT', 'UNIUSDT', 'BCHUSDT', 'SUIUSDT', 'FETUSDT', 'RENDERUSDT', 'PEPEUSDT', 'SHIBUSDT']
    url = "https://api.binance.com/api/v3/ticker/24hr"
    try:
        r = requests.get(url, timeout=5)
        data = r.json()
        return [d for d in data if d['symbol'] in assets]
    except:
        return None

# Alternatif: Eğer sunucu engellendiyse manuel bir veri oluşturup tabloyu diri tutalım
def process_rows(raw_data):
    assets = ['BTCUSDT', 'ETHUSDT', 'SOLUSDT', 'AVAXUSDT', 'XRPUSDT', 'BNBUSDT', 'ADAUSDT', 'DOGEUSDT', 'DOTUSDT', 'LINKUSDT', 'MATICUSDT', 'TRXUSDT', 'UNIUSDT', 'BCHUSDT', 'SUIUSDT', 'FETUSDT', 'RENDERUSDT', 'PEPEUSDT', 'SHIBUSDT']
    rows = []
    if raw_data:
        for item in raw_data:
            p, h, l = float(item['lastPrice']), float(item['highPrice']), float(item['lowPrice'])
            v = (float(item['quoteVolume']) / 1_000_000) / 24
            guc = int(((p - l) / (h - l)) * 100) if (h - l) != 0 else 50
            guc = max(min(guc, 99), 1)
            
            if guc > 88: sig, ana = "🛡️ SELL", "🚨 ZİRVE: Kâr Al / PEAK: Take Profit"
            elif guc < 15: sig, ana = "💰 BUY", "🔥 DİP: Topla / BOTTOM: Accumulate"
            else: sig, ana = "📈 FOLLOW", "💎 TREND: Takip / TREND: Watch"
            
            rows.append({"SDR SİNYAL": sig, "VARLIK / ASSET": item['symbol'].replace("USDT", ""), "FİYAT / PRICE": f"{p:,.2f} $", "HACİM / VOL (1H)": f"${v:,.2f} M", "GÜÇ / POWER (%)": f"%{guc}", "POWER_NUM": guc, "ANALİZ / ANALYSIS": ana})
    else:
        # Veri gelmiyorsa en azından yapıyı göster
        for sym in assets:
            rows.append({"SDR SİNYAL": "⌛ BEKLİYOR", "VARLIK / ASSET": sym.replace("USDT", ""), "FİYAT / PRICE": "Yenileyin", "HACİM / VOL (1H)": "---", "GÜÇ / POWER (%)": "---", "POWER_NUM": 0, "ANALİZ / ANALYSIS": "Tarayıcıyı Yenilemeyi Deneyin"})
    return pd.DataFrame(rows)

# --- 4. PANEL ---
su_an_tr = datetime.utcnow() + timedelta(hours=3)

st.markdown(f"""
    <div class="top-bar">
        <div style='color:#00ffcc;'>📡 SDR BROWSER GATEWAY</div>
        <div style='color:white;'>📅 {su_an_tr.strftime("%d.%m.%Y")} | 🇹🇷 TR: {su_an_tr.strftime("%H:%M:%S")}</div>
        <div style='color:#FFD700;'>SDR PRESTIGE</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="main-title">SDR PRESTIGE GLOBAL</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">SADRETTİN TURAN VIP ANALYTICS</div>', unsafe_allow_html=True)

# Veriyi çek ve işle
import requests
raw = get_data_via_python()
df = process_rows(raw)

st.dataframe(df[["SDR SİNYAL", "VARLIK / ASSET", "FİYAT / PRICE", "HACİM / VOL (1H)", "GÜÇ / POWER (%)", "ANALİZ / ANALYSIS"]].style.set_properties(**{
    'background-color': '#000000', 'color': '#FFD700', 'font-weight': 'bold'
}), use_container_width=True, hide_index=True, height=600)

# --- 5. BİLGİ KUTULARI ---
st.write("---")
c1, c2 = st.columns(2)
with c1:
    st.markdown("""<div class="info-box" style="border-left: 12px solid #ff4b4b;">
        <h3 style='color:#ff4b4b;'>⚠️ YASAL UYARI / LEGAL NOTICE</h3>
        <p><b>[TR]:</b> Bu paneldeki veriler bilgilendirme amaçlıdır. Yatırım tavsiyesi değildir. Kripto paralar risk içerir, sorumluluk kullanıcıya aittir.</p>
        <p><i><b>[EN]:</b> For informational purposes only. Not investment advice. Users assume all risk.</i></p>
    </div>""", unsafe_allow_html=True)
with c2:
    st.markdown("""<div class="info-box" style="border-left: 12px solid #FFD700;">
        <h3 style='color:#FFD700;'>🛡️ SDR STRATEJİ / STRATEGY</h3>
        <p><b>[TR]:</b> %88+ Kâr Al, %15- Kademeli Topla. Binance verileri IP engeli yoksa 15 saniyede bir akar.</p>
        <p><i><b>[EN]:</b> 88%+ Take Profit, 15%- Accumulate. Data flows every 15s if no IP block.</i></p>
    </div>""", unsafe_allow_html=True)

st.markdown("<p style='text-align:center; opacity: 0.6; color:#FFD700;'>© 2026 SDR SADRETTİN TURAN • PRESTIGE GLOBAL</p>", unsafe_allow_html=True)
