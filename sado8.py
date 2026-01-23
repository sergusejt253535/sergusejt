import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta
from streamlit_autorefresh import st_autorefresh

# --- 1. AYARLAR & OTOMATİK GÜNCELLEME (15 SANİYE) ---
st.set_page_config(page_title="SDR ALGORITHMIC TERMINAL", layout="wide")
st_autorefresh(interval=15 * 1000, key="sdr_algorithmic_core")

# --- 2. ÖZEL SDR TASARIM (PREMIUM DARK) ---
st.markdown("""
    <style>
    .stApp { background-color: #050505 !important; }
    .top-bar { display: flex; justify-content: space-between; align-items: center; padding: 15px; border-bottom: 2px solid #FFD700; margin-bottom: 20px; }
    .main-title { color: #00d4ff; text-align: center; font-family: 'Arial Black'; font-size: 50px; text-shadow: 0px 0px 20px #00d4ff; }
    .sub-title { color: #ffffff; text-align: center; font-family: 'Courier New'; font-size: 18px; letter-spacing: 4px; margin-bottom: 25px; }
    
    /* Tabloyu özelleştir */
    div[data-testid="stDataFrame"] { border: 2px solid #FFD700 !important; border-radius: 10px; }
    .info-box { background: #111; border: 1px solid #FFD700; padding: 25px; border-radius: 15px; color: white; min-height: 250px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SDR ÖZEL ALGORİTMA MOTORU ---
def sdr_engine():
    assets = ['BTCUSDT', 'ETHUSDT', 'SOLUSDT', 'AVAXUSDT', 'XRPUSDT', 'BNBUSDT', 'ADAUSDT', 'DOGEUSDT', 'LINKUSDT', 'SUIUSDT', 'PEPEUSDT', 'FETUSDT']
    rows = []
    try:
        # Binance verisine saldırıyoruz
        r = requests.get("https://api.binance.com/api/v3/ticker/24hr", timeout=10)
        data = r.json()
        filtered = [d for d in data if d['symbol'] in assets]
        
        for item in filtered:
            p = float(item['lastPrice'])
            h = float(item['highPrice'])
            l = float(item['lowPrice'])
            v = float(item['quoteVolume']) / 1_000_000 # Milyon Dolar
            
            # GÜÇ HESABI (Fiyatın 24s içindeki yeri)
            guc = int(((p - l) / (h - l)) * 100) if (h-l) != 0 else 50
            
            # --- SDR ÖZEL ANALİZ ALGORİTMASI (TR/EN) ---
            if guc > 85:
                analiz = "🚨 KRİTİK ZİRVE: Kâr Al / CRITICAL PEAK: Take Profit"
                sinyal = "🛡️ SELL"
            elif guc < 15:
                analiz = "🔥 DİP FIRSATI: Topla / BOTTOM ENTRY: Accumulate"
                sinyal = "💰 BUY"
            elif v > 500: # Hacim patlaması varsa
                analiz = "🐋 BALİNA GİRİŞİ: Takip Et / WHALE INFLOW: Follow"
                sinyal = "📈 ATTENTION"
            else:
                analiz = "⌛ YATAY SEYİR: Bekle / NEUTRAL: Wait"
                sinyal = "🥷 WATCH"
            
            rows.append({
                "SDR SİNYAL": sinyal,
                "VARLIK (ASSET)": item['symbol'].replace("USDT", ""),
                "FİYAT (PRICE)": f"{p:,.2f} $",
                "GÜÇ (POWER %)": f"%{guc}",
                "HACİM (VOL 24H)": f"${v:,.1f}M",
                "SDR VIP ANALİZ / ANALYSIS": analiz
            })
    except:
        return pd.DataFrame()
    return pd.DataFrame(rows)

# --- 4. PANEL GÖRÜNÜMÜ ---
now = datetime.utcnow() + timedelta(hours=3)
st.markdown(f"""
    <div class="top-bar">
        <div style='color:#00ffcc;'>📡 SDR ALGO-ENGINE ACTIVE</div>
        <div style='color:white;'>📅 {now.strftime("%d.%m.%Y")} | 🇹🇷 TR: {now.strftime("%H:%M:%S")}</div>
        <div style='color:#FFD700;'>SDR PRESTIGE</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="main-title">SDR PRESTIGE GLOBAL</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">ALGORITHMIC TRADING TERMINAL</div>', unsafe_allow_html=True)

# Tabloyu Getir
df = sdr_engine()

if not df.empty:
    st.dataframe(df.style.set_properties(**{
        'background-color': '#000',
        'color': '#FFD700',
        'border-color': '#444'
    }), use_container_width=True, hide_index=True, height=500)
else:
    st.warning("📡 API Verisi Alınıyor, Lütfen Bekleyin... / Connecting to API...")

# --- 5. BİLGİ KUTULARI (UZUN VE DETAYLI) ---
st.write("---")
c1, c2 = st.columns(2)

with c1:
    st.markdown("""<div class="info-box" style="border-left: 10px solid #ff4b4b;">
        <h3 style='color:#ff4b4b;'>⚠️ YASAL UYARI / LEGAL NOTICE</h3>
        <p><b>[TR]:</b> Bu algoritmik tablo, Sadrettin Turan'a özel matematiksel modellerle hesaplanmaktadır. 
        Sunulan analizler ve sinyaller kesinlik içermez ve yatırım tavsiyesi değildir. 
        Kripto piyasasındaki volatilite nedeniyle oluşabilecek kayıplardan sistem sorumlu tutulamaz.</p>
        <hr style='border: 0.1px solid #333;'>
        <p><i><b>[EN]:</b> This algorithmic table is calculated using mathematical models exclusive to Sadrettin Turan. 
        The signals and analyses provided are not guaranteed and do not constitute investment advice. 
        The system cannot be held responsible for losses due to market volatility.</i></p>
    </div>""", unsafe_allow_html=True)

with c2:
    st.markdown("""<div class="info-box" style="border-left: 10px solid #FFD700;">
        <h3 style='color:#FFD700;'>🛡️ ANALİZ METODU / ANALYSIS METHOD</h3>
        <p><b>[TR]:</b> SDR Algoritması, fiyatın 24 saatlik en düşük ve en yüksek seviyesine olan uzaklığını, 
        hacim ağırlıklı ortalamalarla birleştirir. Güç %15'in altındaysa toplama, %85'in üzerindeyse boşaltma stratejisi izlenir. 
        Sistem her 15 saniyede bir Binance Core üzerinden veriyi yeniler.</p>
        <hr style='border: 0.1px solid #333;'>
        <p><i><b>[EN]:</b> The SDR Algorithm combines the price's distance from 24h lows/highs with volume-weighted averages. 
        A strategy of accumulation is followed below 15% Power, and distribution above 85%. 
        The system refreshes every 15 seconds via Binance Core.</i></p>
    </div>""", unsafe_allow_html=True)

st.markdown("<p style='text-align:center; opacity: 0.5; color:#FFD700;'>© 2026 SDR SADRETTİN TURAN • PRESTIGE GLOBAL TERMINAL • SECURED BY CORE API</p>", unsafe_allow_html=True)
