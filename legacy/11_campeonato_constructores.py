import pandas as pd
import matplotlib.pyplot as plt
import sqlite3

conn = sqlite3.connect('f1_proyecto.db')

# 1. Traemos equipo, carrera y puntos
query = """
    SELECT resultados.id_carrera, pilotos.equipo, resultados.puntos
    FROM resultados
    JOIN pilotos ON resultados.id_piloto = pilotos.id_piloto
"""
df = pd.read_sql(query, conn)

# 2. EL TRUCO MAESTRO
# aggfunc='sum' -> Le dice: "Si encuentras dos Red Bull en la misma carrera, SÚMALOS"
df_equipos = df.pivot_table(index='id_carrera', columns='equipo', values='puntos', aggfunc='sum')

# 3. Rellenar ceros y Acumular (Lo que aprendiste hace 10 minutos)
df_equipos = df_equipos.fillna(0)
df_mundial_equipos = df_equipos.cumsum()

print(df_mundial_equipos)

# 4. Graficar
df_mundial_equipos.plot(marker='s', linestyle='-', linewidth=3) # 's' es square (cuadrado)
plt.title('Campeonato de Constructores (Equipos)')
plt.ylabel('Puntos Acumulados')
plt.grid(True)
plt.show()

df_mundial_equipos.to_csv('reporte_constructores.csv', sep=',', index=True, encoding='utf-8')
print('archivo guardado')