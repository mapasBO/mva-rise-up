# Tarija - Galería de mapas

Todos los mapas son composiciones A4 exportadas de `MVA_Tarija.qgz` (script `scripts/tarija/phase3b_layouts.py`), 24 mapas, mostrados aquí a 150 dpi. Haga clic en un mapa para abrirlo en tamaño completo. Las leyendas son bilingües (EN/ES). Valores 0-1, 1 = mayor vulnerabilidad.

**Cómo leer los mapas.** Los rásters de indicadores y de dimensiones usan 5 clases fijas de 0.2; BIO2, BIO3 y URB3 son categóricos. Los mapas de hexágonos usan las clases de la guía (0-0.33-0.66-máx). Los mapas combinados usan además clases complementarias (desviaciones estándar o quintiles), porque con clases fijas casi todo Tarija queda en una sola clase; muestran hotspots *relativos* dentro de Tarija, no vulnerabilidad alta absoluta (ver [04](04_fase3_hotspots.md)). Los 14 barrios etiquetados están distribuidos de forma pareja; la capa de barrios cubre solo el centro consolidado (34% del área urbana).

## Indicadores de cambio climático

<table>
<tr>
<td align="center" width="50%"><a href="../../img/tarija/maps/Tarija_CCInd3_Riverine-Flood.png"><img src="../../img/tarija/maps/Tarija_CCInd3_Riverine-Flood.png" width="400" alt="CC3 Inundación fluvial (HAND por flujo)"></a><br><sub>CC3 Inundación fluvial (HAND por flujo)</sub></td>
<td align="center" width="50%"><a href="../../img/tarija/maps/Tarija_CCInd4_Landslide.png"><img src="../../img/tarija/maps/Tarija_CCInd4_Landslide.png" width="400" alt="CC4 Deslizamientos (susceptibilidad por pendiente)"></a><br><sub>CC4 Deslizamientos (susceptibilidad por pendiente)</sub></td>
</tr>
<tr>
<td align="center" width="50%"><a href="../../img/tarija/maps/Tarija_CCInd5_Urban-Heat-Island.png"><img src="../../img/tarija/maps/Tarija_CCInd5_Urban-Heat-Island.png" width="400" alt="CC5 Isla de calor urbana"></a><br><sub>CC5 Isla de calor urbana</sub></td>
<td align="center" width="50%"><a href="../../img/tarija/maps/Tarija_CCInd6_Wildfire-Interface.png"><img src="../../img/tarija/maps/Tarija_CCInd6_Wildfire-Interface.png" width="400" alt="CC6 Interfaz urbano-vegetación (incendios)"></a><br><sub>CC6 Interfaz urbano-vegetación (incendios)</sub></td>
</tr>
</table>

## Indicadores de biodiversidad

<table>
<tr>
<td align="center" width="50%"><a href="../../img/tarija/maps/Tarija_BIOInd1_MSA.png"><img src="../../img/tarija/maps/Tarija_BIOInd1_MSA.png" width="400" alt="BIO1 Pérdida de biodiversidad (1 - MSA)"></a><br><sub>BIO1 Pérdida de biodiversidad (1 - MSA)</sub></td>
<td align="center" width="50%"><a href="../../img/tarija/maps/Tarija_BIOInd2_Protected-Areas.png"><img src="../../img/tarija/maps/Tarija_BIOInd2_Protected-Areas.png" width="400" alt="BIO2 Protección ponderada por tipo de zona"></a><br><sub>BIO2 Protección ponderada por tipo de zona</sub></td>
</tr>
<tr>
<td align="center" width="50%"><a href="../../img/tarija/maps/Tarija_BIOInd3_Natural-Cover-Loss.png"><img src="../../img/tarija/maps/Tarija_BIOInd3_Natural-Cover-Loss.png" width="400" alt="BIO3 Pérdida de cobertura natural 1985-2024"></a><br><sub>BIO3 Pérdida de cobertura natural 1985-2024</sub></td>
</tr>
</table>

## Indicadores urbanos

<table>
<tr>
<td align="center" width="50%"><a href="../../img/tarija/maps/Tarija_URBInd1_Population.png"><img src="../../img/tarija/maps/Tarija_URBInd1_Population.png" width="400" alt="URB1 Población en edades sensibles"></a><br><sub>URB1 Población en edades sensibles</sub></td>
<td align="center" width="50%"><a href="../../img/tarija/maps/Tarija_URBInd3_Urban-Growth.png"><img src="../../img/tarija/maps/Tarija_URBInd3_Urban-Growth.png" width="400" alt="URB3 Crecimiento urbano ponderado por antigüedad"></a><br><sub>URB3 Crecimiento urbano ponderado por antigüedad</sub></td>
</tr>
<tr>
<td align="center" width="50%"><a href="../../img/tarija/maps/Tarija_URBInd4_Informal-Settlement.png"><img src="../../img/tarija/maps/Tarija_URBInd4_Informal-Settlement.png" width="400" alt="URB4 Asentamientos informales (proxy de vivienda)"></a><br><sub>URB4 Asentamientos informales (proxy de vivienda)</sub></td>
<td align="center" width="50%"><a href="../../img/tarija/maps/Tarija_URBInd5_Access-Facilities.png"><img src="../../img/tarija/maps/Tarija_URBInd5_Access-Facilities.png" width="400" alt="URB5 Acceso caminable a equipamientos"></a><br><sub>URB5 Acceso caminable a equipamientos</sub></td>
</tr>
</table>

