# Tarija - Phase 1: indicators in the guide structure (guide sections 3-4)

Script: `scripts/tarija/phase1_organize_outputs.py` (run in the QGIS Python console). Log: `MVA/BOL/Tarija/phase1_log.csv`.

**What was done**
- 11 indicators written to `Data_Output/CC|BIO|URB` with the guide naming. All are GeoTIFF Float32, NoData -9999, on the MVA grid (EPSG:32720, 12.5 m, 1,114 x 1,194 cells).
- 10 indicators were copied with **cell values unchanged** (checked cell by cell against the source).
- The urban heat island indicator was moved from its 30 m Landsat grid to the 12.5 m grid with **nearest neighbour** (no interpolation; mean unchanged, 0.503). NaN cells became NoData.
- Base layers in `Data_Output/Base_Layer`: urban area (CRS assigned to EPSG:32720), municipal boundary, 86 neighbourhoods, 21 districts, 6,042 census blocks (GeoPackage) and the hillshade clipped to the grid extent.
- The QGIS metadata (.qmd) and style (.qml) of each source were copied next to each output, with the new name and a history entry.
- Excluded: URBInd2 Land Cover. Not applicable: CCInd1-2 (coastal).

**Result**
| Dim. | Output | Method | Valid cells | Mean |
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

**Note for Phase 2:** coverage differs between indicators (the urban area has 669,265 cells). Population (81%) and housing (67%) only cover populated blocks; MSA (97%) and the heat island (slightly beyond the mask) also differ. The averaging rule for cells where some indicators have no data must be decided before computing dimension vulnerability.
