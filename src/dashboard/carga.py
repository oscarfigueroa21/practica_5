import pandas as pd
import streamlit as st
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
RUTA_PREPARADOS = BASE_DIR / "data" / "data-processed" / "consumo_preparado.parquet"

# Parámetros de escala del conjunto de entrenamiento (2006-2009)
PARAMETROS_ESCALA = {
    'Global_active_power':   {'media': 1.0916, 'std': 1.0573},
    'Global_reactive_power': {'media': 0.1237, 'std': 0.1127},
    'Voltage':               {'media': 240.8399, 'std': 3.2390},
    'Sub_metering_1':        {'media': 1.1183, 'std': 6.1530},
    'Sub_metering_2':        {'media': 1.2985, 'std': 5.8220},
    'Sub_metering_3':        {'media': 6.4584, 'std': 8.4371},
}

@st.cache_data
def cargar_datos_preparados():
    df = pd.read_parquet(RUTA_PREPARADOS)
    return df

@st.cache_data
def obtener_datos_fisicos(df_preparado):
    df_fisico = pd.DataFrame(index=df_preparado.index)
    
    # Reconstrucción de magnitudes físicas
    for col, param in PARAMETROS_ESCALA.items():
        if col in df_preparado.columns:
            df_fisico[col] = df_preparado[col] * param['std'] + param['media']
    
    # Asegurar no negatividad en potencias y submedidores
    df_fisico['Global_active_power'] = df_fisico['Global_active_power'].clip(lower=0)
    df_fisico['Global_reactive_power'] = df_fisico['Global_reactive_power'].clip(lower=0)
    df_fisico['Sub_metering_1'] = df_fisico['Sub_metering_1'].clip(lower=0)
    df_fisico['Sub_metering_2'] = df_fisico['Sub_metering_2'].clip(lower=0)
    df_fisico['Sub_metering_3'] = df_fisico['Sub_metering_3'].clip(lower=0)
    
    # Consumo activo total en Wh por minuto
    energia_total_wh = df_fisico['Global_active_power'] * 1000.0 / 60.0
    sub_sum = df_fisico['Sub_metering_1'] + df_fisico['Sub_metering_2'] + df_fisico['Sub_metering_3']
    df_fisico['Sub_metering_resto'] = (energia_total_wh - sub_sum).clip(lower=0)
    
    # Energía activa en kWh por minuto
    df_fisico['Energia_kWh'] = df_fisico['Global_active_power'] / 60.0
    
    return df_fisico

def filtrar_por_fechas(df, fecha_inicio, fecha_fin):
    # Asegurar formato Timestamp al inicio y fin del día
    inicio = pd.to_datetime(fecha_inicio).floor('D')
    fin = pd.to_datetime(fecha_fin).ceil('D') - pd.Timedelta(seconds=1)
    return df.loc[inicio:fin]

def agregar_temporal(df_fisico, nivel='Día'):
    mapeo_freq = {
        'Hora': 'h',
        'Día': 'D',
        'Semana': 'W',
        'Mes': 'ME'
    }
    freq = mapeo_freq.get(nivel, 'D')
    
    # Promedios para potencias y voltajes; suma para energía en kWh y submedidores
    agg_dict = {
        'Global_active_power': 'mean',
        'Global_reactive_power': 'mean',
        'Voltage': 'mean',
        'Energia_kWh': 'sum',
        'Sub_metering_1': lambda x: x.sum() / 1000.0, # Convertir Wh a kWh
        'Sub_metering_2': lambda x: x.sum() / 1000.0,
        'Sub_metering_3': lambda x: x.sum() / 1000.0,
        'Sub_metering_resto': lambda x: x.sum() / 1000.0,
    }
    
    cols_existentes = {k: v for k, v in agg_dict.items() if k in df_fisico.columns}
    df_agg = df_fisico.resample(freq).agg(cols_existentes)
    return df_agg
