# ERA5
Scripts de campos sinópticos y de mesoescala a partir de las variables de este reanálisis 
## Para bajar los datos del reanálisis
En la página del Copernicus : https://cds.climate.copernicus.eu/cdsapp#!/dataset/reanalysis-era5-pressure-levels?tab=overview
se encuentran para distintos niveles verticales y de forma horaria.
#
Se recomienda bajar a partir del CDS API (https://cds.climate.copernicus.eu/api-how-to) que es más rápido y se puede hacer un script automatizado.
#
Las variables de presión a nivel del mar o topografía del modelo se obtienen del 'single pressure level ERA5' (https://cds.climate.copernicus.eu/cdsapp#!/dataset/reanalysis-era5-single-levels?tab=overview)
#
Para acceder a cada base de datos es necesario crearse un usuario y contraseña (libre).
#
La topografia puede bajarse desde la pagina del https://www.ngdc.noaa.gov/mgg/global/ que tienen netCDF o geoTIFF de perfiles
de terreno con distintas resoluciones (un ejemplo esta aqui presente: 'topografia_Etopo_bedrock.nc').

El otro archivo 'TOPOGRAFIA_ERA5.nc' corresponde con la topografia propia del ERA5 para Sudamérica. Si se quiere una topografia con mayor definicion ver el reporistorio de terreno-netCDF. 
