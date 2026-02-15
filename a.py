import pandas as pd
import sqlite3
import os

# 1. Conectar a la base de datos (se crea si no existe)
# Fíjate que en tu imagen la DB está dentro de la carpeta 'data'
conexion = sqlite3.connect('data1/f1_proyecto.db')

# 2. ESTA ES LA VARIABLE QUE DICES
# Una lista con los nombres exactos de tus archivos (sin el .csv para hacerlo más limpio)
lista_archivos = ['constructors', 'drivers', 'races', 'results']

# 3. El ciclo "For" (el motor que hace el trabajo)
for nombre in lista_archivos:
    
    # Construimos la ruta completa: "data/" + "constructors" + ".csv"
    ruta_archivo = f"data1/{nombre}.csv"
    
    # Leemos el CSV
    df = pd.read_csv(ruta_archivo)
    
    # Lo guardamos en la base de datos
    # Usamos el mismo 'nombre' para la tabla (ej: tabla 'constructors')
    df.to_sql(name=nombre, con=conexion, if_exists='replace', index=False)
    
    print(f"--> Archivo {nombre}.csv convertido a tabla SQL exitosamente.")

# 4. Cerramos
conexion.close()