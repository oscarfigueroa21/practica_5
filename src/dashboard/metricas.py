import pandas as pd

def calcular_kpis_principales(df_fisico):
    if df_fisico.empty:
        return {}
    
    energia_total_kwh = df_fisico['Energia_kWh'].sum()
    potencia_media = df_fisico['Global_active_power'].mean()
    potencia_max = df_fisico['Global_active_power'].max()
    voltaje_medio = df_fisico['Voltage'].mean()
    
    # Submedidores en kWh para la distribución
    sub1_kwh = df_fisico['Sub_metering_1'].sum() / 1000.0
    sub2_kwh = df_fisico['Sub_metering_2'].sum() / 1000.0
    sub3_kwh = df_fisico['Sub_metering_3'].sum() / 1000.0
    resto_kwh = df_fisico['Sub_metering_resto'].sum() / 1000.0
    
    return {
        'energia_total_kwh': energia_total_kwh,
        'potencia_media_kw': potencia_media,
        'potencia_max_kw': potencia_max,
        'voltaje_medio_v': voltaje_medio,
        'sub1_kwh': sub1_kwh,
        'sub2_kwh': sub2_kwh,
        'sub3_kwh': sub3_kwh,
        'resto_kwh': resto_kwh
    }
