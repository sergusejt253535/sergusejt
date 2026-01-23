import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta
import plotly.express as px
from streamlit_autorefresh import st_autorefresh

# --- 1. AYARLAR ---
st.set_page_config(page_title="SDR PRESTIGE GLOBAL", layout="wide")

# Veriyi her 15 saniyede bir otomatik tazeler
st_autorefresh(interval=15 * 1000, key="sdr_standard_engine")

# --- 2. GÖRSEL TASARIM (CSS) ---
st.markdown("""
    <style>
    .stApp { background-color: #000000 !important; }
    .top-bar { display: flex; justify-content: space-between; align-items: center; padding: 15px; border-bottom: 3px solid #FFD700; margin-bottom: 15px; }
    .main-title { color: #00d4ff; text-align: center; font-family: 'Arial Black'; font-size: 55px; text-shadow: 0px 0px 30px #00d4ff; }
    .sub-title { color: #ffffff; text-align: center; font-family: 'Courier New'; font-size: 20px; letter-spacing: 5px; margin-bottom: 20px; }
    div[data-testid="stDataFrame"] { background-color: #000000 !important; border: 4px solid #FFD700 !important; border-radius: 15px; }
    .stDataFrame td { color: #FFD700 !important; font-weight: bold !important; font-size: 18px !important; }
    .info-box { background-color: #111; border: 2px solid #FFD700; padding: 25px; border-radius: 15px; color: white; min-height: 250px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. VERİ ÇEKME MOTORU ---
def get_live_data():
    assets = ['BTCUSDT', 'ETHUSDT', 'SOLUSDT', 'AVAXUSDT', 'XRPUSDT', 'BNBUSDT', 'ADAUSDT', 'DOGEUSDT', 'DOTUSDT', 'LINKUSDT', 'MATICUSDT', 'TRXUSDT', 'UNIUSDT', 'BCHUSDT', 'SUIUSDT', 'FETUSDT', 'RENDERUSDT', 'PEPEUSDT', 'SHIBUSDT']
    rows = []
    
    try:
        # Binance ana sunucusundan veri çekimi
        url = "https://api.binance.com/api/v3/ticker/24hr"
        r = requests.get(url, timeout=10)
        data = r.json()
        
        # Sadece listedeki coinleri ayıkla
        active_data = [d for d in data if d['symbol'] in assets]
        
        for item in active_data:
            p = float(item['lastPrice'])
            h = float(item['highPrice'])
            l = float(item['lowPrice'])
            v = (float(item['quoteVolume']) / 1_000_000) / 24 # 1 Saatlik ortalama hacim tahmini
            
            # SDR Güç Analizi
            diff = h - l
            guc = int(((p - l) / diff) * 100) if diff != 0 else 50
            guc = max(min(guc, 99), 1)
            
            # Sinyal ve Analiz Mantığı
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
        # Bağlantı koparsa tablo yapısı bozulmasın diye boş satırlar
        for sym in assets:
            rows.append({"SDR SİNYAL": "🔄 CONNECTING", "VARLIK / ASSET": sym.replace("USDT", ""), "FİYAT / PRICE": "---", "HACİM / VOL (1H)": "---", "GÜÇ / POWER (%)": "---", "POWER_NUM": 0, "ANALİZ / ANALYSIS": "BAĞLANTI BEKLENİYOR / WAITING CONNECTION"})
    
    return pd.DataFrame(rows)

# --- 4. PANEL GÖVDESİ ---
su_an_utc = datetime.utcnow()
su_an_tr = su_an_utc + timedelta(hours=3)

st.markdown(f"""
    <div class="top-bar">
        <div style='color:#00ffcc; font-weight:bold;'>OFFICIAL BINANCE DATA FEED</div>
        <div style='color:white;'>📅 {su_an_tr.strftime("%d.%m.%Y")} | 🇹🇷 TR: {su_an_tr.strftime("%H:%M:%S")}</div>
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

# GRAFİK BÖLÜMÜ
st.write("---")
fig = px.bar(df, x='VARLIK / ASSET', y='POWER_NUM', color='POWER_NUM', color_continuous_scale='Blues')
fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color="white"))
st.plotly_chart(fig, use_container_width=True)

# --- 5. BİLGİ KUTULARI (UZUN VE DETAYLI) ---
st.write("---")
c1, c2 = st.columns(2)
with c1:
    st.markdown("""<div class="info-box" style="border-left: 12px solid #ff4b4b;">
        <h3 style='color:#ff4b4b;'>⚠️ YASAL UYARI / LEGAL NOTICE</h3>
        <p><b>[TR]:</b> Bu panelde sunulan tüm veriler, analizler ve sinyaller sadece bilgilendirme amaçlıdır. Hiçbir şekilde yatırım danışmanlığı teşkil etmez. Kripto varlık piyasaları yüksek derecede oynaklık ve risk taşır; bu nedenle yatırımlarınızda oluşabilecek herhangi bir maddi zarardan SDR Prestige Global veya sistem sorumlu tutulamaz. Karar vermeden önce kendi araştırmanızı yapmanız önerilir.</p>
        <hr style='border:0.1px solid #333'>
        <p><i><b>[EN]:</b> All data, analysis, and signals presented on this panel are for informational purposes only. It does not constitute investment advice. Cryptocurrency markets carry high volatility and risk; therefore, SDR Prestige Global or the system cannot be held responsible for any financial losses. It is recommended to conduct your own research before making decisions.</i></p>
    </div>""", unsafe_allow_html=True)

with c2:
    st.markdown("""<div class="info-box" style="border-left: 12px solid #FFD700;">
        <h3 style='color:#FFD700;'>🛡️ SDR STRATEJİ / STRATEGY</h3>
        <p><b>[TR]:</b> Sistem, varlığın son 24 saatteki en düşük ve en yüksek seviyelerine göre güncel fiyatın konumunu ölçer. Güç (POWER) %88 üzerindeyse, varlık zirve noktasına yakındır ve kâr realizasyonu düşünülmelidir. %15'in altındaki seviyeler ise 'aşırı satış' bölgesini işaret eder ve kademeli toplama için fırsat olabilir. Veriler 15 saniyede bir güncellenir.</p>
        <hr style='border:0.1px solid #333'>
        <p><i><b>[EN]:</b> The system measures the position of the current price based on the last 24-hour low and high. If POWER is above 88%, the asset is near its peak, and profit-taking should be considered. Levels below 15% indicate an 'oversold' zone and potential accumulation opportunity. Data updates every 15 seconds.</i></p>
    </div>""", unsafe_allow_html=True)

st.markdown("<p style='text-align:center; opacity: 0.6; color:#FFD700;'>© 2026 SDR SADRETTİN TURAN • PRESTIGE GLOBAL TERMINAL</p>", unsafe_allow_html=True)
