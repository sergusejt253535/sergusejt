import streamlit as st
from datetime import datetime, timedelta
import streamlit.components.v1 as components
from streamlit_autorefresh import st_autorefresh

# --- 1. AYARLAR ---
st.set_page_config(page_title="SDR PRESTIGE GLOBAL", layout="wide")

# 15 Saniyede bir sayfayı canlı tutar
st_autorefresh(interval=15 * 1000, key="sdr_prestige_refresh")

# --- 2. CSS TASARIM (PRESTIGE GÖRÜNÜM) ---
st.markdown("""
    <style>
    .stApp { background-color: #000000 !important; }
    .top-bar { display: flex; justify-content: space-between; align-items: center; padding: 15px; border-bottom: 3px solid #FFD700; margin-bottom: 15px; }
    .main-title { color: #00d4ff; text-align: center; font-family: 'Arial Black'; font-size: 55px; text-shadow: 0px 0px 30px #00d4ff; margin-bottom: 0px; }
    .sub-title { color: #ffffff; text-align: center; font-family: 'Courier New'; font-size: 20px; letter-spacing: 5px; margin-bottom: 20px; font-weight: bold; }
    .info-box { background-color: #0a0a0a; border: 2px solid #FFD700; padding: 25px; border-radius: 15px; color: white; min-height: 280px; box-shadow: 0px 0px 20px rgba(255, 215, 0, 0.1); }
    hr { border: 0.1px solid #333 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. ÜST PANEL ---
su_an_tr = datetime.utcnow() + timedelta(hours=3)

st.markdown(f"""
    <div class="top-bar">
        <div style='color:#00ffcc; font-weight:bold;'>📡 SDR PRESTIGE ENGINE | V3.0</div>
        <div style='color:white; font-size:16px;'>📅 {su_an_tr.strftime("%d.%m.%Y")} | 🇹🇷 TR: {su_an_tr.strftime("%H:%M:%S")}</div>
        <div style='color:#FFD700; font-weight:bold; letter-spacing:2px;'>SDR TERMINAL</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="main-title">SDR PRESTIGE GLOBAL</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">SADRETTİN TURAN VIP ANALYTICS</div>', unsafe_allow_html=True)

# --- 4. ÖZELLEŞTİRİLMİŞ ANALİZ TABLOSU (TRADINGVIEW CORE) ---
# Burada tabloyu senin istediğin 'Analiz' ağırlıklı hale getirdim
st.markdown("### 💎 SDR VIP PİYASA ANALİZİ / VIP MARKET ANALYSIS")

sdr_widget = """
<div class="tradingview-widget-container">
  <div class="tradingview-widget-container__widget"></div>
  <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-screener.js" async>
  {
  "width": "100%",
  "height": 650,
  "defaultColumn": "overview",
  "screener_type": "crypto_mkt",
  "displayCurrency": "USD",
  "colorTheme": "dark",
  "locale": "tr",
  "isTransparent": true,
  "symbols": {
    "tickers": [
      "BINANCE:BTCUSDT", "BINANCE:ETHUSDT", "BINANCE:SOLUSDT", "BINANCE:AVAXUSDT", 
      "BINANCE:XRPUSDT", "BINANCE:BNBUSDT", "BINANCE:ADAUSDT", "BINANCE:DOGEUSDT", 
      "BINANCE:LINKUSDT", "BINANCE:SUIUSDT", "BINANCE:PEPEUSDT", "BINANCE:RENDERUSDT"
    ],
    "groups": [ { "name": "SDR VIP LIST", "originalName": "SDR VIP LIST" } ]
  },
  "columns": [
    "base_currency_logoid", "name", "close", "change", "high", "low", "volume", "Recommend.All"
  ]
  }
  </script>
</div>
"""
# "Recommend.All" sütunu senin istediğin TR/EN analiz (Al/Sat/Tut) sinyallerini otomatik verir.
components.html(sdr_widget, height=650)

# --- 5. DETAYLI BİLGİ KUTULARI (TR/EN) ---
st.write("---")
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
        <div class="info-box" style="border-left: 12px solid #ff4b4b;">
            <h3 style='color:#ff4b4b;'>⚠️ YASAL UYARI / LEGAL NOTICE</h3>
            <p><b>[TR]:</b> Bu terminalde yer alan hiçbir veri, analiz veya TradingView göstergesi <b>yatırım danışmanlığı</b> kapsamında değildir. SDR Prestige Global, verileri sadece takip amaçlı sunar. Kripto varlıklar yüksek sermaye kaybı riski taşır; kararlarınızdan doğacak her türlü maddi zarardan sistem sorumlu tutulamaz.</p>
            <hr>
            <p><i><b>[EN]:</b> No data, analysis, or TradingView indicators on this terminal constitute <b>investment advice</b>. SDR Prestige Global presents data for tracking purposes only. Crypto assets carry a high risk of capital loss; the system cannot be held responsible for any financial damage.</i></p>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class="info-box" style="border-left: 12px solid #FFD700;">
            <h3 style='color:#FFD700;'>🛡️ SDR STRATEJİ / STRATEGY</h3>
            <p><b>[TR]:</b> Sıcak para akışını yakalamak için tablodaki "Hacim" (Volume) ve "Teknik Derecelendirme" (Recommend) kısmına odaklanın. "GÜÇLÜ AL" sinyali veren varlıklar trend başlangıcını işaret edebilir. Güvenli bölge için fiyatın günlük dip (Low) seviyesine yakınlığını kontrol edin. Sistem TradingView altyapısıyla her 15 saniyede bir tazelenir.</p>
            <hr>
            <p><i><b>[EN]:</b> Focus on "Volume" and "Technical Rating" (Recommend) to capture hot money flows. "STRONG BUY" signals may indicate the start of a trend. Check the proximity to the daily "Low" for safe entry zones. Updates every 15s via TradingView.</i></p>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br><p style='text-align:center; opacity: 0.6; color:#FFD700;'>© 2026 SDR SADRETTİN TURAN • PRESTIGE GLOBAL TERMINAL • POWERED BY TRADINGVIEW</p><br>", unsafe_allow_html=True)
