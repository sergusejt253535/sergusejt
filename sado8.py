import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta
import plotly.express as px
import random
from streamlit_autorefresh import st_autorefresh

# --- 1. AYARLAR ---
st.set_page_config(page_title="SDR PRESTIGE GLOBAL", layout="wide")

# --- 2. GÜNCELLEME MOTORU (15 Saniyeye Çektim) ---
st_autorefresh(interval=15 * 1000, key="datarefresh")

# --- 3. CSS TASARIM ---
st.markdown("""
    <style>
    .stApp { background-color: #000000 !important; }
    .top-bar { display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; padding: 15px; background-color: #000000; border-bottom: 3px solid #FFD700; margin-bottom: 15px; }
    .main-title { color: #00d4ff; text-align: center; font-family: 'Arial Black'; font-size: 55px; margin-bottom: 0px; text-shadow: 0px 0px 30px #00d4ff; }
    .sub-title { color: #ffffff; text-align: center; font-family: 'Courier New'; font-size: 20px; letter-spacing: 5px; margin-bottom: 20px; }
    
    [data-testid="stMetric"] { background-color: #000000 !important; border: 2px solid #FFD700 !important; border-radius: 15px; padding: 20px !important; }
    [data-testid="stMetricLabel"] { color: #ffffff !important; font-size: 18px !important; font-weight: bold !important; }
    [data-testid="stMetricValue"] { color: #FFD700 !important; font-size: 38px !important; }

    div[data-testid="stDataFrame"] { 
        background-color: #000000 !important; 
        border: 4px solid #FFD700 !important; 
        border-radius: 15px;
    }
    .stDataFrame td, .stDataFrame th { font-size: 24px !important; font-weight: bold !important; }
    .info-box { background-color: #000000; border: 2px solid #FFD700; padding: 25px; border-radius: 15px; height: 100%; margin-bottom: 15px; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. VERİ MOTORU ---
def get_live_data():
    assets = ['BTCUSDT', 'ETHUSDT', 'SOLUSDT', 'AVAXUSDT', 'XRPUSDT', 'BNBUSDT', 'ADAUSDT', 'DOGEUSDT', 'DOTUSDT', 'LINKUSDT', 'MATICUSDT', 'TRXUSDT', 'UNIUSDT', 'BCHUSDT', 'SUIUSDT', 'FETUSDT', 'RENDERUSDT', 'PEPEUSDT', 'SHIBUSDT']
    try:
        # Binance'ten 24 saatlik tüm verileri çekiyoruz (Fiyatlar kesin doğru)
        r = requests.get("https://api.binance.com/api/v3/ticker/24hr", timeout=10)
        data = r.json()
        active = [i for i in data if i['symbol'] in assets]
        rows = []
        total_vol = 0
        for item in active:
            p = float(item.get('lastPrice', 0))
            h = float(item.get('highPrice', 0))
            l = float(item.get('lowPrice', 0))
            v_1h = (float(item.get('quoteVolume', 0)) / 1_000_000) / 24
            total_vol += v_1h
            
            # Güç Analizi (Gerçek Fiyat Hareketine Dayalı)
            guc = int(((p - l) / (h - l)) * 100) if (h - l) != 0 else 50
            guc = max(min(guc, 99), 1)

            if guc > 88: d, e = "🛡️ SELL", "🚨 ZİRVE: Kâr Al / PEAK: Take Profit"
            elif guc < 15: d, e = "💰 BUY", "🔥 DİP: Topla / BOTTOM: Accumulate"
            elif 15 <= guc < 40: d, e = "🥷 WAIT", "⌛ PUSUDA / AMBUSH: Wait"
            else: d, e = "📈 FOLLOW", "💎 TRENDİ İZLE / WATCHING"
            
            rows.append({
                "SDR SİNYAL": d, "VARLIK/ASSET": item['symbol'].replace("USDT", ""),
                "FİYAT/PRICE": f"{p:,.2f} $", "HACİM/VOL (1H)": f"${v_1h:,.2f} M",
                "GÜÇ/POWER (%)": f"%{guc}", "POWER_NUM": guc, "SDR ANALİZ / ANALYSIS": e
            })
        return pd.DataFrame(rows), total_vol
    except:
        return pd.DataFrame(), 0

# --- 5. PANEL TASARIMI ---
su_an_utc = datetime.utcnow()
su_an_tr = su_an_utc + timedelta(hours=3)

# Visitor Sayacı
if 'fake_counter' not in st.session_state:
    st.session_state.fake_counter = random.randint(225, 275)
else:
    st.session_state.fake_counter += random.randint(-1, 2)

# Üst Bar
st.markdown(f"""
    <div class="top-bar">
        <div style='color:#00ffcc; font-weight:bold;'>OFFICIAL BINANCE API | UPDATE: 15S</div>
        <div style='text-align:center;'>
            <span style='color:#FFD700; font-weight:bold;'>📅 {su_an_tr.strftime("%d.%m.%Y")}</span>
            &nbsp;&nbsp;&nbsp;&nbsp;
            <span style='color:#ffffff;'>👥 VISITORS: {st.session_state.fake_counter}</span>
            &nbsp;&nbsp;&nbsp;&nbsp;
            <span style='color:#00d4ff;'>🌍 UTC: {su_an_utc.strftime("%H:%M:%S")}</span>
            &nbsp;&nbsp;&nbsp;&nbsp;
            <span style='color:#00ffcc;'>🇹🇷 TR: {su_an_tr.strftime("%H:%M:%S")}</span>
        </div>
        <div style='color:#FFD700; font-weight:bold;'>SDR PRESTIGE</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="main-title">SDR PRESTIGE GLOBAL</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">SADRETTİN TURAN VIP ANALYTICS</div>', unsafe_allow_html=True)

df, t_vol = get_live_data()

if not df.empty:
    m1, m2, m3 = st.columns([1,1,2])
    m1.metric("💰 BUY ZONE", len(df[df['SDR SİNYAL'] == "💰 BUY"]))
    m2.metric("🛡️ SELL ZONE", len(df[df['SDR SİNYAL'] == "🛡️ SELL"]))
    m3.metric("📊 TOTAL VOLUME (1H)", f"${t_vol:,.2f} M")
    
    st.write("---")
    
    # Ana Tablo
    st.dataframe(df[["SDR SİNYAL", "VARLIK/ASSET", "FİYAT/PRICE", "HACİM/VOL (1H)", "GÜÇ/POWER (%)", "SDR ANALİZ / ANALYSIS"]].style.set_properties(**{
        'background-color': '#000000', 'color': '#FFD700', 'border-color': '#FFD700', 'font-weight': 'bold'
    }), use_container_width=True, hide_index=True, height=700)
    
    st.write("---")
    
    # Grafik
    fig = px.bar(df, x='VARLIK/ASSET', y='POWER_NUM', color='POWER_NUM', color_continuous_scale='Blues', title="GLOBAL POWER ANALYSIS (%)")
    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color="white"))
    st.plotly_chart(fig, use_container_width=True)
    
    # Bilgi Kutuları
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""
        <div class="info-box" style="border-left: 10px solid #ff4b4b;">
            <h3 style='color:#ff4b4b; margin-top:0;'>⚠️ YASAL UYARI / LEGAL NOTICE</h3>
            <p style='color:#ffffff;'><b>YATIRIM DANIŞMANLIĞI DEĞİLDİR. / NOT AN INVESTMENT ADVICE.</b></p>
            <p style='color:#cccccc;'>Veri kaynağı: Resmi Binance API. Tüm kararlar kullanıcıya aittir.</p>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="info-box" style="border-left: 10px solid #FFD700;">
            <h3 style='color:#FFD700; margin-top:0;'>🛡️ SDR STRATEJİ / STRATEGY</h3>
            <p style='color:#ffffff;'>🚀 <b>%88+ POWER:</b> Kar Al (Take Profit).</p>
            <p style='color:#ffffff;'>📉 <b>%15- POWER:</b> Toplama (Accumulation).</p>
            <p style='color:#00d4ff;'>Sistem 15 saniyede bir Binance üzerinden güncellenir.</p>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br><p style='text-align:center; opacity: 0.5; color:white;'>© 2026 SDR SADRETTİN TURAN • OFFICIAL BINANCE DATA</p>", unsafe_allow_html=True)
