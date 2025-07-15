import streamlit as st
import matplotlib.pyplot as plt

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

    # Gráfico de barras con matplotlib
    categorias = ['Bueno', 'Moderado', 'Malo']
    valores = [100, 50, 30]  # Valores ilustrativos

    fig, ax = plt.subplots()
    bars = ax.bar(categorias, valores, color=['green', 'orange', 'red'])
    ax.set_title("Calidad del aire (categorías)")
    ax.set_ylabel("Indicadores")
    ax.set_ylim(0, 120)

    # Destacar barra correspondiente al valor
    if nivel == "BUENO":
        bars[0].set_alpha(1.0)
        bars[1].set_alpha(0.3)
        bars[2].set_alpha(0.3)
    elif nivel == "MODERADO":
        bars[0].set_alpha(0.3)
        bars[1].set_alpha(1.0)
        bars[2].set_alpha(0.3)
    else:
        bars[0].set_alpha(0.3)
        bars[1].set_alpha(0.3)
        bars[2].set_alpha(1.0)

    st.pyplot(fig)

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

