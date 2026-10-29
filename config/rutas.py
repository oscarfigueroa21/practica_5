from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent.parent

if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

RUTA_DATOS_CRUDOS = (
    BASE_DIR
    / "data"
    / "data-raw"
    / "household_power_consumption.txt"
)

DIR_DATOS_RAW = BASE_DIR / "data" / "data-raw"
DIR_DATOS_PROCESADOS = BASE_DIR / "data" / "data-processed"
RUTA_DATOS_CRUDOS = DIR_DATOS_RAW / "household_power_consumption.txt"

# Dataset limpio e imputado, sin escalar (unidades reales, lo usa el dashboard)
RUTA_DATOS_LIMPIOS = DIR_DATOS_PROCESADOS / "consumo_limpio.parquet"

# Dataset final del Paso 6: normalizado, sin variables redundantes y con PCs
RUTA_DATOS_PREPARADOS = DIR_DATOS_PROCESADOS / "consumo_preparado.parquet"

RUTA_TRANSACCIONES= BASE_DIR / "src" / "models" / "transacciones.py"
RUTA_INPUT_REGLAS = DIR_DATOS_PROCESADOS / "input_reglas_asociacion.csv"

