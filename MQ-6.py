import streamlit as st

st.set_page_config(page_title="Detección de Gas (MQ-6)", page_icon="🔥", layout="centered")

st.title("🔥 Detector de Gas con MQ-6")

valor = st.number_input("Ingresa el valor del sensor MQ-6 (0-1023):", min_value=0, max_value=1023)

if st.button("Evaluar nivel de gas"):
    if valor > 500:
        nivel = "PELIGROSO"
        mensaje = "🚨 ¡Posible fuga de gas! Ventila el área y evacúa."
        color = "red"
    elif valor > 300:
        nivel = "MODERADO"
        mensaje = "⚠️ Concentración perceptible, revisa ventilación."
        color = "orange"
    else:
        nivel = "SEGURO"
        mensaje = "✅ Nivel seguro de gas detectado."
        color = "green"

    # Mostrar mensaje con color
    st.markdown(f"<h2 style='color: {color};'>{nivel}</h2>", unsafe_allow_html=True)
    st.write(mensaje)

    # Barra de progreso (normalizada, suponiendo 600 como máximo)
    progreso = min(valor / 600, 1.0)
    st.progress(progreso)

    # Recomendaciones
    st.markdown("### Recomendaciones:")
    if nivel == "PELIGROSO":
        st.write("- Corta el suministro de gas inmediatamente.")
        st.write("- Ventila el área y evacúa si es necesario.")
        st.write("- No uses aparatos eléctricos.")
    elif nivel == "MODERADO":
        st.write("- Revisa posibles fugas.")
        st.write("- Mejora la ventilación del lugar.")
    else:
        st.write("- Todo en orden. Mantén ventilación adecuada.")
