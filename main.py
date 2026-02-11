import pandas as pd
import sqlite3
import f1_tools as tool  # Importamos TU archivo de herramientas

print("🦁 SISTEMA F1 PROFESIONAL INICIADO...")

# --- 1. CONEXIÓN (El cambio clave) ---
# Como moviste el archivo, ahora tienes que entrar a la carpeta 'data'
conn = sqlite3.connect("data/f1_proyecto.db")


# --- 3. USANDO TUS HERRAMIENTAS ---
print("Selecciona que reporte ver: ")

opcion = input("Ingrese P para Pilotos o C para Constructores: ").upper()

if opcion == "P":
    query = """
    SELECT r.year AS temporada, d.forename || ' ' || d.surname AS nombre, SUM(res.points) AS puntos
    FROM results res 
    JOIN drivers d ON res.driverId = d.driverId
    JOIN races r ON res.raceId = r.raceId
    WHERE d.driverID IN (
        SELECT driverId 
        FROM results 
        GROUP BY driverId 
        ORDER BY SUM(points) DESC 
        LIMIT 10
    )
    GROUP BY r.year, d.driverId
    ORDER BY r.year ASC
    """
    titulo_archivo = "reporte_top10_pilotos"
    titulo_grafico = "Top 10 Pilotos de la Historia (Por Puntos)"

elif opcion == "C":
    query = """ SELECT r.year AS temporada, c.name AS nombre, SUM(res.points) AS puntos
    FROM results res
    JOIN constructors c ON res.constructorId = c.constructorId 
    JOIN races r ON res.raceId = r.raceId
    WHERE c.constructorId IN (
        SELECT constructorId FROM results
        GROUP BY constructorId ORDER BY SUM(points) DESC
        LIMIT 10)
        GROUP BY r.year, c.constructorId
        ORDER BY r.year ASC
        """

    titulo_archivo = "reporte_top10_constructores"
    titulo_grafico = "Top 10 Constructores de la Historia"

else:
    print("Error: Ingrese opcion Valida")


# 1. Ejecutar la consulta SQL (Igual que siempre)
print(f"⏳ Extrayendo datos...")
df_raw = pd.read_sql(query, conn)

# 2. USAR TU TOOL: Primero procesamos los datos
df_listo = tool.procesar_datos(df_raw)
# 3. USAR TU TOOL: Luego graficamos
tool.generar_salidas(df_listo, titulo_grafico, titulo_archivo)

# 4. Cerrar conexión
conn.close()
print("\n🏁 Proceso terminado.")