import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
import random
import time
from streamlit_autorefresh import st_autorefresh

# --- 1. GLOBAL KONFİGÜRASYON ---
st.set_page_config(
    page_title="SDR PRESTIGE GLOBAL | V3",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 15 saniyede bir otomatik yenileme tetikleyicisi
st_autorefresh(interval=15 * 1000, key="sdr_refresh_engine")

# --- 2. GELİŞMİŞ CSS TASARIMI (UI/UX) ---
st.markdown("""
    <style>
    .stApp { background-color: #000000 !important; }
    
    /* Üst Bar Tasarımı */
    .top-bar { 
        display: flex; 
        justify-content: space-between; 
        align-items: center; 
        padding: 20px; 
        background: linear-gradient(90deg, #000000 0%, #1a1a1a 50%, #000000 100%);
        border-bottom: 3px solid #FFD700; 
        margin-bottom: 20px;
        border-radius: 0 0 15px 15px;
    }
    
    /* Başlıklar */
    .main-title { 
        color: #00d4ff; 
        text-align: center; 
        font-family: 'Arial Black', sans-serif; 
        font-size: 60px; 
        margin-bottom: 0px; 
        text-shadow: 0px 0px 35px #00d4ff;
        letter-spacing: 2px;
    }
    .sub-title { 
        color: #ffffff; 
        text-align: center; 
        font-family: 'Courier New', monospace; 
        font-size: 22px; 
        letter-spacing: 8px; 
        margin-bottom: 30px;
        font-weight: bold;
    }
    
    /* Tablo ve Veri Alanları */
    div[data-testid="stDataFrame"] { 
        background-color: #000000 !important; 
        border: 4px solid #FFD700 !important; 
        border-radius: 20px;
        padding: 10px;
    }
    
    /* Bilgi Kutuları (Uzun ve Detaylı) */
    .info-box { 
        background: rgba(20, 20, 20, 0.9); 
        border: 2px solid #FFD700; 
        padding: 30px; 
        border-radius: 20px; 
        color: white; 
        height: 100%;
        box-shadow: 0px 0px 15px rgba(255, 215, 0, 0.2);
    }
    
    /* Metrikler */
    [data-testid="stMetric"] {
        background: #0a0a0a !important;
        border: 1px solid #333 !important;
        padding: 15px !important;
        border-radius: 10px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. VERİ MOTORU (SDR CORE ENGINE) ---
def fetch_binance_data():
    assets = [
        'BTCUSDT', 'ETHUSDT', 'SOLUSDT', 'AVAXUSDT', 'XRPUSDT', 
        'BNBUSDT', 'ADAUSDT', 'DOGEUSDT', 'DOTUSDT', 'LINKUSDT', 
        'MATICUSDT', 'TRXUSDT', 'UNIUSDT', 'BCHUSDT', 'SUIUSDT', 
        'FETUSDT', 'RENDERUSDT', 'PEPEUSDT', 'SHIBUSDT'
    ]
    
    rows = []
    total_volume_1h = 0
    
    endpoints = [
        "https://api.binance.com/api/v3/ticker/24hr",
        "https://api1.binance.com/api/v3/ticker/24hr",
        "https://api3.binance.com/api/v3/ticker/24hr"
    ]
    
    raw_data = None
    for url in endpoints:
        try:
            response = requests.get(url, headers={'User-Agent': 'SDR_VIP_Terminal'}, timeout=8)
            if response.status_code == 200:
                raw_data = response.json()
                break
        except:
            continue
            
    if raw_data:
        filtered_data = [d for d in raw_data if d['symbol'] in assets]
        for item in filtered_data:
            last_p = float(item['lastPrice'])
            high_p = float(item['highPrice'])
            low_p = float(item['lowPrice'])
            volume = (float(item['quoteVolume']) / 1_000_000) / 24
            total_volume_1h += volume
            
            # SDR Güç İndeksi Hesaplama
            diff = high_p - low_p
            power_idx = int(((last_p - low_p) / diff) * 100) if diff != 0 else 50
            power_idx = max(min(power_idx, 99), 1)
            
            # Dinamik Analiz ve Sinyal (TR/EN)
            if power_idx >= 88:
                signal = "🛡️ SELL"
                analysis = "🚨 ZİRVE: Kâr Al & Nakde Geç / PEAK: Take Profit & Move to Cash"
            elif power_idx <= 15:
                signal = "💰 BUY"
                analysis = "🔥 DİP: Kademeli Topla / BOTTOM: Start Accumulating"
            elif 15 < power_idx < 40:
                signal = "🥷 WAIT"
                analysis = "⌛ PUSU: Giriş İçin Onay Bekle / AMBUSH: Wait for Confirmation"
            else:
                signal = "📈 FOLLOW"
                analysis = "💎 TREND: Pozisyonu Koru / TREND: Maintain Position"
                
            rows.append({
                "SDR SİNYAL": signal,
                "VARLIK / ASSET": item['symbol'].replace("USDT", ""),
                "FİYAT / PRICE": f"{last_p:,.2f} $",
                "HACİM / VOL (1H)": f"${volume:,.2f} M",
                "GÜÇ / POWER (%)": f"%{power_idx}",
                "POWER_VAL": power_idx,
                "ANALİZ / ANALYSIS": analysis
            })
            
    return pd.DataFrame(rows), total_volume_1h

# --- 4. ÜST PANEL VE ZAMANLAYICI ---
now_utc = datetime.utcnow()
now_tr = now_utc + timedelta(hours=3)

st.markdown(f"""
    <div class="top-bar">
        <div style='color:#00ffcc; font-weight:bold;'>📡 OFFICIAL BINANCE CORE API</div>
        <div style='text-align:center; color:white; font-size:18px;'>
            <b>📅 {now_tr.strftime("%d.%m.%Y")}</b> | 
            <b>🌍 UTC: {now_utc.strftime("%H:%M:%S")}</b> | 
            <b>🇹🇷 TR: {now_tr.strftime("%H:%M:%S")}</b>
        </div>
        <div style='color:#FFD700; font-weight:bold; letter-spacing:2px;'>SDR PRESTIGE</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="main-title">SDR PRESTIGE GLOBAL</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">SADRETTİN TURAN VIP ANALYTICS</div>', unsafe_allow_html=True)

# --- 5. ANA İÇERİK ---
df, total_vol = fetch_binance_data()

if not df.empty:
    # Özet Metrikler
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("💰 BUY OPPORTUNITY", len(df[df['SDR SİNYAL'] == "💰 BUY"]))
    m2.metric("🛡️ PROFIT TAKING", len(df[df['SDR SİNYAL'] == "🛡️ SELL"]))
    m3.metric("📊 AVG MARKET POWER", f"%{int(df['POWER_VAL'].mean())}")
    m4.metric("📈 TOTAL VOL (1H)", f"${total_vol:,.1f}M")

    # Ana Tablo
    st.dataframe(
        df[["SDR SİNYAL", "VARLIK / ASSET", "FİYAT / PRICE", "HACİM / VOL (1H)", "GÜÇ / POWER (%)", "ANALİZ / ANALYSIS"]],
        use_container_width=True,
        hide_index=True,
        height=550
    )
    
    # Grafik Bölümü
    st.write("---")
    fig = px.bar(
        df, x='VARLIK / ASSET', y='POWER_VAL', color='POWER_VAL',
        color_continuous_scale='Blues',
        labels={'POWER_VAL': 'MARKET POWER %'},
        title="SDR GLOBAL POWER DYNAMICS (%)"
    )
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color="white"),
        height=400
    )
    st.plotly_chart(fig, use_container_width=True)

