import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

conn = sqlite3.connect('f1_proyecto.db')

# 1. Traemos y Preparamos los datos (Igual que antes)
query = """
    SELECT resultados.id_carrera, pilotos.equipo, resultados.puntos
    FROM resultados
    JOIN pilotos ON resultados.id_piloto = pilotos.id_piloto
"""
df = pd.read_sql(query, conn)
df_equipos = df.pivot_table(index='id_carrera', columns='equipo', values='puntos', aggfunc='sum').fillna(0)
df_mundial = df_equipos.cumsum()

# --- AQUÍ EMPIEZA LA INTELIGENCIA ARTIFICIAL BÁSICA ---

# Paso 1: Aislar la última carrera (La foto final)
ultima_carrera = df_mundial.iloc[-1] 

# Paso 2: Preguntarle a Python quién ganó
nombre_campeon = ultima_carrera.idxmax() # Encuentra el nombre
puntos_campeon = ultima_carrera.max()    # Encuentra los puntos

# Paso 3: Calcular la diferencia con el segundo (Opcional, pero pro)
# Ordenamos de mayor a menor y agarramos el segundo
segundo_lugar = ultima_carrera.sort_values(ascending=False).iloc[1]
diferencia = puntos_campeon - segundo_lugar

""" # 1. Buscamos DÓNDE está el máximo (nos devuelve la fila)
indice_ganador = df['Puntos'].idxmax() 
# Resultado: 1

# 2. Usamos ese índice para buscar el NOMBRE en esa fila
nombre_ganador = df.loc[indice_ganador, 'Equipo']
# Traducción: "Pandas, ve a la fila 1 y tráeme lo que hay en la columna 'Equipo'"

print(f"El ganador es: {nombre_ganador}") 
# Resultado: Ferrari """




# --- RESULTADO FINAL ---
print("\n" + "="*40)
print("🏁  RESULTADOS OFICIALES DE LA TEMPORADA  🏁")
print("="*40)
print(f"🏆 CAMPEÓN:   {nombre_campeon.upper()}")
print(f"🥇 PUNTOS:    {puntos_campeon}")
print(f"🚀 VENTAJA:   Ganó por {diferencia} puntos de diferencia.")
print("="*40 + "\n")

plt.title(f'Campeonato mundial ganador: {nombre_campeon.upper()}')
plt.grid(True)
plt.savefig('Grafico_campeonato.png', dpi=300, bbox_inches='tight')
print('Grafico guardado')
plt.show()
