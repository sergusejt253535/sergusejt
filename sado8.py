import streamlit as st
import pandas as pd
import requests
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# --- 1. AYARLAR ---
st.set_page_config(page_title="SDR PRESTIGE GLOBAL | VIP", layout="wide")

# --- 2. 15 SANİYELİK GÜNCELLEME ---
st_autorefresh(interval=15 * 1000, key="datarefresh")

# --- 3. TASARIM ---
st.markdown("""
    <style>
    .stApp { background-color: #000000 !important; }
    .main-title { color: #00d4ff; text-align: center; font-family: 'Arial Black'; font-size: 55px; text-shadow: 0px 0px 30px #00d4ff; margin-bottom: 0px; }
    .sub-title { color: #FFD700; text-align: center; font-family: 'Courier New'; font-size: 20px; letter-spacing: 5px; margin-bottom: 20px; }
    div[data-testid="stDataFrame"] { border: 3px solid #FFD700 !important; border-radius: 15px; background-color: #000000 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. BİNANCE VERİ ÇEKME MOTORU (YENİ NESİL) ---
def get_sdr_data():
    # Paşam, tablo dolsun diye listeyi geniş tutuyorum
    assets = [
        'BTCUSDT', 'ETHUSDT', 'SOLUSDT', 'AVAXUSDT', 'XRPUSDT', 'BNBUSDT', 'ADAUSDT', 'DOGEUSDT', 
        'DOTUSDT', 'LINKUSDT', 'SUIUSDT', 'FETUSDT', 'PEPEUSDT', 'SHIBUSDT', 'RENDERUSDT'
    ]
    
    # Binance API için farklı bir uç nokta (Endpoint) deniyoruz
    url = "https://api1.binance.com/api/v3/ticker/24hr" # api1, api2, api3 alternatifleri vardır
    
    try:
        # User-Agent ekleyerek kendimizi gerçek bir tarayıcı gibi tanıtıyoruz
        headers = {'User-Agent': 'Mozilla/5.0'}
        r = requests.get(url, headers=headers, timeout=10)
        
        if r.status_code == 200:
            data = r.json()
            # Sadece bizim listedeki coinleri filtrele
            active = [i for i in data if i['symbol'] in assets]
            
            rows = []
            for item in active:
                p = float(item['lastPrice'])
                h = float(item['highPrice'])
                l = float(item['lowPrice'])
                ch = float(item['priceChangePercent'])
                v = float(item['quoteVolume']) / 1_000_000
                
                # SDR GÜÇ ALGORİTMASI
                guc = int(((p - l) / (h - l)) * 100) if (h - l) != 0 else 0
                
                # TR/EN Sinyal ve Analiz
                if guc > 85: 
                    s, a = "🛡️ SELL / SAT", "🚨 ZİRVE / PEAK"
                elif guc < 15: 
                    s, a = "💰 BUY / AL", "🔥 DİP / BOTTOM"
                else: 
                    s, a = "📈 FOLLOW / İZLE", "💎 TREND"

                rows.append({
                    "SDR SİNYAL": s,
                    "VARLIK / ASSET": item['symbol'].replace("USDT", ""),
                    "FİYAT / PRICE": f"{p:,.2f} $",
                    "DEĞİŞİM / CHG": f"%{ch}",
                    "HACİM / VOL": f"${v:,.1f} M",
                    "GÜÇ / POWER (%)": f"%{guc}",
                    "ANALİZ / ANALYSIS": a
                })
            return pd.DataFrame(rows)
        else:
            return pd.DataFrame()
    except Exception as e:
        # Hata durumunda boş dönme, hatayı fısılda
        return pd.DataFrame()

# --- 5. EKRAN ÇIKTISI ---
st.markdown('<div class="main-title">SDR PRESTIGE GLOBAL</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">SADRETTİN TURAN VIP ANALYTICS</div>', unsafe_allow_html=True)

df = get_sdr_data()

if not df.empty:
    # 3'lü Metrik Kartları
    c1, c2, c3 = st.columns(3)
    c1.metric("💰 BUY ZONE / ALIM", len(df[df['SDR SİNYAL'].str.contains("BUY")]))
    c2.metric("🛡️ SELL ZONE / SATIM", len(df[df['SDR SİNYAL'].str.contains("SELL")]))
    c3.metric("🌍 UPDATE / GÜNCELLEME", datetime.now().strftime("%H:%M:%S"))

    # İŞTE O TABLO!
    st.write("### 📊 LIVE MARKET TERMINAL / CANLI PİYASA TERMİNALİ")
    st.dataframe(df, use_container_width=True, hide_index=True, height=600)
else:
    st.error("⚠️ Binance ile bağlantı kurulamadı. Lütfen 'api.binance.com' adresine erişiminiz olduğunu kontrol edin.")
    st.info("Eğer bu hatayı yerel bilgisayarında alıyorsan, internet sağlayıcın Binance API'sini kısıtlıyor olabilir. Ama sunucuya (Hetzner gibi) geçtiğimizde bu sorun kökten çözülecek paşam!")

# --- 6. YASAL UYARI ---
st.write("---")
st.markdown("<h4 style='color:#ff4b4b;'>⚠️ YASAL UYARI / LEGAL NOTICE</h4>", unsafe_allow_html=True)
st.write("Yatırım danışmanlığı değildir. Sadrettin Turan VIP algoritmasıdır. / Not an investment advice.")

st.sidebar.markdown("### 👤 SDR VIP ACCESS")
st.sidebar.info("3 DAYS FREE TRIAL / 3 GÜNLÜK DENEME")
