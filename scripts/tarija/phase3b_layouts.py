"""
MVA Tarija - Print layouts with legends for every map (indicators, vulnerability, hexagons, bivariate).
MVA Tarija - Composiciones de impresión con leyenda para cada mapa (indicadores, vulnerabilidad, hexágonos, bivariados).

Run inside QGIS (Python console). Works on MVA_Tarija.qgz without opening it, then saves it.
"""
import os
from qgis.core import (QgsProject, QgsPrintLayout, QgsLayoutItemMap, QgsLayoutItemLegend, QgsLayoutItemLabel,
                       QgsLayoutItemPicture, QgsLayoutItemScaleBar, QgsLayoutPoint, QgsLayoutSize, QgsUnitTypes,
                       QgsRectangle, QgsLayoutItemPage, QgsLegendStyle, QgsVectorLayer)
from qgis.PyQt.QtGui import QFont, QColor

ROOT = r'C:/MVA/BOL/Tarija'  # <- edit: your local folder / editar: su carpeta local
PROJ = ROOT + '/MVA_Tarija.qgz'
LEG = ROOT + '/Data_Output/Combined/Tarija_Bivariate_Legend_{}.png'
CREDIT = ('Source / Fuente: RISE_UP Tarija MVA, UN-Habitat (2026). Method / Método: UN-Habitat & UNITAR-UNOSAT, '
          'Geospatial Workflow for MVA (2024). CRS EPSG:32720 - WGS 84 / UTM 20S.')

pr = QgsProject.instance() if os.path.normcase(QgsProject.instance().fileName()) == os.path.normcase(PROJ) else QgsProject()
if pr is not QgsProject.instance(): pr.read(PROJ)
lm = pr.layoutManager()


def L(name, group=None):
    if group:
        g = pr.layerTreeRoot().findGroup(group)
        for n in g.findLayers():
            if n.layer().name() == name: return n.layer()
        raise KeyError(f'{name} in {group}')
    ls = pr.mapLayersByName(name)
    if not ls: raise KeyError(name)
    return ls[0]


HILL, URBAN = L('Tarija_Hillshade'), L('Tarija_UrbanArea')
NB = pr.mapLayersByName('Tarija_Neighbourhoods (outline)')
NB = NB[0] if NB else None
ext = URBAN.extent(); ext.grow(400)
from qgis.core import QgsFillSymbol
URBAN.renderer().setSymbol(QgsFillSymbol.createSimple({'color': '0,0,0,0', 'outline_color': '#000000', 'outline_width': '0.5'}))

IND = [  # layer, title EN, title ES
    ('Tarija_CCInd3_Riverine-Flood', 'CC Indicator 3 - Riverine flood (flow-path HAND)', 'Indicador CC 3 - Inundación fluvial (HAND por flujo)'),
    ('Tarija_CCInd4_Landslide', 'CC Indicator 4 - Landslide (slope susceptibility)', 'Indicador CC 4 - Deslizamientos (susceptibilidad por pendiente)'),
    ('Tarija_CCInd5_Urban-Heat-Island', 'CC Indicator 5 - Urban heat island', 'Indicador CC 5 - Isla de calor urbana'),
    ('Tarija_CCInd6_Wildfire-Interface', 'CC Indicator 6 - Urban-vegetation interface (wildfire)', 'Indicador CC 6 - Interfaz urbano-vegetación (incendios)'),
    ('Tarija_BIOInd1_MSA', 'BIO Indicator 1 - Biodiversity loss (1 - MSA)', 'Indicador BIO 1 - Pérdida de biodiversidad (1 - MSA)'),
    ('Tarija_BIOInd2_Protected-Areas', 'BIO Indicator 2 - Protection weighted by zone type', 'Indicador BIO 2 - Protección ponderada por tipo de zona'),
    ('Tarija_BIOInd3_Natural-Cover-Loss', 'BIO Indicator 3 - Natural cover loss 1985-2024', 'Indicador BIO 3 - Pérdida de cobertura natural 1985-2024'),
    ('Tarija_URBInd1_Population', 'URB Indicator 1 - Population at sensitive ages', 'Indicador URB 1 - Población en edades sensibles'),
    ('Tarija_URBInd3_Urban-Growth', 'URB Indicator 3 - Urban growth weighted by age', 'Indicador URB 3 - Crecimiento urbano ponderado por antigüedad'),
    ('Tarija_URBInd4_Informal-Settlement', 'URB Indicator 4 - Informal settlement (housing proxy)', 'Indicador URB 4 - Asentamientos informales (proxy de vivienda)'),
    ('Tarija_URBInd5_Access-Facilities', 'URB Indicator 5 - Walking access to facilities', 'Indicador URB 5 - Acceso caminable a equipamientos'),
    ('Tarija_Climate_Vulnerability', 'Climate vulnerability (mean of CC indicators)', 'Vulnerabilidad climática (promedio de indicadores CC)'),
    ('Tarija_Biodiversity_Vulnerability', 'Biodiversity vulnerability (mean of BIO indicators)', 'Vulnerabilidad de biodiversidad (promedio de indicadores BIO)'),
    ('Tarija_Urban_Vulnerability', 'Urban vulnerability (mean of URB indicators)', 'Vulnerabilidad urbana (promedio de indicadores URB)'),
    ('Tarija_Combined_Vulnerability', 'Combined MVA vulnerability (mean of 3 dimensions)', 'Vulnerabilidad combinada MVA (promedio de 3 dimensiones)'),
]
HEX = [
    ('Tarija_Hexagon_500m_CC', None, 'Climate vulnerability - 500 m hexagons (guide classes)', 'Vulnerabilidad climática - hexágonos de 500 m (clases de la guía)'),
    ('Tarija_Hexagon_500m_URB', None, 'Urban vulnerability - 500 m hexagons (guide classes)', 'Vulnerabilidad urbana - hexágonos de 500 m (clases de la guía)'),
    ('Tarija_Hexagon_500m_BIO', None, 'Biodiversity vulnerability - 500 m hexagons (guide classes)', 'Vulnerabilidad de biodiversidad - hexágonos de 500 m (clases de la guía)'),
    ('Tarija_Hexagon_500m_Combined', None, 'Combined MVA vulnerability - 500 m hexagons (guide classes)', 'Vulnerabilidad combinada MVA - hexágonos de 500 m (clases de la guía)'),
    ('Tarija_Hexagon_500m_Combined (quintiles)', None, 'Combined MVA vulnerability - 500 m hexagons, quintiles (complementary)', 'Vulnerabilidad combinada MVA - hexágonos de 500 m, quintiles (complementario)'),
]
BIV = [
    ('URB', 'CC', 'Bivariate hotspots - Urban x Climate (guide)', 'Hotspots bivariados - Urbana x Clima (guía)'),
    ('BIO', 'CC', 'Bivariate hotspots - Climate x Biodiversity', 'Hotspots bivariados - Clima x Biodiversidad'),
    ('URB', 'BIO', 'Bivariate hotspots - Urban x Biodiversity', 'Hotspots bivariados - Urbana x Biodiversidad'),
]


