# Tarija - Fase 1: indicadores en la estructura de la guía (secciones 3-4)

Script: `scripts/tarija/phase1_organize_outputs.py` (se ejecuta en la consola Python de QGIS). Registro: `MVA/BOL/Tarija/phase1_log.csv`.

**Qué se hizo**
- 11 indicadores escritos en `Data_Output/CC|BIO|URB` con los nombres de la guía. Todos en GeoTIFF Float32, NoData -9999, sobre la grilla del MVA (EPSG:32720, 12.5 m, 1,114 x 1,194 celdas).
- 10 indicadores se copiaron con **los valores sin cambios** (verificado celda por celda contra la fuente).
- La isla de calor pasó de su grilla Landsat de 30 m a la de 12.5 m con **vecino más cercano** (sin interpolar; la media no cambia, 0.503). Las celdas NaN quedaron como NoData.
- Capas base en `Data_Output/Base_Layer`: área urbana (CRS asignado a EPSG:32720), límite municipal, 86 barrios, 21 distritos, 6,042 manzanos (GeoPackage) y el sombreado del relieve recortado a la grilla.
- Junto a cada producto se copiaron los metadatos (.qmd) y el estilo (.qml) de la fuente, con el nombre nuevo y una entrada de historial.
- Excluido: URBInd2 Cobertura del suelo. No aplica: CCInd1-2 (costeros).

**Resultado**
| Dim. | Producto | Método | Celdas válidas | Media |
|---|---|---|---|---|
| CC | Tarija_CCInd3_Riverine-Flood | copy | 669,265 | 0.159 |
| CC | Tarija_CCInd4_Landslide | copy | 669,246 | 0.370 |
| CC | Tarija_CCInd5_Urban-Heat-Island | nearest 30→12.5 m | 676,219 | 0.503 |
| CC | Tarija_CCInd6_Wildfire-Interface | copy | 669,265 | 0.263 |
| BIO | Tarija_BIOInd1_MSA | copy | 648,634 | 0.518 |
| BIO | Tarija_BIOInd2_Protected-Areas | copy | 669,265 | 0.897 |
| BIO | Tarija_BIOInd3_Natural-Cover-Loss | copy | 669,265 | 0.515 |
| URB | Tarija_URBInd1_Population | copy | 543,610 | 0.261 |
| URB | Tarija_URBInd3_Urban-Growth | copy | 669,265 | 0.095 |
| URB | Tarija_URBInd4_Informal-Settlement | copy | 446,019 | 0.428 |
| URB | Tarija_URBInd5_Access-Facilities | copy | 658,914 | 0.371 |

**Nota para la Fase 2:** la cobertura cambia entre indicadores (el área urbana tiene 669,265 celdas). Población (81%) y vivienda (67%) solo cubren manzanos poblados; el MSA (97%) y la isla de calor (algo más allá de la máscara) también difieren. Antes de calcular la vulnerabilidad por dimensión hay que decidir cómo promediar las celdas donde falta algún indicador.
