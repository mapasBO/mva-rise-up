# Tarija - Fase 3: agregación en hexágonos, coropletas y mapas bivariados (sección 5 de la guía)

Script: `scripts/tarija/phase3_hotspots.py`. Registro: `MVA/BOL/Tarija/phase3_log.csv`. Proyecto QGIS: `MVA/BOL/Tarija/MVA_Tarija.qgz`, grupo *Phase 3 - Hotspots (guide section 5)*.

**Igual que la guía**
- Grilla de hexágonos con espaciado horizontal y vertical de 500 m (`Base_Layer/Tarija_Hexagon_500m.gpkg`).
- Estadística zonal (media) de cada dimensión: `Combined/Tarija_Hexagon_500m_CC|URB|BIO.gpkg` (campos `CC_mean`, `URB_mean`, `BIO_mean`, más conteo de celdas).
- Coropletas con 3 clases de intervalo igual 0-0.33 / 0.33-0.66 / 0.66-máx, borde blanco y colores de la guía (URB #e8e8e8/#eeaeae/#f47474; CC #e8e8e8/#aec3bc/#749f91).
- Mapa bivariado Urbana sobre Clima con modo de fusión *Multiplicar* y leyenda 3x3.

**Agregados (desviaciones documentadas)**
- Extensión de la grilla tomada del área urbana y no del límite de la ciudad (en Tarija el límite es todo el municipio); se conservan solo los 550 hexágonos que tocan el área urbana.
- Dos pares bivariados más con la misma técnica: Clima x Biodiversidad y Urbana x Biodiversidad. Rampa de biodiversidad: #e8e8e8 / #c3b3d8 / #9972af.
- Hexágonos de la vulnerabilidad combinada y una tabla por barrio con las medias de las cuatro dimensiones (`Combined/Tarija_Neighbourhoods_MVA.gpkg`).
- Leyendas generadas por el script (`Combined/Tarija_Bivariate_Legend_*.png`) en lugar del complemento Bivariate Legend.

**Resultados (550 hexágonos)**

| Dimensión | Baja (0-0.33) | Media (0.33-0.66) | Alta (0.66-máx) | Media |
|---|---|---|---|---|
| Clima | 282 | 268 | 0 | 0.34 |
| Urbana | 385 | 165 | 0 | 0.29 |
| Biodiversidad | 16 | 239 | 294 | 0.64 |
| Combinada | 10 | 540 | 0 | 0.42 |

Bivariado Urbana x Clima (hexágonos): baja-baja 220; solo clima media 165; solo urbana media 62; **ambas medias 103** (ningún hexágono llega a la clase alta en ninguna de las dos). Los 103 hexágonos "ambas medias" son los hotspots de Tarija con la clasificación de la guía; están en la periferia norte, este y sur.

**Nota de lectura:** a 500 m la dimensión climática sí muestra las laderas periféricas (clase media), que a 12.5 m se diluían. Con las clases fijas de la guía ningún hexágono llega a "alta" en clima ni en urbana; los hotspots son por lo tanto las superposiciones media-media, no valores altos absolutos.

**Mapa combinado complementario (fuera de la guía):** `Tarija_Hexagon_500m_Combined` con clases por quintiles (estilo `Combined/Tarija_Hexagon_500m_Combined_quintiles.qml`; cortes 0.275 / 0.386 / 0.407 / 0.425 / 0.452 / 0.586). Con las 3 clases de la guía, 540 de 550 hexágonos caen en la clase media, por eso se usan quintiles para mostrar diferencias relativas dentro de Tarija. Q5 (0.452-0.586) marca el 20% de hexágonos más vulnerables: bordes norte, oeste y este, y el sur. Son hotspots relativos, no vulnerabilidad alta en términos absolutos.

**Clases por desviación estándar para los mapas combinados (complementario, decisión del equipo 2026-11-25):** con las clases fijas de la guía casi todo el índice combinado cae en una o dos clases. Las clases se fijan en la media ± 0.5 y ± 1.5 desviaciones estándar de cada mapa: raster `Tarija_Combined_Vulnerability` (media 0.415, DE 0.066): 0.315 / 0.382 / 0.448 / 0.515, celdas 6 / 25 / 40 / 22 / 7 %; hexágonos `Tarija_Hexagon_500m_Combined` (media 0.420, DE 0.044): 0.353 / 0.398 / 0.442 / 0.487, hexágonos 27 / 140 / 245 / 93 / 45. Estilos: `Combined/Tarija_Combined_Vulnerability_StdDev.qml`, `Combined/Tarija_Hexagon_500m_Combined_StdDev.qml`; en el proyecto QGIS ambas capas conservan el estilo de la guía como segundo estilo con nombre. 'Muy alta' = más de 1.5 DE sobre la media de Tarija (relativo, no absoluto).

**Composiciones de mapas:** 24 composiciones A4 en `MVA_Tarija.qgz`: 23 creadas con `scripts/tarija/phase3b_layouts.py` (indicadores, rasters de vulnerabilidad, mapas de hexágonos y los tres bivariados con su leyenda 3x3) y una hecha a mano (hexágonos combinados con un recuadro del centro a 1:42.000). Todos los mapas muestran los límites de barrios; se etiquetan 14 barrios principales, uno por celda de 2 km (el barrio más grande de cada celda) para repartir los nombres sin superposiciones: Avaroa, B. Aeropuerto, Catedral, El Constructor, Los Chapacos, Lourdes, Morros Blancos, San Antonio, San Blas, San Jerónimo, San Luis, Tabladita II, Torrecillas, Virgen de Fátima. La capa de barrios cubre el 34% del área urbana (el centro consolidado), por eso la periferia no tiene nombres de barrio.

**Leyendas:** `scripts/tarija/phase3c_legends.py` carga los estilos de `styles/tarija` y limpia todas las leyendas: un título corto EN/ES de dos o tres líneas en lugar del nombre del archivo, sin la entrada "Banda 1 (Gray)", etiquetas de clase bilingües con su rango de valores (p. ej. *Very low / Muy baja (0.00-0.20)*) y las etiquetas categóricas largas divididas en líneas (BIO2, BIO3, URB3, raster combinado, mapas de hexágonos). La isla de calor urbana (CC5) y la pérdida de biodiversidad (BIO1) usan las mismas 5 clases fijas que los demás indicadores. En URB3 la clase 0 (consolidado o sin crecimiento) es gris claro (#ececec) para que resalte el crecimiento urbano nuevo. Luego el script exporta todas las composiciones a PNG a 300 dpi (`Data_Output/Maps_PNG`) y a 150 dpi (`docs/img/tarija/maps`).
