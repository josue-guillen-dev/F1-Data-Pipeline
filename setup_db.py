import pandas as pd
import sqlite3
import os

# 1. Configuración: Nombres de archivos y base de datos
DB_NAME = "f1_proyecto.db"
DATA_DIR = "data"

# Lista de archivos CSV que vamos a cargar
archivos_csv = {
    "results.csv": "results",           # Archivo -> Nombre de tabla en SQL
    "drivers.csv": "drivers",
    "constructors.csv": "constructors",
    "races.csv": "races"
}

def crear_base_datos():
    # Conectamos (si no existe, la crea vacía)
    conn = sqlite3.connect(os.path.join(DATA_DIR, DB_NAME))
    print(f"🔌 Conectado a la base de datos: {DB_NAME}")
    
    # Recorremos la lista de archivos
    for archivo, nombre_tabla in archivos_csv.items():
        ruta_csv = os.path.join(DATA_DIR, archivo)
        
        try:
            print(f"⏳ Cargando {archivo} en tabla '{nombre_tabla}'...")
            
            # MAGIA PANDAS: Lee el CSV
            df = pd.read_csv(ruta_csv)
            
            # MAGIA SQL: Lo vuelca directo a la base de datos
            # if_exists='replace': Si la tabla existe, la borra y la crea de nuevo
            df.to_sql(nombre_tabla, conn, if_exists='replace', index=False)
            
            print(f"✅ {nombre_tabla} cargada exitosamente ({len(df)} filas).")
            
        except Exception as e:
            print(f"❌ Error cargando {archivo}: {e}")

    conn.close()
    print("\n🏁 ¡Base de Datos lista para trabajar!")

if __name__ == "__main__":
    crear_base_datos()