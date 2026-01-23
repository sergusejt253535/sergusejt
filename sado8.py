import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta
import plotly.express as px
from streamlit_autorefresh import st_autorefresh

# --- 1. AYARLAR ---
st.set_page_config(page_title="SDR PRESTIGE GLOBAL", layout="wide")
st_autorefresh(interval=15 * 1000, key="sdr_final_heist")

# --- 2. CSS TASARIM ---
st.markdown("""
    <style>
    .stApp { background-color: #000000 !important; }
    .top-bar { display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; padding: 15px; border-bottom: 3px solid #FFD700; margin-bottom: 15px; }
    .main-title { color: #00d4ff; text-align: center; font-family: 'Arial Black'; font-size: 55px; text-shadow: 0px 0px 30px #00d4ff; }
    .sub-title { color: #ffffff; text-align: center; font-family: 'Courier New'; font-size: 20px; letter-spacing: 5px; margin-bottom: 20px; }
    div[data-testid="stDataFrame"] { background-color: #000000 !important; border: 4px solid #FFD700 !important; border-radius: 15px; }
    .stDataFrame td { color: #FFD700 !important; font-weight: bold !important; font-size: 18px !important; }
    .info-box { background-color: #111; border: 2px solid #FFD700; padding: 25px; border-radius: 15px; color: white; min-height: 250px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. VERİ MOTORU (AGRESİF MOD) ---
def get_live_data():
    assets = ['BTCUSDT', 'ETHUSDT', 'SOLUSDT', 'AVAXUSDT', 'XRPUSDT', 'BNBUSDT', 'ADAUSDT', 'DOGEUSDT', 'DOTUSDT', 'LINKUSDT', 'MATICUSDT', 'TRXUSDT', 'UNIUSDT', 'BCHUSDT', 'SUIUSDT', 'FETUSDT', 'RENDERUSDT', 'PEPEUSDT', 'SHIBUSDT']
    rows = []
    
    try:
        # Doğrudan Pandas ile JSON okumayı dene (Bazen engelleri aşar)
        url = "https://api.binance.com/api/v3/ticker/24hr"
        all_data = pd.read_json(url)
        active_data = all_data[all_data['symbol'].isin(assets)]
        
        for _, item in active_data.iterrows():
            p = float(item['lastPrice'])
            h = float(item['highPrice'])
            l = float(item['lowPrice'])
            v = (float(item['quoteVolume']) / 1_000_000) / 24
            
            diff = h - l
            guc = int(((p - l) / diff) * 100) if diff != 0 else 50
            guc = max(min(guc, 99), 1)
            
            if guc > 88: 
                sig, ana = "🛡️ SELL", "🚨 ZİRVE: Kâr Al & Nakde Geç / PEAK: Take Profit & Exit"
            elif guc < 15: 
                sig, ana = "💰 BUY", "🔥 DİP: Kademeli Topla / BOTTOM: Accumulate"
            elif 15 <= guc < 40:
                sig, ana = "🥷 WAIT", "⌛ PUSU: Bekle ve İzle / AMBUSH: Wait & Watch"
            else: 
                sig, ana = "📈 FOLLOW", "💎 TREND: Takip Et / TREND: Keep Following"
            
            rows.append({
                "SDR SİNYAL": sig, "VARLIK / ASSET": item['symbol'].replace("USDT", ""),
                "FİYAT / PRICE": f"{p:,.2f} $", "HACİM / VOL (1H)": f"${v:,.2f} M",
                "GÜÇ / POWER (%)": f"%{guc}", "POWER_NUM": guc, "ANALİZ / ANALYSIS": ana
            })
    except:
        # Hata durumunda boş dönme, "Veri Bekleniyor" satırları oluştur
        for sym in assets:
            rows.append({
                "SDR SİNYAL": "🔄 CONNECTING", "VARLIK / ASSET": sym.replace("USDT", ""),
                "FİYAT / PRICE": "---", "HACİM / VOL (1H)": "---", 
                "GÜÇ / POWER (%)": "%50", "POWER_NUM": 50, "ANALİZ / ANALYSIS": "API BEKLENİYOR / WAITING FOR API"
            })
    
    return pd.DataFrame(rows)

# --- 4. PANEL ---
su_an_utc = datetime.utcnow()
su_an_tr = su_an_utc + timedelta(hours=3)

st.markdown(f"""
    <div class="top-bar">
        <div style='color:#00ffcc; font-weight:bold;'>OFFICIAL BINANCE API | 15S</div>
        <div style='color:white;'>📅 {su_an_tr.strftime("%d.%m.%Y")} | 🌍 UTC: {su_an_utc.strftime("%H:%M:%S")} | 🇹🇷 TR: {su_an_tr.strftime("%H:%M:%S")}</div>
        <div style='color:#FFD700; font-weight:bold;'>SDR PRESTIGE</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="main-title">SDR PRESTIGE GLOBAL</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">SADRETTİN TURAN VIP ANALYTICS</div>', unsafe_allow_html=True)

df = get_live_data()

# ANA TABLO
st.dataframe(df[["SDR SİNYAL", "VARLIK / ASSET", "FİYAT / PRICE", "HACİM / VOL (1H)", "GÜÇ / POWER (%)", "ANALİZ / ANALYSIS"]].style.set_properties(**{
    'background-color': '#000000', 'color': '#FFD700', 'font-weight': 'bold'
}), use_container_width=True, hide_index=True, height=600)

st.write("---")

# GRAFİK
fig = px.bar(df, x='VARLIK / ASSET', y='POWER_NUM', color='POWER_NUM', color_continuous_scale='Blues')
fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color="white"))
st.plotly_chart(fig, use_container_width=True)

# --- 5. DETAYLI ALT KUTULAR ---
st.write("---")
c1, col_space, c2 = st.columns([10, 1, 10]) # Ortada boşluk bıraktık daha prestijli dursun

with c1:
    st.markdown("""<div class="info-box" style="border-left: 12px solid #ff4b4b;">
        <h3 style='color:#ff4b4b;'>⚠️ YASAL UYARI / LEGAL NOTICE</h3>
        <p><b>[TR]:</b> Bu panelde sunulan veriler sadece bilgilendirme amaçlıdır. Yatırım danışmanlığı kapsamında değildir. Kripto paralar yüksek risk içerir, tüm karar ve sorumluluk kullanıcıya aittir.</p>
        <hr style='border:0.1px solid #333'>
        <p><i><b>[EN]:</b> The data presented here is for informational purposes only. It is not investment advice. Cryptocurrencies involve high risk; all decisions and responsibilities belong to the user.</i></p>
    </div>""", unsafe_allow_html=True)

with c2:
    st.markdown("""<div class="info-box" style="border-left: 12px solid #FFD700;">
        <h3 style='color:#FFD700;'>🛡️ SDR STRATEJİ / STRATEGY</h3>
        <p><b>[TR]:</b> Güç %88 üzerindeyse zirve noktasına yaklaşılmıştır, kâr alımı düşünülmelidir. %15 altı ise güvenli toplama bölgesidir. Sistem Binance üzerinden verileri 15 saniyede bir günceller.</p>
        <hr style='border:0.1px solid #333'>
        <p><i><b>[EN]:</b> If power is above 88%, the peak is near and profit-taking should be considered. Below 15% is the safe accumulation zone. System updates every 15s via Binance API.</i></p>
    </div>""", unsafe_allow_html=True)

st.markdown("<br><p style='text-align:center; opacity: 0.6; color:#FFD700;'>© 2026 SDR SADRETTİN TURAN • PRESTIGE GLOBAL TERMINAL</p>", unsafe_allow_html=True)
