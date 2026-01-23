import streamlit as st
from datetime import datetime, timedelta
import streamlit.components.v1 as components
from streamlit_autorefresh import st_autorefresh

# --- 1. AYARLAR ---
st.set_page_config(page_title="SDR PRESTIGE GLOBAL", layout="wide")

# 15 saniyede bir ekranın canlı kalmasını sağlar
st_autorefresh(interval=15 * 1000, key="sdr_vip_refresh")

# --- 2. CSS TASARIM (PRESTIGE SİYAH & ALTIN) ---
st.markdown("""
    <style>
    .stApp { background-color: #000000 !important; }
    .top-bar { display: flex; justify-content: space-between; align-items: center; padding: 15px; border-bottom: 3px solid #FFD700; margin-bottom: 15px; }
    .main-title { color: #00d4ff; text-align: center; font-family: 'Arial Black'; font-size: 55px; text-shadow: 0px 0px 30px #00d4ff; }
    .sub-title { color: #ffffff; text-align: center; font-family: 'Courier New'; font-size: 20px; letter-spacing: 5px; margin-bottom: 25px; font-weight: bold; }
    .info-box { background-color: #0c0c0c; border: 2px solid #FFD700; padding: 30px; border-radius: 20px; color: white; min-height: 280px; }
    hr { border: 0.1px solid #333 !important; margin: 25px 0 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. ÜST BİLGİ BARI ---
now_tr = datetime.utcnow() + timedelta(hours=3)

st.markdown(f"""
    <div class="top-bar">
        <div style='color:#00ffcc; font-weight:bold;'>📡 SDR PRESTIGE GLOBAL CORE</div>
        <div style='color:white;'>📅 {now_tr.strftime("%d.%m.%Y")} | 🇹🇷 TR: {now_tr.strftime("%H:%M:%S")}</div>
        <div style='color:#FFD700; font-weight:bold;'>SDR VIP TERMINAL</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="main-title">SDR PRESTIGE GLOBAL</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">SADRETTİN TURAN VIP ANALYTICS</div>', unsafe_allow_html=True)

# --- 4. ÖZELLEŞTİRİLMİŞ ANALİZ TABLOSU (SDR MODU) ---
# Bu yapı doğrudan senin tarayıcın üzerinden aktığı için IP engeline takılmaz.
st.markdown("### 💎 SDR STRATEJİK ANALİZ TABLOSU / STRATEGIC ANALYSIS TABLE")

sdr_screener = """
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
    "tickers": [],
    "groups": [
      {
        "name": "Binance",
        "originalName": "Binance"
      }
    ]
  },
  "columns": [
    "base_currency_logoid",
    "name",
    "Recommend.All",
    "close",
    "change",
    "high",
    "low",
    "volume",
    "market_cap_calc"
  ],
  "showToolbar": true
  }
  </script>
</div>
"""
# Not: "Recommend.All" sütunu senin istediğin "Analiz Fikrini" (Al/Sat/Nötr) verir.
components.html(sdr_screener, height=650)

# --- 5. DETAYLI BİLGİ VE YASAL UYARI KUTULARI (TR/EN) ---
st.write("---")
c1, c2 = st.columns(2)

with c1:
    st.markdown("""
        <div class="info-box" style="border-left: 12px solid #ff4b4b;">
            <h3 style='color:#ff4b4b;'>⚠️ YASAL UYARI / LEGAL NOTICE</h3>
            <p><b>[TR]:</b> Bu terminalde sunulan veriler, grafikler ve otomatik analiz sinyalleri asla <b>yatırım danışmanlığı</b> veya <b>sıcak para garantisi</b> olarak değerlendirilmemelidir. SDR Prestige Global, TradingView verilerini sadece takip kolaylığı sağlamak amacıyla sunar. Kripto para yatırımları tüm sermayenizi kaybetme riski taşır. Tüm sorumluluk ve risk kullanıcıya aittir.</p>
            <hr>
            <p><i><b>[EN]:</b> No data, charts, or automated analysis signals presented on this terminal should be considered as <b>investment advice</b>. SDR Prestige Global provides TradingView data for tracking convenience only. Cryptocurrency investments carry the risk of losing all your capital. All responsibility and risks belong to the user.</i></p>
        </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
        <div class="info-box" style="border-left: 12px solid #FFD700;">
            <h3 style='color:#FFD700;'>🛡️ SDR STRATEJİ VE ANALİZ / STRATEGY & ANALYSIS</h3>
            <p><b>[TR]:</b> Sıcak para akışını yakalamak için tablodaki <b>"Teknik Derecelendirme" (Recommend)</b> sütununa odaklanın. "Güçlü Al" sinyalleri, teknik göstergelerin (RSI, Moving Averages vb.) yukarı yönlü olduğunu gösterir. Hacim (Volume) sütunundaki ani artışlar, büyük paranın giriş yaptığı varlıkları işaret eder. Karar vermeden önce varlığın 24 saatlik dip (Low) seviyesine yakınlığını kontrol edin.</p>
            <hr>
            <p><i><b>[EN]:</b> Focus on the <b>"Technical Rating" (Recommend)</b> column to catch hot money flows. "Strong Buy" signals indicate that technical indicators (RSI, Moving Averages, etc.) are trending upwards. Sudden spikes in the Volume column point to assets where "big money" is entering. Check the 24-hour Low levels before making a final decision.</i></p>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br><p style='text-align:center; opacity: 0.6; color:#FFD700; font-size:14px;'>© 2026 SDR SADRETTİN TURAN • PRESTIGE GLOBAL TERMINAL • SECURED DATA INTERFACE</p><br>", unsafe_allow_html=True)
