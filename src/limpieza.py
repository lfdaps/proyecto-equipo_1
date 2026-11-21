"""Limpieza de los datos de clientes de tarjeta de crédito.

Son las mismas decisiones de la sección 3 del notebook, escritas como funciones
para que train.py (y cualquier otro script) las pueda reutilizar sin copiar código.
"""

from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]  # src/limpieza.py -> src/ -> proyecto-equipo_1/
ARCHIVO_DATOS = RAIZ / "data" / "raw" / "default_credit_card_clients.csv"
OBJETIVO = "default payment next month"


def cargar_datos(ruta: Path = ARCHIVO_DATOS) -> pd.DataFrame:
    """Lee el CSV original (lo genera src/convertir_a_csv.py a partir del .xls)."""
    return pd.read_csv(ruta)


def limpiar(df: pd.DataFrame) -> pd.DataFrame:
    """Aplica las decisiones de limpieza del notebook y devuelve una copia limpia."""
    df_limpio = df.copy()

    # Las filas sin variable objetivo no sirven para entrenar ni para evaluar.
    df_limpio = df_limpio.dropna(subset=[OBJETIVO])

    # Decisión 1: SEX pasa de código a texto, para que el modelo la trate como categoría
    df_limpio["SEX"] = df_limpio["SEX"].map({1: "hombre", 2: "mujer"})

    # Decisión 2: EDUCATION a texto; los códigos sin documentar (0, 5, 6) se unen a "otros"
    df_limpio["EDUCATION"] = df_limpio["EDUCATION"].map({
        1: "posgrado", 2: "universidad", 3: "bachillerato",
        4: "otros", 5: "otros", 6: "otros", 0: "otros",
    })

    # Decisión 3: MARRIAGE a texto; el código sin documentar (0) se une a "otros"
    df_limpio["MARRIAGE"] = df_limpio["MARRIAGE"].map({1: "casado", 2: "soltero", 3: "otros", 0: "otros"})

    # Decisión 4: PAY_0 se renombra PAY_1, para que coincida con BILL_AMT1 y PAY_AMT1 (septiembre)
    df_limpio = df_limpio.rename(columns={"PAY_0": "PAY_1"})

    # Decisión 5: los 35 clientes con el mismo perfil NO se eliminan (tienen ID distinto)
    return df_limpio