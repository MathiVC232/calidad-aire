import streamlit as st
import pandas as pd
import time
import random
import pydeck as pdk

# Configuración de la página
st.set_page_config(page_title="Calidad del Aire Ecuador", page_icon="🌎", layout="wide")

st.title("🌬️ Evaluador Mejorado de Calidad del Aire – Ecuador")

# ---------- Datos simulados ----------
ciudades = {
    "Quito": {"aqi": 170, "lat": -0.2295, "lon": -78.5243},
    "Guayaquil": {"aqi": 145, "lat": -2.1709, "lon": -79.9224},
    "Cuenca": {"aqi": 100, "lat": -2.9006, "lon": -79.0045},
    "Loja": {"aqi": 70, "lat": -3.9931, "lon": -79.2042},
    "Ambato": {"aqi": 120, "lat": -1.2417, "lon": -78.6197},
    "Machala": {"aqi": 130, "lat": -3.2581, "lon": -79.9554},
    "Esmeraldas": {"aqi": 130, "lat": 0.9517, "lon": -79.6616},
    "Manta": {"aqi": 125, "lat": -0.9677, "lon": -80.7128},
    "Riobamba": {"aqi": 105, "lat": -1.6646, "lon": -78.6546},
    "Tulcán": {"aqi": 65, "lat": 0.8143, "lon": -77.7174},
    "Tena": {"aqi": 75, "lat": -1.0375, "lon": -77.8139},
    "Galápagos": {"aqi": 40, "lat": -0.9022, "lon": -89.5926}
}

# ---------- Selección de ciudad principal ----------
col1, col2 = st.columns(2)
with col1:
    ciudad = st.selectbox("🌆 Selecciona una ciudad", ciudades.keys())

# ---------- Mapa interactivo ----------
st.subheader("🗺️ Ubicación de la ciudad seleccionada")

df_map = pd.DataFrame([{
    "ciudad": ciudad,
    "lat": ciudades[ciudad]["lat"],
    "lon": ciudades[ciudad]["lon"]
}])

st.pydeck_chart(pdk.Deck(
    map_style='mapbox://styles/mapbox/light-v9',
    initial_view_state=pdk.ViewState(
        latitude=ciudades[ciudad]["lat"],
        longitude=ciudades[ciudad]["lon"],
        zoom=6,
        pitch=40,
    ),
    layers=[
        pdk.Layer(
            'ScatterplotLayer',
            data=df_map,
            get_position='[lon, lat]',
            get_color='[255, 0, 0, 160]',
            get_radius=10000,
        ),
    ],
))

# ---------- Mostrar AQI ----------
aqi = ciudades[ciudad]["aqi"]
st.metric(label=f"💨 AQI en {ciudad}", value=aqi)

# ---------- Evaluación y color ----------
if aqi > 150:
    nivel, color, emoji = "MALO", "red", "❌"
elif aqi > 100:
    nivel, color, emoji = "MODERADO", "orange", "⚠️"
else:
    nivel, color, emoji = "BUENO", "green", "✅"

st.markdown(f"""
<div style="background-color:{color};padding:20px;border-radius:10px;">
    <h2 style="color:white;text-align:center;">{emoji} {nivel}</h2>
</div>
""", unsafe_allow_html=True)

# ---------- Comparador ----------
with col2:
    comparar = st.selectbox("🔁 Comparar con otra ciudad", [c for c in ciudades if c != ciudad])
    aqi2 = ciudades[comparar]["aqi"]
    st.metric(label=f"AQI en {comparar}", value=aqi2)

# ---------- Gráfico de evolución diaria ----------
st.subheader("📈 Evolución simulada del AQI durante el día")

horas = [f"{h}:00" for h in range(6, 20)]
datos_simulados = [aqi + random.randint(-15, 15) for _ in horas]

df_graf = pd.DataFrame({"Hora": horas, "AQI": datos_simulados})
st.line_chart(df_graf.set_index("Hora"))

# ---------- Botón de alerta ----------
if st.button("🚨 Activar Alerta Sanitaria"):
    with st.expander("🔊 Instrucciones en caso de alerta"):
        st.write("- Evita salir de casa.")
        st.write("- Usa mascarilla si es necesario salir.")
        st.write("- Cierra puertas y ventanas.")
        st.write("- Activa purificador o crea un filtro casero.")

# ---------- Recomendaciones según perfil ----------
st.subheader("👤 Personaliza las recomendaciones")

edad = st.slider("Edad", 5, 90, 16)
asma = st.checkbox("Tengo asma o problemas respiratorios")
zona = st.radio("¿Dónde vives?", ["Urbana", "Rural"])

st.markdown("### Recomendaciones para ti:")

if aqi > 150:
    st.error("❌ Evita salir.")
    if asma:
        st.warning("⚠️ Riesgo alto para personas con asma.")
elif aqi > 100:
    st.warning("⚠️ Precaución al hacer ejercicio afuera.")
else:
    st.success("✅ Puedes salir con tranquilidad.")

if zona == "Urbana" and aqi > 120:
    st.info("🌇 Usa plantas purificadoras dentro de casa o ventilación cruzada.")

if zona == "Rural" and aqi < 100:
    st.info("🌳 Disfruta del aire limpio de tu zona rural.")

# ---------- Pie de página ----------
st.markdown("---")
st.caption("🌐 Proyecto estudiantil – Unidad Educativa Julio Pierregrosse – App desarrollada en Streamlit")
