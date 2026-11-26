# Overview and deviations from the guide

## Phases

| Phase | Guide sections | Output |
|---|---|---|
| 0 Setup | Folder hierarchy and naming | Folders, mapping table, repository skeleton |
| 1 Indicators | 2, 3, 4.2-4.4 | Indicators renamed/completed in Data_Output |
| 2 Vulnerability | 4.5 | Dimension and combined vulnerability |
| 3 Hotspots | 5 | 500 m hexagons (and barrios), choropleths, three bivariate maps, 24 map layouts |
| 4 Documentation | - | This repository (EN/ES) |

## Deviations from the guide (Tarija)

| Topic | Guide | This application | Reason |
|---|---|---|---|
| CRS | WGS 84 / Pseudo-Mercator (EPSG:3857) | Tarija: WGS 84 / UTM 20S (EPSG:32720) | Web Mercator inflates distances ~7-8% at 21.5 S; UTM keeps true cell size, areas and zonal statistics |
| Cell size | 10 m | 12.5 m | Native resolution of the project DEM (ALOS PALSAR RTC); finer inputs are not aggregated, coarser ones are only oversampled (nearest neighbour) |
| Vector format | Shapefile | GeoPackage | Long field names, UTF-8, one file per product |
| Normalization | Min-max | Min-max on the 5th-95th percentile range where outliers dominate (documented per indicator) | Avoids a few extreme cells compressing the scale |
| Indicator numbering | CCInd1-4, BIOInd1, URBInd1-4 | Guide numbers kept (CCInd1-2 coastal = not applicable in Tarija); extensions numbered after them (CCInd5-6, BIOInd3, URBInd5) | Same numbering in both cities for comparison |
| Data_Input / Process | Copies of raw and intermediate data | README pointers to the existing data inventory | Avoid duplicating GB of data and copies drifting apart |
| Protected areas | Protected Planet | Municipal PMOT protection zones, weighted by type | No national protected area inside the urban area |
| Informal settlements | Official dataset | Proxy from 2024 census housing deprivation (4 of 5 SDG 11.1.1 criteria) until the municipal dataset is received | Official layer pending from GAM Tarija |
| Landslide indicator | CCInd4 Landslide (susceptibility data) | Slope susceptibility only, normalized p5-p95 of urban slope | Team decision (2026-11-25); the composite version (streams + bare soil) is not used |
| Excluded guide indicator | URBInd2 Land Cover | Not included in Tarija | Team decision (2026-11-25): former land-cover layer is in EPSG:4326 with unconfirmed weights |
| Climate aggregation | Simple mean of indicators | Simple mean, as in the guide (team decision 2026-11-25) | Multi-hazard maximum, removing indicators and weights were tested and rejected to keep the method and comparability with other cities applying the guide |
| Hexagon grid extent | City boundary | Urban area; only hexagons intersecting it | Tarija's boundary is the whole municipality |
| Bivariate maps | Urban x Climate | Also Climate x Biodiversity and Urban x Biodiversity (BIO ramp #e8e8e8/#c3b3d8/#9972af) | Show the three dimension overlaps the MVA aims to identify |
| Combined hexagon map | Not mapped | Complementary map with quintile classes | Guide classes put 540 of 550 hexagons in one class |
| Combined map classes | Fixed 0.2 (raster) / not mapped (hexagons) | Mean ± 0.5 and ± 1.5 SD (complementary style; guide style kept) | Fixed classes leave the combined index in one or two classes |
