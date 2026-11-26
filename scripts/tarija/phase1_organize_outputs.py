"""
MVA Tarija - Phase 1: organize validated layers into the guide's Data_Output structure.
MVA Tarija - Fase 1: organizar las capas validadas en la estructura Data_Output de la guía.

Run inside QGIS (Python console):  exec(open(r'<path>/phase1_organize_outputs.py', encoding='utf-8').read())

What it does / Qué hace:
- Base layers (vector): copy to GeoPackage, assign EPSG:32720 where the CRS is undefined.
- Indicators already on the MVA grid: copy cell values unchanged; harmonize to Float32 with NoData = -9999.
- Urban heat island (30 m Landsat grid): resample to the 12.5 m MVA grid with nearest neighbour (no value is
  interpolated); NaN cells become NoData -9999.
- Hillshade: clip to the MVA grid extent (cartographic background only).
- Copy the QGIS metadata (.qmd) and style (.qml) of each source next to the new file, recording the new name.
- Write a log (phase1_log.csv) with source, output, grid and value checks.
"""
import os, csv, shutil, datetime
import numpy as np
from osgeo import gdal, ogr, osr

gdal.UseExceptions()
SRC = r'C:/DATA/Data_inventory_Tarija'  # <- edit: your local folder / editar: su carpeta local
OUT = r'C:/MVA/BOL/Tarija/Data_Output'  # <- edit: your local folder / editar: su carpeta local
CITY = 'Tarija'
EPSG = 32720
GRID = dict(xmin=314925.0, ymin=7610425.0, xmax=328850.0, ymax=7625350.0, res=12.5, ncols=1114, nrows=1194)
NODATA = -9999.0
STAMP = datetime.date.today().isoformat()

CC, BIO, URB = SRC + '/1_CambioClimatico/Rasters/', SRC + '/2_Biodiversidad/Rasters/', SRC + '/3_Urbano/Rasters/'
RASTERS = [  # (dimension folder, new name, source file, method)
    ('CC',  'Tarija_CCInd3_Riverine-Flood',       CC + 'MVA_CC_Ind_AmenazaInundacion_HANDflujo_TAR.tif', 'copy'),
    ('CC',  'Tarija_CCInd4_Landslide',            CC + 'MVA_CC_Ind_SusceptibilidadPendiente_TAR.tif',    'copy'),
    ('CC',  'Tarija_CCInd5_Urban-Heat-Island',    CC + 'MVA_CC_Ind_UHI_Clasificado_0a1_TAR.tif',         'align_nearest'),
    ('CC',  'Tarija_CCInd6_Wildfire-Interface',   CC + 'MVA_CC_Ind_InterfazUrbanoVegetacion_TAR.tif',    'copy'),
    ('BIO', 'Tarija_BIOInd1_MSA',                 BIO + 'MVA_BIO_Ind_PerdidaBiodiversidad_TAR_Aligned.tif', 'copy'),
    ('BIO', 'Tarija_BIOInd2_Protected-Areas',     BIO + 'MVA_BIO_Ind_ProteccionPonderada_TAR.tif',       'copy'),
    ('BIO', 'Tarija_BIOInd3_Natural-Cover-Loss',  BIO + 'MVA_BIO_Ind_PerdidaCoberturaNatural3N_TAR.tif', 'copy'),
    ('URB', 'Tarija_URBInd1_Population',          URB + 'MVA_URB_Ind_DensidadPoblacionSensible_TAR.tif', 'copy'),
    ('URB', 'Tarija_URBInd3_Urban-Growth',        URB + 'MVA_URB_Ind_CrecimientoUrbanoPonderado_TAR.tif', 'copy'),
    ('URB', 'Tarija_URBInd4_Informal-Settlement', URB + 'MVA_URB_Ind_VulnerabilidadHabitacional_TAR_Relleno.tif', 'copy'),
    ('URB', 'Tarija_URBInd5_Access-Facilities',   URB + 'MVA_URB_Ind_AccesoEquipamientosRed_TAR.tif',    'copy'),
    ('Base_Layer', 'Tarija_Hillshade',            SRC + '/4_Referencias/Rasters/Hillshade_Tarija.tif',  'clip_background'),
]
VECTORS = [  # (new name, gpkg, layer, assign_crs)
    ('Tarija_UrbanArea',            SRC + '/3_Urbano/Urbano.gpkg',           'area_urbana_tarija',       True),
    ('Tarija_CityBoundary',         SRC + '/4_Referencias/Referencias.gpkg', 'limite_municipal_cercado', False),
    ('Tarija_Neighbourhoods',       SRC + '/3_Urbano/Urbano.gpkg',           'barrios',                  False),
    ('Tarija_Districts',            SRC + '/3_Urbano/Urbano.gpkg',           'distritos_municipales',    False),
    ('Tarija_CensusBlocks_INE2024', SRC + '/3_Urbano/Urbano.gpkg',           'manzanos_ine_2024',        False),
]
QMD_GPKG = {'area_urbana_tarija': 'Urbano__area_urbana_tarija', 'manzanos_ine_2024': 'Urbano__manzanos_ine_2024'}


