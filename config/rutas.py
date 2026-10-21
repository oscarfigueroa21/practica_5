from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

RUTA_DATOS_CRUDOS = (
    BASE_DIR
    / "data"
    / "data-raw"
    / "household_power_consumption.txt"
)