else:
    st.error("🚨 API CONNECTION DELAY: Re-establishing secure tunnel...")

# --- 6. DETAYLI BİLGİ VE YASAL UYARI (GENİŞLETİLMİŞ) ---
st.write("---")
col_a, col_b = st.columns(2)

with col_a:
    st.markdown("""
        <div class="info-box" style="border-left: 12px solid #ff4b4b;">
            <h3 style='color:#ff4b4b;'>⚠️ YASAL UYARI / LEGAL NOTICE</h3>
            <p><b>[TR] ÖNEMLİ BİLGİLENDİRME:</b> Bu platformda paylaşılan hiçbir veri, analiz veya sinyal 
            <b>yatırım danışmanlığı</b> kapsamında değildir. SDR Prestige Global, Binance üzerinden gelen ham verileri 
            kendi algoritmalarıyla işler. Kripto varlık piyasaları aşırı oynaklık gösterir; 
            bu nedenle oluşabilecek maddi zararlardan sistem sorumlu tutulamaz. Yatırım yapmadan önce kendi araştırmanızı yapınız.</p>
            <hr style='border: 0.5px solid #333;'>
            <p><i><b>[EN] IMPORTANT DISCLOSURE:</b> None of the data, analysis, or signals shared on this platform 
            constitute <b>investment advice</b>. SDR Prestige Global processes raw data from Binance using its 
            own proprietary algorithms. Crypto-asset markets exhibit extreme volatility; therefore, the system 
            cannot be held responsible for any financial losses. Always conduct your own research before investing.</i></p>
        </div>
    """, unsafe_allow_html=True)

with col_b:
    st.markdown("""
        <div class="info-box" style="border-left: 12px solid #FFD700;">
            <h3 style='color:#FFD700;'>🛡️ STRATEJİ REHBERİ / STRATEGY GUIDE</h3>
            <p><b>[TR] SİSTEM NASIL ÇALIŞIR?</b><br>
            • <b>%88-99 (ZİRVE):</b> Fiyatın doyum noktasına ulaştığını ve kâr satışlarının başlayabileceğini gösterir.<br>
            • <b>%1-15 (DİP):</b> Fiyatın aşırı satış yediğini ve güvenli alım bölgesine girdiğini işaret eder.<br>
            • <b>GÜNCELLEME:</b> Veriler her 15 saniyede bir otomatik olarak global borsalardan çekilir.</p>
            <hr style='border: 0.5px solid #333;'>
            <p><i><b>[EN] HOW THE SYSTEM WORKS?</b><br>
            • <b>%88-99 (PEAK):</b> Indicates price saturation and possible profit-taking zones.<br>
            • <b>%1-15 (BOTTOM):</b> Signals oversold conditions and potential entry/accumulation zones.<br>
            • <b>UPDATES:</b> Data is automatically fetched from global exchanges every 15 seconds.</i></p>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br><p style='text-align:center; opacity: 0.6; color:#FFD700; font-size:14px;'>© 2026 SDR SADRETTİN TURAN • PRESTIGE GLOBAL TERMINAL • SECURED BY CORE API</p><br>", unsafe_allow_html=True
