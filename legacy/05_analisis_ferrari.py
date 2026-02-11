import sqlite3
import pandas as pd

conexion = sqlite3.connect("f1_proyecto.db")

consulta = "SELECT resultados.id_carrera, pilotos.nombre, resultados.posicion, resultados.puntos FROM resultados INNER JOIN pilotos ON resultados.id_piloto = pilotos.id_piloto WHERE pilotos.equipo == 'Ferrari'"

df = pd.read_sql(consulta, conexion)

print(df)