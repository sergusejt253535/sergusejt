import streamlit as st
import pandas as pd
import requests
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# --- 1. AYARLAR ---
st.set_page_config(page_title="SDR PRESTIGE - CANLI TABLO", layout="wide")

# --- 2. 15 SANİYELİK GÜNCELLEME MOTORU ---
st_autorefresh(interval=15 * 1000, key="datarefresh")

# --- 3. TASARIM (TABLOYU ÖNE ÇIKARAN SİYAH & ALTIN) ---
st.markdown("""
    <style>
    .stApp { background-color: #000000 !important; }
    .main-title { color: #00d4ff; text-align: center; font-family: 'Arial Black'; font-size: 50px; text-shadow: 0px 0px 20px #00d4ff; }
    
    /* TABLO TASARIMI: PİYASADA YOK DEDİĞİN TABLO İŞTE BU! */
    div[data-testid="stDataFrame"] {
        border: 4px solid #FFD700 !important;
        border-radius: 15px;
        background-color: #000000 !important;
        padding: 5px;
    }
    .stDataFrame td, .stDataFrame th { font-size: 20px !important; color: #FFD700 !important; font-weight: bold !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. BİNANCE CANLI VERİ MOTORU (30+ COIN) ---
def get_sdr_live_table():
    assets = [
        'BTCUSDT', 'ETHUSDT', 'SOLUSDT', 'AVAXUSDT', 'XRPUSDT', 'BNBUSDT', 'ADAUSDT', 'DOGEUSDT', 
        'DOTUSDT', 'LINKUSDT', 'MATICUSDT', 'NEARUSDT', 'SUIUSDT', 'FETUSDT', 'OPUSDT', 'ARBUSDT', 
        'TIAUSDT', 'PEPEUSDT', 'SHIBUSDT', 'RENDERUSDT', 'LTCUSDT', 'BCHUSDT', 'APTUSDT', 'FILUSDT', 
        'ICPUSDT', 'STXUSDT', 'INJUSDT', 'GALAUSDT', 'TRXUSDT', 'ORDIUSDT'
    ]
    try:
        # Binance'den 24 saatlik tüm ticker verilerini alıyoruz
        r = requests.get("https://api.binance.com/api/v3/ticker/24hr", timeout=10)
        data = r.json()
        # Sadece senin istediğin coinleri süzüyoruz
        active = [i for i in data if i['symbol'] in assets]
        rows = []
        for item in active:
            p = float(item.get('lastPrice', 0)) # Güncel Fiyat
            h = float(item.get('highPrice', 0)) # 24s En Yüksek
            l = float(item.get('lowPrice', 0)) # 24s En Düşük
            ch = float(item.get('priceChangePercent', 0)) # Değişim
            
            # SDR GÜÇ ALGORİTMASI (Fiyatın gün içindeki yerini ölçer)
            guc = int(((p - l) / (h - l)) * 100) if (h - l) != 0 else 0
            
            # Sinyal Kararları
            if guc > 85: 
                s, a = "🛡️ SELL / SAT", "🚨 KÂR AL / TAKE PROFIT"
            elif guc < 15: 
                s, a = "💰 BUY / AL", "🔥 DİP: TOPLA / ACCUMULATE"
            else: 
                s, a = "📈 FOLLOW / İZLE", "💎 TREND TAKİBİ / TRACKING"

            rows.append({
                "SDR SİNYAL": s,
                "VARLIK / ASSET": item['symbol'].replace("USDT", ""),
                "FİYAT / PRICE": f"{p:,.2f} $",
                "24S DEĞİŞİM": f"%{ch}",
                "GÜÇ / POWER (%)": f"%{guc}",
                "SDR ANALİZ / ANALYSIS": a
            })
        return pd.DataFrame(rows)
    except Exception as e:
        return pd.DataFrame()

# --- 5. EKRAN ÇIKTISI ---
st.markdown('<div class="main-title">SDR PRESTIGE GLOBAL TERMINAL</div>', unsafe_allow_html=True)
st.write(f"<p style='text-align:center; color:white;'>Güncelleme / Last Update: {datetime.now().strftime('%H:%M:%S')}</p>", unsafe_allow_html=True)

df = get_sdr_live_table()

if not df.empty:
    # İŞTE O TABLO SADO'M, EKRANI KAPLIYOR!
    st.dataframe(
        df, 
        use_container_width=True, 
        hide_index=True, 
        height=1000 # Boyunu devasa yaptım ki her şey gözüksün
    )
else:
    st.error("Veri bağlantısı kurulamadı. Binance API kontrol ediliyor...")

st.markdown("<p style='text-align:center; color:#444;'>© 2026 SDR VIP Sadrettin Turan</p>", unsafe_allow_html=True)
