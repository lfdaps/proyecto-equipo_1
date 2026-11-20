"""Pruebas de la API con pytest (como tests/test_api.py del módulo 08).

Ejecutar desde la carpeta del proyecto:

    uv run pytest -v

El TestClient simula pedidos a la API SIN encender el servidor.
Las pruebas que necesitan el modelo se saltan si models/modelo.joblib no existe.
"""

import pytest
from fastapi.testclient import TestClient

from api import config
from api.main import app
from api.schemas import EJEMPLO_CLIENTE

requiere_modelo = pytest.mark.skipif(
    not config.MODEL_PATH.exists(),
    reason="Primero genera el modelo ejecutando el notebook completo (sección 6.1)",
)

CLIENTE_AL_DIA = {
    **EJEMPLO_CLIENTE,
    "LIMIT_BAL": 300000,
    "PAY_1": -1,
    "PAY_2": -1,
    "PAY_3": -1,
    "PAY_AMT1": 5000,
    "PAY_AMT2": 5000,
}


@pytest.fixture(scope="module")
def cliente():
    # El "with" ejecuta el lifespan: carga el modelo
    with TestClient(app) as c:
        yield c


def test_health_responde(cliente):
    respuesta = cliente.get("/health")
    assert respuesta.status_code == 200
    assert respuesta.json()["api_version"] == config.API_VERSION


@requiere_modelo
def test_predict_cliente_valido(cliente):
    respuesta = cliente.post("/predict", json=EJEMPLO_CLIENTE)
    assert respuesta.status_code == 200
    cuerpo = respuesta.json()
    assert cuerpo["clase"] in ("no paga", "paga")
    assert 0 <= cuerpo["probabilidad_no_pago"] <= 1
    assert cuerpo["umbral"] == 0.3


@requiere_modelo
def test_atrasado_mas_riesgoso_que_al_dia(cliente):
    """Sentido común: un cliente atrasado debe tener más riesgo que uno al día."""
    atrasado = cliente.post("/predict", json=EJEMPLO_CLIENTE).json()
    al_dia = cliente.post("/predict", json=CLIENTE_AL_DIA).json()
    assert atrasado["probabilidad_no_pago"] > al_dia["probabilidad_no_pago"]
    assert al_dia["clase"] == "paga"


@pytest.mark.parametrize(
    "cambio",
    [
        {"LIMIT_BAL": -1000},        # cupo negativo
        {"PAY_1": 15},               # estado de pago fuera de -2 a 9
        {"EDUCATION": "doctorado"},  # categoría no permitida
        {"PAY_AMT1": "mucho"},       # tipo incorrecto
    ],
)
def test_datos_invalidos_422(cliente, cambio):
    respuesta = cliente.post("/predict", json={**EJEMPLO_CLIENTE, **cambio})
    assert respuesta.status_code == 422


def test_campo_faltante_422(cliente):
    incompleto = {k: v for k, v in EJEMPLO_CLIENTE.items() if k != "LIMIT_BAL"}
    assert cliente.post("/predict", json=incompleto).status_code == 422