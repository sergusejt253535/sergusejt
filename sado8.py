import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta
from streamlit_autorefresh import st_autorefresh

# --- 1. AYARLAR & 15 SANİYE GÜNCELLEME ---
st.set_page_config(page_title="SDR ALGORITHMIC TERMINAL", layout="wide")
st_autorefresh(interval=15 * 1000, key="sdr_ghost_engine")

# --- 2. PRESTİJ TASARIM (CSS) ---
st.markdown("""
    <style>
    .stApp { background-color: #000000 !important; }
    .top-bar { display: flex; justify-content: space-between; align-items: center; padding: 15px; border-bottom: 2px solid #FFD700; margin-bottom: 20px; }
    .main-title { color: #00d4ff; text-align: center; font-family: 'Arial Black'; font-size: 50px; text-shadow: 0px 0px 20px #00d4ff; }
    .sub-title { color: #ffffff; text-align: center; font-family: 'Courier New'; font-size: 18px; letter-spacing: 5px; margin-bottom: 25px; }
    div[data-testid="stDataFrame"] { border: 2px solid #FFD700 !important; border-radius: 10px; background-color: #000; }
    .info-box { background: #0a0a0a; border: 1px solid #FFD700; padding: 25px; border-radius: 15px; color: white; min-height: 280px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SDR ALGORİTMİK VERİ MOTORU (GLOBAL HUB) ---
def get_sdr_data():
    # Binance engeline karşı Global Hub kullanıyoruz
    assets = "BTC,ETH,SOL,AVAX,XRP,BNB,ADA,DOGE,LINK,SUI,PEPE,FET,MATIC,DOT"
    url = f"https://min-api.cryptocompare.com/data/pricemultifull?fsyms={assets}&tsyms=USD"
    
    rows = []
    try:
        r = requests.get(url, timeout=10)
        data = r.json()['RAW']
        
        for coin in data:
            item = data[coin]['USD']
            p = float(item['PRICE'])
            h = float(item['HIGH24HOUR'])
            l = float(item['LOW24HOUR'])
            v = float(item['VOLUME24HOURTO']) / 1_000_000 # Milyon $
            change = float(item['CHANGEPCT24HOUR'])
            
            # SDR GÜÇ ANALİZİ (Price Positioning)
            guc = int(((p - l) / (h - l)) * 100) if (h - l) != 0 else 50
            guc = max(min(guc, 99), 1)
            
            # --- SDR VIP ANALİZ SÜTUNU (TR/EN) ---
            if guc > 88:
                analiz = "🛡️ SATIŞ BÖLGESİ: Kâr Al / SELL ZONE: Take Profit"
                sig = "🔴 SELL"
            elif guc < 15:
                analiz = "💰 TOPLAMA ALANI: Kademeli Al / ENTRY ZONE: Accumulate"
                sig = "🟢 BUY"
            elif change > 5:
                analiz = "🚀 GÜÇLÜ TREND: Takip Et / STRONG TREND: Follow"
                sig = "⚡ BOOM"
            else:
                analiz = "⌛ YATAY PİYASA: Pusuya Yat / NEUTRAL: Wait in Ambush"
                sig = "🥷 WAIT"
            
            rows.append({
                "SDR SİNYAL": sig,
                "VARLIK (ASSET)": coin,
                "FİYAT (PRICE)": f"{p:,.2f} $",
                "24H DEĞİŞİM": f"%{change:,.2f}",
                "GÜÇ (POWER)": f"%{guc}",
                "SDR VIP ANALİZ / ALGORITHMIC ANALYSIS": analiz
            })
    except:
        # Hata anında bile tablo iskeleti kalsın
        return pd.DataFrame([{"SDR SİNYAL": "🔄", "VARLIK (ASSET)": "RECONNECTING", "FİYAT (PRICE)": "---", "24H DEĞİŞİM": "---", "GÜÇ (POWER)": "---", "SDR VIP ANALİZ / ALGORITHMIC ANALYSIS": "SİSTEM BAĞLANIYOR / RECONNECTING TO HUB..."}])
    
    return pd.DataFrame(rows)

# --- 4. PANEL ---
now = datetime.utcnow() + timedelta(hours=3)
st.markdown(f"""
    <div class="top-bar">
        <div style='color:#00ffcc; font-weight:bold;'>📡 SDR GHOST-HUB ENGINE ACTIVE</div>
        <div style='color:white;'>📅 {now.strftime("%d.%m.%Y")} | 🇹🇷 TR: {now.strftime("%H:%M:%S")}</div>
        <div style='color:#FFD700; font-weight:bold;'>SDR PRESTIGE</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="main-title">SDR PRESTIGE GLOBAL</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">SADRETTİN TURAN VIP ANALYTICS</div>', unsafe_allow_html=True)

# Tabloyu Bas
df = get_sdr_data()
st.dataframe(df.style.set_properties(**{
    'background-color': '#000',
    'color': '#FFD700',
    'font-weight': 'bold'
}), use_container_width=True, hide_index=True, height=550)

# --- 5. BİLGİ KUTULARI ---
st.write("---")
c1, c2 = st.columns(2)

with c1:
    st.markdown("""<div class="info-box" style="border-left: 10px solid #ff4b4b;">
        <h3 style='color:#ff4b4b;'>⚠️ YASAL UYARI / LEGAL NOTICE</h3>
        <p><b>[TR]:</b> SDR Prestige Global terminali, karmaşık algoritmalar kullanarak veri sunar. Bu veriler hiçbir şekilde yatırım tavsiyesi veya sıcak para vaadi değildir. Tüm risk kullanıcıya aittir.</p>
        <hr style='border: 0.1px solid #333;'>
        <p><i><b>[EN]:</b> The SDR Prestige terminal provides data using complex algorithms. This information is not investment advice. All risks are the responsibility of the user.</i></p>
    </div>""", unsafe_allow_html=True)

with c2:
    st.markdown("""<div class="info-box" style="border-left: 10px solid #FFD700;">
        <h3 style='color:#FFD700;'>🛡️ SDR VIP ALGORİTMA / ALGO-GUIDE</h3>
        <p><b>[TR]:</b> Tablodaki analiz sütunu, fiyatın gün içi dip ve zirve dengesini ölçerek SDR modeline göre yorum yapar. Sistem her 15 saniyede bir küresel veri merkezlerinden güncellenir.</p>
        <hr style='border: 0.1px solid #333;'>
        <p><i><b>[EN]:</b> The analysis column interprets the market using the SDR model by measuring intraday balance. Updates every 15s from global data hubs.</i></p>
    </div>""", unsafe_allow_html=True)

st.markdown("<p style='text-align:center; opacity: 0.5; color:#FFD700;'>© 2026 SDR SADRETTİN TURAN • PRESTIGE GLOBAL • PRIVATE ALGORITHMIC INTERFACE</p>", unsafe_allow_html=True)
