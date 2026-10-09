import pandas as pd
import plotly.express as px
import streamlit as st


st.set_page_config(
    page_title="Tablero ejecutivo de operación",
    page_icon="📊",
    layout="wide",
)


@st.cache_data
def cargar_datos() -> pd.DataFrame:
    """Carga los datos que utilizará la aplicación."""
    datos = pd.read_csv("datos_ejemplo.csv")
    datos["Fecha"] = pd.to_datetime(datos["Fecha"])
    return datos


df = cargar_datos()

st.title("Tablero ejecutivo de operación")
st.caption(
    "Consulta los indicadores principales por área y región. "
    "Usa los filtros de la barra lateral para ajustar los resultados."
)

st.write("**Desarrollado por:** Karen Hernández Mendoza")


# ---------------- Filtros ----------------
st.sidebar.header("Filtros")

areas_disponibles = sorted(df["Área"].unique())
areas_seleccionadas = st.sidebar.multiselect(
    "Área",
    options=areas_disponibles,
    default=areas_disponibles,
)

# Mejora: filtro adicional por región
regiones_disponibles = sorted(df["Región"].unique())
regiones_seleccionadas = st.sidebar.multiselect(
    "Región",
    options=regiones_disponibles,
    default=regiones_disponibles,
)

df_filtrado = df[
    df["Área"].isin(areas_seleccionadas)
    & df["Región"].isin(regiones_seleccionadas)
].copy()

if df_filtrado.empty:
    st.warning("No hay datos para los filtros seleccionados. Elige al menos un área y una región.")
    st.stop()


# ---------------- Indicadores ----------------
col1, col2, col3 = st.columns(3)
col1.metric("Casos totales", f"{int(df_filtrado['Casos'].sum()):,}")
col2.metric("Tiempo promedio", f"{df_filtrado['Tiempo_min'].mean():.1f} min")
col3.metric("Satisfacción promedio", f"{df_filtrado['Satisfacción'].mean():.1f}")


# ---------------- Vistas ----------------
tab_resumen, tab_datos = st.tabs(["Resumen", "Datos"])

with tab_resumen:
    casos_por_fecha = (
        df_filtrado.groupby("Fecha", as_index=False)["Casos"]
        .sum()
        .sort_values("Fecha")
    )
    fig_fecha = px.line(
        casos_por_fecha,
        x="Fecha",
        y="Casos",
        markers=True,
        title="Casos por fecha",
    )
    st.plotly_chart(fig_fecha, width="stretch")

    casos_por_region = (
        df_filtrado.groupby("Región", as_index=False)["Casos"]
        .sum()
        .sort_values("Casos", ascending=False)
    )
    fig_region = px.bar(
        casos_por_region,
        x="Región",
        y="Casos",
        title="Casos por región",
    )
    st.plotly_chart(fig_region, width="stretch")

with tab_datos:
    st.subheader("Datos filtrados")
    st.dataframe(df_filtrado, width="stretch", hide_index=True)