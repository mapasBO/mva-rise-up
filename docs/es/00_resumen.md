# Resumen y desviaciones respecto de la guía

## Fases

| Fase | Secciones de la guía | Producto |
|---|---|---|
| 0 Preparación | Jerarquía de carpetas y nombres | Carpetas, tabla de correspondencias, esqueleto del repositorio |
| 1 Indicadores | 2, 3, 4.2-4.4 | Indicadores renombrados/completados en Data_Output |
| 2 Vulnerabilidad | 4.5 | Vulnerabilidad por dimensión y combinada |
| 3 Hotspots | 5 | Hexágonos de 500 m (y barrios), coropletas, tres mapas bivariados, 24 composiciones |
| 4 Documentación | - | Este repositorio (EN/ES) |

## Desviaciones respecto de la guía (Tarija)

| Tema | Guía | Esta aplicación | Motivo |
|---|---|---|---|
| CRS | WGS 84 / Pseudo-Mercator (EPSG:3857) | Tarija: WGS 84 / UTM 20S (EPSG:32720) | Web Mercator agranda las distancias ~7-8% a 21.5° S; UTM conserva el tamaño real de celda, las áreas y la estadística zonal |
| Tamaño de celda | 10 m | 12.5 m | Resolución nativa del DEM del proyecto (ALOS PALSAR RTC); los insumos finos no se agregan y los gruesos solo se sobremuestrean (vecino más cercano) |
| Formato vectorial | Shapefile | GeoPackage | Nombres de campo largos, UTF-8, un archivo por producto |
| Normalización | Mín-máx | Mín-máx sobre el rango p5-p95 cuando hay valores atípicos (documentado por indicador) | Evita que pocas celdas extremas compriman la escala |
| Numeración de indicadores | CCInd1-4, BIOInd1, URBInd1-4 | Se mantienen los números de la guía (CCInd1-2 costeros = no aplica en Tarija); las extensiones van después (CCInd5-6, BIOInd3, URBInd5) | Misma numeración en ambas ciudades para comparar |
| Data_Input / Process | Copias de datos crudos e intermedios | README con punteros al inventario de datos existente | Evitar duplicar GB de datos y copias desactualizadas |
| Áreas protegidas | Protected Planet | Zonas de protección del PMOT, ponderadas por tipo | No hay áreas protegidas nacionales dentro del área urbana |
| Asentamientos informales | Dato oficial | Proxy con privación habitacional del censo 2024 (4 de 5 criterios ODS 11.1.1) hasta recibir el dato municipal | Capa oficial pendiente del GAM Tarija |
| Indicador de deslizamientos | CCInd4 Deslizamientos (dato de susceptibilidad) | Solo susceptibilidad por pendiente, normalizada entre p5 y p95 de la pendiente urbana | Decisión del equipo (2026-11-25); no se usa la versión compuesta (cauces + suelo desnudo) |
| Indicador de la guía excluido | URBInd2 Cobertura del suelo | No se incluye en Tarija | Decisión del equipo (2026-11-25): la capa anterior está en EPSG:4326 y con pesos sin confirmar |
| Agregación climática | Promedio simple de indicadores | Promedio simple, como la guía (decisión del equipo, 2026-11-25) | Se probaron y descartaron el máximo multiamenaza, quitar indicadores y pesos, para mantener el método y la comparabilidad con otras ciudades que apliquen la guía |
| Extensión de la grilla de hexágonos | Límite de la ciudad | Área urbana; solo hexágonos que la tocan | En Tarija el límite es todo el municipio |
| Mapas bivariados | Urbana x Clima | También Clima x Biodiversidad y Urbana x Biodiversidad (rampa BIO #e8e8e8/#c3b3d8/#9972af) | Mostrar las tres superposiciones que el MVA busca identificar |
| Mapa combinado por hexágono | No se mapea | Mapa complementario con quintiles | Con las clases de la guía 540 de 550 hexágonos quedan en una sola clase |
| Clases de los mapas combinados | Fijas de 0.2 (raster) / no se mapea (hexágonos) | Media ± 0.5 y ± 1.5 DE (estilo complementario; se conserva el de la guía) | Con clases fijas el índice combinado queda en una o dos clases |
