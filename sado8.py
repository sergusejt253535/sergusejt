import streamlit as st
import pandas as pd
import requests
import plotly.express as px
from datetime import datetime, timedelta
from streamlit_autorefresh import st_autorefresh

# --- 1. AYARLAR & 15 SANİYE GÜNCELLEME ---
st.set_page_config(page_title="SDR PRESTIGE GLOBAL", layout="wide")

# Sayfayı her 15 saniyede bir canlandırır (Zaman ve Veri için)
st_autorefresh(interval=15 * 1000, key="sdr_full_engine")

# --- 2. PRESTİJ TASARIM (CSS) ---
st.markdown("""
    <style>
    .stApp { background-color: #000000 !important; }
    .top-bar { 
        display: flex; justify-content: space-between; align-items: center; 
        padding: 15px; border-bottom: 2px solid #FFD700; margin-bottom: 20px; 
    }
    .main-title { color: #00d4ff; text-align: center; font-family: 'Arial Black'; font-size: 50px; text-shadow: 0px 0px 20px #00d4ff; }
    .sub-title { color: #ffffff; text-align: center; font-family: 'Courier New'; font-size: 18px; letter-spacing: 5px; margin-bottom: 25px; }
    div[data-testid="stDataFrame"] { border: 2px solid #FFD700 !important; border-radius: 10px; background-color: #000; }
    .info-box { background: #0a0a0a; border: 1px solid #FFD700; padding: 25px; border-radius: 15px; color: white; min-height: 280px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SAAT VE ZAMAN DİLİMLERİ ---
utc_now = datetime.utcnow()
tr_now = utc_now + timedelta(hours=3)

st.markdown(f"""
    <div class="top-bar">
        <div style='color:#00ffcc; font-weight:bold;'>📡 SDR GLOBAL ENGINE ACTIVE</div>
        <div style='color:white; font-family:monospace;'>
            <b>UTC:</b> {utc_now.strftime("%H:%M:%S")} | <b>TR:</b> {tr_now.strftime("%H:%M:%S")}
        </div>
        <div style='color:#FFD700; font-weight:bold;'>SDR PRESTIGE</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="main-title">SDR PRESTIGE GLOBAL</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">SADRETTİN TURAN VIP ANALYTICS</div>', unsafe_allow_html=True)

# --- 4. VERİ VE GRAFİK MOTORU ---
def get_sdr_full_data():
    assets = "BTC,ETH,SOL,AVAX,XRP,BNB,ADA,DOGE,LINK,SUI,PEPE,FET,RENDER"
    url = f"https://min-api.cryptocompare.com/data/pricemultifull?fsyms={assets}&tsyms=USD"
    rows = []
    try:
        r = requests.get(url, timeout=10)
        data = r.json()['RAW']
        for coin in data:
            item = data[coin]['USD']
            p, h, l = float(item['PRICE']), float(item['HIGH24HOUR']), float(item['LOW24HOUR'])
            change = float(item['CHANGEPCT24HOUR'])
            guc = int(((p - l) / (h - l)) * 100) if (h - l) != 0 else 50
            guc = max(min(guc, 99), 1)

            # SDR VIP ANALİZ (TR/EN)
            if guc > 85: ana = "🛡️ ZİRVE: Kâr Al / PEAK: Take Profit"; sig = "🔴 SELL"
            elif guc < 15: ana = "💰 DİP: Kademeli Al / BOTTOM: Accumulate"; sig = "🟢 BUY"
            else: ana = "📈 TRENDİ İZLE / WATCH TREND"; sig = "🥷 WAIT"

            rows.append({
                "SİNYAL": sig, "VARLIK": coin, "FİYAT": p, 
                "DEĞİŞİM": change, "GÜÇ %": guc, "SDR VIP ANALİZ / ANALYSIS": ana
            })
    except: return pd.DataFrame()
    return pd.DataFrame(rows)

df = get_sdr_full_data()

if not df.empty:
    # Tablo Kısmı
    st.dataframe(df.style.format({"FİYAT": "{:,.2f} $", "DEĞİŞİM": "% {:,.2f}", "GÜÇ %": "% {}"}).set_properties(**{
        'background-color': '#000', 'color': '#FFD700', 'font-weight': 'bold'
    }), use_container_width=True, hide_index=True)

    # --- GRAFİKLER BÖLÜMÜ ---
    st.write("---")
    col_g1, col_g2 = st.columns(2)
    with col_g1:
        fig_price = px.bar(df, x='VARLIK', y='DEĞİŞİM', color='DEĞİŞİM', title="Günlük Değişim / Daily Change (%)", color_continuous_scale='RdYlGn')
        fig_price.update_layout(plot_bgcolor='black', paper_bgcolor='black', font=dict(color="white"))
        st.plotly_chart(fig_price, use_container_width=True)
    with col_g2:
        fig_power = px.line(df, x='VARLIK', y='GÜÇ %', title="SDR Güç Endeksi / SDR Power Index", markers=True)
        fig_power.update_layout(plot_bgcolor='black', paper_bgcolor='black', font=dict(color="white"))
        st.plotly_chart(fig_power, use_container_width=True)
else:
    st.error("Veri bekleniyor... / Waiting for data...")

# --- 5. BİLGİ KUTULARI ---
st.write("---")
c1, c2 = st.columns(2)
with c1:
    st.markdown("""<div class="info-box" style="border-left: 10px solid #ff4b4b;">
        <h3 style='color:#ff4b4b;'>⚠️ YASAL UYARI / LEGAL NOTICE</h3>
        <p>[TR]: Veriler bilgilendirme amaçlıdır, yatırım tavsiyesi değildir. [EN]: Data is for info only, not investment advice.</p>
    </div>""", unsafe_allow_html=True)
with c2:
    st.markdown("""<div class="info-box" style="border-left: 10px solid #FFD700;">
        <h3 style='color:#FFD700;'>🛡️ STRATEJİ / STRATEGY</h3>
        <p>[TR]: 15 saniyede bir güncellenir. %15 altı alış, %85 üstü satış bölgesidir. [EN]: Refreshes every 15s. <15% buy, >85% sell.</p>
    </div>""", unsafe_allow_html=True)
