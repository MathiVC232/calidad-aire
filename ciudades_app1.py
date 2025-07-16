import streamlit as st
import pydeck as pdk
import pandas as pd

st.title("Mapa interactivo básico con PyDeck - Calidad del Aire Ecuador")

# Datos de ejemplo (latitud, longitud, AQI, provincia)
data = pd.DataFrame({
    'Provincia': ['Pichincha', 'Guayas', 'Azuay', 'Loja', 'Tungurahua'],
    'Lat': [-0.1807, -2.1894, -2.8974, -4.0041, -1.2532],
    'Lon': [-78.4678, -79.8891, -78.9959, -79.2047, -78.6158],
    'AQI': [170, 145, 100, 70, 120]
})

def get_color(aqi):
    if aqi > 150:
        return [255, 0, 0]       # rojo
    elif aqi > 100:
        return [255, 165, 0]     # naranja
    else:
        return [0, 128, 0]       # verde

data['color'] = data['AQI'].apply(get_color)

# Crear el mapa PyDeck
layer = pdk.Layer(
    'ScatterplotLayer',
    data=data,
    get_position='[Lon, Lat]',
    get_color='color',
    get_radius=30000,
    pickable=True,
    radius_min_pixels=10,
    radius_max_pixels=40,
)

# Configuración del visor
view_state = pdk.ViewState(
    latitude=-1.5,
    longitude=-78.5,
    zoom=6,
    pitch=0,
)

r = pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    tooltip={"text": "{Provincia}\nAQI: {AQI}"}
)

st.pydeck_chart(r)

# Selección y recomendaciones
prov = st.selectbox("Selecciona una provincia:", data['Provincia'])
aqi_sel = data.loc[data['Provincia'] == prov, 'AQI'].values[0]

st.metric(f"AQI en {prov}", aqi_sel)

if aqi_sel > 150:
    st.error("❌ Calidad del aire MALA. Usa mascarilla y evita salir.")
elif aqi_sel > 100:
    st.warning("⚠️ Calidad MODERADA. Precaución si tienes asma o problemas respiratorios.")
else:
    st.success("✅ Calidad BUENA. Puedes salir con tranquilidad.")
