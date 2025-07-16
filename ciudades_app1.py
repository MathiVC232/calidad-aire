import streamlit as st
import pydeck as pdk
import pandas as pd
import random

st.set_page_config(page_title="Calidad del Aire Ecuador", page_icon="🌬️", layout="wide")
st.title("🌬️ Evaluador Interactivo de Calidad del Aire – Ecuador")

# ============================ DATOS BASE ============================
data = pd.DataFrame({
    'Provincia': [
        'Azuay', 'Bolívar', 'Carchi', 'Cañar', 'Chimborazo', 'Cotopaxi', 'El Oro', 'Esmeraldas', 'Galápagos',
        'Guayas', 'Imbabura', 'Loja', 'Los Ríos', 'Manabí', 'Morona Santiago', 'Napo', 'Orellana',
        'Pastaza', 'Pichincha', 'Santa Elena', 'Santo Domingo', 'Sucumbíos', 'Tungurahua', 'Zamora Chinchipe'
    ],
    'Lat': [
        -2.8974, -1.7468, 0.8143, -2.549, -1.6646, -0.9333, -3.2581, 0.9517, -0.9022,
        -2.1894, 0.349, -3.9931, -1.045, -0.9677, -2.4621, -1.0375, -0.4629,
        -1.6095, -0.1807, -2.2297, -0.2542, 0.0886, -1.2532, -4.0690
    ],
    'Lon': [
        -78.9959, -79.1882, -77.7174, -78.938, -78.6546, -78.6167, -79.9554, -79.6616, -89.5926,
        -79.8891, -78.13, -79.2042, -79.476, -80.7128, -78.0636, -77.8139, -76.9851,
        -77.9874, -78.4678, -80.8592, -79.1695, -76.9991, -78.6158, -78.9546
    ],
    'AQI': [
        100, 90, 65, 95, 105, 110, 130, 130, 40,
        145, 85, 70, 115, 125, 90, 75, 70,
        95, 170, 120, 110, 65, 120, 80
    ]
})

# ============================ FUNCIONES ============================
def get_color(aqi):
    if aqi > 150:
        return [255, 0, 0]
    elif aqi > 100:
        return [255, 165, 0]
    else:
        return [0, 128, 0]

data['color'] = data['AQI'].apply(get_color)

# ============================ MAPA PYDECK ============================
st.subheader("🗾 Mapa interactivo de provincias")
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
view_state = pdk.ViewState(latitude=-1.5, longitude=-78.5, zoom=5.5, pitch=0)
r = pdk.Deck(layers=[layer], initial_view_state=view_state, tooltip={"text": "{Provincia}\nAQI: {AQI}"})
st.pydeck_chart(r)

# ============================ DETALLE DE UNA PROVINCIA ============================
st.header("🏠 Selecciona una provincia para ver detalles")
prov = st.selectbox("Provincia", data['Provincia'])
sel = data[data['Provincia'] == prov].iloc[0]

st.metric(f"AQI en {prov}", sel['AQI'])

if sel['AQI'] > 150:
    color, msg = "red", "❌ MALO – Usa mascarilla"
elif sel['AQI'] > 100:
    color, msg = "orange", "⚠️ MODERADO – Precaución si tienes asma"
else:
    color, msg = "green", "✅ BUENO – Puedes salir tranquilo"

st.markdown(f"""
<div style='background-color:{color};padding:1rem;border-radius:0.5rem;text-align:center;'>
    <h2 style='color:white'>{msg}</h2>
</div>
""", unsafe_allow_html=True)

# ============================ GRAFICO SIMULADO ============================
st.subheader("📊 Evolución simulada del AQI durante el día")
horas = [f"{h}:00" for h in range(6, 20)]
valores = [max(0, sel['AQI'] + random.randint(-10, 10)) for _ in horas]
df_graf = pd.DataFrame({"Hora": horas, "AQI": valores})
st.line_chart(df_graf.set_index("Hora"))

# ============================ COMPARAR OTRA PROVINCIA ============================
st.subheader("🔀 Comparar con otra provincia")
otra = st.selectbox("Otra provincia", [p for p in data['Provincia'] if p != prov])
valor_otra = data.loc[data['Provincia'] == otra, 'AQI'].values[0]
st.metric(f"AQI en {otra}", valor_otra)

# ============================ RECOMENDACIONES ============================
st.header("👤 Personaliza tus recomendaciones")
edad = st.slider("Edad", 5, 90, 16)
asma = st.checkbox("Tengo asma o problemas respiratorios")
zona = st.radio("¿Dónde vives?", ["Urbana", "Rural"])

st.markdown("### 📄 Recomendaciones para ti:")

if sel['AQI'] > 150:
    st.error("❌ Evita salir. Riesgo alto.")
    if asma:
        st.warning("⚠️ Riesgo grave si tienes asma.")
elif sel['AQI'] > 100:
    st.warning("⚠️ Precaución al hacer ejercicio afuera.")
else:
    st.success("✅ Puedes salir con tranquilidad.")

if zona == "Urbana" and sel['AQI'] > 120:
    st.info("🌇 Usa plantas purificadoras o ventilación cruzada.")
elif zona == "Rural" and sel['AQI'] < 100:
    st.info("🌳 Disfruta del aire limpio de tu zona rural.")

if edad < 12 and sel['AQI'] > 100:
    st.warning("👧 Niños deben evitar actividades físicas al aire libre.")
elif edad > 65 and sel['AQI'] > 100:
    st.warning("👴 Personas mayores deben tomar precauciones.")

# ============================ ALERTA SANITARIA ============================
if st.button("🚨 Activar Alerta Sanitaria"):
    st.warning("🚨 ALERTA ACTIVADA")
    with st.expander("🔊 Instrucciones en caso de alerta"):
        st.write("- Evita salir de casa.")
        st.write("- Usa mascarilla si es necesario salir.")
        st.write("- Cierra puertas y ventanas.")
        st.write("- Usa purificador o crea un filtro casero.")

st.markdown("---")
st.caption("🌐 Proyecto estudiantil – Unidad Educativa Julio Pierregrosse – App desarrollada en Streamlit")
