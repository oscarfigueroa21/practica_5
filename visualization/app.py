import sys
from pathlib import Path
import streamlit as st
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

from src.dashboard.carga import (
    cargar_datos_preparados,
    obtener_datos_fisicos,
    filtrar_por_fechas,
    agregar_temporal
)
from src.dashboard.metricas import calcular_kpis_principales
from src.dashboard.graficas import (
    figura_serie_temporal,
    figura_desglose_apilado,
    figura_dona_zonas,
    figura_heatmap_semanal,
    figura_pca_2d
)

st.set_page_config(
    page_title="Consumo Eléctrico Doméstico",
    layout="wide"
)

# Carga de datos
df_preparado = cargar_datos_preparados()
df_fisico = obtener_datos_fisicos(df_preparado)

fecha_min = df_fisico.index.min().date()
fecha_max = df_fisico.index.max().date()

# Barra lateral con filtros
st.sidebar.header("Filtros")

fechas_seleccionadas = st.sidebar.date_input(
    "Rango de fechas",
    value=(fecha_min, fecha_max),
    min_value=fecha_min,
    max_value=fecha_max
)

if isinstance(fechas_seleccionadas, (tuple, list)) and len(fechas_seleccionadas) == 2:
    f_inicio, f_fin = fechas_seleccionadas
else:
    f_inicio, f_fin = fecha_min, fecha_max

nivel_agg = st.sidebar.selectbox(
    "Agregación temporal",
    options=["Día", "Hora", "Semana", "Mes"],
    index=0
)

# Filtrado de datos
df_filtrado_fisico = filtrar_por_fechas(df_fisico, f_inicio, f_fin)
df_filtrado_prep = filtrar_por_fechas(df_preparado, f_inicio, f_fin)

if df_filtrado_fisico.empty:
    st.warning("No se encontraron registros en el rango de fechas seleccionado.")
    st.stop()

# KPIs y agregación temporal
kpis = calcular_kpis_principales(df_filtrado_fisico)
df_agg = agregar_temporal(df_filtrado_fisico, nivel=nivel_agg)

# Título y métricas principales
st.title("Consumo Eléctrico Doméstico")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Consumo Total", f"{kpis['energia_total_kwh']:,.1f} kWh")
col2.metric("Potencia Media", f"{kpis['potencia_media_kw']:.2f} kW")
col3.metric("Potencia Máxima", f"{kpis['potencia_max_kw']:.2f} kW")
col4.metric("Voltaje Promedio", f"{kpis['voltaje_medio_v']:.1f} V")

st.markdown("---")

# Visualizaciones organizadas por pestañas
tab1, tab2, tab3, tab4 = st.tabs([
    "Evolución Temporal",
    "Consumo por Circuitos",
    "PCA",
    "Tabla de Datos"
])

with tab1:
    st.plotly_chart(figura_serie_temporal(df_agg, nivel=nivel_agg), use_container_width=True)
    st.plotly_chart(figura_heatmap_semanal(df_filtrado_fisico), use_container_width=True)

with tab2:
    col_izq, col_der = st.columns([3, 2])
    with col_izq:
        st.plotly_chart(figura_desglose_apilado(df_agg, nivel=nivel_agg), use_container_width=True)
    with col_der:
        st.plotly_chart(figura_dona_zonas(kpis), use_container_width=True)

with tab3:
    st.plotly_chart(figura_pca_2d(df_filtrado_prep), use_container_width=True)

with tab4:
    st.dataframe(df_agg.round(2), use_container_width=True)
