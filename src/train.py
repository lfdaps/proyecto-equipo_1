"""Entrena el modelo de riesgo de incumplimiento y lo deja listo para la API.

Uso (desde la carpeta del proyecto):

    uv run python -m src.train

Qué hace, paso a paso:
    1. Carga el CSV y lo limpia con src/limpieza.py (las mismas reglas del notebook).
    2. Divide train/test (80/20), estratificado y con semilla 42.
    3. Arma el pipeline: preprocesamiento + árbol de decisión.
    4. Busca los hiperparámetros con GridSearchCV (5 partes del train), buscando el mejor recall.
    5. Evalúa en test UNA sola vez, con el umbral 0,3 elegido en la sección 5.6 del notebook.
    6. Reentrena con todos los datos y guarda:
         models/modelo.joblib -> el pipeline (lo que carga la API)
         models/modelo.json   -> versión, fecha, variables, umbral y métricas
"""

import json
from datetime import datetime

import joblib
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.metrics import confusion_matrix, f1_score, precision_score, recall_score
from sklearn.model_selection import GridSearchCV, StratifiedKFold, train_test_split
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.tree import DecisionTreeClassifier

from src.limpieza import OBJETIVO, RAIZ, cargar_datos, limpiar

VERSION = "1.0.0"
SEMILLA = 42
UMBRAL = 0.3  # elegido con validación cruzada en la sección 5.6 del notebook
CRITERIO_RECALL = 0.50  # criterio de éxito definido en la sección 1

VARIABLES_NUMERICAS = ["LIMIT_BAL", "PAY_1", "PAY_2", "PAY_3", "PAY_AMT1", "PAY_AMT2"]
VARIABLES_CATEGORICAS = ["EDUCATION", "MARRIAGE"]
VARIABLES = VARIABLES_NUMERICAS + VARIABLES_CATEGORICAS

# Combinaciones que prueba GridSearchCV
GRILLA = {
    "modelo__max_depth": [2, 3, 4, 5, 6, 7, 8, 9, 10],
    "modelo__min_samples_leaf": [1, 20, 50],
}

CARPETA_MODELOS = RAIZ / "models"
RUTA_MODELO = CARPETA_MODELOS / "modelo.joblib"
RUTA_METADATA = CARPETA_MODELOS / "modelo.json"


def construir_pipeline() -> Pipeline:
    """Preprocesamiento (igual al de la sección 5.3) + árbol de decisión."""
    preprocesamiento = ColumnTransformer([
        ("num", make_pipeline(SimpleImputer(strategy="median"), StandardScaler()), VARIABLES_NUMERICAS),
        ("cat", make_pipeline(SimpleImputer(strategy="most_frequent"),
                              OneHotEncoder(handle_unknown="ignore")), VARIABLES_CATEGORICAS),
    ])
    return Pipeline([
        ("preprocesamiento", preprocesamiento),
        ("modelo", DecisionTreeClassifier(random_state=SEMILLA)),
    ])


def main() -> None:
    # 1. Datos
    df = limpiar(cargar_datos())
    X, y = df[VARIABLES], df[OBJETIVO]

    # 2. Train y test
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=SEMILLA, stratify=y,
    )
    print(f"Datos: {len(df):,} clientes · train: {len(X_train):,} · test: {len(X_test):,}")

    # 3 y 4. Pipeline y búsqueda de hiperparámetros (solo con train)
    print("Buscando hiperparámetros con GridSearchCV (5 partes, scoring = recall)...")
    busqueda = GridSearchCV(
        construir_pipeline(),
        GRILLA,
        scoring="recall",
        cv=StratifiedKFold(n_splits=5, shuffle=True, random_state=SEMILLA),
    )
    busqueda.fit(X_train, y_train)
    pipeline = busqueda.best_estimator_
    mejores = {nombre.split("__")[-1]: valor for nombre, valor in busqueda.best_params_.items()}
    print(f"   Mejores hiperparámetros: {mejores} · recall promedio en CV: {busqueda.best_score_:.3f}")

    # 5. Evaluación en test, una sola vez, con el umbral elegido
    prob_test = pipeline.predict_proba(X_test)[:, 1]
    pred_test = (prob_test >= UMBRAL).astype(int)
    tn, fp, fn, tp = confusion_matrix(y_test, pred_test).ravel()
    metricas = {
        "precision": round(precision_score(y_test, pred_test), 3),
        "recall": round(recall_score(y_test, pred_test), 3),
        "F1": round(f1_score(y_test, pred_test), 3),
        "matriz_confusion": {"TN": int(tn), "FP": int(fp), "FN": int(fn), "TP": int(tp)},
    }
    cumple = metricas["recall"] >= CRITERIO_RECALL
    print(f"Test con umbral {UMBRAL}: precision {metricas['precision']} · "
          f"recall {metricas['recall']} · F1 {metricas['F1']}")
    print(f"   Criterio de éxito (recall >= {CRITERIO_RECALL}): {'CUMPLE' if cumple else 'NO CUMPLE'}")

    # 6. Reentrenar con todos los datos y guardar
    pipeline.fit(X, y)
    CARPETA_MODELOS.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipeline, RUTA_MODELO)
    metadata = {
        "modelo": "Árbol de decisión (pipeline de scikit-learn)",
        "version": VERSION,
        "entrenado_en": datetime.now().isoformat(timespec="seconds"),
        "variables_numericas": VARIABLES_NUMERICAS,
        "variables_categoricas": VARIABLES_CATEGORICAS,
        "hiperparametros": mejores,
        "umbral": UMBRAL,
        "metricas_test": metricas,
        "cumple_criterio_exito": cumple,
        "clientes_entrenamiento_final": len(X),
    }
    RUTA_METADATA.write_text(json.dumps(metadata, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Modelo guardado en:    {RUTA_MODELO.relative_to(RAIZ)}")
    print(f"Metadatos guardados en: {RUTA_METADATA.relative_to(RAIZ)}")


if __name__ == "__main__":
    main()
