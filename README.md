# Predicción de incumplimiento de pago en tarjetas de crédito

> Identificar con anticipación qué clientes de tarjeta de crédito tienen más probabilidad de no pagar, para que el banco pueda decidir mejor a quién aprueba o aumenta el cupo y reducir sus pérdidas por cartera.

## Equipo_1

| Integrante | Rol principal | GitHub |
|---|---|---|
| Luisa Fernanda Pérez Sánchez | piloto | @lfdaps |
| Christian Paul Vélez Pazmiño | copiloto | @cristianvelez632-pixel |
| Richard Eduardo Bedoya Cortés | relator | @Richy2145 |
| Santiago Jaramillo Sepúlveda | relator | @sjsepulveda0108-coder |

## Problema de negocio

El banco necesita saber, antes de la fecha de pago, qué clientes de tarjeta de crédito probablemente *no pagarán el mes siguiente*, para priorizar la cobranza preventiva y no aumentar el cupo a clientes de alto riesgo.

- **Decisión que apoya:** a quién llamar primero y a quién no subirle el cupo.
- **Quién decide:** el área de riesgo de crédito y cobranza.
- **Tipo de análisis:** predictivo (clasificación).
- **Criterio de éxito:** detectar al menos el 50 % de los clientes que no pagan (recall de la clase 1 ≥ 0,50 en test) y superar al baseline en F1.
- **KPI 1:** tasa de incumplimiento mensual de la cartera (hoy 22,1 %; meta < 20 % en 6 meses).
- **KPI 2:** % de clientes con al menos un mes de atraso en su último pago (meta: −2 puntos en 6 meses).

## Dataset

