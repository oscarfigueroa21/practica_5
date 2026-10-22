from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

RUTA_DATOS_CRUDOS = (
    BASE_DIR
    / "data"
    / "data-raw"
    / "household_power_consumption.txt"
)

DIR_DATOS_PROCESADOS = BASE_DIR / "data" / "data-processed"

# Dataset limpio e imputado, sin escalar (unidades reales, lo usa el dashboard)
RUTA_DATOS_LIMPIOS = DIR_DATOS_PROCESADOS / "consumo_limpio.parquet"

# Dataset final del Paso 6: normalizado, sin variables redundantes y con PCs
RUTA_DATOS_PREPARADOS = DIR_DATOS_PROCESADOS / "consumo_preparado.parquet"