def srs():
    s = osr.SpatialReference(); s.ImportFromEPSG(EPSG); return s.ExportToWkt()


def read(path):
    ds = gdal.Open(path); b = ds.GetRasterBand(1)
    a = b.ReadAsArray().astype('float64'); nd = b.GetNoDataValue()
    valid = np.isfinite(a)
    if nd is not None and np.isfinite(nd): valid &= (a != nd)
    if nd is not None and nd < -1e30: valid &= (a > -1e30)
    return ds, a, valid


def on_grid(ds):
    gt = ds.GetGeoTransform()
    return (abs(gt[0] - GRID['xmin']) < 1e-6 and abs(gt[3] - GRID['ymax']) < 1e-6 and abs(gt[1] - GRID['res']) < 1e-9
            and ds.RasterXSize == GRID['ncols'] and ds.RasterYSize == GRID['nrows'])


def write_grid(path, arr, valid, like=None):
    drv = gdal.GetDriverByName('GTiff')
    o = drv.Create(path, GRID['ncols'], GRID['nrows'], 1, gdal.GDT_Float32, options=['COMPRESS=DEFLATE', 'PREDICTOR=2', 'TILED=YES'])
    o.SetGeoTransform((GRID['xmin'], GRID['res'], 0, GRID['ymax'], 0, -GRID['res'])); o.SetProjection(srs())
    out = np.where(valid, arr, NODATA).astype('float32')
    b = o.GetRasterBand(1); b.SetNoDataValue(NODATA); b.WriteArray(out); b.ComputeStatistics(False); o.FlushCache(); o = None


def copy_sidecars(src, dst_noext, new_name, note):
    base = os.path.splitext(src)[0]
    for ext in ('.qml',):
        if os.path.exists(base + ext): shutil.copy2(base + ext, dst_noext + ext)
    q = base + '.qmd'
    if not os.path.exists(q) and base.endswith('_Aligned'): q = base[:-8] + '.qmd'
    if os.path.exists(q): add_history(q, dst_noext + '.qmd', new_name, note)


def add_history(qmd_in, qmd_out, new_name, note):
    s = open(qmd_in, encoding='utf-8').read()
    h = '<history>%s: Phase 1 of the MVA guide workflow - %s Saved as %s.</history>' % (STAMP, note, new_name)
    s = s.replace('<identifier>', '<identifier>', 1)
    s = s.replace('</history>', '</history>\n  ' + h, 1) if '</history>' in s else s.replace('</qgis>', '  ' + h + '\n</qgis>')
    import re
    s = re.sub(r'<identifier>.*?</identifier>', '<identifier>%s</identifier>' % new_name, s, count=1, flags=re.S)
    open(qmd_out, 'w', encoding='utf-8').write(s)


