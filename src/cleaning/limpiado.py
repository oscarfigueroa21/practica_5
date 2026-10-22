import pandas as pd
from sklearn.preprocessing import StandardScaler

FECHA_CORTE = '2009-12-31 23:59:00'

def casteo_datos(RUTA_DATOS_CRUDOS):
    df_casteado = pd.read_csv(RUTA_DATOS_CRUDOS, sep=';', na_values='?', low_memory=False)
    
    # Combinar Date y Time en una sola columna de tipo datetime64
    df_casteado['Date-time'] = pd.to_datetime(
        df_casteado['Date'] + ' ' + df_casteado['Time'], 
        format='%d/%m/%Y %H:%M:%S'
    )
    
    # Establecer la columna Date-time como índice y eliminar las columnas Date y Time
    df_casteado = df_casteado.set_index('Date-time')
    df_casteado = df_casteado.drop(columns=['Date', 'Time'])

    # Casteo de las columnas de tipo object a tipo float
    df_casteado['Global_active_power'] = pd.to_numeric(df_casteado['Global_active_power'], errors='coerce')
    df_casteado['Global_reactive_power'] = pd.to_numeric(df_casteado['Global_reactive_power'], errors='coerce')
    df_casteado['Voltage'] = pd.to_numeric(df_casteado['Voltage'], errors='coerce')
    df_casteado['Global_intensity'] = pd.to_numeric(df_casteado['Global_intensity'], errors='coerce')
    df_casteado['Sub_metering_1'] = pd.to_numeric(df_casteado['Sub_metering_1'], errors='coerce')
    df_casteado['Sub_metering_2'] = pd.to_numeric(df_casteado['Sub_metering_2'], errors='coerce')

    return df_casteado

def deduplicar(df):
    return df[~df.index.duplicated(keep='first')]

def imputar_faltantes(df):
    return df.interpolate()

def obtener_datos_limpios(RUTA_DATOS_CRUDOS):
    df_casteado = casteo_datos(RUTA_DATOS_CRUDOS)
    df_deduplicado = deduplicar(df_casteado)
    df_limpio = imputar_faltantes(df_deduplicado)
    return df_limpio

def normalizar_zscore(df_limpio, fecha_corte=FECHA_CORTE):
    scaler = StandardScaler()
    scaler.fit(df_limpio.loc[:fecha_corte])
    df_z = pd.DataFrame(
        scaler.transform(df_limpio), 
        columns=df_limpio.columns, 
        index=df_limpio.index
    )
    return df_z, scaler

def limpieza_imputacion(df_casteado):
    df_deduplicado = deduplicar(df_casteado)
    df_interpolado = imputar_faltantes(df_deduplicado)
    df_z_score, _ = normalizar_zscore(df_interpolado)
    return df_z_score
