import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

conexion = sqlite3.connect('f1_proyecto.db')

resultado = 'SELECT pilotos.nombre, pilotos.equipo, SUM(resultados.puntos) as total_puntos FROM resultados INNER JOIN pilotos ON resultados.id_piloto = pilotos.id_piloto GROUP BY pilotos.nombre ORDER BY total_puntos DESC'

df = pd.read_sql(resultado, conexion)

plt.figure(figsize=(10,5))
plt.bar(df['nombre'], df['total_puntos'])
plt.title('Campeonato mundial f1 2026')

plt.savefig('reporte_oficial_f1.png', dpi= 300, bbox_inches='tight')
plt.show()