import pandas as pd

df_pilotos = {
    'id_piloto' : [1,2,3,4],
    'nombre': ['Max Verstappen', 'Lewis Hamilton', 'Fernando Alonso', 'Charles Leclerc'],
    'equipo': ['Red Bull', 'Ferrari', 'Aston Martin', 'Ferrari'],
    'nacionalidad': ['Holandés', 'Británico', 'Español', 'Monegasco']
}
piloto = pd.DataFrame(df_pilotos)

df_resultados = [
    [101, 1, 1, 25],  # Max en carrera 101 (Ganó)
    [101, 2, 3, 15],  # Hamilton en carrera 101 (3ro)
    [101, 3, 2, 18],  # Alonso en carrera 101 (2do)
    [101, 4, 5, 10],  # Leclerc en carrera 101 (5to)
    [102, 1, 2, 18],  # Max en carrera 102 (2do)
    [102, 4, 1, 25]   # Leclerc en carrera 102 (Ganó)
]
resultado = pd.DataFrame(df_resultados, columns=['id_carrera','id_piloto','posicion', 'puntos'])

piloto.to_csv('f1_pilotos.csv', index= False)
resultado.to_csv('f1_resultados.csv', index= False)

print(df_pilotos)
print(df_resultados)