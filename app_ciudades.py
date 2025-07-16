import streamlit as st

# Configurar la página
st.set_page_config(page_title="Simulador Calidad del Aire", page_icon="🌬️", layout="centered")

# Título principal
st.title("🌍 Simulador de Calidad del Aire por Ciudad")

st.markdown("""
Selecciona una ciudad del Ecuador para consultar un valor **simulado** del Índice de Calidad del Aire (AQI), basado en datos históricos y condiciones comunes.
""")

# Datos reales aproximados (valores AQI típicos)
datos_realistas = {
    "Quito": 85,
    "Guayaquil": 155,
    "Cuenca": 95,
    "Loja": 70,
    "Ambato": 115,
    "Esmeraldas": 130,
    "Manta": 105
}

# Descripciones por nivel AQI
niveles = {
    "BUENO": {"color": "green", "emoji": "✅", "mensaje": "Puedes respirar tranquilo 😌"},
    "MODERADO": {"color": "orange", "emoji": "⚠️", "mensaje": "Precaución para personas con asma"},
    "MALO": {"color": "red", "emoji": "❌", "mensaje": "Evita salir sin mascarilla 😷"}
}

# Elegir ciudad
ciudad = st.selectbox("🌆 Elige una ciudad:", list(datos_realistas.keys()))

# Obtener valor AQI
aqi = datos_realistas[ciudad]
st.markdown(f"### AQI en **{ciudad}**: `{aqi}`")

# Evaluación
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

# Mostrar barra de AQI
st.markdown("#### Indicador visual del nivel AQI")
st.progress(min(aqi / 200, 1.0))

# Recomendaciones extra
st.markdown("### 📝 Recomendaciones:")
if nivel == "MALO":
    st.write("- Usa mascarilla N95 si sales a la calle.")
    st.write("- Cierra ventanas y evita ejercitarte afuera.")
    st.write("- Usa purificadores o plantas si estás en casa.")
elif nivel == "MODERADO":
    st.write("- Personas con asma o alergias deben tener cuidado.")
    st.write("- Evita actividades físicas intensas al aire libre.")
else:
    st.write("- No hay restricciones. ¡Disfruta el día!")

# Pie de página
st.markdown("---")
st.caption("🌐 Simulación educativa basada en datos de ciudades del Ecuador. Proyecto estudiantil – Julio Pierregrosse.")
