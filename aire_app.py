import streamlit as st

st.set_page_config(page_title="Calidad del Aire", page_icon="🌬️", layout="centered")

st.title("🌱 Evaluador de Calidad del Aire")

valor = st.number_input("Ingresa el valor del sensor MQ-135 (0-1023):", min_value=0, max_value=1023)

if st.button("Evaluar calidad del aire"):
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

    # Mostrar mensaje con color
    st.markdown(f"<h2 style='color: {color};'>{nivel}</h2>", unsafe_allow_html=True)
    st.write(mensaje)

    # Mostrar barra de progreso para visualizar la calidad
    progreso = min(valor / 200, 1.0)  # Normaliza valor entre 0 y 1 (suponiendo 200 como máximo para escala)
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
