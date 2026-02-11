import pandas as pd
import matplotlib.pyplot as plt
import os  # Necesario para crear carpetas y rutas


def procesar_datos(df_raw):
    """
    Convierte los datos crudos en una tabla acumulativa (Historia completa).
    """
    if df_raw.empty:
        print("❌ Error: No llegaron datos.")
        return None

    # 1. Pivotar (Años vs Nombres)
    df_pivot = df_raw.pivot_table(
        index="temporada", columns="nombre", values="puntos", aggfunc="sum"
    ).fillna(0)
    # 2. Acumular (Suma histórica)
    df_acumulado = df_pivot.cumsum()

    return df_acumulado


def generar_salidas(df, titulo_grafico, nombre_archivo):
    """
    Guarda el CSV, genera el gráfico, guarda el PNG y lo muestra.
    """
    if df is None:
        return

    # --- 1. PREPARAR CARPETA ---
    if not os.path.exists("export"):
        os.makedirs("export")
        print("📁 Carpeta 'export' creada.")

    # --- 2. GUARDAR EXCEL/CSV ---
    ruta_csv = f"export/{nombre_archivo}.csv"
    df.to_csv(ruta_csv)
    print(f"💾 Datos guardados en: {ruta_csv}")

    # --- 3. GENERAR GRÁFICO ---
    print(f"📈 Generando gráfico: {titulo_grafico}...")

    # Crear figura y ejes
    plt.figure(figsize=(14, 7))  # Tamaño grande para HD

    # Dibujar las líneas (Iteramos sobre las columnas para control total)
    for columna in df.columns:
        plt.plot(df.index, df[columna], label=columna, linewidth=2)

    # Decoración
    plt.title(titulo_grafico, fontsize=16)
    plt.ylabel("Puntos Acumulados (Historia)", fontsize=12)
    plt.xlabel("Temporada", fontsize=12)
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.legend(bbox_to_anchor=(1.01, 1), loc="upper left")  # Leyenda afuera
    plt.tight_layout()  # Ajustar márgenes

    # --- 4. GUARDAR PNG ---
    ruta_png = f"export/{nombre_archivo}.png"
    plt.savefig(ruta_png, dpi=300)  # dpi=300 es Alta Calidad
    print(f"📸 Imagen guardada en: {ruta_png}")

    # --- 5. MOSTRAR ---
    plt.show()
