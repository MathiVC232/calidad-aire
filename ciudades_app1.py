import streamlit as st
import pandas as pd
import random
import pydeck as pdk

# Configuración de la página
st.set_page_config(page_title="Calidad del Aire Ecuador", page_icon="🌎", layout="wide")

st.title("🌬️ Evaluador Mejorado de Calidad del Aire – Ecuador")

# Datos simulados para provincias y capitales
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

# ===== SECCIÓN 1: Ciudad seleccionada =====
st.header("🌆 Información de la ciudad seleccionada")

ciudad = st.selectbox("Selecciona una ciudad:", list(ciudades.keys()))
info = ciudades[ciudad]
aqi = info["aqi"]

st.metric(label=f"AQI en {ciudad}", value=aqi)

# Evaluación con color y emoji
if aqi > 150:
    nivel, color, emoji = "MALO", [255, 0, 0], "❌"
elif aqi > 100:
    nivel, color, emoji = "MODERADO", [255, 165, 0], "⚠️"
else:
    nivel, color, emoji = "BUENO", [0, 128, 0], "✅"

st.markdown(f"""
<div style="background-color:rgb({color[0]}, {color[1]}, {color[2]}); padding: 20px; border-radius: 10px; color: white; text-align: center;">
    <h2>{emoji} {nivel}</h2>
</div>
""", unsafe_allow_html=True)

# Mapa con PyDeck centrado en la ciudad seleccionada
df = pd.DataFrame([{
    "lat": info["lat"],
    "lon": info["lon"],
    "ciudad": ciudad,
    "aqi": aqi,
    "color": color
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
            data=df,
            get_position='[lon, lat]',
            get_color='color',
            get_radius=20000,
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

# ===== SECCIÓN 2: Comparar con otra ciudad =====
st.header("🔁 Comparar con otra ciudad")
otra_ciudad = st.selectbox("Selecciona la ciudad para comparar:", [c for c in ciudades if c != ciudad])
aqi2 = ciudades[otra_ciudad]["aqi"]
st.metric(label=f"AQI en {otra_ciudad}", value=aqi2)

# ===== SECCIÓN 3: Mapa general con PyDeck (todas las ciudades) =====
st.header("🗺️ Mapa interactivo de todas las ciudades del Ecuador")

df_all = pd.DataFrame([{
    "lat": data["lat"],
    "lon": data["lon"],
    "ciudad": nombre,
    "aqi": data["aqi"],
    "color": [255, 0, 0] if data["aqi"] > 150 else [255, 165, 0] if data["aqi"] > 100 else [0, 128, 0]
} for nombre, data in ciudades.items()])

st.pydeck_chart(pdk.Deck(
    map_style="mapbox://styles/mapbox/light-v9",
    initial_view_state=pdk.ViewState(
        latitude=-1.5,
        longitude=-78.0,
        zoom=6,
        pitch=0,
    ),
    layers=[
        pdk.Layer(
            "ScatterplotLayer",
            data=df_all,
            get_position='[lon, lat]',
            get_color='color',
            get_radius=15000,
            picka
