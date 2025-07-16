import streamlit as st
import pydeck as pdk
import pandas as pd

st.set_page_config(page_title="Calidad del Aire Ecuador", page_icon="🌬️", layout="wide")
st.title("🌬️ Evaluador de Calidad del Aire – Ecuador")

# Datos ejemplo (latitud, longitud, AQI, provincia)
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

# Crear la capa de puntos para PyDeck
layer = pdk.Layer(
    'ScatterplotLayer',
    data=data,
    get_position='[Lon, Lat]',
    get_color='color',
    get_radius=30000,
    pickable=True,
    radius_min_pixels=15,
    radius_max_pixels=40,
)

# Configurar la vista inicial del mapa
view_state = pdk.ViewState(
    latitude=-1.5,
    longitude=-78.5,
    zoom=6,
    pitch=0,
)

# Crear el mapa con PyDeck
r = pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    tooltip={"text": "{Provincia}\nAQI: {AQI}"}
)

st.subheader("Mapa interactivo de Provincias con Calidad del Aire")
st.pydeck_chart(r)

# Selección de provincia para mostrar detalles
provincia_seleccionada = st.selectbox("Selecciona una provincia para ver detalles:", data['Provincia'])

aqi_seleccion = data.loc[data['Provincia'] == provincia_seleccionada, 'AQI'].values[0]
st.metric(label=f"AQI en {provincia_seleccionada}", value=aqi_seleccion)

# Recomendaciones según AQI
if aqi_seleccion > 150:
    st.error("❌ Calidad del aire MALA. Usa mascarilla y evita salir.")
elif aqi_seleccion > 100:
    st.warning("⚠️ Calidad MODERADA. Precaución si tienes asma o problemas respiratorios.")
else:
    st.success("✅ Calidad BUENA. Puedes salir con tranquilidad.")

# Gráfico simulado de evolución diaria del AQI
st.subheader("📈 Evolución simulada del AQI durante el día")

horas = [f"{h}:00" for h in range(6, 20)]
datos_simulados = [max(0, aqi_seleccion + (i - 7) * 5) for i in range(len(horas))]

df_grafico = pd.DataFrame({"Hora": horas, "AQI": datos_simulados})

st.line_chart(df_grafico.set_index("Hora"))

st.markdown("---")
st.caption("🌐 Proyecto estudiantil – Unidad Educativa Julio Pierregrosse – App en Streamlit")