- **Fuente:** [UCI Machine Learning Repository – Default of Credit Card Clients](https://archive.ics.uci.edu/dataset/350/default+of+credit+card+clients) (Yeh y Lien, 2009).
- **Qué es una fila:** un cliente de tarjeta de crédito de un banco de Taiwán, con su historial de abril a septiembre de 2005.
- **Tamaño:** 30.000 filas × 25 columnas, sin nulos.
- **Variable objetivo:** default payment next month (1 = no paga el mes siguiente: 22,1 %; 0 = paga: 77,9 %).
- **Variables:** cupo (LIMIT_BAL), sexo, educación, estado civil, edad, estado de pago de cada mes (PAY_0, PAY_2 a PAY_6), valor facturado (BILL_AMT1 a 6) y valor pagado (PAY_AMT1 a 6), en dólares taiwaneses.
- **Archivos:** data/raw/default of credit card clients.xls (original) y data/raw/default_credit_card_clients.csv (el que usa el notebook, generado con src/convertir_a_csv.py). 

## Hallazgos principales

1. **El atraso reciente es la mejor señal:** con 2 meses de atraso en septiembre no paga el 69 % de los clientes, frente al 13 % de los que están al día.
2. **Menos cupo, más incumplimiento:** el cupo mediano de quienes no pagan es 90.000 y el de quienes pagan es 150.000.
3. **La edad casi no influye:** la mediana es de 34 años tanto en los que pagan como en los que no (rechazamos la hipótesis de que los jóvenes incumplen más).

## Resultados del modelo

Métrica principal: *recall* de la clase "no paga" en los datos de prueba (de cada 100 clientes que no pagan, ¿a cuántos detectamos?).

| Modelo | Recall (test) | F1 (test) |
|---|---|---|
| Baseline (siempre "paga") | 0,000 | 0,000 |
| Regresión logística | 0,239 | 0,356 |
| *Árbol de decisión (elegido)* | *0,372* | *0,476* |

El árbol, con 8 variables, detecta a 37 de cada 100 clientes que no pagan, frente a ninguno del baseline, y no tiene *overfitting*. Con el umbral de 0,5 que usa `predict()` todavía no alcanza el criterio de éxito (50 %): se le escapan sobre todo los clientes que venían al día en sus pagos.

**Umbral de decisión:** el umbral se eligió solo con los datos de entrenamiento, usando validación cruzada de 5 partes: se escogió el umbral más alto con un recall promedio de al menos 0,50, que fue **0,3**. Después se evaluó el test una sola vez: el árbol detecta a 50 de cada 100 clientes que no pagan (recall de 0,501 y F1 de 0,516) y **cumple el criterio de éxito**, a cambio de más llamadas preventivas a clientes que sí pagan (585 falsas alarmas frente a 255).

## Límites del modelo

- Casi no detecta a los clientes que venían al día y aun así no pagaron, que son la mitad de los que no pagan.
- Los datos son de un banco de Taiwán en 2005; para usarlo en otro país o en otra época habría que revisarlo con datos nuevos.
- Con clientes nuevos, el recall podría quedar un poco por debajo de 0,50 (en la validación cruzada varió ± 0,025).
- Solo usa el cupo, los pagos, la educación y el estado civil; no conoce los ingresos ni el empleo del cliente.

## Cómo ejecutar

Requisitos: tener instalados `git` y `uv`. En Windows (PowerShell):

```powershell
git clone https://github.com/lfdaps/proyecto-equipo_1.git
cd proyecto-equipo_1
uv sync
uv run jupyter lab
```

Luego se abre `notebooks/proyecto_equipo.ipynb`, se elige el kernel `.venv` y se ejecuta *Restart Kernel and Run All*.

> El dataset ya está en `data/raw/` como CSV. Solo si hay que regenerarlo desde el Excel original: `uv run python src/convertir_a_csv.py`.

### Cómo entrenar el modelo

El modelo que usa la API se entrena con un solo comando, sin abrir el notebook:

```powershell
uv run python -m src.train
```

Este comando (`src/train.py`) hace lo mismo que las secciones 3 y 5 del notebook, en orden:

1. Carga el CSV y lo limpia con `src/limpieza.py`, con las mismas reglas de la sección 3.
2. Separa 80 % para entrenamiento y 20 % para prueba, de forma estratificada y con semilla 42.
3. Busca la profundidad del árbol y el tamaño mínimo de las hojas con `GridSearchCV`, usando solo el entrenamiento (5 partes) y eligiendo por recall. El mejor resultado fue una profundidad de 5.
4. Evalúa una sola vez en prueba con el umbral 0,3: recall de 0,501, así que cumple el criterio de éxito.
5. Vuelve a entrenar con los 30.000 clientes y guarda dos archivos en `models/`:
   - `modelo.joblib`: el pipeline completo (preprocesamiento y árbol), que es lo que carga la API.
   - `modelo.json`: versión, fecha, variables, hiperparámetros, umbral y métricas de prueba.

Tarda unos 10 segundos. Ninguno de los dos archivos se sube a GitHub, porque se pueden volver a generar con este comando.

## API

La API recibe los datos de un cliente y responde si probablemente no pagará el mes siguiente. Usa el modelo guardado en `models/modelo.joblib` y el umbral de 0,3 guardado en `models/modelo.json`; los dos se generan con `uv run python -m src.train`.

Para encenderla:

```powershell
uv run uvicorn api.main:app --reload
```

Luego se abre http://127.0.0.1:8000/docs para probarla desde el navegador.

| Endpoint | Para qué sirve |
|---|---|
| `GET /health` | Dice si la API está funcionando y si cargó el modelo |
| `GET /model-info` | Muestra la versión del modelo y el umbral |
| `POST /predict` | Recibe los datos de un cliente y devuelve la clase, la probabilidad y el umbral |
| `POST /predict/batch` | Recibe una lista de clientes (máximo 100) y devuelve una predicción por cliente, en el mismo orden |

Ejemplo de solicitud a `/predict`:

```json
{
  "LIMIT_BAL": 50000,
  "PAY_1": 2,
  "PAY_2": 2,
  "PAY_3": 0,
  "PAY_AMT1": 0,
  "PAY_AMT2": 1500,
  "EDUCATION": "universidad",
  "MARRIAGE": "soltero"
}
```

Respuesta:

```json
{
  "clase": "no paga",
  "probabilidad_no_pago": 0.73,
  "umbral": 0.3,
  "version_modelo": "1.0.0"
}
```


| Código | Significa | Cuándo pasa |
|---|---|---|
| 200 | Todo bien | La predicción se hizo |
| 422 | Datos inválidos | Falta un dato, el tipo es incorrecto o el valor no tiene sentido (por ejemplo, cupo negativo o un nivel educativo que no existe) |
| 413 | Solicitud demasiado grande | Se mandaron más de 100 clientes a `/predict/batch` |
| 503 | Servicio no disponible | No se encontró el modelo; hay que ejecutar `uv run python -m src.train` primero |

Para ejecutar las pruebas automáticas:

```powershell
uv run python -m pytest -v
```

## Estructura

```
proyecto-equipo_1/
├── README.md                     ← resumen, cómo ejecutar, resultados y límites
├── pyproject.toml / uv.lock      ← entorno reproducible (uv)
├── .github/
│   └── pull_request_template.md  ← plantilla de los pull requests
├── data/
│   ├── raw/                      ← dataset original (.xls) y su versión CSV
│   └── processed/                ← datos limpios (los genera el notebook; no se suben)
├── notebooks/
│   └── proyecto_equipo.ipynb     ← el proyecto completo
├── src/
│   ├── convertir_a_csv.py        ← convierte el .xls a CSV (se ejecuta una vez)
│   ├── limpieza.py               ← las reglas de limpieza del notebook, como funciones
│   └── train.py                  ← entrena el modelo y guarda modelo.joblib y modelo.json
├── api/                          ← la API (FastAPI): main.py, schemas.py, modelo.py, config.py
├── tests/                        ← pruebas automáticas de la API
├── docs/
│   └── 00_acuerdos_equipo.md     ← acuerdos del equipo
└── models/                       ← modelo.joblib y modelo.json (los genera src/train.py; no se suben)
```

## Avance

- [x] 00 Entorno con uv
- [x] 01 Repositorio en GitHub
- [x] 02 Problema y datos (secciones 0, 1 y 2 del notebook)
- [x] 03 Limpieza y EDA (secciones 3 y 4)
- [x] 04 Modelo (sección 5)
- [x] Avance intermedio (4 de noviembre)
- [x] 05 Conclusiones (sección 6)
- [x] Pipeline de entrenamiento (`src/train.py`)
- [x] API con FastAPI y pruebas
- [ ] 06 Sustentación (25 de noviembre)
