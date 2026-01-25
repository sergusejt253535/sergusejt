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
    .stApp { background-color: #000000 !important; }
    .top-bar { display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; padding: 15px; background-color: #000000; border-bottom: 3px solid #FFD700; margin-bottom: 15px; }
    .main-title { color: #00d4ff; text-align: center; font-family: 'Arial Black'; font-size: 55px; margin-bottom: 0px; text-shadow: 0px 0px 30px #00d4ff; }
    .sub-title { color: #ffffff; text-align: center; font-family: 'Courier New'; font-size: 20px; letter-spacing: 5px; margin-bottom: 20px; }
    
    [data-testid="stMetric"] { background-color: #000000 !important; border: 2px solid #FFD700 !important; border-radius: 15px; padding: 20px !important; }
    [data-testid="stMetricLabel"] { color: #ffffff !important; }
    [data-testid="stMetricValue"] { color: #FFD700 !important; }

    div[data-testid="stDataFrame"] { 
        background-color: #000000 !important; 
        border: 4px solid #FFD700 !important; 
        border-radius: 15px;
    }
    
    div[data-testid="stDataFrame"] div[role="columnheader"] {
        background-color: #000000 !important;
        color: #FFD700 !important;
        font-weight: bold !important;
    }
    .info-box { background-color: #000000; border: 2px solid #FFD700; padding: 25px; border-radius: 15px; height: 100%; margin-bottom: 15px; }
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
                    "FİYAT/PRICE": p,
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
    m1, m2, m3 = st.columns([1, 1, 2])
    m1.metric("💰 BUY ZONE", len(df[df['SDR SİNYAL'] == "💰 BUY"]))
    m2.metric("🛡️ SELL ZONE", len(df[df['SDR SİNYAL'] == "🛡️ SELL"]))
    m3.metric("📊 TOTAL VOL (1H)", f"${t_vol:,.2f} M")

    def apply_style(df):
        return df.style.set_properties(**{
            'background-color': '#000000',
            'color': '#00d4ff',
            'border-color': '#FFD700',
            'font-weight': 'bold'
        }).set_properties(subset=["SDR ANALİZ / ANALYSIS"], **{
            'color': '#FFD700'
        }).format({
            "FİYAT/PRICE": "{:,.2f} $",
            "DEĞİŞİM/CHG": "% {:,.2f}",
            "HACİM/VOL (1H)": "$ {:,.2f} M",
            "GÜÇ/POWER (%)": "% {}"
        })

    st.dataframe(apply_style(df), use_container_width=True, hide_index=True, height=600)

    st.write("---")
    
    # --- YENİ EKLENEN GRAFİK ---
    st.write("### 📊 GLOBAL GÜÇ ANALİZİ (%) / POWER INDEX")
    fig = px.bar(df, x='VARLIK/ASSET', y='GÜÇ/POWER (%)', color='GÜÇ/POWER (%)', color_continuous_scale='Blues')
    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color="white"))
    st.plotly_chart(fig, use_container_width=True)

    # --- YENİ EKLENEN BİLGİ KUTULARI ---
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""
        <div class="info-box" style="border-left: 10px solid #ff4b4b;">
            <h3 style='color:#ff4b4b; margin-top:0;'>⚠️ YASAL UYARI / LEGAL NOTICE</h3>
            <p style='color:#ffffff;'><b>YATIRIM DANIŞMANLIĞI DEĞİLDİR. / NOT AN INVESTMENT ADVICE.</b></p>
            <p style='color:#cccccc;'>Bu paneldeki veriler algoritmik hesaplamalardır. Karar yetkisi kullanıcıya aittir.</p>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="info-box" style="border-left: 10px solid #FFD700;">
            <h3 style='color:#FFD700; margin-top:0;'>🛡️ SDR STRATEJİ / STRATEGY</h3>
            <p style='color:#ffffff;'>🚀 <b>%88-100 POWER:</b> Kâr al, nakde geç.</p>
            <p style='color:#ffffff;'>📉 <b>%0-15 POWER:</b> Kademeli alım bölgesi.</p>
            <p style='color:#00d4ff;'>⚡ Risk yönetimi için %50 nakit korunmalıdır.</p>
        </div>
        """, unsafe_allow_html=True)

    st.write("---")
    st.markdown("<p style='text-align:center; opacity: 0.5; color:white;'>© 2026 SDR PRESTIGE • SADRETTİN TURAN</p>", unsafe_allow_html=True)
else:
    st.info("🔄 Veri akışı optimize ediliyor...")
