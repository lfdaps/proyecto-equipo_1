"""Esquemas de entrada y salida de la API (Pydantic), como en el módulo 08.

Los nombres de los campos son los mismos 8 variables con las que se entrenó el modelo
(sección 5.1 del notebook), ya limpias: PAY_1 (antes PAY_0) y educación y estado civil en texto.
"""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

Educacion = Literal["posgrado", "universidad", "bachillerato", "otros"]
EstadoCivil = Literal["casado", "soltero", "otros"]

EJEMPLO_CLIENTE = {
    "LIMIT_BAL": 50000,
    "PAY_1": 2,
    "PAY_2": 2,
    "PAY_3": 0,
    "PAY_AMT1": 0,
    "PAY_AMT2": 1500,
    "EDUCATION": "universidad",
    "MARRIAGE": "soltero",
}


class ClienteEntrada(BaseModel):
    """Datos de un cliente de tarjeta de crédito (montos en dólares taiwaneses)."""

    model_config = ConfigDict(json_schema_extra={"examples": [EJEMPLO_CLIENTE]})

    LIMIT_BAL: int = Field(gt=0, description="Cupo de crédito de la tarjeta")
    PAY_1: int = Field(ge=-2, le=9, description="Estado de pago de septiembre: -1 = al día, 1 = un mes de atraso, ..., 9 = nueve o más")
    PAY_2: int = Field(ge=-2, le=9, description="Estado de pago de agosto")
    PAY_3: int = Field(ge=-2, le=9, description="Estado de pago de julio")
    PAY_AMT1: int = Field(ge=0, description="Valor pagado en septiembre")
    PAY_AMT2: int = Field(ge=0, description="Valor pagado en agosto")
    EDUCATION: Educacion = Field(description="Nivel educativo")
    MARRIAGE: EstadoCivil = Field(description="Estado civil")


class PrediccionSalida(BaseModel):
    """Respuesta de /predict: la clase, la probabilidad y el umbral usado."""

    clase: Literal["no paga", "paga"]
    probabilidad_no_pago: float = Field(description="Probabilidad (0 a 1) de que el cliente no pague el mes siguiente")
    umbral: float = Field(description="Si la probabilidad es mayor o igual al umbral, la clase es 'no paga'")
    version_modelo: str


class LoteEntrada(BaseModel):
    """Entrada de /predict/batch: una lista de clientes."""

    clientes: list[ClienteEntrada] = Field(min_length=1)


class LoteSalida(BaseModel):
    """Respuesta de /predict/batch: una predicción por cliente, en el mismo orden."""

    predicciones: list[PrediccionSalida]
    cantidad: int