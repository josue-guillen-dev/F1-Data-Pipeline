import pandas as pd
import matplotlib.pyplot as plt


def analizar_campeonato(df):
    # Aquí adentro va la magia
    # 1. Limpieza
    df = df.fillna(0).astype(int)# <--- ¡AQUÍ ESTÁ LA MAGIA!
    df_acumulado = df.cumsum()
    # 2. Encontrar al Ganador (Para el título)
    ultimo_dia = df_acumulado.iloc[-1]
    campeon = ultimo_dia.idxmax()
    # 3. La parte importante: RETURN
    return df_acumulado, campeon


# Creamos datos falsos rápido
datos = pd.DataFrame({
    'redbull': [25,25,None],
    'ferrari': [18,18,25],
})

# LLAMAMOS A LA FUNCIÓN
# Fíjate cómo atrapamos las 2 cosas que nos devuelve
tabla_lista, ganador = analizar_campeonato(datos)
print(f'El ganador calculado es: {ganador}')
print(tabla_lista)