log = []
for dim, name, src, method in RASTERS:
    dst = os.path.join(OUT, dim, name + '.tif')
    ds, a, valid = read(src)
    if method == 'copy':
        assert on_grid(ds), 'not on MVA grid: ' + src
        write_grid(dst, a, valid)
        note = 'cell values copied unchanged from %s (Float32, NoData -9999).' % os.path.basename(src)
    elif method == 'align_nearest':
        tmp = gdal.Warp('/vsimem/uhi.tif', ds, dstSRS='EPSG:%d' % EPSG, outputBounds=(GRID['xmin'], GRID['ymin'], GRID['xmax'], GRID['ymax']),
                        xRes=GRID['res'], yRes=GRID['res'], resampleAlg='near', srcNodata='nan', dstNodata=NODATA, outputType=gdal.GDT_Float32)
        tmp = None
        ds2, a2, v2 = read('/vsimem/uhi.tif'); v2 &= (a2 != NODATA)
        write_grid(dst, a2, v2); ds2 = None; gdal.Unlink('/vsimem/uhi.tif')
        note = 'resampled from the 30 m Landsat grid to the 12.5 m MVA grid with nearest neighbour (no interpolation); NaN set to NoData -9999.'
    elif method == 'clip_background':
        gdal.Translate(dst, ds, projWin=[GRID['xmin'], GRID['ymax'], GRID['xmax'], GRID['ymin']], creationOptions=['COMPRESS=DEFLATE'])
        note = 'clipped to the MVA grid extent without resampling (cartographic background).'
    ds = None
    copy_sidecars(src, os.path.splitext(dst)[0], name, note)
    # checks
    ds_o, ao, vo = read(dst)
    _, asrc, vsrc = read(src)
    same = ''
    if method == 'copy':
        same = bool(np.array_equal(vo, vsrc) and np.allclose(ao[vo], asrc[vsrc].astype('float32')))
    log.append(dict(dimension=dim, output=name + '.tif', source=os.path.relpath(src, SRC), method=method, on_mva_grid=on_grid(ds_o),
                    nodata=ds_o.GetRasterBand(1).GetNoDataValue(), valid_cells=int(vo.sum()),
                    min=round(float(ao[vo].min()), 4), max=round(float(ao[vo].max()), 4), mean=round(float(ao[vo].mean()), 4),
                    identical_to_source=same))
    ds_o = None

for name, gpkg, lyr, assign in VECTORS:
    dst = os.path.join(OUT, 'Base_Layer', name + '.gpkg')
    if os.path.exists(dst): gdal.GetDriverByName('GPKG').Delete(dst)
    opts = dict(format='GPKG', layerName=name, layers=[lyr])
    if assign: opts['dstSRS'] = 'EPSG:%d' % EPSG; opts['srcSRS'] = 'EPSG:%d' % EPSG
    gdal.VectorTranslate(dst, gpkg, **opts)
    q = os.path.join(os.path.dirname(gpkg), 'metadata', QMD_GPKG.get(lyr, '') + '.qmd')
    if lyr in QMD_GPKG and os.path.exists(q):
        add_history(q, os.path.splitext(dst)[0] + '.qmd', name, 'copied from %s|%s%s.' % (os.path.basename(gpkg), lyr, ' with CRS assigned to EPSG:32720' if assign else ''))
    v = ogr.Open(dst); L = v.GetLayer(0); sr = L.GetSpatialRef()
    try:
        sr.AutoIdentifyEPSG()
    except Exception:
        pass
    log.append(dict(dimension='Base_Layer', output=name + '.gpkg', source=os.path.relpath(gpkg, SRC) + '|' + lyr, method='copy' + ('+assign_crs' if assign else ''),
                    on_mva_grid='', nodata='', valid_cells=L.GetFeatureCount(), min='', max='', mean='',
                    identical_to_source='CRS ' + (sr.GetAuthorityName(None) or '') + ':' + (sr.GetAuthorityCode(None) or '') if sr else 'no CRS'))
    v = None

with open(os.path.join(OUT, '..', 'phase1_log.csv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=list(log[0].keys())); w.writeheader(); w.writerows(log)
for r in log: print(r)
