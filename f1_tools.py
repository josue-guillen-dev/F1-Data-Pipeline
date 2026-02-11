import pandas as pd
import matplotlib.pyplot as plt

# --- HERRAMIENTA 1: LIMPIEZA ---
def limpiar_datos(df):
    """Rellena nulos con 0 y convierte a enteros."""
    
    # 1. COMPLETA ESTA LÍNEA (Usa fillna y astype)
    df_limpio = df.fillna(0).astype(int) 
    
    return df_limpio

# --- HERRAMIENTA 2: LÓGICA DE NEGOCIO ---
def obtener_campeon(df):
    """Calcula acumulado y saca al ganador."""
    
    # 2. CALCULA EL ACUMULADO
    df_acumulado = df.cumsum()
    
    # 3. ENCUENTRA AL GANADOR (Fila final)
    ultima_fila = df_acumulado.iloc[-1]
    
    ganador = ultima_fila.idxmax()
    puntos = ultima_fila.max()
    
    return df_acumulado, ganador, puntos

# --- HERRAMIENTA 3: EXPORTAR (La más importante ahora) ---
def guardar_todo(df, nombre_archivo, titulo_grafico):
    """Guarda CSV y PNG en la carpeta 'export/'."""
    
    # OJO AQUÍ: Definimos la ruta para que caiga en la carpeta correcta
    ruta_csv = f"export/{nombre_archivo}.csv"
    ruta_img = f"export/{nombre_archivo}.png"
    
    # 4. GUARDA EL CSV (Usa la variable ruta_csv)
    df.to_csv(ruta_csv, sep=';')
    print(f"✅ CSV guardado en: {ruta_csv}")

    # 5. GENERA Y GUARDA EL GRÁFICO
    plt.figure(figsize=(10,6))
    df.plot(linewidth=2)
    plt.title(titulo_grafico)
    plt.grid(True)
    
    # Guarda la imagen en la carpeta export
    plt.savefig(ruta_img, dpi=300, bbox_inches='tight')
    plt.close() # Cierra el gráfico para liberar memoria
    print(f"📸 Imagen guardada en: {ruta_img}")