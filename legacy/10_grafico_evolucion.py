import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

conexion = sqlite3.connect("f1_proyecto.db")

consulta = "SELECT resultados.id_carrera, pilotos.id_piloto, pilotos.nombre, resultados.puntos FROM resultados JOIN pilotos ON resultados.id_piloto = pilotos.id_piloto"

df = pd.read_sql(consulta, conexion)
df['sub_total'] = df.groupby('nombre')['puntos'].cumsum()


# --- AQUÍ OCURRE LA MAGIA (PIVOT) ---
# index: Lo que va en el eje X (Las Carreras)
# columns: Lo que crea las líneas de colores (Los Nombres)
# values: Lo que marca la altura (Los Puntos)

df_pivot = df.pivot_table(index="id_carrera", columns="nombre", values='sub_total').fillna(0)

# --- 2. LA MAGIA: Calculamos el ACUMULADO ---

print(df_pivot)

# 3. Graficar
# Pandas tiene un atajo para graficar directo sin escribir tanto matplotlib

df_pivot.plot(marker="o", linestyle="-", linewidth=3) 

plt.title("evolucion de los pilotos")
plt.xlabel("carrera (ID)")
plt.ylabel("puntos obtenidos")
plt.grid(True)  # Pone la cuadrícula de fondo
plt.legend(title="pilotos")

plt.show()