## Vulnerabilidad (ráster 12.5 m)

<table>
<tr>
<td align="center" width="50%"><a href="../../img/tarija/maps/Tarija_Climate_Vulnerability.png"><img src="../../img/tarija/maps/Tarija_Climate_Vulnerability.png" width="400" alt="Vulnerabilidad climática"></a><br><sub>Vulnerabilidad climática</sub></td>
<td align="center" width="50%"><a href="../../img/tarija/maps/Tarija_Biodiversity_Vulnerability.png"><img src="../../img/tarija/maps/Tarija_Biodiversity_Vulnerability.png" width="400" alt="Vulnerabilidad de biodiversidad"></a><br><sub>Vulnerabilidad de biodiversidad</sub></td>
</tr>
<tr>
<td align="center" width="50%"><a href="../../img/tarija/maps/Tarija_Urban_Vulnerability.png"><img src="../../img/tarija/maps/Tarija_Urban_Vulnerability.png" width="400" alt="Vulnerabilidad urbana"></a><br><sub>Vulnerabilidad urbana</sub></td>
<td align="center" width="50%"><a href="../../img/tarija/maps/Tarija_Combined_Vulnerability.png"><img src="../../img/tarija/maps/Tarija_Combined_Vulnerability.png" width="400" alt="Vulnerabilidad combinada (clases por desviación estándar)"></a><br><sub>Vulnerabilidad combinada (clases por desviación estándar)</sub></td>
</tr>
</table>

## Hexágonos de 500 m

<table>
<tr>
<td align="center" width="50%"><a href="../../img/tarija/maps/Tarija_Hexagon_500m_CC.png"><img src="../../img/tarija/maps/Tarija_Hexagon_500m_CC.png" width="400" alt="Clima (clases de la guía)"></a><br><sub>Clima (clases de la guía)</sub></td>
<td align="center" width="50%"><a href="../../img/tarija/maps/Tarija_Hexagon_500m_BIO.png"><img src="../../img/tarija/maps/Tarija_Hexagon_500m_BIO.png" width="400" alt="Biodiversidad (clases de la guía)"></a><br><sub>Biodiversidad (clases de la guía)</sub></td>
</tr>
<tr>
<td align="center" width="50%"><a href="../../img/tarija/maps/Tarija_Hexagon_500m_URB.png"><img src="../../img/tarija/maps/Tarija_Hexagon_500m_URB.png" width="400" alt="Urbana (clases de la guía)"></a><br><sub>Urbana (clases de la guía)</sub></td>
<td align="center" width="50%"><a href="../../img/tarija/maps/Tarija_Hexagon_500m_Combined.png"><img src="../../img/tarija/maps/Tarija_Hexagon_500m_Combined.png" width="400" alt="Combinada (clases por desviación estándar)"></a><br><sub>Combinada (clases por desviación estándar)</sub></td>
</tr>
<tr>
<td align="center" width="50%"><a href="../../img/tarija/maps/Tarija_Hexagon_500m_Combined_Quintiles.png"><img src="../../img/tarija/maps/Tarija_Hexagon_500m_Combined_Quintiles.png" width="400" alt="Combinada (quintiles, complementario)"></a><br><sub>Combinada (quintiles, complementario)</sub></td>
<td align="center" width="50%"><a href="../../img/tarija/maps/Tarija_Hexagon_500m_Combined_InsetExample.png"><img src="../../img/tarija/maps/Tarija_Hexagon_500m_Combined_InsetExample.png" width="400" alt="Combinada (clases DE) con recuadro del centro"></a><br><sub>Combinada (clases DE) con recuadro del centro</sub></td>
</tr>
</table>

## Hotspots bivariados

<table>
<tr>
<td align="center" width="50%"><a href="../../img/tarija/maps/Tarija_Bivariate_URB_x_CC.png"><img src="../../img/tarija/maps/Tarija_Bivariate_URB_x_CC.png" width="400" alt="Urbana x Clima (guía)"></a><br><sub>Urbana x Clima (guía)</sub></td>
<td align="center" width="50%"><a href="../../img/tarija/maps/Tarija_Bivariate_BIO_x_CC.png"><img src="../../img/tarija/maps/Tarija_Bivariate_BIO_x_CC.png" width="400" alt="Clima x Biodiversidad"></a><br><sub>Clima x Biodiversidad</sub></td>
</tr>
<tr>
<td align="center" width="50%"><a href="../../img/tarija/maps/Tarija_Bivariate_URB_x_BIO.png"><img src="../../img/tarija/maps/Tarija_Bivariate_URB_x_BIO.png" width="400" alt="Urbana x Biodiversidad"></a><br><sub>Urbana x Biodiversidad</sub></td>
</tr>
</table>

**Leyendas bivariadas (3x3):** [URB_x_CC](../../img/tarija/legends/Tarija_Bivariate_Legend_URB_x_CC.png) · [BIO_x_CC](../../img/tarija/legends/Tarija_Bivariate_Legend_BIO_x_CC.png) · [URB_x_BIO](../../img/tarija/legends/Tarija_Bivariate_Legend_URB_x_BIO.png)
