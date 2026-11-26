# Scripts

PyQGIS scripts per guide step (QGIS 3.44). Run them in order (1, 2, 3, 3b, 3c) in the QGIS Python console:
`exec(open(r'<path>/phase2_vulnerability.py', encoding='utf-8').read())`.
Before running, edit the folder lines marked `# <- edit` at the top of each script.

Scripts PyQGIS por paso de la guía (QGIS 3.44). Se ejecutan en la consola Python de QGIS con la línea anterior.
Antes de ejecutar, edite las líneas de carpeta marcadas con `# <- edit` al inicio de cada script.

| Script | Phase / Fase | Output / Producto |
|---|---|---|
| `tarija/phase1_organize_outputs.py` | 1 | Indicators renamed onto the MVA grid / Indicadores renombrados en la grilla MVA |
| `tarija/phase2_vulnerability.py` | 2 | Dimension and combined vulnerability / Vulnerabilidad por dimensión y combinada |
| `tarija/phase3_hotspots.py` | 3 | 500 m hexagons, choropleths, bivariate maps / Hexágonos, coropletas, bivariados |
| `tarija/phase3b_layouts.py` | 3 | A4 print layouts / Composiciones A4 |
| `tarija/phase3c_legends.py` | 3 | Clean bilingual legends, PNG export (300 and 150 dpi) / Leyendas bilingües limpias, exportación PNG |
