"""Configuración de la API: rutas y valores fijos en un solo lugar (como en el módulo 08)."""

from pathlib import Path

API_VERSION = "1.0.0"
TITULO = "API de riesgo de incumplimiento de tarjetas de crédito"
DESCRIPCION = (
    "Estima si un cliente de tarjeta de crédito no pagará el mes siguiente. "
    "Modelo: árbol de decisión (pipeline de scikit-learn) del proyecto del Equipo 1."
)

# Carpeta raíz del proyecto: api/config.py -> api/ -> proyecto-equipo_1/
RAIZ = Path(__file__).resolve().parents[1]
MODEL_PATH = RAIZ / "models" / "modelo.joblib"
METADATA_PATH = MODEL_PATH.with_suffix(".json")

# Umbral elegido con validación cruzada en la sección 5.6 del notebook.
# Si existe models/modelo.json con un "umbral", se usa ese valor (lo agregará train.py).
UMBRAL_POR_DEFECTO = 0.3
