"""
MVA Tarija - Phase 3: hexagon aggregation, choropleths and bivariate hotspot maps (guide section 5).
MVA Tarija - Fase 3: agregación en hexágonos, coropletas y mapas bivariados de hotspots (sección 5 de la guía).

Run inside QGIS (Python console):  exec(open(r'<path>/phase3_hotspots.py', encoding='utf-8').read())

Guide steps reproduced / pasos de la guía:
- 5.2 Hexagon grid, horizontal and vertical spacing 500 m; zonal statistics (mean) of each dimension.
- 5.3 Choropleth per dimension: 3 equal-interval classes 0-0.33 / 0.33-0.66 / 0.66-max, white outline, guide colours.
- 5.4 Bivariate map: top layer with blending mode Multiply over the bottom layer, plus a 3x3 legend.
Additions / agregados (documented):
- Grid extent from the urban area (the guide uses the city boundary; in Tarija that is the whole municipality) and only
  hexagons that intersect the urban area are kept.
- Three bivariate pairs instead of one: Urban x Climate (guide), Climate x Biodiversity and Urban x Biodiversity.
  Biodiversity colour ramp (not in the guide): #e8e8e8 / #c3b3d8 / #9972af.
- Hexagon layer for the combined vulnerability and a neighbourhood (barrio) aggregation of all dimensions.
"""
import os, csv
import processing
from qgis.core import (QgsProject, QgsVectorLayer, QgsRasterLayer, QgsGraduatedSymbolRenderer, QgsRendererRange,
                       QgsFillSymbol, QgsCoordinateReferenceSystem, QgsLayerTreeLayer)
from qgis.PyQt.QtGui import QColor, QImage, QPainter, QFont, QPen
from qgis.PyQt.QtCore import Qt, QRectF

ROOT = r'C:/MVA/BOL/Tarija'  # <- edit: your local folder / editar: su carpeta local
OUT = ROOT + '/Data_Output'
PROJ = ROOT + '/MVA_Tarija.qgz'
CRS = 'EPSG:32720'
DIMS = {  # key: (raster, field prefix, colours low/mid/high, label EN, label ES)
    'CC':  (OUT + '/CC/Tarija_Climate_Vulnerability.tif',       'CC_',   ['#e8e8e8', '#aec3bc', '#749f91'], 'Climate', 'Clima'),
    'URB': (OUT + '/URB/Tarija_Urban_Vulnerability.tif',        'URB_',  ['#e8e8e8', '#eeaeae', '#f47474'], 'Urban', 'Urbana'),
    'BIO': (OUT + '/BIO/Tarija_Biodiversity_Vulnerability.tif', 'BIO_',  ['#e8e8e8', '#c3b3d8', '#9972af'], 'Biodiversity', 'Biodiversidad'),
    'Combined': (OUT + '/Combined/Tarija_Combined_Vulnerability.tif', 'COMB_', ['#e8e8e8', '#bdbdbd', '#636363'], 'Combined', 'Combinada'),
}
BREAKS = [(0.0, 0.33), (0.33, 0.66), (0.66, 1.0)]
PAIRS = [('URB', 'CC'), ('BIO', 'CC'), ('URB', 'BIO')]  # (top, bottom) as in guide 5.4.1 (URB on top of CC)


def nv(x):
    if x is None: return None
    try:
        if hasattr(x, 'isNull') and x.isNull(): return None
        return float(x)
    except Exception:
        return None


def cls(v):
    if v is None: return None
    return 1 if v < 0.33 else (2 if v < 0.66 else 3)


def rm(path):
    import time
    for ext in ('', '-wal', '-shm', '.qml'):
        q = path + ext if ext != '.qml' else os.path.splitext(path)[0] + '.qml'
        for _ in range(5):
            try:
                if os.path.exists(q): os.remove(q)
                break
            except PermissionError:
                time.sleep(1)


for _p in [OUT + '/Base_Layer/Tarija_Hexagon_500m.gpkg', OUT + '/Combined/Tarija_Neighbourhoods_MVA.gpkg'] + \
          [OUT + f'/Combined/Tarija_Hexagon_500m_{k}.gpkg' for k in DIMS]:
    rm(_p)

