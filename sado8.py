import streamlit as st
import pandas as pd
import requests
import plotly.graph_objects as go
from datetime import datetime, timedelta
from streamlit_autorefresh import st_autorefresh

# --- 1. AYARLAR & 15 SANİYE GÜNCELLEME ---
st.set_page_config(page_title="SDR PRESTIGE GLOBAL | V.FINAL", layout="wide")
st_autorefresh(interval=15 * 1000, key="sdr_final_show")

# --- 2. ÜST DÜZEY VIP TASARIM (CSS) ---
st.markdown("""
    <style>
    .stApp { background-color: #000000 !important; }
    .top-bar { display: flex; justify-content: space-between; align-items: center; padding: 20px; border-bottom: 4px solid #FFD700; margin-bottom: 25px; background: #080808; border-radius: 0 0 15px 15px; }
    .main-title { color: #00d4ff; text-align: center; font-family: 'Impact'; font-size: 65px; text-shadow: 0px 0px 35px #00d4ff; margin-bottom: 5px; }
    .sub-title { color: #ffffff; text-align: center; font-family: 'Courier New'; font-size: 24px; letter-spacing: 8px; margin-bottom: 35px; font-weight: bold; }
    div[data-testid="stDataFrame"] { border: 3px solid #FFD700 !important; border-radius: 15px; background-color: #000 !important; }
    .info-box { background: #0a0a0a; border: 2px solid #FFD700; padding: 35px; border-radius: 20px; color: white; min-height: 320px; box-shadow: 0px 0px 15px rgba(255, 215, 0, 0.2); }
    hr { border: 0.5px solid #333 !important; margin: 40px 0 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. UTC & TR ZAMAN DİLİMLERİ ---
utc_now = datetime.utcnow()
tr_now = utc_now + timedelta(hours=3)

st.markdown(f"""
    <div class="top-bar">
        <div style='color:#00ffcc; font-weight:bold; font-size:20px;'>📡 SDR GLOBAL CORE ACTIVE</div>
        <div style='color:white; font-family:monospace; font-size:20px;'>
            <b>UTC:</b> {utc_now.strftime("%H:%M:%S")} | <b>TR:</b> {tr_now.strftime("%H:%M:%S")}
        </div>
        <div style='color:#FFD700; font-weight:bold; font-size:20px; letter-spacing:3px;'>SDR PRESTIGE</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="main-title">SDR PRESTIGE GLOBAL</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">SADRETTİN TURAN VIP ANALYTICS</div>', unsafe_allow_html=True)

# --- 4. VERİ VE SDR ALGORİTMA MOTORU ---
def get_sdr_exclusive_data():
    # Binance ve Global Hub hibrit veri akışı
    assets = "BTC,ETH,SOL,AVAX,XRP,BNB,ADA,DOGE,LINK,SUI,PEPE,FET,RENDER,MATIC"
    url = f"https://min-api.cryptocompare.com/data/pricemultifull?fsyms={assets}&tsyms=USD"
    rows = []
    try:
        r = requests.get(url, timeout=10).json()['RAW']
        for coin in r:
            i = r[coin]['USD']
            p, h, l, c = i['PRICE'], i['HIGH24HOUR'], i['LOW24HOUR'], i['CHANGEPCT24HOUR']
            v = i['VOLUME24HOURTO'] / 1_000_000
            # SDR GÜÇ ANALİZİ
            guc = int(((p - l) / (h - l)) * 100) if (h-l) != 0 else 50
            guc = max(min(guc, 99), 1)
            
            # --- SDR VIP ANALİZ SÜTUNU (TR/EN) ---
            if guc > 88:
                ana = "🛡️ KRİTİK ZİRVE: Kâr Al / CRITICAL PEAK: Take Profit"
                sig = "🔴 SELL"
            elif guc < 15:
                ana = "💰 DİP FIRSATI: Kademeli Al / BOTTOM ENTRY: Accumulate"
                sig = "🟢 BUY"
            elif v > 1000:
                ana = "🐋 BALİNA HAREKETİ: Takip Et / WHALE INFLOW: Follow"
                sig = "⚡ ALERT"
            else:
                ana = "📈 TREND TAKİBİ: Bekle / TREND WATCH: Wait"
                sig = "🥷 WAIT"

            rows.append({
                "SİNYAL": sig, "VARLIK / ASSET": coin, "FİYAT / PRICE": p, 
                "DEĞİŞİM %": c, "GÜÇ / POWER %": guc, "SDR VIP ANALİZ / ALGORITHMIC ANALYSIS": ana
            })
    except: return pd.DataFrame()
    return pd.DataFrame(rows)

df = get_sdr_exclusive_data()

if not df.empty:
    # VIP TABLO
    st.dataframe(df.style.format({"FİYAT / PRICE": "{:,.2f} $", "DEĞİŞİM %": "% {:,.2f}", "GÜÇ / POWER %": "% {}"}).set_properties(**{
        'background-color': '#000', 'color': '#FFD700', 'font-weight': 'bold', 'font-size': '16px'
    }), use_container_width=True, hide_index=True, height=500)

    # --- PROFESYONEL GRAFİKLER ---
    st.write("---")
    g1, g2 = st.columns(2)
    with g1:
        fig1 = go.Figure(go.Bar(x=df['VARLIK / ASSET'], y=df['DEĞİŞİM %'], marker_color=df['DEĞİŞİM %'], marker_colorscale='RdYlGn'))
        fig1.update_layout(title="Piyasa Nabzı / Market Pulse (%)", template="plotly_dark", plot_bgcolor='black', paper_bgcolor='black')
        st.plotly_chart(fig1, use_container_width=True)
    with g2:
        fig2 = go.Figure(go.Scatter(x=df['VARLIK / ASSET'], y=df['GÜÇ / POWER %'], mode='lines+markers', fill='toself', line=dict(color='#00d4ff')))
        fig2.update_layout(title="SDR Güç Endeksi / SDR Power Index", template="plotly_dark", plot_bgcolor='black', paper_bgcolor='black')
        st.plotly_chart(fig2, use_container_width=True)
else:
    st.warning("📡 Veri Hattına Bağlanılıyor... / Connecting to SDR Hub...")

# --- 5. BİLGİ KUTULARI (TR/EN) ---
st.write("---")
c1, c2 = st.columns(2)
with c1:
    st.markdown("""<div class="info-box" style="border-left: 15px solid #ff4b4b;">
        <h3 style='color:#ff4b4b;'>⚠️ YASAL UYARI / LEGAL NOTICE</h3>
        <p><b>[TR]:</b> SDR Prestige Global terminali bilgilendirme amaçlıdır. Sunulan algoritmik analizler yatırım tavsiyesi değildir.</p>
        <p><i><b>[EN]:</b> Information purposes only. Algorithmic analyses provided are not investment advice.</i></p>
    </div>""", unsafe_allow_html=True)
with c2:
    st.markdown("""<div class="info-box" style="border-left: 15px solid #FFD700;">
        <h3 style='color:#FFD700;'>🛡️ SDR VIP STRATEJİ / STRATEGY</h3>
        <p><b>[TR]:</b> Güç %15 altı toplama, %88 üstü boşaltma bölgesidir. Veriler 15 saniyede bir küresel ağdan yenilenir.</p>
        <p><i><b>[EN]:</b> Accumulate below 15% Power, exit above 88%. Data refreshes every 15s via global network.</i></p>
    </div>""", unsafe_allow_html=True)

st.markdown("<p style='text-align:center; opacity: 0.5; color:#FFD700; font-size:14px;'>© 2026 SDR SADRETTİN TURAN • PRESTIGE GLOBAL TERMINAL</p>", unsafe_allow_html=True)
