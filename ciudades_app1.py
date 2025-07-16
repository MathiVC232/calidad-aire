import streamlit as st
import requests
import pydeck as pdk
import json
import pandas as pd

st.set_page_config(page_title="Calidad del Aire Ecuador", page_icon="🌎", layout="wide")
st.title("🌬️ Evaluador Mejorado de Calidad del Aire – Ecuador")

# Cargar GeoJSON desde URL (prueba esta que sí funciona)
url = "https://raw.githubusercontent.com/codeforamerica/click_that_hood/main/public/data/ecuador-provincias.geojson"
response = requests.get(url)
geojson = response.json()

# Datos AQI ejemplo
aqi_por_provincia = {
    "Pichincha": 170,
    "Guayas": 145,
    "Azuay": 100,
    "Loja": 70,
    "Tungurahua": 120,
    "El Oro": 130,
    "Esmeraldas": 130,
    "Manabí": 125,
    "Chimborazo": 105,
    "Carchi": 65,
    "Napo": 75,
    "Galápagos": 40,
    # Completa según necesites
}

def get_color(aqi):
    if aqi > 150:
        return [255, 0, 0, 140]
    elif aqi > 100:
        return [255, 165, 0, 140]
    else:
        return [0, 128, 0, 140]

for feature in geojson["features"]:
    nombre = feature["properties"]["name"]
    aqi = aqi_por_provincia.get(nombre, 50)
    feature["properties"]["fill_color"] = get_color(aqi)
    feature["properties"]["aqi"] = aqi

provincias = list(aqi_por_provincia.keys())
seleccion = st.selectbox("Selecciona una provincia:", provincias)

aqi_seleccion = aqi_por_provincia[seleccion]
st.metric(label=f"AQI en {seleccion}", value=aqi_seleccion)

if aqi_seleccion > 150:
    st.error("❌ Calidad del aire MALA. Usa mascarilla y evita salir.")
elif aqi_seleccion > 100:
    st.warning("⚠️ Calidad MODERADA. Precaución si tienes asma o problemas respiratorios.")
else:
    st.success("✅ Calidad BUENA. Puedes salir con tranquilidad.")

layer = pdk.Layer(
    "GeoJsonLayer",
    geojson,
    pickable=True,
    auto_highlight=True,
    get_fill_color="properties.fill_color",
    get_line_color=[255, 255, 255],
    line_width_min_pixels=1,
)

view_state = pdk.ViewState(
    latitude=-1.5,
    longitude=-78.5,
    zoom=6,
    pitch=0,
)

deck = pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    map_style="mapbox://styles/mapbox/light-v9",
    tooltip={"text": "{name}\nAQI: {aqi}"},
)

st.pydeck_chart(deck)

st.subheader("📈 Evolución simulada del AQI durante el día")
horas = [f"{h}:00" for h in range(6, 20)]
datos_simulados = [max(0, aqi_seleccion + (i - 7)*5) for i in range(len(horas))]
df_graf = pd.DataFrame({"Hora": horas, "AQI": datos_simulados})
st.line_chart(df_graf.set_index("Hora"))

st.markdown("---")
st.caption("🌐 Proyecto estudiantil – Unidad Educativa Julio Pierregrosse – App desarrollada en Streamlit")
