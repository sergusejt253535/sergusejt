import streamlit as st
import random

# Her şeyi boşver, ekranı simsiyah yap
st.set_page_config(page_title="SADO TEST", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: red !important; }
    .test-box {
        background-color: yellow;
        color: black;
        padding: 50px;
        text-align: center;
        font-size: 50px;
        font-weight: bold;
        border: 10px solid black;
        margin-top: 100px;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="test-box">⚠️ DİKKAT! <br> BU BİR TESTTİR! <br> SİSTEMİ SİKTİK Mİ? ⚠️</div>', unsafe_allow_html=True)

st.write("Eğer bu sarı-kırmızı kutuyu görüyorsan, sistem çalışıyor demektir paşam!")
st.write(f"Rastgele Sayı: {random.randint(1, 1000000)}")
