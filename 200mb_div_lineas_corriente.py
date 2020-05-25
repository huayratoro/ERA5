## Script para graficar lineas de corriente y geopotencial en 200 mb
## Powered by HUAYRA TORO
#  
from netCDF4 import Dataset
import matplotlib.pyplot as plt
import numpy as np
import cartopy.feature as cfeature
import cartopy.crs as ccrs
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
from os import listdir
from matplotlib.ticker import FixedLocator
from datetime import datetime, timedelta
import matplotlib.pylab as plt

states_provinces = cfeature.NaturalEarthFeature(
        category='cultural',
        name='admin_1_states_provinces_lines',
        scale='10m',
        facecolor='none',edgecolor='black')

countries = cfeature.NaturalEarthFeature(
        category='cultural',
        name='admin_0_countries',
        scale='10m',
        facecolor='none',edgecolor='black')

### la ruta del netCDF 
pfile = '../.nc'
salida = '../'
#################################################################################################################################################
# establecer la fecha de inicio de la serie 
fecha_ini = datetime.strptime('01-04-2020 11:00', '%d-%m-%Y %H:%M')
# tambien se puede extraer desde el reanalisis:
# se carga la variable 'time' que son las horas desde
# el 1/1/1900. Se le suman a esa fecha la cantidad de horas de la
# variable time y se obtiene la fecha correspondiente. 
## en este caso el netCDF4 tiene 6 tiempos diferentes 
## el grafico sera de 2 filas con 3 columnas para cada tiempo 
for i in range(0, 6) :

	######################## LEYENDO LOS DATOS #########################
	file1 = Dataset(pfile, 'r')
	lat  = file1.variables[u'latitude'][:]
	lon  = file1.variables[u'longitude'][:]
	niveles = file1.variables[u'level'][:]	# niveles de presion
	div = file1.variables['d'][:]	# divergencia
	ugrd = file1.variables['u'][:]	# viento zonal
	vgrd = file1.variables['v'][:]	# viento meridional
	file1.close()

	## obtengo cada variables en el nivel de 200 mb	
	l = np.where(niveles == 200)
	div = div[i+2,int(l[0]),:,:] * 100000
	ugrd = ugrd[i+2,int(l[0]),:,:]
	vgrd = vgrd[i+2,int(l[0]),:,:]

	####### GRAFICADO ######## 

	if i == 0 :
		fig=plt.figure(figsize=(20,11))
	ax1 = plt.subplot(2, 3, i + 1, projection=ccrs.PlateCarree())
	# delimitacion de latitudes y longitudes
	ax1.set_extent([-90, -30, -10, -60], crs=ccrs.PlateCarree())

	## lineas de corriente 
	strm = ax1.streamplot(lon, lat, ugrd, vgrd, density=2,color = np.sqrt(ugrd**2 + vgrd**2),linewidth=1, cmap='copper')
	## divergencia
	cint = np.arange(-8, 9)
	cm = ax1.contourf(lon, lat, div, cint[cint != 0], extend='both', cmap='PiYG', transform=ccrs.PlateCarree())
	# Agregamos la línea de costas
	ax1.coastlines(resolution='10m',linewidth=0.6)   
	# Agregamos los límites de los países
	ax1.add_feature(countries,linewidth=0.4)
	# Agregamos los límites de las provincias
	ax1.add_feature(states_provinces,linewidth=0.4)
	# Definimos donde aparecen los ticks con las latitudes y longitudes
	# en este caso aparecen en la izquierda y abajo de los subplots
	if (i == 0) or (i == 3):
		ax1.set_yticks(np.arange(-60, -10, 5), crs=ccrs.PlateCarree())
		lat_formatter = LatitudeFormatter()
		ax1.yaxis.set_major_formatter(lat_formatter)
	if (i >= 3):
		ax1.set_xticks(np.arange(-90, -30,10), crs=ccrs.PlateCarree())
		lon_formatter = LongitudeFormatter(zero_direction_label=True)
		ax1.xaxis.set_major_formatter(lon_formatter)
	# títulos 
	if i == 0 :
		plt.title(str(fecha_ini) + ' UTC', fontsize = 14)
	if i > 0 :
		plt.title(str((fecha_ini+timedelta(hours=i*6))) + ' UTC', fontsize = 14)
	
	# se modifica el tamaño de los subplots
	fig.subplots_adjust(
	top=0.968,
	bottom=0.031,
	left=0.013,
	right=0.953,
	hspace=0.115,
	wspace=0.0)
## para la barra de colores
cb_ax = fig.add_axes([0.95, 0.25, 0.02, 0.5])
cbar = fig.colorbar(cm, cax=cb_ax)

plt.savefig(salida + '200mb_div_lineas_corriente.png', dpi = 300, bbox_inches = 'tight')
plt.close('all')
