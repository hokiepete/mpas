"""
Plot_Res[1]        	601
#FTLE_Min[0]       	-180
#FTLE_Max[0]       	179.75
#FTLE_Res[0]       	1440
#FTLE_Min[1]       	-66.5
#FTLE_Max[1]       	66.5
#FTLE_Res[1]       	533


Surface Velocity ROMS data (km/hr)
#Data_XMin = -180.0
#Data_XMax = 179.75
#Data_XRes = 1440
#Data_YMin = -89.75
#Data_YMax = 89.75
#Data_YRes = 719
ZONE T="0009" I=719 J=1440
"""

import pandas as pd
import h5py as hp
import numpy as np
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['text.usetex']=True
matplotlib.rcParams['mathtext.fontset'] = 'cm'
matplotlib.rcParams['lines.linewidth']=1
plt.rc('font', **{'family': 'serif', 'serif': ['cmr10']})
titlefont = {'fontsize':12}
labelfont = {'fontsize':10}
tickfont = {'fontsize':8}

loadfile = pd.read_csv("roms0000.dat", delimiter=" ",names=['uvar','vvar','na'])
u = 1/(3.6)*np.reshape(loadfile['uvar'].as_matrix(),(719,1440),order='C')
v = 1/(3.6)*np.reshape(loadfile['vvar'].as_matrix(),(719,1440),order='C')
x = np.linspace(-180,179.25,1440)
y = np.linspace(-89.75,89.75,719)
x,y = np.meshgrid(x,y)


with hp.File("FTLEOutput_global_60km.mat",'r') as loadfile:
    lon = loadfile[loadfile['X'][0, 0]][:]
    lat = loadfile[loadfile['X'][0, 1]][:]
    ftle = loadfile['F'][:]
    loadfile.close()
plt.close('all')
lon_min = lon[0]
lon_max = lon[-1]
lat_min = lat[0]
lat_max = lat[-1]

width =6.5
plt.close('all')

fig = plt.figure(figsize=(width,width/1.618))
print( lon_min, lon_max ,lat_min ,lat_max)
m = Basemap(llcrnrlon=lon_min,
            llcrnrlat=lat_min,
            urcrnrlon=lon_max,
            urcrnrlat=lat_max,
            #lat_0=(lat_max - lat_min)/2,
            #lon_0=(lon_max-lon_min)/2,
            projection='merc',
            resolution = 'l',
            area_thresh=1000.,
            )
x=x[abs(y)<=lat_max].reshape((533,1440))
u=u[abs(y)<=lat_max].reshape((533,1440))
v=v[abs(y)<=lat_max].reshape((533,1440))
y=y[abs(y)<=lat_max].reshape((533,1440))
gs = 25
velquiver = m.quiver(x[::gs,::gs],y[::gs,::gs],u[::gs,::gs],v[::gs,::gs],latlon=True,color='C0')
qk = plt.quiverkey(velquiver, 0.9*m.urcrnrx, 1.03*m.urcrnry, 10, '$10 m/s$', labelpos='E', coordinates='data', fontproperties={'size': '10'})
m.drawcoastlines(color='dimgray')
m.drawcountries(color='dimgray')
parallels = np.arange(-60,80,30)
#parallels = np.arange(np.floor(lat_min),lat_max+2,2)
m.drawparallels(parallels,labels=[1,0,0,0],fontsize=10)
# draw meridians
meridians = np.arange(-180,180,45)
#meridians = np.arange(np.floor(lon_max),lon_min-2,-2)
m.drawmeridians(meridians,labels=[0,0,0,1],fontsize=10)
plt.xticks(**tickfont)
plt.yticks(**tickfont)

plt.savefig('Global_quiver_60km.png', transparent=True,dpi=300, bbox_inches='tight')#,padding=0.05)
fig = plt.figure(figsize=(width,width/1.618))

lon, lat = np.meshgrid(lon,lat,indexing='ij')
#m.pcolormesh(lon,lat,ftle,latlon=True,shading='gourand',cmap='viridis')
m.contourf(lon,lat,ftle,latlon=True,levels=np.linspace(ftle.min(axis=None),ftle.max(axis=None),301),vmin=0.0,vmax=0.12,cmap='viridis')
#plt.colorbar()
m.drawcoastlines()
#m.drawrivers()
#m.drawstates()

m.drawcountries()
parallels = np.arange(-60,80,30)
#parallels = np.arange(np.floor(lat_min),lat_max+2,2)
m.drawparallels(parallels,labels=[1,0,0,0],fontsize=10)
# draw meridians
meridians = np.arange(-180,180,45)
#meridians = np.arange(np.floor(lon_max),lon_min-2,-2)
m.drawmeridians(meridians,labels=[0,0,0,1],fontsize=10)
plt.xticks(**tickfont)
plt.yticks(**tickfont)
#plt.show()
#plt.subplots_adjust(wspace=0, hspace=-0.1)
plt.savefig('Global_FLTE_60km.png', transparent=True,dpi=300, bbox_inches='tight')#,padding=0.05)
#'''