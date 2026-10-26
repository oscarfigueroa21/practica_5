def crear_transacciones_reglas(df_limpio, umbral_cocina=0, umbral_lavanderia=0, umbral_climatizacion=0):

    df_horario = df_limpio.resample('h').agg({
        'Sub_metering_1': 'sum',
        'Sub_metering_2': 'sum',
        'Sub_metering_3': 'sum',
        'Global_active_power': 'mean',
        'Global_reactive_power': 'mean',
        'Voltage': 'mean',
        'Global_intensity': 'mean'
    }).dropna()

    df_horario['Cocina'] = df_horario['Sub_metering_1'] > umbral_cocina
    df_horario['Lavanderia'] = df_horario['Sub_metering_2'] > umbral_lavanderia
    df_horario['Climatizacion'] = df_horario['Sub_metering_3'] > umbral_climatizacion

    dias_map = {
        0: 'Lunes', 1: 'Martes', 2: 'Miercoles', 3: 'Jueves', 
        4: 'Viernes', 5: 'Sabado', 6: 'Domingo'
    }
    df_horario['Dia_Semana'] = df_horario.index.dayofweek.map(dias_map)

    def categorizar_hora(hora):
        if 0 <= hora < 6:
            return 'Madrugada'
        elif 6 <= hora < 12:
            return 'Manana'
        elif 12 <= hora < 14:
            return 'Mediodia'
        elif 14 <= hora < 19:
            return 'Tarde'
        else:
            return 'Noche'

    df_horario['Tiempo_Dia'] = df_horario.index.hour.map(categorizar_hora)

    return df_horario

def guardar_input_reglas(df_horario, ruta_salida="data/data-processed/input_reglas_asociacion.csv"):
    df_horario.to_csv(ruta_salida, index=True)
    print(f"Dataset guardado exitosamente en: {ruta_salida}")