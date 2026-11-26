# Tarija - Fase 2: vulnerabilidad por dimensión y combinada (sección 4.5 de la guía)

Script: `scripts/tarija/phase2_vulnerability.py`. Registro: `MVA/BOL/Tarija/phase2_log.csv`.

**Regla (decisión del equipo, 2026-11-25):** cada dimensión = promedio de los indicadores **disponibles** en cada celda, con pesos iguales; combinada = promedio de las tres dimensiones. Todo recortado al área urbana (669,287 celdas, regla de centro de celda). Un raster complementario por dimensión (`*_IndicatorCount`, `Tarija_Combined_DimensionCount`) registra cuántos insumos entraron en cada celda.

**Productos** (`Data_Output/CC|BIO|URB|Combined`, GeoTIFF Float32, NoData -9999, con .qmd bilingüe y estilo .qml de 5 clases): `Tarija_Climate_Vulnerability`, `Tarija_Biodiversity_Vulnerability`, `Tarija_Urban_Vulnerability`, `Tarija_Combined_Vulnerability`.

| Dimensión | Insumos | Celdas con todos los insumos | Media | Clases % (muy baja / baja / moderada / alta / muy alta) |
|---|---|---|---|---|
| Climática | 4 | 99.8% | 0.324 | 19.7 / 51.2 / 26.2 / 2.8 / 0.0 |
| Biodiversidad | 3 | 96.8% | 0.645 | 2.0 / 11.7 / 22.0 / 52.9 / 11.3 |
| Urbana | 4 | 65.9% | 0.278 | 29.2 / 54.8 / 15.2 / 0.7 / 0.1 |
| Combinada | 3 dim. | 99.8% | 0.415 | 0.0 / 42.2 / 57.2 / 0.5 / 0.0 |

**Observaciones**
- Biodiversidad es la dimensión más alta (media 0.64), por la protección ponderada (84% del área urbana fuera de toda zona de protección) y el MSA (centro consolidado 0.7-0.9).
- Clima y biodiversidad tienen correlación negativa (r = -0.47): las laderas periféricas con vegetación cercana puntúan alto en deslizamientos/incendios pero bajo en pérdida de cobertura natural. La urbana es casi independiente de ambas (r ~ 0).
- Promediar tres dimensiones comprime el índice combinado hacia las clases medias (99% entre 0.2 y 0.6). Es esperable con promedios de pesos iguales; los hotspots deben leerse con la agregación por hexágonos y el mapa bivariado (Fase 3), no solo con clases fijas de 0.2.
- La vulnerabilidad urbana usa los cuatro indicadores en el 65.9% del área urbana; en el resto falta vivienda y/o población (suelo no poblado).
