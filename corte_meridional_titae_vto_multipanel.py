#############################################################################
## Script para hacer un corte meridional de temperatura potencial equivalente 
## y viento con los datos del reanálisis ERA5 
## resultan en 6 graficos para 6 horas distintas en un multipanel.
## se necesitan dos NETCDF, uno con la topografia y el otro con los datos
## para cada nivel de presion
## POWERED BY HUAYRA-TORO
############################################################################# 

from netCDF4 import Dataset
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta
import metpy.calc as mpcalc
from metpy.units import units
import scipy.ndimage as ndimage
import metpy.calc as mpcalc
from metpy.units import units
import matplotlib as mpl

datos_horarios = '...'
## los datos de topografia pueden ser bajados del ERA5 o sino estan en el repositorio
topografia = '...'

# es un grafico de 6 tiempos.
fecha_ini = datetime.strptime('01-04-2020 11:00', '%d-%m-%Y %H:%M')
j = 10	# a partir de la hora 10
delta = 6	# cada 6 horas
lon_corte = -64.25	# lugar central del corte vertical
for i in range(0, 6) :

	## cargo la topografia del ERA5
	top = Dataset(topografia)
	z_sup = top.variables[u'z'][:]	# mgp
	lat_z  = top.variables[u'latitude'][:]
	lon_z  = top.variables[u'longitude'][:]
	top.close()

	## cargo los datos del reanalisis
	file1 = Dataset(datos_horarios, 'r')
	lat  = file1.variables[u'latitude'][:]
	lon  = file1.variables[u'longitude'][:]
	niveles = file1.variables[u'level'][:]	# niveles de presion
	## el reanalisis debe tener estas variables para calcular titae y viento
	w = file1.variables['w'][:]	# es omega Pa s-1
	t = file1.variables['t'][:]	# temperatura
	q = file1.variables['q'][:]	# humedad especifica
	v = file1.variables['v'][:]	# viento meridional

	## selecciono los niveles entre 100 - 1000 hPa
	niveles = niveles[2:len(niveles)]
	
	## corto los datos en la longitud correspondiente 
	lugar = int(np.where(lon == float(lon_corte))[0])
	lugar_z = int(np.where(lon_z == float(lon_corte))[0])
	
	vgrd = v[j,2:29,:,lugar]
	q = q[j,2:29,:,lugar]
	t = t[j,2:29,:,lugar]
	omega = w[j,2:29,:,lugar]
	
	## hay que transformar omega a w:
	rgas = 287.058
	g    = 9.80665	
	vvel = np.zeros([int((omega.shape)[0]), int((omega.shape)[1])])
	for ii in range(0,int((omega.shape)[0])) :
		rho  = niveles[ii]/(rgas*t[ii,:])
		a = -omega[ii,:]/(rho*g)
		vvel[ii,:] = a

	## calculo la temperatura potencial equivalente
	e = mpcalc.vapor_pressure(1000. * units.mbar, q)
	td = mpcalc.dewpoint(e)
	titae = np.zeros([int((omega.shape)[0]), int((omega.shape)[1])])
	for iii in range(0,int((omega.shape)[0])) :
		titae[iii,:] = mpcalc.equivalent_potential_temperature((niveles[iii]*100) * units.pascal, t[iii,:]*units.kelvin, td[iii,:])
	titae = ndimage.gaussian_filter(titae, sigma=1, order=0) 	

	## paso el geopotencial del terreno a presion para poder graficarlo junto a lo demas
	z_sup = z_sup[0,:,lugar_z] / 9.80665
	press = (100000 - (1.2)*9.81*(z_sup)) / 100

	####### GRAFICADO ######## 
	if i == 0 :
		fig=plt.figure(figsize=(18,12))
	ax1 = plt.subplot(3, 3, i + 1)

	## temperatura potencial equivalente en sombreado
	im=ax1.contourf(lat, niveles, titae, np.arange(300, 380, 5), cmap='rainbow', extend='both')
	cbar = plt.colorbar(im)
	## En flechas el viento meridional vs el vertical
	q = ax1.quiver(lat, niveles, vgrd*1.94, vvel*1.94, scale=350)

	## se grafica el terreno en sombreado negro
	plt.plot(lat_z, press, color = 'black')
	plt.fill_between(lat_z, 1000,press, facecolor = 'black')
	plt.gca().invert_yaxis()
	
	plt.xlim([-27, -22])
	plt.ylim([1000, 100])

	if i == 0 :
		plt.title(str(fecha_ini) + ' UTC', fontsize = 10)
	if i > 0 :
		plt.title(str((fecha_ini+timedelta(hours=delta))) + ' UTC', fontsize = 10)
		delta = delta + 6
	j = j + 6

plt.savefig('.../corte_meridional_titae_vto.png', dpi = 300, bbox_inches = 'tight')
plt.close('all')

