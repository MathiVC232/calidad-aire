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

# Convertir a DataFrame para pydeck
df_ciudades = pd.DataFrame([
    {"Ciudad": c, "Lat": d["lat"], "Lon": d["lon"], "AQI": d["aqi"]} for c, d in ciudades.items()
])

def color_por_aqi(aqi):
    if aqi > 150:
        return [255, 0, 0]       # rojo
    elif aqi > 100:
        return [255, 165, 0]     # naranja
    else:
        return [0, 128, 0]       # verde

df_ciudades['color'] = df_ciudades['AQI'].apply(color_por_aqi)

# SECCIÓN 1: Ciudad seleccionada y detalles
st.header("🌆 Información de la ciudad seleccionada")
ciudad = st.selectbox("Selecciona una ciudad:", df_ciudades['Ciudad'])
info = df_ciudades[df_ciudades['Ciudad'] == ciudad].iloc[0]
aqi = info['AQI']

st.metric(label=f"AQI en {ciudad}", value=aqi)

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

# Mapa centrado en la ciudad seleccionada (pydeck)
st.subheader(f"🗺️ Mapa de {ciudad}")

view_ciudad = pdk.ViewState(
    latitude=info['Lat'],
    longitude=info['Lon'],
    zoom=12,
    pitch=0,
)

layer_ciudad = pdk.Layer(
    "ScatterplotLayer",
    data=[info],
    get_position='[Lon, Lat]',
    get_color=info['color'],
    get_radius=5000,
    radius_min_pixels=20,
    radius_max_pixels=40,
)

deck_ciudad = pdk.Deck(
    layers=[layer_ciudad],
    initial_view_state=view_ciudad,
    tooltip={"text": f"{ciudad}\nAQI: {aqi}"}
)

st.pydeck_chart(deck_ciudad)

# Gráfico evolución AQI simulado
st.subheader("📈 Evolución simulada del AQI durante el día")
horas = [f"{h}:00" for h in range(6, 20)]
datos_simulados = [max(0, aqi + random.randint(-15, 15)) for _ in horas]
df_graf = pd.DataFrame({"Hora": horas, "AQI": datos_simulados})
st.line_chart(df_graf.set_index("Hora"))

# SECCIÓN 2: Comparar con otra ciudad
st.header("🔁 Comparar con otra ciudad")
otra_ciudad = st.selectbox("Selecciona la ciudad para comparar:", [c for c in df_ciudades['Ciudad'] if c != ciudad])
aqi2 = df_ciudades[df_ciudades['Ciudad'] == otra_ciudad]['AQI'].values[0]
st.metric(label=f"AQI en {otra_ciudad}", value=aqi2)

# SECCIÓN 3: Mapa general con pydeck (todas las ciudades)
st.header("🗺️ Mapa general interactivo de todas las ciudades")

layer_general = pdk.Layer(
    "ScatterplotLayer",
    data=df_ciudades,
    get_position='[Lon, Lat]',
    get_color='color',
    get_radius=30000,
    pickable=True,
    radius_min_pixels=15,
    radius_max_pixels=40,
)

view_general = pdk.ViewState(
    latitude=-1.5,
    longitude=-78.5,
    zoom=6,
    pitch=0,
)

deck_general = pdk.Deck(
    layers=[layer_general],
    initial_view_state=view_general,
    tooltip={"text": "{Ciudad}\nAQI: {AQI}"}
)

st.pydeck_chart(deck_general)

# SECCIÓN 4: Recomendaciones personalizadas
st.header("👤 Personaliza las recomendaciones")

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

# SECCIÓN 5: Botón alerta y consejos
if st.button("🚨 Activar Alerta Sanitaria"):
    with st.expander("🔊 Instrucciones en caso de alerta"):
        st.write("- Evita salir de casa.")
        st.write("- Usa mascarilla si es necesario salir.")
        st.write("- Cierra puertas y ventanas.")
        st.write("- Activa purificador o crea un filtro casero.")

st.markdown("---")
st.caption("🌐 Proyecto estudiantil – Unidad Educativa Julio Pierregrosse – App desarrollada en Streamlit")
