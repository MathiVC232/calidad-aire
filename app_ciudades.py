import streamlit as st
import pandas as pd
import random
import pydeck as pdk

# Configuración página
st.set_page_config(page_title="Calidad del Aire Ecuador", page_icon="🌎", layout="wide")

st.title("🌬️ Evaluador Mejorado de Calidad del Aire – Ecuador")

# Datos simulados
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

# ======= SECCIÓN 1: Detalle de ciudad seleccionada =======
st.header("🌆 Información de la ciudad seleccionada")

ciudad = st.selectbox("Selecciona una ciudad:", list(ciudades.keys()))
info = ciudades[ciudad]
aqi = info["aqi"]

st.metric(label=f"AQI en {ciudad}", value=aqi)

# Evaluación con color y emoji
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

# Mapa centrado en la ciudad seleccionada
df_ciudad = pd.DataFrame([{
    "ciudad": ciudad,
    "lat": info["lat"],
    "lon": info["lon"],
    "aqi": aqi
}])

st.subheader(f"🗺️ Mapa interactivo de {ciudad}")
st.pydeck_chart(pdk.Deck(
    map_style="mapbox://styles/mapbox/light-v9",
    initial_view_state=pdk.ViewState(
        latitude=info["lat"],
        longitude=info["lon"],
        zoom=10,
        pitch=0,
    ),
    layers=[
        pdk.Layer(
            "ScatterplotLayer",
            data=df_ciudad,
            get_position='[lon, lat]',
            get_fill_color="[255, 0, 0, 160]",
            get_radius=10000,
            pickable=True,
        )
    ],
    tooltip={"text": "{ciudad}\nAQI: {aqi}"}
))

# Gráfico simulado evolución del AQI
st.subheader("📈 Evolución simulada del AQI durante el día")

horas = [f"{h}:00" for h in range(6, 20)]
datos_simulados = [aqi + random.randint(-15, 15) for _ in horas]

df_graf = pd.DataFrame({"Hora": horas, "AQI": datos_simulados})
st.line_chart(df_graf.set_index("Hora"))

# ======= SECCIÓN 2: Comparar con otra ciudad =======
st.header("🔁 Comparar con otra ciudad")

otra_ciudad = st.selectbox("Selecciona la ciudad para comparar:", [c for c in ciudades if c != ciudad])
aqi2 = ciudades[otra_ciudad]["aqi"]
st.metric(label=f"AQI en {otra_ciudad}", value=aqi2)

# ======= SECCIÓN 3: Mapa general con todas las ciudades =======
st.header("🗺️ Mapa interactivo de todas las ciudades del Ecuador")

df_todas = pd.DataFrame([
    {"ciudad": nombre, "lat": info["lat"], "lon": info["lon"], "aqi": info["aqi"]}
    for nombre, info in ciudades.items()
])

layer = pdk.Layer(
    "ScatterplotLayer",
    data=df_todas,
    get_position='[lon, lat]',
    get_fill_color="""
        [aqi > 150 ? 255 : aqi > 100 ? 255 : 0,
         aqi <= 100 ? 200 : 165,
         0, 160]
    """,
    get_radius=7000,
    pickable=True,
)

st.pydeck_chart(pdk.Deck(
    map_style="mapbox://styles/mapbox/light-v9",
    initial_view_state=pdk.ViewState(
        latitude=-1.5,
        longitude=-78.0,
        zoom=5.5,
        pitch=0,
    ),
    layers=[layer],
    tooltip={"text": "📍 {ciudad}\nAQI: {aqi}"}
))

# ======= SECCIÓN 4: Botón de alerta y recomendaciones (puedes seguir agregando aquí) =======
if st.button("🚨 Activar Alerta Sanitaria"):
    with st.expander("🔊 Instrucciones en caso de alerta"):
        st.write("- Evita salir de casa.")
        st.write("- Usa mascarilla si es necesario salir.")
        st.write("- Cierra puertas y ventanas.")
        st.write("- Activa purificador o crea un filtro casero.")

st.markdown("---")
st.caption("🌐 Proyecto estudiantil – Unidad Educativa Julio Pierregrosse – App desarrollada en Streamlit")
