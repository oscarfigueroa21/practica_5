import pandas as pd 
from sklearn.preprocessing import StandardScaler

def casteo_datos(RUTA_DATOS_CRUDOS):
    df_casteado= pd.read_csv(RUTA_DATOS_CRUDOS,sep=';')
    # Combinar Date y Time en una sola columna de tipo datetime64
    df_casteado['Date-time'] = pd.to_datetime(df_casteado['Date'].astype(str) + ' ' + df_casteado['Time'].astype(str))
    
    #Establecer la columna Date-time como índice y eliminar las columnas Date y Time
    df_casteado = df_casteado.set_index('Date-time')
    df_casteado = df_casteado.drop(columns=['Date', 'Time'])

    #Casteo de las columnas de tipo object a tipo float
    df_casteado['Global_active_power']= pd.to_numeric(df_casteado['Global_active_power'], errors='coerce')
    df_casteado['Global_reactive_power']= pd.to_numeric(df_casteado['Global_reactive_power'], errors='coerce')
    df_casteado['Voltage']= pd.to_numeric(df_casteado['Voltage'], errors='coerce')
    df_casteado['Global_intensity']= pd.to_numeric(df_casteado['Global_intensity'], errors='coerce')
    df_casteado['Sub_metering_1']= pd.to_numeric(df_casteado['Sub_metering_1'], errors='coerce')
    df_casteado['Sub_metering_2']= pd.to_numeric(df_casteado['Sub_metering_2'], errors='coerce')


    return df_casteado

def limpieza_imputacion(df_casteado):
    
    df_interpolado = df_casteado.interpolate()
    scaler = StandardScaler()
    df_z_score = pd.DataFrame(scaler.fit_transform(df_interpolado), columns=df_interpolado.columns,index=df_interpolado.index)
    
    return df_z_score


