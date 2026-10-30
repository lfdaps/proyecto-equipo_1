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

_(se completa en el módulo 02)_

## Dataset

- **Fuente:** [UCI Machine Learning Repository – Default of Credit Card Clients](https://archive.ics.uci.edu/dataset/350/default+of+credit+card+clients)
- **Tamaño:** 30.000 filas × 25 columnas
- **Variable objetivo:** `default payment next month`

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
- [ ] 02 Problema y datos (secciones 0, 1 y 2 del notebook)
- [ ] 03 Limpieza y EDA (secciones 3 y 4)
- [ ] 04 Modelo (sección 5)
- [ ] Avance intermedio (4 de noviembre)
- [ ] 05 Conclusiones y esquema de la presentación (sección 6)
- [ ] 06 Sustentación (25 de noviembre)
