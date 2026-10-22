# Predicción de incumplimiento de pago en tarjetas de crédito

> Identificar con anticipación qué clientes de tarjeta de crédito tienen más probabilidad de no pagar, para que el banco pueda decidir mejor a quién aprueba o aumenta el cupo y reducir sus pérdidas por cartera.

## Equipo_1

| Integrante | Rol principal | GitHub |
|---|---|---|
| Luisa Fernanda Pérez Sánchez | piloto | @lfdaps |
| Christian Paul Vélez Pazmiño | copiloto | @cristianvelez632-pixel |
| Richard Eduardo Bedoya Cortés | relator | @RichyBedoya2145 |
| Santiago Jaramillo Sepúlveda | relator | @sjsepulveda0108-coder |

## Problema de negocio

_(se completa en el módulo 02)_

## Dataset

- **Fuente:** [UCI Machine Learning Repository – Default of Credit Card Clients](https://archive.ics.uci.edu/dataset/350/default+of+credit+card+clients)
- **Tamaño:** 30.000 filas × 25 columnas
- **Variable objetivo:** `default payment next month`

## Cómo ejecutar

```bash
uv sync
uv run jupyter lab
```

## Estructura

```
├── data/raw/          ← datos originales
├── data/processed/    ← datos limpios (generados)
├── docs/              ← problema, charter, decisiones
├── notebooks/         ← exploración
├── src/               ← código reutilizable (limpieza, train, api)
└── models/            ← modelos entrenados (generados)
```

## Avance

- [ ] 00 Entorno con uv
- [ ] 01 Repositorio en GitHub
- [ ] 02 Problema y KPIs
- [ ] 03 Project charter
- [ ] 04 Limpieza
- [ ] 05 EDA
- [ ] 06 Baseline
- [ ] 07 Pipeline de entrenamiento
- [ ] 08 API
- [ ] 09 Entrega final
