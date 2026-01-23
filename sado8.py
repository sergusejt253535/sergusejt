import streamlit as st
from datetime import datetime, timedelta
import streamlit.components.v1 as components
from streamlit_autorefresh import st_autorefresh

# --- 1. AYARLAR ---
st.set_page_config(page_title="SDR PRESTIGE GLOBAL", layout="wide")
st_autorefresh(interval=15 * 1000, key="sdr_final_fix")

# --- 2. GÖRSEL TASARIM (CSS) ---
st.markdown("""
    <style>
    .stApp { background-color: #000000 !important; }
    .top-bar { display: flex; justify-content: space-between; align-items: center; padding: 15px; border-bottom: 2px solid #FFD700; margin-bottom: 20px; }
    .main-title { color: #00d4ff; text-align: center; font-family: 'Impact'; font-size: 60px; text-shadow: 0px 0px 30px #00d4ff; }
    .sub-title { color: #ffffff; text-align: center; font-family: 'Courier New'; font-size: 20px; letter-spacing: 5px; margin-bottom: 30px; font-weight: bold; }
    .info-box { background: #0a0a0a; border: 2px solid #FFD700; padding: 25px; border-radius: 15px; color: white; min-height: 300px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. ÜST PANEL ---
now_tr = datetime.utcnow() + timedelta(hours=3)
st.markdown(f"""
    <div class="top-bar">
        <div style='color:#00ffcc; font-weight:bold;'>📡 SDR CORE V3.1</div>
        <div style='color:white;'>📅 {now_tr.strftime("%d.%m.%Y")} | 🇹🇷 TR: {now_tr.strftime("%H:%M:%S")}</div>
        <div style='color:#FFD700; font-weight:bold;'>SDR PRESTIGE</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="main-title">SDR PRESTIGE GLOBAL</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">SADRETTİN TURAN VIP ANALYTICS</div>', unsafe_allow_html=True)

# --- 4. TRADINGVIEW SCREENER ---
st.markdown("### 💎 STRATEJİK PİYASA ANALİZİ / STRATEGIC MARKET ANALYSIS")
sdr_widget_code = """
<div class="tradingview-widget-container">
  <div class="tradingview-widget-container__widget"></div>
  <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-screener.js" async>
  {
  "width": "100%", "height": 600, "defaultColumn": "overview", "screener_type": "crypto_mkt",
  "displayCurrency": "USD", "colorTheme": "dark", "locale": "tr", "isTransparent": true,
  "symbols": { "tickers": [], "groups": [{ "name": "Binance", "originalName": "Binance" }] },
  "columns": ["base_currency_logoid", "name", "Recommend.All", "close", "change", "high", "low", "volume", "market_cap_calc"],
  "showToolbar": true
  }
  </script>
</div>
"""
components.html(sdr_widget_code, height=620)

# --- 5. BİLGİ KUTULARI (TR/EN) ---
st.write("---")
c1, c2 = st.columns(2)

with c1:
    st.markdown("""
        <div class="info-box" style="border-left: 10px solid #ff4b4b;">
            <h3 style='color:#ff4b4b;'>⚠️ YASAL UYARI / LEGAL NOTICE</h3>
            <p><b>[TR]:</b> Bu terminaldeki veriler bilgilendirme amaçlıdır. Yatırım danışmanlığı kapsamında değildir. Kripto paralar risk içerir, sorumluluk kullanıcıya aittir.</p>
            <hr style='border: 0.1px solid #333;'>
            <p><i><b>[EN]:</b> Information here is for tracking only. Not investment advice. Cryptocurrencies involve high risk; all responsibilities belong to the user.</i></p>
        </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
        <div class="info-box" style="border-left: 10px solid #FFD700;">
            <h3 style='color:#FFD700;'>🛡️ STRATEJİ / STRATEGY</h3>
            <p><b>[TR]:</b> Sıcak para akışı için "Hacim" ve "Teknik Derecelendirme" (Recommend) sütunlarını takip edin. Güçlü Al sinyalleri trend başlangıcı olabilir.</p>
            <hr style='border: 0.1px solid #333;'>
            <p><i><b>[EN]:</b> Track "Volume" and "Technical Rating" to catch hot money flows. Strong Buy signals may indicate the start of a trend.</i></p>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br><p style='text-align:center; opacity: 0.5; color:#FFD700;'>© 2026 SDR SADRETTİN TURAN • PRESTIGE GLOBAL TERMINAL</p>", unsafe_allow_html=True)
