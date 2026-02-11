import sqlite3
import pandas as pd

conexion = sqlite3.connect('f1_proyecto.db')

consulta = 'SELECT pilotos.equipo, SUM(resultados.puntos) as total FROM resultados INNER JOIN pilotos ON resultados.id_piloto = pilotos.id_piloto GROUP BY pilotos.equipo HAVING total > 30 ORDER BY total DESC'

df = pd.read_sql(consulta, conexion)

print(df)