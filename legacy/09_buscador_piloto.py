import sqlite3
import pandas as pd

conexion = sqlite3.connect("f1_proyecto.db")

# .strip() quita espacios vacíos al inicio/final (por si se le va el dedo)
# .title() pone la primera Letra Mayúscula de cada palabra
piloto = input("Ingrese piloto a buscar: ").strip().title()

consulta = f"SELECT resultados.id_carrera, pilotos.id_piloto, pilotos.nombre, pilotos.nacionalidad, pilotos.equipo, resultados.posicion, SUM(resultados.puntos)as Puntos FROM resultados INNER JOIN pilotos ON resultados.id_piloto = pilotos.id_piloto WHERE pilotos.nombre LIKE '%{piloto}%' GROUP BY resultados.id_carrera"

df = pd.read_sql(consulta, conexion)

if df.empty:
    print(f"ERROR: No encontramos a '{piloto}'. revisa si lo escribiste bien")
else:
    print('piloto encontrado')
    print(df)
