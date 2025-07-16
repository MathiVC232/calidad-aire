import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd

st.set_page_config(page_title="Calidad del Aire Básico", page_icon="🌎", layout="wide")
st.title("🌬️ Evaluador Básico de Calidad del Aire en Ecuador (sin archivos)")

# Datos AQI de ejemplo
aqi_por_provincia = {
    "Pichincha": 170,
    "Guayas": 145,
    "Azuay": 100,
    "Loja": 70,
    "Tungurahua": 120,
}

def get_color(aqi):
    if aqi > 150:
        return "red"
    elif aqi > 100:
        return "orange"
    else:
        return "green"

# Coordenadas muy simples de polígonos (solo aproximados)
provincias_coords = {
    "Pichincha": [
        [-0.1, -78.6],
        [-0.5, -78.2],
        [-0.3, -78.0],
    ],
    "Guayas": [
        [-2.5, -79.5],
        [-2.9, -79.0],
        [-3.0, -79.6],
    ],
    "Azuay": [
        [-2.8, -78.8],
        [-3.1, -78.4],
        [-3.3, -78.9],
    ],
    "Loja": [
        [-4.0, -79.3],
        [-4.3, -79.1],
        [-4.4, -79.5],
    ],
    "Tungurahua": [
        [-1.3, -78.5],
        [-1.6, -78.3],
        [-1.4, -78.1],
    ],
}

# Crear mapa
m = folium.Map(location=[-1.5, -78.5], zoom_start=6)

# Añadir polígonos con color y tooltip
for provincia, coords in provincias_coords.items():
    aqi = aqi_por_provincia.get(provincia, 50)
    color = get_color(aqi)
    folium.Polygon(
        locations=coords,
        color="black",
        fill=True,
        fill_color=color,
        fill_opacity=0.6,
        tooltip=f"{provincia}: AQI {aqi}"
    ).add_to(m)

# Mostrar mapa en Streamlit
st.subheader("Mapa básico de Provincias y Calidad del Aire")
st_folium(m, width=700, height=500)

# Selección de provincia para mostrar detalles
provincias = list(aqi_por_provincia.keys())
seleccion = st.selectbox("Selecciona una provincia para ver detalles:", provincias)

aqi_seleccion = aqi_por_provincia[seleccion]
st.metric(label=f"AQI en {seleccion}", value=aqi_seleccion)

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
datos_simulados = [max(0, aqi_seleccion + (i - 7)*5) for i in range(len(horas))]
df_graf = pd.DataFrame({"Hora": horas, "AQI": datos_simulados})
st.line_chart(df_graf.set_index("Hora"))

st.markdown("---")
st.caption("🌐 Proyecto estudiantil – Unidad Educativa Julio Pierregrosse – App básica en Streamlit")
