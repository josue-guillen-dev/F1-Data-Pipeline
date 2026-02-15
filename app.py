import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import altair as alt

# --- CONFIGURACIÓN DE PÁGINA (Opcional, pero se ve mejor) ---
st.set_page_config(page_title="F1 Dashboard", page_icon="🏎️", layout="wide")
    # --- 1. FUNCIÓN DE CARGA DE DATOS OPTIMIZADA (CACHÉ) ---
@st.cache_data(ttl=3600)# Se actualiza cada 1 hora automáticamente
def cargar_datos_f1():
    conn = sqlite3.connect("data/f1_proyecto.db")

    query = """ 
            SELECT ra.raceId, ra.year, ra.name AS race_name, d.nationality AS nacionalidad,  d.forename || ' ' || d.surname AS nombre, c.name AS escuderia , r.grid, r.positionOrder, r.points AS puntos
            FROM results r 
            JOIN races ra ON r.raceId = ra.raceID
            JOIN drivers d ON r.driverId = d.driverId
            JOIN constructors c ON r.constructorId = c.constructorId
            ORDER BY ra.year DESC, ra.raceId ASC
            """

    df = pd.read_sql(query, conn)
    conn.close()
        # Convertimos el año a texto para que el gráfico no use decimales
    df["year"] = df["year"].astype(str)

        # --- LIMPIEZA DE DATOS (Data Cleaning) ---
        # Creamos un diccionario: { "Nombre Sucio" : "Nombre Limpio" }
    correcciones_nacionalidad = {
            'Argentine': 'Argentine',
            'Argentinian ': 'Argentine',
            'Argentine-Italian': 'Argentine', # Simplificamos duales
            'American': 'USA',
            'American-Italian': 'USA',
            'British': 'UK' }
        # Aplicamos el reemplazo en la columna 'nacionalidad'
        # Si el nombre no está en el diccionario, lo deja tal cual.
    df['nacionalidad'] = df['nacionalidad'].replace(correcciones_nacionalidad)

    return df
        
df = cargar_datos_f1()

# --- LÓGICA DE REMONTADAS (Fuera de los Tabs) ---
df_filtrado = df.copy()

#wiht tab 1 📊 Resumen de Temporada
# creamos filtros arriba de todo
(col1,col2,col3,col4,) = st.columns(4)

# --- FILTRO 1: AÑO (El "Jefe" de los filtros) ---
with col1:
    lista_anio = sorted(df['year'].unique(), reverse=True)
    select_anio = st.multiselect("📅 Temporada", lista_anio)

if select_anio:
    df_filtrado = df_filtrado[df_filtrado["year"].isin(select_anio)]

# --- FILTRO 2: NACIONALIDAD (Depende del Año) ---
with col2:
    lista_nacionalidad = sorted(df_filtrado['nacionalidad'].unique())
    select_nationality = st.multiselect("🌍 Nacionalidad", lista_nacionalidad)
    
if select_nationality:
    df_filtrado = df_filtrado[df_filtrado['nacionalidad'].isin(select_nationality)]

# --- FILTRO 3: PILOTO (Depende de Año + Nacionalidad) ---
with col3:
    lista_piloto = sorted(df_filtrado['nombre'].unique())
    select_piloto = st.multiselect("🏎️ Pilotos", lista_piloto)

if select_piloto:
    df_filtrado = df_filtrado[df_filtrado['nombre'].isin(select_piloto)]

# --- FILTRO 4: ESCUDERÍA (Depende de todo lo anterior) ---
with col4:
    lista_constructores = sorted(df_filtrado["escuderia"].unique())
    select_constructor = st.multiselect("🛠️ Escudería", lista_constructores)
    
if select_constructor:
    df_filtrado= df_filtrado[df_filtrado["escuderia"].isin(select_constructor)]    
    

