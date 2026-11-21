"""API del Equipo 1: riesgo de incumplimiento de tarjetas de crédito 

Levantar el servidor (desde la carpeta del proyecto):

    uv run uvicorn api.main:app --reload

Luego abrir http://127.0.0.1:8000/docs para probarla desde el navegador.

Endpoints:
    GET  /health      -> ¿está viva la API? ¿cargó el modelo?
    GET  /model-info  -> versión y umbral del modelo
    POST /predict     -> riesgo de UN cliente
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException

from api import config
from api.modelo import ModeloNoDisponible, ServicioModelo
from api.schemas import ClienteEntrada, LoteEntrada, LoteSalida, PrediccionSalida

estado: dict = {"servicio": None, "error": None}


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Se ejecuta UNA vez al arrancar la API: carga el modelo en memoria."""
    try:
        estado["servicio"] = ServicioModelo()
        estado["error"] = None
    except ModeloNoDisponible as error:
        # La API arranca igual, pero /health avisa y /predict responde 503.
        estado["servicio"], estado["error"] = None, str(error)
    yield
    estado["servicio"] = None


app = FastAPI(title=config.TITULO, description=config.DESCRIPCION, version=config.API_VERSION, lifespan=lifespan)


def obtener_servicio() -> ServicioModelo:
    """Devuelve el modelo cargado, o un error 503 si no está disponible."""
    if estado["servicio"] is None:
        raise HTTPException(status_code=503, detail=estado["error"] or "Modelo no cargado")
    return estado["servicio"]


@app.get("/health", tags=["Monitoreo"])
def health() -> dict:
    """Chequeo de salud: dice si la API está viva y si cargó el modelo."""
    servicio = estado["servicio"]
    return {
        "status": "healthy" if servicio else "degraded",
        "api_version": config.API_VERSION,
        "modelo_cargado": servicio is not None,
    }


@app.get("/model-info", tags=["Monitoreo"])
def model_info() -> dict:
    """Datos del modelo: versión, umbral y lo que haya en models/modelo.json."""
    servicio = obtener_servicio()
    return {**servicio.metadata, "version": servicio.version, "umbral": servicio.umbral}


@app.post("/predict", response_model=PrediccionSalida, tags=["Predicción"])
def predict(cliente: ClienteEntrada) -> PrediccionSalida:
    """Estima si un cliente no pagará el mes siguiente.

    Si los datos no cumplen el esquema (cupo negativo, estado de pago 15, educación inválida…),
    FastAPI responde 422 automáticamente, antes de llegar a esta función.
    """
    servicio = obtener_servicio()
    clase, probabilidad = servicio.predecir(cliente)
    return PrediccionSalida(
        clase=clase,
        probabilidad_no_pago=probabilidad,
        umbral=servicio.umbral,
        version_modelo=servicio.version,
    )


@app.post("/predict/batch", response_model=LoteSalida, tags=["Predicción"])
def predict_batch(lote: LoteEntrada) -> LoteSalida:
    """Estima el riesgo de varios clientes en una sola petición (máximo config.MAX_BATCH)."""
    servicio = obtener_servicio()
    if len(lote.clientes) > config.MAX_BATCH:
        raise HTTPException(status_code=413, detail=f"Máximo {config.MAX_BATCH} clientes por petición")
    resultados = servicio.predecir_lote(lote.clientes)
    predicciones = [
        PrediccionSalida(clase=clase, probabilidad_no_pago=prob, umbral=servicio.umbral, version_modelo=servicio.version)
        for clase, prob in resultados
    ]
    return LoteSalida(predicciones=predicciones, cantidad=len(predicciones))