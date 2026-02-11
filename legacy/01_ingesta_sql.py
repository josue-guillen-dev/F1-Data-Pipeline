import pandas as pd
import sqlite3

df_pilotos = pd.read_csv('f1_pilotos.csv')
df_resultados = pd.read_csv('f1_resultados.csv')

conexion = sqlite3.connect('f1_proyecto.db')

df_pilotos.to_sql('pilotos', conexion, if_exists='replace', index=False)
df_resultados.to_sql('resultados', conexion, if_exists='replace', index=False)

conexion.close()