# ---- 5.2 hexagon grid --------------------------------------------------------------------------------------
urban = QgsVectorLayer(OUT + '/Base_Layer/Tarija_UrbanArea.gpkg', 'urban', 'ogr')
grid = processing.run('native:creategrid', {'TYPE': 4, 'EXTENT': urban.extent(), 'HSPACING': 500, 'VSPACING': 500,
                                             'HOVERLAY': 0, 'VOVERLAY': 0, 'CRS': QgsCoordinateReferenceSystem(CRS),
                                             'OUTPUT': 'TEMPORARY_OUTPUT'})['OUTPUT']
hexp = OUT + '/Base_Layer/Tarija_Hexagon_500m.gpkg'
processing.run('native:extractbylocation', {'INPUT': grid, 'PREDICATE': [0], 'INTERSECT': urban, 'OUTPUT': hexp})

# ---- zonal statistics per dimension -------------------------------------------------------------------------
out_layers, log = {}, []
for k, (ras, pre, cols, en, es) in DIMS.items():
    p = OUT + f'/Combined/Tarija_Hexagon_500m_{k}.gpkg'
    processing.run('native:zonalstatisticsfb', {'INPUT': hexp, 'INPUT_RASTER': ras, 'RASTER_BAND': 1, 'COLUMN_PREFIX': pre,
                                               'STATISTICS': [0, 2], 'OUTPUT': p})
    out_layers[k] = p

# neighbourhood aggregation (extension)
nb = OUT + '/Base_Layer/Tarija_Neighbourhoods.gpkg'
cur = nb
for k, (ras, pre, cols, en, es) in DIMS.items():
    tmp = processing.run('native:zonalstatisticsfb', {'INPUT': cur, 'INPUT_RASTER': ras, 'RASTER_BAND': 1, 'COLUMN_PREFIX': pre,
                                                     'STATISTICS': [2], 'OUTPUT': 'TEMPORARY_OUTPUT'})['OUTPUT']
    cur = tmp
nbp = OUT + '/Combined/Tarija_Neighbourhoods_MVA.gpkg'
processing.run('native:savefeatures', {'INPUT': cur, 'OUTPUT': nbp})


# ---- 5.3 choropleth styles --------------------------------------------------------------------------------
def choropleth(layer, field, cols, label_es, blend=False):
    rngs = []
    vals = [nv(f[field]) for f in layer.getFeatures() if nv(f[field]) is not None]
    top = max(max(vals), 0.66) if vals else 1.0
    for (lo, hi), c, lab in zip(BREAKS, cols, ['Low / Baja', 'Medium / Media', 'High / Alta']):
        sym = QgsFillSymbol.createSimple({'color': c, 'outline_color': '#ffffff', 'outline_width': '0.26'})
        rngs.append(QgsRendererRange(lo, top if hi == 1.0 else hi, sym, f'{lab} ({lo:.2f}-{(top if hi == 1.0 else hi):.2f})'))
    r = QgsGraduatedSymbolRenderer(field, rngs); r.setClassAttribute(field)
    layer.setRenderer(r)
    if blend:
        from qgis.PyQt.QtGui import QPainter as QP
        layer.setBlendMode(QP.CompositionMode_Multiply)
    return layer


for k, p in out_layers.items():
    pre, cols = DIMS[k][1], DIMS[k][2]
    l = QgsVectorLayer(p, f'Tarija_Hexagon_500m_{k}', 'ogr')
    choropleth(l, pre + 'mean', cols, DIMS[k][4]); l.saveNamedStyle(os.path.splitext(p)[0] + '.qml')
    vals = [nv(f[pre + 'mean']) for f in l.getFeatures()]
    n = len(vals); c = [sum(1 for v in vals if cls(v) == i) for i in (1, 2, 3)]; nn = sum(1 for v in vals if v is None)
    log.append(dict(layer=f'Tarija_Hexagon_500m_{k}', hexagons=n, no_data=nn, low_0_033=c[0], medium_033_066=c[1], high_066_max=c[2],
                    mean=round(sum(v for v in vals if v is not None) / max(n - nn, 1), 3)))


