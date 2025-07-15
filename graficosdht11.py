import serial
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import pandas as pd
import datetime

# Configuración
PUERTO = 'COM3'         # Cambia al puerto correcto
BAUDIOS = 9600
TIEMPO_ENTRE_LECTURAS = 1000  # milisegundos
MAX_PUNTOS = 50

# Inicializar serial
arduino = serial.Serial(PUERTO, BAUDIOS)
arduino.flushInput()

# Listas para almacenar datos
temps = []
humedades = []
tiempos = []
datos = []  # Para pandas

tiempo_actual = 0

# Configurar gráfico
fig, (ax1, ax2) = plt.subplots(2, 1)
fig.suptitle("Temperatura y Humedad en Tiempo Real")

def actualizar(frame):
    global tiempo_actual

    if arduino.in_waiting:
        try:
            linea = arduino.readline().decode('utf-8').strip()
            if "Error" in linea:
                print("Lectura inválida.")
                return
            datos_linea = linea.split("\t")
            if len(datos_linea) == 2:
                temp = float(datos_linea[0])
                hum = float(datos_linea[1])

                temps.append(temp)
                humedades.append(hum)
                tiempos.append(tiempo_actual)
                tiempo_actual += 1

                # Guardar en lista para pandas
                datos.append({"Tiempo": tiempo_actual, "Temperatura": temp, "Humedad": hum})

                # Mantener solo últimos MAX_PUNTOS puntos
                if len(tiempos) > MAX_PUNTOS:
                    tiempos.pop(0)
                    temps.pop(0)
                    humedades.pop(0)

                # Graficar temperatura
                ax1.clear()
                ax1.plot(tiempos, temps, color='red')
                ax1.set_title("Temperatura (°C)")
                ax1.set_ylabel("°C")
                ax1.grid(True)

                # Graficar humedad
                ax2.clear()
                ax2.plot(tiempos, humedades, color='blue')
                ax2.set_title("Humedad (%)")
                ax2.set_ylabel("%")
                ax2.set_xlabel("Tiempo (s)")
                ax2.grid(True)

        except Exception as e:
            print(f"Error al procesar datos: {e}")

ani = FuncAnimation(fig, actualizar, interval=TIEMPO_ENTRE_LECTURAS)

try:
    plt.tight_layout()
    plt.show()
finally:
    # Al cerrar el gráfico, guardar datos en Excel
    df = pd.DataFrame(datos)
    archivo_excel = f"dht11_datos_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.xlsx"
    df.to_excel(archivo_excel, index=False)
    print(f"Datos guardados en {archivo_excel}")
