import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

COLOR_ACTIVA = "#00ADB5"      # Cian
COLOR_REACTIVA = "#FFB703"    # Ámbar
COLOR_SUB1 = "#E63946"        # Coral (Cocina)
COLOR_SUB2 = "#FB8500"        # Naranja (Lavandería)
COLOR_SUB3 = "#2A9D8F"        # Verde (Climatización)
COLOR_RESTO = "#6C757D"       # Gris (Otros aparatos)

def figura_serie_temporal(df_agregado, nivel="Día"):
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df_agregado.index,
        y=df_agregado['Global_active_power'],
        mode='lines',
        name='Potencia Activa Promedio (kW)',
        line=dict(color=COLOR_ACTIVA, width=2)
    ))
    
    fig.add_trace(go.Scatter(
        x=df_agregado.index,
        y=df_agregado['Global_reactive_power'],
        mode='lines',
        name='Potencia Reactiva Promedio (kW)',
        line=dict(color=COLOR_REACTIVA, width=1.5, dash='dot')
    ))
    
    fig.update_layout(
        title=f"Evolución del Consumo Eléctrico (Agrupación por {nivel})",
        xaxis_title="Fecha",
        yaxis_title="Potencia (kW)",
        hovermode="x unified",
        template="plotly_white",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    return fig

def figura_desglose_apilado(df_agregado, nivel="Día"):
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df_agregado.index, y=df_agregado['Sub_metering_3'],
        mode='lines', stackgroup='one', name='Climatización (Sub 3)',
        line=dict(width=0.5, color=COLOR_SUB3), fillcolor=COLOR_SUB3
    ))
    fig.add_trace(go.Scatter(
        x=df_agregado.index, y=df_agregado['Sub_metering_2'],
        mode='lines', stackgroup='one', name='Lavandería (Sub 2)',
        line=dict(width=0.5, color=COLOR_SUB2), fillcolor=COLOR_SUB2
    ))
    fig.add_trace(go.Scatter(
        x=df_agregado.index, y=df_agregado['Sub_metering_1'],
        mode='lines', stackgroup='one', name='Cocina (Sub 1)',
        line=dict(width=0.5, color=COLOR_SUB1), fillcolor=COLOR_SUB1
    ))
    fig.add_trace(go.Scatter(
        x=df_agregado.index, y=df_agregado['Sub_metering_resto'],
        mode='lines', stackgroup='one', name='Otros Circuitos',
        line=dict(width=0.5, color=COLOR_RESTO), fillcolor=COLOR_RESTO
    ))
    
    fig.update_layout(
        title=f"Distribución del Consumo de Energía por Zonas (kWh por {nivel})",
        xaxis_title="Fecha",
        yaxis_title="Energía (kWh)",
        hovermode="x unified",
        template="plotly_white",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    return fig

def figura_dona_zonas(kpis):
    labels = ['Cocina (Sub 1)', 'Lavandería (Sub 2)', 'Climatización (Sub 3)', 'Otros Circuitos']
    values = [kpis.get('sub1_kwh', 0), kpis.get('sub2_kwh', 0), kpis.get('sub3_kwh', 0), kpis.get('resto_kwh', 0)]
    colors = [COLOR_SUB1, COLOR_SUB2, COLOR_SUB3, COLOR_RESTO]
    
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.55,
        marker=dict(colors=colors),
        textinfo='percent+label',
        hoverinfo='label+value+percent'
    )])
    
    fig.update_layout(
        title="Proporción Total de Energía por Área",
        template="plotly_white",
        showlegend=False
    )
    return fig

def figura_heatmap_semanal(df_fisico):
    # Crear copia con hora y día de semana
    df_temp = pd.DataFrame({
        'Hora': df_fisico.index.hour,
        'DiaSemana': df_fisico.index.day_name(),
        'Potencia': df_fisico['Global_active_power']
    })
    
    orden_dias = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    dias_espanol = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
    
    pivot = df_temp.pivot_table(index='DiaSemana', columns='Hora', values='Potencia', aggfunc='mean')
    pivot = pivot.reindex(orden_dias)
    pivot.index = dias_espanol
    
    fig = px.imshow(
        pivot,
        labels=dict(x="Hora del Día (0 a 23 hrs)", y="Día de la Semana", color="Potencia Media (kW)"),
        x=list(range(24)),
        y=dias_espanol,
        color_continuous_scale="Viridis",
        aspect="auto"
    )
    fig.update_layout(
        title="Mapa de Calor: Rutina de Consumo Semanal (Hora vs Día)",
        template="plotly_white"
    )
    return fig

def figura_pca_2d(df_preparado, n_puntos=15000):
    np.random.seed(42)
    n = min(len(df_preparado), n_puntos)
    muestra = df_preparado.sample(n=n, random_state=42).copy()
    muestra['Hora'] = muestra.index.hour
    
    fig = px.scatter(
        muestra,
        x='Componente_1',
        y='Componente_2',
        color='Hora',
        color_continuous_scale='Turbo',
        opacity=0.45,
        labels={
            'Componente_1': 'Componente 1 (Nivel General de Consumo)',
            'Componente_2': 'Componente 2 (Reactiva vs Climatización)',
            'Hora': 'Hora (0-23)'
        },
        title=f"Proyección en 2D de Componentes Principales (Muestra interactiva de {n:,} registros)"
    )
    fig.update_layout(template="plotly_white")
    return fig
