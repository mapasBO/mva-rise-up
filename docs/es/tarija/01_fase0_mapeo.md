# Tarija - Fase 0: correspondencia de capas existentes con la guía

CRS EPSG:32720, grilla del MVA de 12.5 m (1,114 x 1,194 celdas, origen 314925 E / 7625350 N). Carpeta raíz: `MVA/BOL/Tarija`. Las capas existentes ya están calculadas y validadas; en la Fase 1 se copian y renombran según la convención de la guía `Ciudad_DimIndN_Nombre`.

| Etapa | Dim. | § Guía | Nombre nuevo | Fuente actual | Acción | Fase | Notas |
|---|---|---|---|---|---|---|---|
| Data_Output | Base_Layer | 3 / 5 | Tarija_UrbanArea.gpkg | Data_inventory_Tarija/3_Urbano/Urbano.gpkg\|area_urbana_tarija | Copy + assign EPSG:32720 | 1 | Máscara de análisis (~10,457 ha). Hoy QGIS lee el CRS como indefinido. |
| Data_Output | Base_Layer | 3 | Tarija_CityBoundary.gpkg | Data_inventory_Tarija/4_Referencias/Referencias.gpkg\|limite_municipal_cercado | Copy | 1 | Límite del municipio de Cercado. |
| Data_Output | Base_Layer | 5 | Tarija_Neighbourhoods.gpkg | Data_inventory_Tarija/3_Urbano/Urbano.gpkg\|barrios | Copy | 1 | 86 barrios; segunda unidad de agregación además de los hexágonos. |
| Data_Output | Base_Layer | 5 | Tarija_Districts.gpkg | Data_inventory_Tarija/3_Urbano/Urbano.gpkg\|distritos_municipales | Copy | 1 | 21 distritos municipales. |
| Data_Output | Base_Layer | 2.5 | Tarija_CensusBlocks_INE2024.gpkg | Data_inventory_Tarija/3_Urbano/Urbano.gpkg\|manzanos_ine_2024 | Copy | 1 | 6,042 manzanos, INE 2024. |
| Data_Output | Base_Layer | - | Tarija_Hillshade.tif | Data_inventory_Tarija/4_Referencias/Rasters/Hillshade_Tarija.tif | Copy (clip to MVA grid) | 1 | 12.5 m. |
| Data_Output | Base_Layer | 5.2 | Tarija_Hexagon_500m.gpkg | (to be created) | Create | 3 | Grilla de hexágonos de 500 m sobre el área urbana. |
| Data_Output | CC | 4.2.1 | Tarija_CCInd1_Coastal-Erosion | - | Not applicable | - | Ciudad sin costa. |
| Data_Output | CC | 4.2.2 | Tarija_CCInd2_Coastal-Inundation | - | Not applicable | - | Ciudad sin costa. |
| Data_Output | CC | 4.2.3 | Tarija_CCInd3_Riverine-Flood.tif | Data_inventory_Tarija/1_CambioClimatico/Rasters/MVA_CC_Ind_AmenazaInundacion_HANDflujo_TAR.tif | Copy + rename | 1 | HAND por flujo, 12.5 m. Reemplaza la capa V_AIn del VIDECI (solo pendiente). |
| Data_Output | CC | 4.2.4 | Tarija_CCInd4_Landslide.tif | Data_inventory_Tarija/1_CambioClimatico/Rasters/MVA_CC_Ind_SusceptibilidadPendiente_TAR.tif | Copy + rename | 1 | Susceptibilidad por pendiente (paquete compartido: MVA_CC_Ind_SlopeSusceptibility_TAR), 12.5 m, normalizada entre p5 y p95 de la pendiente urbana (0.59-11.56°). No se usa la versión compuesta. |
| Data_Output | CC | ext. | Tarija_CCInd5_Urban-Heat-Island.tif | Data_inventory_Tarija/1_CambioClimatico/Rasters/MVA_CC_Ind_UHI_Clasificado_0a1_TAR.tif | Copy + align to MVA grid (nearest) + set NoData | 1 | Grilla Landsat de 30 m, desfasada 15 m; NaN sin NoData definido. |
| Data_Output | CC | ext. | Tarija_CCInd6_Wildfire-Interface.tif | Data_inventory_Tarija/1_CambioClimatico/Rasters/MVA_CC_Ind_InterfazUrbanoVegetacion_TAR.tif | Copy + rename | 1 | 12.5 m. |
| Data_Output | CC | 4.5.1 | Tarija_Climate_Vulnerability.tif | (to be computed) | Compute (mean of CC indicators) | 2 |  |
| Data_Output | BIO | 4.3.1 | Tarija_BIOInd1_MSA.tif | Data_inventory_Tarija/2_Biodiversidad/Rasters/MVA_BIO_Ind_PerdidaBiodiversidad_TAR_Aligned.tif | Copy + rename | 1 | 1 - MSA (GLOBIO4 2015), ya alineado a 12.5 m (nativo ~300 m). |
| Data_Output | BIO | 2.4.2 | Tarija_BIOInd2_Protected-Areas.tif | Data_inventory_Tarija/2_Biodiversidad/Rasters/MVA_BIO_Ind_ProteccionPonderada_TAR.tif | Copy + rename | 1 | Ponderado por tipo de zona del PMOT (dato local en vez de Protected Planet). |
| Data_Output | BIO | ext. | Tarija_BIOInd3_Natural-Cover-Loss.tif | Data_inventory_Tarija/2_Biodiversidad/Rasters/MVA_BIO_Ind_PerdidaCoberturaNatural3N_TAR.tif | Copy + rename | 1 | Tres niveles 0 / 0.5 / 1, MapBiomas 1985-2024. |
| Data_Output | BIO | 4.5.2 | Tarija_Biodiversity_Vulnerability.tif | Data_inventory_Tarija/2_Biodiversidad/Rasters/MVA_BIO_Vulnerabilidad_v2_TAR.tif (to verify) | Recompute (mean of BIO indicators) | 2 | El v2 existente se verificará contra el set final de indicadores. |
| Data_Output | URB | 4.4.1 | Tarija_URBInd1_Population.tif | Data_inventory_Tarija/3_Urbano/Rasters/MVA_URB_Ind_DensidadPoblacionSensible_TAR.tif | Copy + rename | 1 | Densidad de edades sensibles (0-19, 60+), INE 2024. |
| Data_Output | URB | 4.4.2 | Tarija_URBInd2_Land-Cover.tif | (missing) - former Data_inventory_Tarija/3_Urbano/Rasters/URBInd_CoberturaSuelo_Tarija.tif | Excluded (team decision 2026-11-25) | - | Se deja fuera del MVA de Tarija (la capa anterior está en EPSG:4326, 30 m, con pesos nunca confirmados). |
| Data_Output | URB | 4.4.3 | Tarija_URBInd3_Urban-Growth.tif | Data_inventory_Tarija/3_Urbano/Rasters/MVA_URB_Ind_CrecimientoUrbanoPonderado_TAR.tif | Copy + rename | 1 | Ponderado por antigüedad de urbanización 1985-2024. |
| Data_Output | URB | 4.4.4 | Tarija_URBInd4_Informal-Settlement.tif | Data_inventory_Tarija/3_Urbano/Rasters/MVA_URB_Ind_VulnerabilidadHabitacional_TAR_Relleno.tif | Copy + rename | 1 | Proxy: 4 de 5 criterios ODS 11.1.1; capa oficial del GAMT pendiente. |
| Data_Output | URB | ext. | Tarija_URBInd5_Access-Facilities.tif | Data_inventory_Tarija/3_Urbano/Rasters/MVA_URB_Ind_AccesoEquipamientosRed_TAR.tif | Copy + rename | 1 | Tiempo de caminata por red (OSM). |
| Data_Output | URB | 4.5.3 | Tarija_Urban_Vulnerability.tif | (to be computed) | Compute (mean of URB indicators) | 2 |  |
| Data_Output | Combined | 4.5.4 | Tarija_Combined_Vulnerability.tif | (to be computed) | Compute (mean of 3 dimensions) | 2 |  |
| Data_Output | Combined | 5.3 / 5.4 | Tarija_Hexagon_500m_CC / _BIO / _URB / _Combined.gpkg | (to be computed) | Zonal statistics + choropleth + bivariate | 3 | También agregado por barrio. |
| Process | CC | 4.2 | (reference only) | Data_inventory_Tarija/1_CambioClimatico/Rasters/CC_HANDflujo_Principal_m_TAR.tif, CC_Aux_SuscQuebradas_TAR.tif, CC_Aux_SuscSueloDesnudo_TAR.tif, MVA_CC_Ind_FrecuenciaIncendios_TAR.tif | Keep in place; listed in Process/README | - | No se duplican para evitar copias desactualizadas. |
| Process | URB | 4.4 | (reference only) | Data_inventory_Tarija/3_Urbano/Rasters/URB_Aux_Friccion_Caminata_TAR.tif, URB_Aux_TiempoCaminata_*_min_TAR.tif, MVA_URB_Ind_VulnerabilidadHabitacional_TAR.tif (+_Origen) | Keep in place; listed in Process/README | - |  |
| Process | BIO | 4.3 | (reference only) | Data_inventory_Tarija/2_Biodiversidad/Rasters/LULC_Transicion_Natural_1985_2024_TAR.tif | Keep in place; listed in Process/README | - |  |
| Data_Input | All | 2 | (reference only) | Data_inventory_Tarija (all source data: DEM, MapBiomas, MSA, MapBiomas Fire, INE 2024, GAM facilities, OSM, VIDECI) | Keep in place; listed in Data_Input/README | - | Ver DATA_INVENTORY_Tarija_2026_EN.xlsx. |
