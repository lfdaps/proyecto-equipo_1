"""Convierte el dataset original de UCI (.xls) a CSV.

Se ejecuta UNA sola vez, desde la carpeta del repositorio:
    uv run python src/convertir_a_csv.py
"""
from pathlib import Path

import pandas as pd

ORIGEN = Path("data/raw/default of credit card clients.xls")
DESTINO = Path("data/raw/default_credit_card_clients.csv")

# El Excel tiene DOS filas de encabezado: la primera dice X1, X2, ..., Y (no sirve)
# y la segunda tiene los nombres reales (ID, LIMIT_BAL, SEX, ...).
# header=1 le dice a pandas que use la segunda fila (se cuenta desde 0) como nombres.
df = pd.read_excel(ORIGEN, header=1)

# index=False evita que pandas agregue una columna extra con el número de fila.
df.to_csv(DESTINO, index=False)

print(f"Listo: {df.shape[0]:,} filas y {df.shape[1]} columnas guardadas en {DESTINO}")