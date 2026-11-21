"""Carga del modelo y predicción
Nuestro modelo es de clasificación: usamos predict_proba() y aplicamos el umbral por fuera,
porque el archivo .joblib no guarda el umbral (predict() siempre usaría 0,5).
"""
 
import json
 
import joblib
import pandas as pd
 
from api import config
from api.schemas import ClienteEntrada
 
 
class ModeloNoDisponible(RuntimeError):
    """El archivo del modelo no existe: hay que generarlo primero."""
 
 
class ServicioModelo:
    """Envuelve el pipeline (preprocesamiento + árbol de decisión) y el umbral."""
 
    def __init__(self, ruta_modelo=config.MODEL_PATH, ruta_metadata=config.METADATA_PATH):
        if not ruta_modelo.exists():
            raise ModeloNoDisponible(
                f"No se encontró el modelo en {ruta_modelo}. "
                "Genéralo ejecutando el notebook completo (sección 6.1)."
            )
        self.pipeline = joblib.load(ruta_modelo)
        self.metadata = json.loads(ruta_metadata.read_text(encoding="utf-8")) if ruta_metadata.exists() else {}
        self.version = str(self.metadata.get("version", "notebook"))
        self.umbral = float(self.metadata.get("umbral", config.UMBRAL_POR_DEFECTO))
 
    def predecir(self, cliente: ClienteEntrada) -> tuple[str, float]:
        """Devuelve la clase ("no paga" o "paga") y la probabilidad de no pago."""
        datos = pd.DataFrame([cliente.model_dump()])
        probabilidad = float(self.pipeline.predict_proba(datos)[0, 1])
        clase = "no paga" if probabilidad >= self.umbral else "paga"
        return clase, round(probabilidad, 3)




    def predecir_lote(self, clientes: list[ClienteEntrada]) -> list[tuple[str, float]]:
        """Igual que predecir(), pero para varios clientes a la vez (una sola llamada al modelo)."""
        datos = pd.DataFrame([cliente.model_dump() for cliente in clientes])
        probabilidades = self.pipeline.predict_proba(datos)[:, 1]
        return [("no paga" if p >= self.umbral else "paga", round(float(p), 3)) for p in probabilidades]