# ---- 5.4 bivariate: crosstabs and legends -------------------------------------------------------------------
def mult(c1, c2):
    a, b = QColor(c1), QColor(c2)
    return QColor(a.red() * b.red() // 255, a.green() * b.green() // 255, a.blue() * b.blue() // 255)


def legend_png(top, bottom, path):
    s, m = 60, 70
    img = QImage(m + 3 * s + 20, m + 3 * s + 40, QImage.Format_ARGB32); img.fill(QColor('white'))
    p = QPainter(img); p.setFont(QFont('Arial', 8))
    for i in range(3):          # bottom layer -> x
        for j in range(3):      # top layer -> y
            p.fillRect(QRectF(m + i * s, 10 + (2 - j) * s, s, s), mult(DIMS[top][2][j], DIMS[bottom][2][i]))
    p.setPen(QPen(QColor('black')))
    p.drawText(QRectF(m, 10 + 3 * s + 4, 3 * s, 16), Qt.AlignCenter, f'{DIMS[bottom][3]} / {DIMS[bottom][4]}  ->')
    p.save(); p.translate(14, 10 + 3 * s); p.rotate(-90)
    p.drawText(QRectF(0, 0, 3 * s, 16), Qt.AlignCenter, f'{DIMS[top][3]} / {DIMS[top][4]}  ->'); p.restore()
    p.end(); img.save(path)


feats = {k: {f['id']: nv(f[DIMS[k][1] + 'mean']) for f in QgsVectorLayer(p, k, 'ogr').getFeatures()} for k, p in out_layers.items()}
cross_log = []
for top, bottom in PAIRS:
    legend_png(top, bottom, OUT + f'/Combined/Tarija_Bivariate_Legend_{top}_x_{bottom}.png')
    ct = {(i, j): 0 for i in (1, 2, 3) for j in (1, 2, 3)}
    for hid, vt in feats[top].items():
        vb = feats[bottom].get(hid)
        if vt is None or vb is None: continue
        ct[(cls(vt), cls(vb))] += 1
    cross_log.append(dict(pair=f'{top} (top/y) x {bottom} (bottom/x)', **{f'{top}{i}_{bottom}{j}': ct[(i, j)] for i in (1, 2, 3) for j in (1, 2, 3)}))

# ---- project: add layers and groups to MVA_Tarija.qgz -------------------------------------------------------
pr = QgsProject(); pr.read(PROJ)
root = pr.layerTreeRoot()
old = root.findGroup('Phase 3 - Hotspots (guide section 5)')
if old: root.removeChildNode(old)
g = root.insertGroup(0, 'Phase 3 - Hotspots (guide section 5)')
gc = g.addGroup('Choropleths (3 classes)')
for k in ('CC', 'URB', 'BIO', 'Combined'):
    l = QgsVectorLayer(out_layers[k], f'Tarija_Hexagon_500m_{k}', 'ogr'); l.loadNamedStyle(os.path.splitext(out_layers[k])[0] + '.qml')
    pr.addMapLayer(l, False); gc.addLayer(l).setItemVisibilityChecked(False)
for top, bottom in PAIRS:
    gb = g.addGroup(f'Bivariate {top} x {bottom}')
    lt = QgsVectorLayer(out_layers[top], f'{top} (Multiply)', 'ogr'); choropleth(lt, DIMS[top][1] + 'mean', DIMS[top][2], '', blend=True)
    lb = QgsVectorLayer(out_layers[bottom], f'{bottom}', 'ogr'); choropleth(lb, DIMS[bottom][1] + 'mean', DIMS[bottom][2], '')
    pr.addMapLayer(lt, False); pr.addMapLayer(lb, False)
    gb.addLayer(lt); gb.addLayer(lb)
    gb.setItemVisibilityChecked((top, bottom) == ('URB', 'CC')); gb.setExpanded(False)
nl = QgsVectorLayer(nbp, 'Tarija_Neighbourhoods_MVA', 'ogr'); pr.addMapLayer(nl, False)
gn = g.addGroup('Neighbourhoods (extension)'); gn.addLayer(nl).setItemVisibilityChecked(False)
old2 = root.findGroup('MVA Tarija - Results (Phase 1-2)')
if old2: old2.setItemVisibilityChecked(False)
pr.write(PROJ)

with open(ROOT + '/phase3_log.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(list(log[0].keys())); [w.writerow(list(r.values())) for r in log]
    w.writerow([]); w.writerow(list(cross_log[0].keys())[:1] + ['3x3 crosstab: top class (1 low,2 med,3 high) x bottom class'])
    for r in cross_log: w.writerow([f'{k}={v}' for k, v in r.items()])
print('hexagons:', QgsVectorLayer(hexp, 'h', 'ogr').featureCount())
for r in log: print(r)
for r in cross_log: print(r)
