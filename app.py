import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import altair as alt

conn = sqlite3.connect("data/f1_proyecto.db")

query = """ 
    SELECT ra.raceId, ra.year, ra.name AS race_name, d.nationality AS nacionalidad,  d.forename || ' ' || d.surname AS nombre, c.name AS escuderia , SUM(r.points) AS puntos, MIN(r.positionOrder) AS mejor_posicion
    FROM results r 
    JOIN races ra ON r.raceId = ra.raceID
    JOIN drivers d ON r.driverId = d.driverId
    JOIN constructors c ON r.constructorId = c.constructorId
    GROUP BY ra.year , ra.name, nombre, escuderia
    ORDER BY ra.year DESC
    """

df = pd.read_sql(query, conn)
# Convertimos el año a texto para que el gráfico no use decimales
df["year"] = df["year"].astype(str)
conn.close()

# --- LIMPIEZA DE DATOS (Data Cleaning) ---
# Creamos un diccionario: { "Nombre Sucio" : "Nombre Limpio" }
correcciones_nacionalidad = {
    'Argentine': 'Argentine',
    'Argentinian ': 'Argentine',
    'Argentine-Italian': 'Argentine', # Simplificamos duales
    'American': 'USA',
    'American-Italian': 'USA',
    'British': 'UK' 
    # Puedes agregar más aquí si encuentras otros errores
}

# Aplicamos el reemplazo en la columna 'nacionalidad'
# Si el nombre no está en el diccionario, lo deja tal cual.
df['nacionalidad'] = df['nacionalidad'].replace(correcciones_nacionalidad)

st.title("🏎️ F1 Histórico: Panel de Control")
st.write("Explora los resultados de toda la historia de la Fórmula 1")

df_filtrado = df.copy()

lista_anio = sorted(df_filtrado["year"].unique(), reverse=True)
lista_piloto = sorted(df_filtrado["nombre"].unique())
lista_constructores = sorted(df_filtrado["escuderia"].unique())
lista_nacionalidad = sorted(df_filtrado["nacionalidad"].unique())

# creamos filtros arriba de todo
(col1,col2,col3,col4,) = st.columns(4)

with col1:
    select_anio = st.multiselect("📅 Temporada", lista_anio)

if select_anio:
    df_filtrado = df_filtrado[df_filtrado["year"].isin(select_anio)]
lista_nacionalidad_dinamica= sorted(df_filtrado["nacionalidad"].unique())

with col2:
    select_nationality = st.multiselect("Nacionalidad", lista_nacionalidad_dinamica)
    
if select_nationality:
    df_filtrado = df_filtrado[df_filtrado['nacionalidad'].isin(select_nationality)]
lista_piloto_dinamica = sorted(df_filtrado['nombre'].unique())

with col3:
    select_piloto = st.multiselect("Pilotos", lista_piloto_dinamica)

if select_piloto:
    df_filtrado = df_filtrado[df_filtrado['nombre'].isin(select_piloto)]
lista_constructor_dinamica = sorted(df_filtrado["escuderia"].unique())

with col4:
    select_constructor = st.multiselect("🛠️ Escudería", lista_constructor_dinamica)
    
if select_constructor:
    df_filtrado= df_filtrado[df_filtrado["escuderia"].isin(select_constructor)]    


# Metricas claves (kpi)

kpi1, kpi2, kpi3 = st.columns([1, 1, 2])

# Valores iniciales (plan B por si no hay datos)
carreras_totales = 0
puntos_totales = 0
piloto_mas_puntos = "N/A"

# Solo calculamos si el filtro trajo algo
if not df_filtrado.empty:
    carreras_totales = df_filtrado["raceId"].nunique()
    puntos_totales = int(df_filtrado["puntos"].sum())

    # Agrupamos por nombre, sumamos puntos, y pedimos el ID (nombre) del Máximo (.idxmax())
    piloto_mas_puntos = df_filtrado.groupby("nombre")["puntos"].sum().idxmax()

kpi1.metric("🏁 Grandes Premios", carreras_totales)
kpi2.metric("🏆 Puntos Totales", puntos_totales)
kpi3.metric("🥇 Piloto Mas puntos", piloto_mas_puntos)


col_graf1, col_graf2 = st.columns(2)

with col_graf1:
    st.subheader("📈 Top 5 Pilotos")
    # 1. Identificamos a los 5 mejores pilotos DEL FILTRO ACTUAL
    top_5_pilotos = df_filtrado.groupby('nombre')['puntos'].sum().sort_values(ascending=False).head(5).index
    # 2. Filtramos el dataframe para dejar solo a esos 5
    df_top_5 = df_filtrado[df_filtrado['nombre'].isin(top_5_pilotos)]
    # 3. Hacemos la tabla pivot y mostramos el grafico
    graf1 = df_top_5.pivot_table(index="year", columns="nombre", values="puntos", aggfunc="sum")
    st.line_chart(graf1)
    
with col_graf2:
    st.subheader("🏆 Top 10 Escuderías")
    # 1. Preparamos los datos (igual que antes, pero 'reset_index' lo convierte en tabla bonita)
    graf2 = df_filtrado.groupby("escuderia")["puntos"].sum().reset_index()
    # 2. Filtramos solo los Top 10
    graf2 = graf2.sort_values('puntos', ascending=False).head(10)
    # 3. Usamos Altair (La herramienta PRO que sí hace caso al orden)
    graf2 = alt.Chart(graf2).mark_bar().encode(
        x=alt.X('puntos', title='Puntos Totales'),
        y=alt.Y('escuderia', sort='-x', title=None),
        tooltip=['escuderia', 'puntos'])
    st.altair_chart(graf2, use_container_width=True)
    
st.divider() # Una linea divisoria gris

# Un "Expander" es una caja que se abre y cierra. Ahorra espacio.
with st.expander("🔎 Ver Datos Detallados (Click para desplegar)"):
    # Mostramos la tabla, pero ocultamos el índice feo de pandas
    st.dataframe(df_filtrado, use_container_width=True, hide_index=True)