"""
MVA Tarija - Clean bilingual legends in the print layouts and export the maps to PNG.
MVA Tarija - Limpia las leyendas bilingües de las composiciones y exporta los mapas a PNG.

Run inside QGIS (Python console) with MVA_Tarija.qgz open, after phase3b_layouts.py:
    exec(open(r'<path>/phase3c_legends.py', encoding='utf-8').read())

What it does / Qué hace:
- Loads the styles in styles/tarija (.qml, bilingual class labels) onto the raster and hexagon layers.
- In each layout legend: custom two- or three-line title, removes the 'Band 1 (Gray)' node,
  and wraps long labels at '|' (' / ' becomes ' /|' in categorical labels).
- Exports every layout to PNG (300 dpi for reports, 150 dpi for the repository gallery).
"""
import os
from qgis.core import (QgsProject, QgsLayoutItemLegend, QgsLayoutExporter, QgsMapLayerLegendUtils,
                       QgsRasterLayer)

ROOT = r'C:/MVA/BOL/Tarija'  # <- edit: your local folder / editar: su carpeta local
REPO = r'C:/MVA/mva-rise-up'  # <- edit: your local clone / editar: su copia local del repositorio
STYLES = REPO + '/styles/tarija'
OUT_300 = ROOT + '/Data_Output/Maps_PNG'
OUT_150 = REPO + '/docs/img/tarija/maps'

# layout name: (layer name, legend title, wrap long labels)
LEGENDS = {
    'Tarija_CCInd3_Riverine-Flood': ('Tarija_CCInd3_Riverine-Flood', 'Riverine flood (HAND) /\nInundación fluvial (HAND)', False),
    'Tarija_CCInd4_Landslide': ('Tarija_CCInd4_Landslide', 'Landslide (slope susceptibility) /\nDeslizamientos (pendiente)', False),
    'Tarija_CCInd5_Urban-Heat-Island': ('Tarija_CCInd5_Urban-Heat-Island', 'Urban heat island (0-1) /\nIsla de calor urbana', False),
    'Tarija_CCInd6_Wildfire-Interface': ('Tarija_CCInd6_Wildfire-Interface', 'Wildfire interface /\nInterfaz urbano-vegetación', False),
    'Tarija_BIOInd1_MSA': ('Tarija_BIOInd1_MSA', 'Biodiversity loss (1 - MSA) /\nPérdida de biodiversidad', False),
    'Tarija_BIOInd2_Protected-Areas': ('Tarija_BIOInd2_Protected-Areas', 'Lack of protection by zone type /\nDesprotección por tipo de zona', True),
    'Tarija_BIOInd3_Natural-Cover-Loss': ('Tarija_BIOInd3_Natural-Cover-Loss', 'Natural cover loss 1985-2024 /\nPérdida de cobertura natural', True),
    'Tarija_URBInd1_Population': ('Tarija_URBInd1_Population', 'Population at sensitive ages /\nPoblación en edades sensibles', False),
    'Tarija_URBInd3_Urban-Growth': ('Tarija_URBInd3_Urban-Growth', 'Urban growth by period /\nCrecimiento urbano por periodo', True),
    'Tarija_URBInd4_Informal-Settlement': ('Tarija_URBInd4_Informal-Settlement', 'Informal settlement (housing proxy) /\nAsentamientos informales (vivienda)', False),
    'Tarija_URBInd5_Access-Facilities': ('Tarija_URBInd5_Access-Facilities', 'Walking access to facilities /\nAcceso caminable a equipamientos', False),
    'Tarija_Climate_Vulnerability': ('Tarija_Climate_Vulnerability', 'Climate vulnerability /\nVulnerabilidad climática', False),
    'Tarija_Biodiversity_Vulnerability': ('Tarija_Biodiversity_Vulnerability', 'Biodiversity vulnerability /\nVulnerabilidad de biodiversidad', False),
    'Tarija_Urban_Vulnerability': ('Tarija_Urban_Vulnerability', 'Urban vulnerability /\nVulnerabilidad urbana', False),
    'Tarija_Combined_Vulnerability': ('Tarija_Combined_Vulnerability', 'Combined MVA vulnerability (SD classes) /\nVulnerabilidad combinada (clases DE)', True),
    'Tarija_Hexagon_500m_CC': ('Tarija_Hexagon_500m_CC', 'Climate vulnerability /\nVulnerabilidad climática\n(hexagon mean / media por hexágono)', True),
    'Tarija_Hexagon_500m_URB': ('Tarija_Hexagon_500m_URB', 'Urban vulnerability /\nVulnerabilidad urbana\n(hexagon mean / media por hexágono)', True),
    'Tarija_Hexagon_500m_BIO': ('Tarija_Hexagon_500m_BIO', 'Biodiversity vulnerability /\nVulnerabilidad de biodiversidad\n(hexagon mean / media por hexágono)', True),
    'Tarija_Hexagon_500m_Combined': ('Tarija_Hexagon_500m_Combined', 'Combined vulnerability (SD classes) /\nVulnerabilidad combinada (clases DE)', False),
    'Tarija_Hexagon_500m_Combined_Quintiles': ('Tarija_Hexagon_500m_Combined (quintiles)', 'Combined vulnerability, quintiles /\nVulnerabilidad combinada, quintiles', True),
}
# style file for layers whose .qml name differs from the layer name / estilo cuando el nombre difiere
STYLE_FILE = {'Tarija_Combined_Vulnerability': 'Tarija_Combined_Vulnerability_StdDev.qml',
              'Tarija_Hexagon_500m_Combined': 'Tarija_Hexagon_500m_Combined_StdDev.qml',
              'Tarija_Hexagon_500m_Combined (quintiles)': 'Tarija_Hexagon_500m_Combined_quintiles.qml'}

pr = QgsProject.instance()
lm = pr.layoutManager()
done = []
for lay_name, (lyr_name, title, wrap) in LEGENDS.items():
    lay = lm.layoutByName(lay_name); ls = pr.mapLayersByName(lyr_name)
    if not lay or not ls:
        print('skip', lay_name); continue
    l = ls[0]
    qml = os.path.join(STYLES, STYLE_FILE.get(lyr_name, lyr_name + '.qml'))
    if os.path.exists(qml):
        l.loadNamedStyle(qml); l.triggerRepaint()
    for it in lay.items():
        if not isinstance(it, QgsLayoutItemLegend): continue
        it.setAutoUpdateModel(False)
        if wrap: it.setWrapString('|')
        root = it.model().rootGroup(); root.clear(); node = root.addLayer(l)
        node.setCustomProperty('legend/title-label', title)
        nodes = it.model().layerLegendNodes(node)
        if isinstance(l, QgsRasterLayer):  # drop 'Band 1 (Gray)' / quitar 'Banda 1 (Gray)'
            keep = [i for i, nd in enumerate(nodes) if not str(nd.data(0)).startswith(('Band', 'Banda'))]
            QgsMapLayerLegendUtils.setLegendNodeOrder(node, keep)
        it.model().refreshLayerLegend(node); it.updateLegend(); it.adjustBoxSize()
    done.append(lay_name)

# export all layouts (including the bivariate maps and any user layout) / exportar todas las composiciones
for lay in lm.printLayouts():
    for dpi, folder in ((300, OUT_300), (150, OUT_150)):
        os.makedirs(folder, exist_ok=True)
        st = QgsLayoutExporter.ImageExportSettings(); st.dpi = dpi
        QgsLayoutExporter(lay).exportToImage(os.path.join(folder, lay.name() + '.png'), st)
pr.write()
print(len(done), 'legends cleaned;', len(lm.printLayouts()), 'layouts exported')
