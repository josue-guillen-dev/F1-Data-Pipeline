import sqlite3
import pandas as pd

conexion = sqlite3.connect('f1_proyecto.db')

consulta = 'SELECT COUNT(DISTINCT id_carrera) as total_carreras, MAX(puntos) as mejor_puntaje,MIN(puntos) as peor_puntaje, SUM(puntos) as suma_total FROM resultados'

df = pd.read_sql(consulta, conexion)

print(df)