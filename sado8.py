import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import streamlit.components.v1 as components
from streamlit_autorefresh import st_autorefresh

# --- 1. AYARLAR ---
st.set_page_config(page_title="SDR PRESTIGE GLOBAL", layout="wide")
st_autorefresh(interval=30 * 1000, key="sdr_immortal_engine")

# --- 2. CSS TASARIM ---
st.markdown("""
    <style>
    .stApp { background-color: #000000 !important; }
    .top-bar { display: flex; justify-content: space-between; align-items: center; padding: 15px; border-bottom: 3px solid #FFD700; margin-bottom: 15px; }
    .main-title { color: #00d4ff; text-align: center; font-family: 'Arial Black'; font-size: 55px; text-shadow: 0px 0px 30px #00d4ff; }
    .sub-title { color: #ffffff; text-align: center; font-family: 'Courier New'; font-size: 20px; letter-spacing: 5px; margin-bottom: 20px; }
    .info-box { background-color: #111; border: 2px solid #FFD700; padding: 25px; border-radius: 15px; color: white; min-height: 250px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. PANEL ÜST KISIM ---
su_an_tr = datetime.utcnow() + timedelta(hours=3)
st.markdown(f"""
    <div class="top-bar">
        <div style='color:#00ffcc; font-weight:bold;'>📡 SDR GLOBAL REAL-TIME FEED</div>
        <div style='color:white;'>📅 {su_an_tr.strftime("%d.%m.%Y")} | 🇹🇷 TR: {su_an_tr.strftime("%H:%M:%S")}</div>
        <div style='color:#FFD700; font-weight:bold;'>SDR PRESTIGE</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="main-title">SDR PRESTIGE GLOBAL</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">SADRETTİN TURAN VIP ANALYTICS</div>', unsafe_allow_html=True)

# --- 4. TRADINGVIEW MARKET TERMINAL (BU ASLA BOŞ GELMEZ) ---
# Bu bileşen veriyi doğrudan senin tarayıcın üzerinden çeker.
st.markdown("### 💎 CANLI PİYASA ANALİZİ / LIVE MARKET ANALYSIS")
tradingview_widget = """
<div class="tradingview-widget-container">
  <div class="tradingview-widget-container__widget"></div>
  <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-screener.js" async>
  {
  "width": "100%",
  "height": "600",
  "defaultColumn": "overview",
  "screener_type": "crypto_mkt",
  "displayCurrency": "USD",
  "colorTheme": "dark",
  "locale": "tr",
  "isTransparent": true
  }
  </script>
</div>
"""
components.html(tradingview_widget, height=600)

# --- 5. DETAYLI BİLGİ KUTULARI (UZUN VE DETAYLI) ---
st.write("---")
c1, c2 = st.columns(2)

with c1:
    st.markdown("""<div class="info-box" style="border-left: 12px solid #ff4b4b;">
        <h3 style='color:#ff4b4b;'>⚠️ YASAL UYARI / LEGAL NOTICE</h3>
        <p><b>[TR]:</b> SDR Prestige Global terminalinde sunulan tüm veriler bilgilendirme amaçlıdır. Kripto paralar yüksek riskli varlıklardır. Burada yer alan bilgiler yatırım danışmanlığı (sıcak para garantisi, kesin kâr vb.) içermez. Tüm yatırım kararları ve oluşabilecek riskler tamamen kullanıcıya aittir. İşlem yapmadan önce uzman yardımı alınız.</p>
        <hr style='border:0.1px solid #333'>
        <p><i><b>[EN]:</b> All data and analysis presented on the SDR Prestige Global terminal are for informational purposes only. Cryptocurrencies are high-risk assets. The information provided here does not constitute investment advice. All investment decisions and risks belong to the user.</i></p>
    </div>""", unsafe_allow_html=True)

with c2:
    st.markdown("""<div class="info-box" style="border-left: 12px solid #FFD700;">
        <h3 style='color:#FFD700;'>🛡️ SDR STRATEJİ / STRATEGY</h3>
        <p><b>[TR]:</b> Piyasadaki ani fırsatları yakalamak için RSI ve Hacim göstergelerini takip edin. Tablodaki "Al" sinyalleri genellikle fiyatın 24 saatlik dip seviyesine (%15 ve altı) yakın olduğunu gösterir. Sıcak para akışını takip etmek için hacim artışı (Volume) olan coinlere odaklanın. Sistem TradingView altyapısıyla kesintisiz güncellenir.</p>
        <hr style='border:0.1px solid #333'>
        <p><i><b>[EN]:</b> Focus on volume spikes to track "hot money" flow. The strategy points to accumulation zones when the price is near its 24-hour low. The system is powered by TradingView for zero-latency updates.</i></p>
    </div>""", unsafe_allow_html=True)

st.markdown("<p style='text-align:center; opacity: 0.6; color:#FFD700;'>© 2026 SDR SADRETTİN TURAN • PRESTIGE GLOBAL TERMINAL</p>", unsafe_allow_html=True)
