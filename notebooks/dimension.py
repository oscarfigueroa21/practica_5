import pandas as pd
def dimensionalidad(df_limpio):
    df_limpio = df_limpio.drop(columns='Global_intensity')
    return df_limpio