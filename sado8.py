import streamlit as st
from datetime import datetime, timedelta
import streamlit.components.v1 as components
from streamlit_autorefresh import st_autorefresh

# --- 1. AYARLAR & PRESTİJ KONFİGÜRASYONU ---
st.set_page_config(page_title="SDR PRESTIGE GLOBAL | V3", layout="wide", initial_sidebar_state="collapsed")

# 15 saniyede bir otomatik tazeleme (Piyasa hızına yetişmek için)
st_autorefresh(interval=15 * 1000, key="sdr_prestige_final")

# --- 2. GÖRSEL ŞÖLEN (CSS) ---
st.markdown("""
    <style>
    /* Arka Fon ve Genel Tema */
    .stApp { background-color: #000000 !important; }
    
    /* Üst Bilgi Çubuğu */
    .top-bar { 
        display: flex; 
        justify-content: space-between; 
        align-items: center; 
        padding: 15px 25px; 
        background: linear-gradient(90deg, #000000, #1a1a1a);
        border-bottom: 2px solid #FFD700; 
        margin-bottom: 20px;
        border-radius: 0 0 20px 20px;
    }
    
    /* Başlık Tasarımları */
    .main-title { 
        color: #00d4ff; 
        text-align: center; 
        font-family: 'Impact', sans-serif; 
        font-size: 65px; 
        text-shadow: 0px 0px 35px #00d4ff;
        margin-bottom: 5px;
    }
    .sub-title { 
        color: #ffffff; 
        text-align: center; 
        font-family: 'Courier New', monospace; 
        font-size: 22px; 
        letter-spacing: 7px; 
        margin-bottom: 30px;
        font-weight: bold;
    }

    /* VIP Bilgi Kutuları */
    .info-box { 
        background: rgba(15, 15, 15, 0.95); 
        border: 2px solid #FFD700; 
        padding: 30px; 
        border-radius: 20px; 
        color: white; 
        min-height: 320px;
        box-shadow: 0px 10px 30px rgba(0,0,0,0.5);
    }
    
    /* Çizgiler ve Detaylar */
    hr { border: 0.5px solid #333 !important; margin: 30px 0 !important; }
    
    /* Tablo Alanı */
    .table-container {
        border: 3px solid #FFD700;
        border-radius: 25px;
        padding: 10px;
        background-color: #0a0a0a;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. ÜST PANEL (ZAMAN VE DURUM) ---
now_tr = datetime.utcnow() + timedelta(hours=3)

st.markdown(f"""
    <div class="top-bar">
        <div style='color:#00ffcc; font-weight:bold; font-size:14px;'>📡 CORE SYSTEM: ONLINE (15s Refresh)</div>
        <div style='color:white; font-size:16px;'>
            <b>DATE:</b> {now_tr.strftime("%d.%m.%Y")} | <b>TR TIME:</b> {now_tr.strftime("%H:%M:%S")}
        </div>
        <div style='color:#FFD700; font-weight:bold; letter-spacing:2px; font-size:14px;'>SDR PRESTIGE TERMINAL</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="main-title">SDR PRESTIGE GLOBAL</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">SADRETTİN TURAN VIP ANALYTICS</div>', unsafe_allow_html=True)

# --- 4. GELİŞMİŞ TRADINGVIEW SCREENER (SDR ÖZEL MODU) ---
st.markdown("### 💎 STRATEJİK PİYASA ANALİZİ / STRATEGIC MARKET ANALYSIS")

# Bu widget üzerinden kolonları senin için özel seçtim: Analiz, Değişim, Hacim, Teknik Puan
sdr_screener_js = """
<div class="tradingview-widget-container" style="border: 2px solid #FFD700; border-radius: 15px; overflow: hidden;">
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
components.html(sdr_screener_js, height=660)

# --- 5. PROFESYONEL BİLGİLENDİRME KUTULARI (TR/EN) ---
st.write("---")
col_tr, col_en = st.columns(2)

with col_tr:
    st.markdown("""
        <div class="info-box" style="border-left: 15px solid #ff4b4b;">
            <h3 style='color:#ff4b4b; text-transform: uppercase;'>⚠️ YASAL UYARI VE RİSK BİLDİRİMİ</h3>
            <p>Bu terminalde sunulan tüm veriler, teknik derecelendirmeler ve otomatik analiz sinyalleri sadece genel bilgilendirme amaçlıdır. 
            Hiçbir şekilde <b>yatırım danışmanlığı</b> veya <b>kesin kazanç vaadi</b> olarak nitelendirilemez. 
            Kripto varlık piyasaları, yüksek oynaklık nedeniyle ana sermayenizin tamamını kaybetmenize neden olabilir. 
            SDR Prestige Global sistemi, TradingView altyapısını kullanarak verileri size ulaştırır; verilerdeki gecikme veya hatalardan 
            veya bu verilere dayanarak aldığınız yatırım kararlarından sistem sorumlu tutulamaz. 
            İşlem yapmadan önce mutlaka profesyonel bir finansal danışmanla görüşmeniz önerilir.</p>
        </div>
    """, unsafe_allow_html=True)

with col_en:
    st.markdown("""
        <div class="info-box" style="border-left: 15px solid #FFD700;">
            <h3 style='color:#FFD700; text-transform: uppercase;'>🛡️ STRATEGY GUIDE & ANALYSIS HUB</h3>
            <p>To identify "hot money" flow and potential entry points, focus on the <b>'Technical Rating' (Recommend)</b> and <b>'Volume'</b> columns. 
            "Strong Buy" ratings indicate that multiple indicators (RSI, Moving A
