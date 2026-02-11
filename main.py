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
    SELECT resultados.id_carrera, pilotos.nombre, resultados.puntos
    FROM resultados 
    JOIN pilotos ON resultados.id_piloto = pilotos.id_piloto
    """
    titulo_archivo = 'reporte_piloto'
    titulo_grafico = 'Campeonato de Pilotos'
    
    
elif opcion == "C":
    query = """ SELECT resultados.id_carrera, pilotos.equipo, resultados.puntos
    FROM resultados
    JOIN pilotos ON resultados.id_piloto = pilotos.id_piloto """
    
    titulo_archivo = 'reporte_constructores'
    titulo_grafico = 'Campeonato de Constructores'
    
else:
    print("Error: Ingrese opcion Valida")

df_raw = pd.read_sql(query, conn).pivot_table(index="id_carrera", columns="nombre", values="puntos", aggfunc="sum")

# A. Limpiar
df_listo = tool.limpiar_datos(df_raw)
# B. Calcular
tabla_final, campeon_nombre, total_puntos = tool.obtener_campeon(df_listo)

# C. Guardar (Automático a la carpeta export)
tool.guardar_todo(tabla_final, titulo_archivo,f"{titulo_grafico} - Ganador: {campeon_nombre}",
    )


print("🏁 PROCESO TERMINADO CON ÉXITO.")
