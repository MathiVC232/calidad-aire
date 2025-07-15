import streamlit as st

st.set_page_config(page_title="Calidad del Aire", page_icon="🌬️", layout="centered")

st.title("🌱 Evaluador de Calidad del Aire")

valor = st.number_input("Ingresa el valor del sensor MQ-135 (0-1023):", min_value=0, max_value=1023)

if st.button("Evaluar calidad del aire"):
    if valor > 150:
        st.error("❌ *MALO – Usa mascarilla 😷*")
    elif valor > 100:
        st.warning("⚠️ *MODERADO – Precaución si tienes asma*")
    else:
        st.success("✅ *BUENO – Puedes salir tranquilo 😊*")
