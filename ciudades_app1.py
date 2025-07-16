import streamlit as st
import pandas as pd
import random

st.set_page_config(page_title="Calidad del Aire Ecuador", page_icon="🌬️", layout="wide")
st.title("🌬️ Evaluador de Calidad del Aire – Ecuador")

# Datos de ciudades
ciudades = {
    "Quito": 170,
    "Guayaquil": 145,
    "Cuenca": 100,
    "Loja": 70,
    "Ambato": 120,
    "Machala": 130,
    "Esmeraldas": 130,
    "Manta": 125,
    "Riobamba": 105,
    "Tulcán": 65,
    "Tena": 75,
    "Galápagos": 40
}

# Convertir a DataFrame
df_ciudades = pd.DataFrame(list(ciudades.items()), columns=["Ciudad", "AQI"])

# Colores según AQI
def nivel_aqi(aqi):
    if aqi > 150:
        return "❌ MALO"
    elif aqi > 100:
        return "⚠️ MODERADO"
    else:
        return "✅ BUENO"

df_ciudades["Nivel"] = df_ciudades["AQI"].apply(nivel_aqi)

# Selección de ciudad
st.header("🌆 Selecciona una ciudad")
ciudad = st.selectbox("Ciudad", df_ciudades["Ciudad"])
aqi = ciudades[ciudad]

# Indicador principal
st.metric(label=f"AQI en {ciudad}", value=aqi)

# Evaluación visual
if aqi > 150:
    color, mensaje = "red", "❌ MALO – Usa mascarilla 😷"
elif aqi > 100:
    color, mensaje = "orange", "⚠️ MODERADO – Precaución si tienes asma"
else:
    color, mensaje = "green", "✅ BUENO – Puedes salir tranquilo 😊"

st.markdown(f"""
<div style="background-color:{color};padding:20px;border-radius:10px;text-align:center;">
    <h2 style="color:white;">{mensaje}</h2>
</div>
""", unsafe_allow_html=True)

# Evolución simulada
st.subheader("📈 Evolución diaria del AQI")
horas = [f"{h}:00" for h in range(6, 20)]
datos = [max(0, aqi + random.randint(-15, 15)) for _ in horas]
df_graf = pd.DataFrame({"Hora": horas, "AQI": datos})
st.line_chart(df_graf.set_index("Hora"))

# Comparar con otra ciudad
st.subheader("🔁 Comparar con otra ciudad")
otra = st.selectbox("Otra ciudad", [c for c in ciudades if c != ciudad])
st.metric(label=f"AQI en {otra}", value=ciudades[otra])

# Tabla resumen de todas las ciudades
st.subheader("📋 Resumen de ciudades")

def color_fila(val):
    if val > 150:
        return "background-color: red; color: white"
    elif val > 100:
        return "background-color: orange; color: black"
    else:
        return "background-color: lightgreen; color: black"

st.dataframe(df_ciudades.style.applymap(color_fila, subset=["AQI"]))

# Recomendaciones personalizadas
st.subheader("👤 Recomendaciones personalizadas")
edad = st.slider("Edad", 5, 90, 16)
asma = st.checkbox("Tengo asma")
zona = st.radio("Vivo en zona:", ["Urbana", "Rural"])

st.markdown("### 📝 Recomendaciones:")

if aqi > 150:
    st.error("❌ Evita salir. Riesgo alto.")
    if asma:
        st.warning("⚠️ Riesgo grave si tienes asma.")
elif aqi > 100:
    st.warning("⚠️ Cuidado al hacer ejercicio al aire libre.")
else:
    st.success("✅ Buen aire, puedes disfrutar del exterior.")

if zona == "Urbana" and aqi > 120:
    st.info("🌇 Usa plantas purificadoras o ventilación cruzada.")
elif zona == "Rural" and aqi < 100:
    st.info("🌳 Disfruta del aire limpio de tu entorno.")

# Botón de alerta
if st.button("🚨 Activar Alerta Sanitaria"):
    st.warning("🚨 ALERTA ACTIVADA")
    with st.expander("🔊 Instrucciones"):
        st.write("- Evita salir.")
        st.write("- Usa mascarilla.")
        st.write("- Cierra puertas y ventanas.")
        st.write("- Usa filtro de aire casero si tienes uno.")

st.markdown("---")
st.caption("🌐 Proyecto estudiantil – Unidad Educativa Julio Pierregrosse – App desarrollada en Streamlit")
