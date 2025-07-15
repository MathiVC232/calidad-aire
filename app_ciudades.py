import streamlit as st

# Datos simulados para cada ciudad (valores de calidad del aire)
datos_ciudades = {
    "Quito": 80,
    "Guayaquil": 160,
    "Cuenca": 110,
    "Loja": 90,
    "Ambato": 130
}

st.title("🌆 Simulador de Calidad del Aire por Ciudad")

ciudad = st.selectbox("Elige una ciudad:", list(datos_ciudades.keys()))

valor = datos_ciudades[ciudad]

st.write(f"Calidad del aire simulada para **{ciudad}**:")

# Evaluar calidad
if valor > 150:
    nivel = "MALO"
    mensaje = "❌ Usa mascarilla 😷"
    color = "red"
elif valor > 100:
    nivel = "MODERADO"
    mensaje = "⚠️ Precaución si tienes asma"
    color = "orange"
else:
    nivel = "BUENO"
    mensaje = "✅ Puedes salir tranquilo 😊"
    color = "green"

# Mostrar resultado
st.markdown(f"<h2 style='color: {color};'>{nivel}</h2>", unsafe_allow_html=True)
st.write(mensaje)

# Barra de progreso para visualización
progreso = min(valor / 200, 1.0)
st.progress(progreso)

# Recomendaciones
st.markdown("### Recomendaciones:")
if nivel == "MALO":
    st.write("- Evita salir si no es necesario.")
    st.write("- Usa mascarilla N95 o similar.")
    st.write("- Mantén las ventanas cerradas.")
elif nivel == "MODERADO":
    st.write("- Evita ejercicio intenso afuera.")
    st.write("- Personas con asma deben tomar precauciones.")
else:
    st.write("- Disfruta el aire libre con tranquilidad.")
