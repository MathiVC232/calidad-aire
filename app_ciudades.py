import streamlit as st

st.set_page_config(page_title="Calidad del Aire Ecuador", page_icon="🇪🇨", layout="centered")

st.title("🇪🇨 Simulador de Calidad del Aire por Capitales del Ecuador")

st.markdown("""
Selecciona la capital de una provincia del Ecuador para consultar un valor **simulado** del Índice de Calidad del Aire (AQI), basado en condiciones típicas.
""")

# Diccionario de provincias y capitales con valores simulados de AQI
capitales_ecuador = {
    "Quito (Pichincha)": 85,
    "Guayaquil (Guayas)": 160,
    "Cuenca (Azuay)": 95,
    "Loja (Loja)": 70,
    "Ambato (Tungurahua)": 115,
    "Riobamba (Chimborazo)": 100,
    "Portoviejo (Manabí)": 125,
    "Machala (El Oro)": 135,
    "Ibarra (Imbabura)": 90,
    "Latacunga (Cotopaxi)": 105,
    "Esmeraldas (Esmeraldas)": 130,
    "Babahoyo (Los Ríos)": 145,
    "Tulcán (Carchi)": 60,
    "Nueva Loja (Sucumbíos)": 110,
    "Tena (Napo)": 75,
    "Puyo (Pastaza)": 80,
    "Zamora (Zamora Chinchipe)": 65,
    "Macas (Morona Santiago)": 78,
    "Puerto Francisco de Orellana (Orellana)": 120,
    "Santo Domingo (Santo Domingo de los Tsáchilas)": 130,
    "Santa Elena (Santa Elena)": 140,
    "Bolívar (Guaranda)": 85,
    "Azogues (Cañar)": 90,
    "San Cristóbal (Galápagos)": 40
}

# Estilos por nivel de AQI
niveles = {
    "BUENO": {"color": "green", "emoji": "✅", "mensaje": "Puedes respirar tranquilo 😌"},
    "MODERADO": {"color": "orange", "emoji": "⚠️", "mensaje": "Precaución para personas con asma"},
    "MALO": {"color": "red", "emoji": "❌", "mensaje": "Evita salir sin mascarilla 😷"}
}

# Menú de selección
ciudad = st.selectbox("🏙️ Selecciona una capital de provincia:", list(capitales_ecuador.keys()))

aqi = capitales_ecuador[ciudad]
st.markdown(f"### AQI simulado para **{ciudad}**: `{aqi}`")

# Clasificación
if aqi > 150:
    nivel = "MALO"
elif aqi > 100:
    nivel = "MODERADO"
else:
    nivel = "BUENO"

info = niveles[nivel]

# Mostrar resultado visual
st.markdown(f"""
<div style="background-color:{info['color']};padding:20px;border-radius:10px;">
    <h2 style="color:white;text-align:center;">{info['emoji']} {nivel}</h2>
    <p style="color:white;text-align:center;font-size:18px;">{info['mensaje']}</p>
</div>
""", unsafe_allow_html=True)

# Indicador visual tipo barra
st.markdown("#### Indicador de nivel AQI")
st.progress(min(aqi / 200, 1.0))

# Recomendaciones según nivel
st.markdown("### 📝 Recomendaciones:")
if nivel == "MALO":
    st.write("- Usa mascarilla N95 si sales.")
    st.write("- Cierra ventanas y evita actividades al aire libre.")
    st.write("- Usa filtros o purificadores si estás en casa.")
elif nivel == "MODERADO":
    st.write("- Evita ejercicio intenso afuera.")
    st.write("- Personas con asma deben tomar precauciones.")
else:
    st.write("- No hay restricciones. ¡Disfruta el aire libre!")

# Pie
st.markdown("---")
st.caption("🌐 Simulación educativa – Proyecto estudiantil de predicción ambiental.")