#wiht tab 2  Análisis de Rendimiento"
# Calculamos la diferencia (Posición salida - Posición llegada)
df_filtrado['diferencia'] = df_filtrado['grid'] - df_filtrado['positionOrder']
# Aplicamos filtro: Solo las que son mayores a 0 (Remontadas reales)
# Y filtramos grid > 0 porque grid=0 significa que salió desde el Pit Lane o error
df_remontada = df_filtrado[(df_filtrado['diferencia'] > 0) & (df_filtrado['grid'] > 0)]



# Crear las pestañas al principio
tab1, tab2 = st.tabs(["📊 Resumen de Temporada", "🎯 Análisis de Rendimiento"])

with tab1:
    st.header("Estadísticas Generales")

    st.title("🏎️ F1 Histórico: Panel de Control")
    st.write("Explora los resultados de toda la historia de la Fórmula 1")

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
        # 1. Obtenemos el Top 5 ordenado
        top_5_data = df_filtrado.groupby('nombre')['puntos'].sum().sort_values(ascending=False).head(5).reset_index()
        top_5_nombres = top_5_data['nombre'].tolist()
        
        # 2. Filtramos para el gráfico
        df_plot = df_filtrado[df_filtrado['nombre'].isin(top_5_nombres)]
        
        if len(df_plot['year'].unique()) == 1:
            # SI ES UN SOLO AÑO: Gráfico de barras horizontales ORDENADO
            chart = alt.Chart(top_5_data).mark_bar().encode(
                x=alt.X('puntos', title='Puntos'),
                y=alt.Y('nombre', sort='-x', title=None), # El '-x' es el truco para ordenar
            ).properties(height=300)
        else:
            # SI SON VARIOS AÑOS: Gráfico de líneas con puntos
            # Agrupamos por año y nombre para que la línea no se vea "quebrada" o sólida
            df_lineas = df_plot.groupby(['year', 'nombre'])['puntos'].sum().reset_index()
            
            chart = alt.Chart(df_lineas).mark_line(point=True).encode(
                x=alt.X('year:O', title='Año'),
                y=alt.Y('puntos:Q', title='Puntos'),
                color=alt.Color('nombre:N', legend=None),
                tooltip=['nombre', 'year', 'puntos']
            ).properties(height=300)

        st.altair_chart(chart, use_container_width=True)
        
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




with tab2:
    st.header("🎯 Análisis de Rendimiento: Las Grandes Remontadas")
    st.write("Este análisis muestra únicamente los casos donde un piloto terminó en una mejor posición de la que comenzó.")
    
    # Slider para filtrar por cuántas posiciones remontó (opcional pero se ve muy pro)
    min_remontada = st.slider('Filtrar por minimo de posiciones ganadas: ',1,15,1)
    df_tab2 = df_filtrado[df_filtrado['diferencia'] >= min_remontada]

    
    # Crear el gráfico de dispersión interactivo
    scatter = alt.Chart(df_tab2).mark_circle(size=80, opacity=0.4).encode(
        x=alt.X('grid:Q', title='Posicion de salida (Grid)'),
        y=alt.Y('positionOrder:Q', title='Posicion de llegada'),
        #xOffset=alt.datum(0.5),
        color=alt.Color('escuderia:N', title='Escuderia'),
        size=alt.Size('diferencia:Q', title='Posiciones Ganadas'),
        tooltip=[alt.Tooltip('nombre:N', title='Piloto'),
        alt.Tooltip('year:O', title='Año'),
        alt.Tooltip('race_name:N', title='Carrera'),
        alt.Tooltip('grid:Q', title='Salió'),
        alt.Tooltip('positionOrder:Q', title='Llegó'),
        alt.Tooltip('diferencia:Q', title='Ganó')]
    ).properties(height=500).interactive()
    
    # Línea de referencia (Opcional)
    st.altair_chart(scatter, use_container_width=True)
    
    st.subheader("📋 Detalle de las remontadas en el gráfico")
    st.dataframe(df_tab2[['year', 'nombre', 'race_name', 'grid', 'positionOrder', 'diferencia']].sort_values('diferencia', ascending=False), hide_index=True)
    
    st.info("💡 Consejo: Pasa el ratón sobre los puntos para ver los detalles del piloto y la carrera.")