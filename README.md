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
│   └── convertir_a_csv.py        ← convierte el .xls a CSV (se ejecuta una vez)
├── docs/
│   └── 00_acuerdos_equipo.md     ← acuerdos del equipo
└── models/                       ← modelo guardado (lo genera el notebook; no se sube)
```

## Avance

- [x] 00 Entorno con uv
- [x] 01 Repositorio en GitHub
- [x] 02 Problema y datos (secciones 0, 1 y 2 del notebook)
- [ ] 03 Limpieza y EDA (secciones 3 y 4)
- [ ] 04 Modelo (sección 5)
- [ ] Avance intermedio (4 de noviembre)
- [ ] 05 Conclusiones y esquema de la presentación (sección 6)
- [ ] 06 Sustentación (25 de noviembre)