def label(lay, text, x, y, w, h, size, bold=False):
    it = QgsLayoutItemLabel(lay); lay.addLayoutItem(it); it.setText(text)
    f = QFont('Arial', size); f.setBold(bold); it.setFont(f)
    it.attemptMove(QgsLayoutPoint(x, y)); it.attemptResize(QgsLayoutSize(w, h)); return it


def new_layout(name, title_en, title_es, layers, legend_layers=None, picture=None, pic_note=None):
    old = lm.layoutByName(name)
    if old: lm.removeLayout(old)
    lay = QgsPrintLayout(pr); lay.initializeDefaults(); lay.setName(name)
    lay.pageCollection().page(0).setPageSize('A4', QgsLayoutItemPage.Landscape)
    label(lay, title_en, 10, 6, 277, 8, 15, True)
    label(lay, title_es, 10, 14, 277, 7, 12)
    m = QgsLayoutItemMap(lay); lay.addLayoutItem(m)
    m.attemptMove(QgsLayoutPoint(10, 23)); m.attemptResize(QgsLayoutSize(185, 165))
    m.setCrs(URBAN.crs()); m.setLayers(layers); m.setKeepLayerSet(True); m.setFrameEnabled(True); m.zoomToExtent(ext)
    if legend_layers:
        lg = QgsLayoutItemLegend(lay); lg.setTitle('Legend / Leyenda'); lg.setLinkedMap(m)
        lg.setAutoUpdateModel(False); root = lg.model().rootGroup(); root.clear()
        for l in legend_layers: root.addLayer(l)
        lg.attemptMove(QgsLayoutPoint(202, 23)); lay.addLayoutItem(lg); lg.adjustBoxSize()
    if picture:
        pc = QgsLayoutItemPicture(lay); lay.addLayoutItem(pc); pc.setPicturePath(picture); pc.attemptMove(QgsLayoutPoint(205, 28))
        pc.attemptResize(QgsLayoutSize(75, 80))
        label(lay, 'Legend / Leyenda', 202, 23, 80, 6, 10, True)
        if pic_note: label(lay, pic_note, 202, 112, 85, 40, 8)
    sb = QgsLayoutItemScaleBar(lay); lay.addLayoutItem(sb); sb.setStyle('Single Box'); sb.setLinkedMap(m); sb.applyDefaultSize()
    sb.setUnits(QgsUnitTypes.DistanceKilometers); sb.setUnitLabel('km'); sb.setNumberOfSegments(2); sb.setUnitsPerSegment(1)
    sb.attemptMove(QgsLayoutPoint(13, 175))
    na = QgsLayoutItemPicture(lay); lay.addLayoutItem(na); na.setPicturePath(':/images/north_arrows/layout_default_north_arrow.svg')
    na.attemptMove(QgsLayoutPoint(182, 26)); na.attemptResize(QgsLayoutSize(10, 12))
    label(lay, CREDIT, 10, 192, 277, 10, 7)
    lm.addLayout(lay); return lay


made = []
base = [l for l in (NB, URBAN, HILL) if l]
for name, te, ts in IND:
    l = L(name)
    made.append(new_layout(name, te, ts, [URBAN, l, HILL], [l]).name())
for name, grp, te, ts in HEX:
    l = L(name)
    made.append(new_layout(name.replace(' (quintiles)', '_Quintiles'), te, ts, [URBAN, l, HILL], [l]).name())
for top, bottom, te, ts in BIV:
    g = f'Bivariate {top} x {bottom}'
    lt, lb = L(f'{top} (Multiply)', g), L(bottom, g)
    names = {'CC': 'Climate / Clima', 'URB': 'Urban / Urbana', 'BIO': 'Biodiversity / Biodiversidad'}
    note = (f'Vertical axis / eje vertical: {names[top]}. Horizontal axis / eje horizontal: {names[bottom]}. '
            'Classes / clases: low 0-0.33, medium 0.33-0.66, high 0.66-1 (hexagon mean, 500 m). '
            'Darkest colour = both dimensions high / color más oscuro = ambas dimensiones altas.')
    made.append(new_layout(f'Tarija_Bivariate_{top}_x_{bottom}', te, ts, [URBAN, lt, lb, HILL], None,
                           LEG.format(f'{top}_x_{bottom}'), note).name())
pr.write(PROJ)
print(len(made), made)
