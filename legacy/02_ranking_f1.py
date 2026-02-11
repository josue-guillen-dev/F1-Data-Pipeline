import sqlite3
import pandas as pd

conexion = sqlite3.connect('f1_proyecto.db')

resultado = 'SELECT pilotos.nombre, pilotos.equipo, SUM(resultados.puntos) as total_puntos FROM resultados INNER JOIN pilotos ON resultados.id_piloto = pilotos.id_piloto GROUP BY pilotos.nombre ORDER BY total_puntos DESC'

f1 = pd.read_sql(resultado, conexion)

print(f1)

conexion.close()