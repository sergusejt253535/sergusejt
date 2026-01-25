import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta
import plotly.express as px
import random
from streamlit_autorefresh import st_autorefresh

# --- 1. AYARLAR ---
st.set_page_config(page_title="SDR PRESTIGE GLOBAL", layout="wide")

# --- 2. GÜNCELLEME MOTORU (15 SANİYE) ---
st_autorefresh(interval=15 * 1000, key="datarefresh")

# --- 3. ÖZEL SDR VIP TASARIMI ---
st.markdown("""
    <style>
    /* Ana Arka Plan */
    .stApp { background-color: #000000 !important; }
    
    /* Üst Bar ve Başlıklar */
    .top-bar { display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; padding: 15px; background-color: #000000; border-bottom: 3px solid #FFD700; margin-bottom: 15px; }
    .main-title { color: #00d4ff; text-align: center; font-family: 'Arial Black'; font-size: 55px; margin-bottom: 0px; text-shadow: 0px 0px 30px #00d4ff; }
    .sub-title { color: #ffffff; text-align: center; font-family: 'Courier New'; font-size: 20px; letter-spacing: 5px; margin-bottom: 20px; }
    
    /* Metrik Kartları */
    [data-testid="stMetric"] { background-color: #000000 !important; border: 2px solid #FFD700 !important; border-radius: 15px; padding: 20px !important; }
    [data-testid="stMetricLabel"] { color: #ffffff !important; }
    [data-testid="stMetricValue"] { color: #FFD700 !important; }

    /* TABLO ÖZEL AYARLARI (SADO'NUN İSTEDİĞİ RENKLER) */
    div[data-testid="stDataFrame"] { 
        background-color: #000000 !important; 
        border: 4px solid #FFD700 !important; 
        border-radius: 15px;
    }
    
    /* Tablo Başlıkları */
    div[data-testid="stDataFrame"] div[role="columnheader"] {
        background-color: #000000 !important;
        color: #FFD700 !important;
        font-weight: bold !important;
    }

    /* Kayan Yazı */
    .ticker-wrap { background: #FFD700; color: black; padding: 5px; font-weight: bold; overflow: hidden; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. DEĞİŞKENLER ---
su_an_utc = datetime.utcnow()
su_an_tr = su_an_utc + timedelta(hours=3)

if 'fake_counter' not in st.session_state:
    st.session_state.fake_counter = random.randint(350, 420)
else:
    st.session_state.fake_counter += random.randint(-1, 2)

# --- 5. GARANTİLİ VERİ MOTORU ---
def get_guaranteed_data():
    coins = ['BTC', 'ETH', 'SOL', 'AVAX', 'XRP', 'BNB', 'ADA', 'DOGE', 'DOT', 'LINK', 'SUI', 'FET', 'RENDER', 'PEPE', 'SHIB']
    fsyms = ",".join(coins)
    url = f"https://min-api.cryptocompare.com/data/pricemultifull?fsyms={fsyms}&tsyms=USD"
    
    try:
        r = requests.get(url, timeout=10)
        data = r.json().get('RAW', {})
        rows = []
        total_vol = 0
        
        for coin in coins:
            if coin in data:
                c_data = data[coin]['USD']
                p = c_data['PRICE']
                h = c_data['HIGH24HOUR']
                l = c_data['LOW24HOUR']
                ch = c_data['CHANGEPCT24HOUR']
                v_1h = c_data['VOLUMEHOUR'] / 1_000_000
                total_vol += v_1h
                
                guc = int(((p - l) / (h - l)) * 100) if (h - l) != 0 else 50
                
                if guc > 88: d, e = "🛡️ SELL", "🚨 ZİRVE: Kâr Al & Nakde Geç / PEAK: Take Profit"
                elif guc < 15: d, e = "💰 BUY", "🔥 DİP: Kademeli Topla / BOTTOM: Accumulate"
                else: d, e = "📈 FOLLOW", "💎 TRENDİ İZLE / WATCHING THE TREND"

                rows.append({
                    "SDR SİNYAL": d, 
                    "VARLIK/ASSET": coin,
                    "FİYAT/PRICE": p, # Renklendirme için sayı olarak bırakıldı
                    "DEĞİŞİM/CHG": ch, 
                    "HACİM/VOL (1H)": v_1h,
                    "GÜÇ/POWER (%)": guc,
                    "SDR ANALİZ / ANALYSIS": e
                })
        return pd.DataFrame(rows), total_vol
    except:
        return pd.DataFrame(), 0

# --- 6. EKRAN ÇIKTISI ---
df, t_vol = get_guaranteed_data()

# Üst Bilgi Barı
st.markdown(f"""<div class="top-bar">
    <div style='color:#00ffcc; font-weight:bold;'>● SDR SECURE DATA | 15S</div>
    <div style='text-align:center;'>
        <span style='color:#ffffff;'>👥 VISITORS:</span> <span style='color:#ff00ff; font-weight:bold;'>{st.session_state.fake_counter}</span>
        &nbsp;&nbsp;&nbsp;&nbsp; <span style='color:#00d4ff;'>🌍 UTC: {su_an_utc.strftime("%H:%M:%S")}</span>
        &nbsp;&nbsp;&nbsp;&nbsp; <span style='color:#00ffcc;'>🇹🇷 TR: {su_an_tr.strftime("%H:%M:%S")}</span>
    </div>
    <div style='color:#FFD700; font-weight:bold;'>SDR PRESTIGE</div>
</div>""", unsafe_allow_html=True)

st.markdown('<div class="main-title">SDR PRESTIGE GLOBAL</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">SADRETTİN TURAN VIP ANALYTICS</div>', unsafe_allow_html=True)

if not df.empty:
    m1, m2, m3 = st.columns([1,1,2])
    m1.metric("💰 BUY ZONE", len(df[df['SDR SİNYAL'] == "💰 BUY"]))
    m2.metric("🛡️ SELL ZONE", len(df[df['SDR SİNYAL'] == "🛡️ SELL"]))
    m3.metric("📊 TOTAL VOL (1H)", f"${t_vol:,.2f} M")

    # --- TABLO RENKLENDİRME MANTIĞI ---
    def style_dataframe(df):
        return df.style.set_properties(**{
            'background-color': '#000000', # Zemin Siyah
            'border-color': '#FFD700',
            'font-weight': 'bold',
            'font-size': '18px'
        }).format({
            "FİYAT/PRICE": "{:,.2f} $",
            "DEĞİŞİM/CHG": "% {:,.2f}",
            "HACİM/VOL (1H)": "$ {:,.2f} M",
            "GÜÇ/POWER (%)": "% {}"
        }).set_properties(subset=["FİYAT/PRICE", "DEĞİŞİM/CHG", "GÜÇ/POWER (%)"], **{
            'color': '#00d4ff' # Değerler Turkuaz/Mavi
        }).set_properties(subset=["SDR ANALİZ / ANALYSIS"], **{
            'color': '#FFD700' # Analiz Bilgisi Altın Sarısı
        })

    st.dataframe(style_dataframe(df), use_container_width=True, hide_index=True, height=750)

    st.write("---")
    st.markdown("<p style='text-align:center; opacity: 0.5; color:white;'>© 2026 SDR PRESTIGE • SADRETTİN TURAN</p>", unsafe_allow_html=True
