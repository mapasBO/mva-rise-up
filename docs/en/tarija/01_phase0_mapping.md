# Tarija - Phase 0: mapping of existing layers to the guide

CRS EPSG:32720, MVA grid 12.5 m (1,114 x 1,194 cells, origin 314925 E / 7625350 N). Folder root: `MVA/BOL/Tarija`. Existing layers were already computed and validated; Phase 1 copies and renames them following the guide's naming convention `City_DimIndN_Name`.

| Stage | Dim. | Guide § | New name | Current source | Action | Phase | Notes |
|---|---|---|---|---|---|---|---|
| Data_Output | Base_Layer | 3 / 5 | Tarija_UrbanArea.gpkg | Data_inventory_Tarija/3_Urbano/Urbano.gpkg\|area_urbana_tarija | Copy + assign EPSG:32720 | 1 | Analysis mask (~10,457 ha). CRS currently undefined in QGIS. |
| Data_Output | Base_Layer | 3 | Tarija_CityBoundary.gpkg | Data_inventory_Tarija/4_Referencias/Referencias.gpkg\|limite_municipal_cercado | Copy | 1 | Cercado municipality boundary. |
| Data_Output | Base_Layer | 5 | Tarija_Neighbourhoods.gpkg | Data_inventory_Tarija/3_Urbano/Urbano.gpkg\|barrios | Copy | 1 | 86 barrios; second aggregation unit besides hexagons. |
| Data_Output | Base_Layer | 5 | Tarija_Districts.gpkg | Data_inventory_Tarija/3_Urbano/Urbano.gpkg\|distritos_municipales | Copy | 1 | 21 municipal districts. |
| Data_Output | Base_Layer | 2.5 | Tarija_CensusBlocks_INE2024.gpkg | Data_inventory_Tarija/3_Urbano/Urbano.gpkg\|manzanos_ine_2024 | Copy | 1 | 6,042 census blocks, INE 2024. |
| Data_Output | Base_Layer | - | Tarija_Hillshade.tif | Data_inventory_Tarija/4_Referencias/Rasters/Hillshade_Tarija.tif | Copy (clip to MVA grid) | 1 | 12.5 m. |
| Data_Output | Base_Layer | 5.2 | Tarija_Hexagon_500m.gpkg | (to be created) | Create | 3 | 500 m hexagon grid over the urban area. |
| Data_Output | CC | 4.2.1 | Tarija_CCInd1_Coastal-Erosion | - | Not applicable | - | Inland city: no coast. |
| Data_Output | CC | 4.2.2 | Tarija_CCInd2_Coastal-Inundation | - | Not applicable | - | Inland city: no coast. |
| Data_Output | CC | 4.2.3 | Tarija_CCInd3_Riverine-Flood.tif | Data_inventory_Tarija/1_CambioClimatico/Rasters/MVA_CC_Ind_AmenazaInundacion_HANDflujo_TAR.tif | Copy + rename | 1 | Flow-path HAND, 12.5 m. Replaces the VIDECI V_AIn layer (slope only). |
| Data_Output | CC | 4.2.4 | Tarija_CCInd4_Landslide.tif | Data_inventory_Tarija/1_CambioClimatico/Rasters/MVA_CC_Ind_SusceptibilidadPendiente_TAR.tif | Copy + rename | 1 | Slope susceptibility (share package: MVA_CC_Ind_SlopeSusceptibility_TAR), 12.5 m, normalized p5-p95 of urban slope (0.59-11.56 deg). The composite version is not used. |
| Data_Output | CC | ext. | Tarija_CCInd5_Urban-Heat-Island.tif | Data_inventory_Tarija/1_CambioClimatico/Rasters/MVA_CC_Ind_UHI_Clasificado_0a1_TAR.tif | Copy + align to MVA grid (nearest) + set NoData | 1 | 30 m Landsat grid, offset 15 m from MVA grid; NaN without NoData. |
| Data_Output | CC | ext. | Tarija_CCInd6_Wildfire-Interface.tif | Data_inventory_Tarija/1_CambioClimatico/Rasters/MVA_CC_Ind_InterfazUrbanoVegetacion_TAR.tif | Copy + rename | 1 | 12.5 m. |
| Data_Output | CC | 4.5.1 | Tarija_Climate_Vulnerability.tif | (to be computed) | Compute (mean of CC indicators) | 2 |  |
| Data_Output | BIO | 4.3.1 | Tarija_BIOInd1_MSA.tif | Data_inventory_Tarija/2_Biodiversidad/Rasters/MVA_BIO_Ind_PerdidaBiodiversidad_TAR_Aligned.tif | Copy + rename | 1 | 1 - MSA (GLOBIO4 2015), already aligned to 12.5 m (native ~300 m). |
| Data_Output | BIO | 2.4.2 | Tarija_BIOInd2_Protected-Areas.tif | Data_inventory_Tarija/2_Biodiversidad/Rasters/MVA_BIO_Ind_ProteccionPonderada_TAR.tif | Copy + rename | 1 | Weighted by PMOT zone type (local data instead of Protected Planet). |
| Data_Output | BIO | ext. | Tarija_BIOInd3_Natural-Cover-Loss.tif | Data_inventory_Tarija/2_Biodiversidad/Rasters/MVA_BIO_Ind_PerdidaCoberturaNatural3N_TAR.tif | Copy + rename | 1 | Three levels 0 / 0.5 / 1, MapBiomas 1985-2024. |
| Data_Output | BIO | 4.5.2 | Tarija_Biodiversity_Vulnerability.tif | Data_inventory_Tarija/2_Biodiversidad/Rasters/MVA_BIO_Vulnerabilidad_v2_TAR.tif (to verify) | Recompute (mean of BIO indicators) | 2 | Existing v2 will be checked against the final indicator set. |
| Data_Output | URB | 4.4.1 | Tarija_URBInd1_Population.tif | Data_inventory_Tarija/3_Urbano/Rasters/MVA_URB_Ind_DensidadPoblacionSensible_TAR.tif | Copy + rename | 1 | Density of sensitive ages (0-19, 60+), INE 2024. |
| Data_Output | URB | 4.4.2 | Tarija_URBInd2_Land-Cover.tif | (missing) - former Data_inventory_Tarija/3_Urbano/Rasters/URBInd_CoberturaSuelo_Tarija.tif | Excluded (team decision 2026-11-25) | - | Left out of the Tarija MVA (former layer in EPSG:4326, 30 m, weights never confirmed). |
| Data_Output | URB | 4.4.3 | Tarija_URBInd3_Urban-Growth.tif | Data_inventory_Tarija/3_Urbano/Rasters/MVA_URB_Ind_CrecimientoUrbanoPonderado_TAR.tif | Copy + rename | 1 | Weighted by age of urbanization 1985-2024. |
| Data_Output | URB | 4.4.4 | Tarija_URBInd4_Informal-Settlement.tif | Data_inventory_Tarija/3_Urbano/Rasters/MVA_URB_Ind_VulnerabilidadHabitacional_TAR_Relleno.tif | Copy + rename | 1 | Proxy: 4 of 5 SDG 11.1.1 criteria; official GAMT layer still pending. |
| Data_Output | URB | ext. | Tarija_URBInd5_Access-Facilities.tif | Data_inventory_Tarija/3_Urbano/Rasters/MVA_URB_Ind_AccesoEquipamientosRed_TAR.tif | Copy + rename | 1 | Walking time by network (OSM). |
| Data_Output | URB | 4.5.3 | Tarija_Urban_Vulnerability.tif | (to be computed) | Compute (mean of URB indicators) | 2 |  |
| Data_Output | Combined | 4.5.4 | Tarija_Combined_Vulnerability.tif | (to be computed) | Compute (mean of 3 dimensions) | 2 |  |
| Data_Output | Combined | 5.3 / 5.4 | Tarija_Hexagon_500m_CC / _BIO / _URB / _Combined.gpkg | (to be computed) | Zonal statistics + choropleth + bivariate | 3 | Also aggregated by barrio. |
| Process | CC | 4.2 | (reference only) | Data_inventory_Tarija/1_CambioClimatico/Rasters/CC_HANDflujo_Principal_m_TAR.tif, CC_Aux_SuscQuebradas_TAR.tif, CC_Aux_SuscSueloDesnudo_TAR.tif, MVA_CC_Ind_FrecuenciaIncendios_TAR.tif | Keep in place; listed in Process/README | - | Not duplicated to avoid copies drifting apart. |
| Process | URB | 4.4 | (reference only) | Data_inventory_Tarija/3_Urbano/Rasters/URB_Aux_Friccion_Caminata_TAR.tif, URB_Aux_TiempoCaminata_*_min_TAR.tif, MVA_URB_Ind_VulnerabilidadHabitacional_TAR.tif (+_Origen) | Keep in place; listed in Process/README | - |  |
| Process | BIO | 4.3 | (reference only) | Data_inventory_Tarija/2_Biodiversidad/Rasters/LULC_Transicion_Natural_1985_2024_TAR.tif | Keep in place; listed in Process/README | - |  |
| Data_Input | All | 2 | (reference only) | Data_inventory_Tarija (all source data: DEM, MapBiomas, MSA, MapBiomas Fire, INE 2024, GAM facilities, OSM, VIDECI) | Keep in place; listed in Data_Input/README | - | See DATA_INVENTORY_Tarija_2026_EN.xlsx. |
