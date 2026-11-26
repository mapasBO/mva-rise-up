# Styles / Estilos

`tarija/`: QGIS styles (.qml) with bilingual legend labels. Load with *Layer Properties > Symbology > Style > Load Style*.
`tarija/`: estilos QGIS (.qml) con etiquetas de leyenda bilingües. Se cargan con *Propiedades de la capa > Simbología > Estilo > Cargar estilo*.

| Style / Estilo | Classes / Clases |
|---|---|
| Indicators and dimension vulnerabilities (rasters) / Indicadores y vulnerabilidades por dimensión | 5 fixed classes 0.2 wide (very low ... very high), #1a9641 / #a6d96a / #ffffbf / #fdae61 / #d7191c. BIO2, BIO3 and URB3 are categorical. / 5 clases fijas de 0.2; BIO2, BIO3 y URB3 son categóricos. |
| `Tarija_Combined_Vulnerability.qml`, `*_StdDev.qml` | Mean ± 0.5 and ± 1.5 standard deviations (complementary) / Media ± 0.5 y ± 1.5 desviaciones estándar (complementario) |
| `Tarija_Hexagon_500m_CC|URB|BIO|Combined.qml` | Guide: 3 classes 0-0.33-0.66-max / Guía: 3 clases |
| `Tarija_Hexagon_500m_Combined_quintiles.qml` | Quintiles (complementary) / Quintiles (complementario) |

Bivariate maps use the hexagon styles with blending mode *Multiply*; their 3x3 legends are in `docs/img/tarija/legends`.
Los mapas bivariados usan los estilos de hexágonos con modo de fusión *Multiplicar*; sus leyendas 3x3 están en `docs/img/tarija/legends`.
