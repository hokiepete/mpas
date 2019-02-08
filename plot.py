
#'''
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
fig = plt.figure(figsize=(width,width*1/1.618))
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
plt.savefig('Global_FLTE_60km.png', transparent=False, bbox_inches='tight')
'''
import pandas as pd
loadfile = pd.read_csv("co.dat", delimiter=" ",names=['uvar','vvar','na'])
u = loadfile['uvar']
v = loadfile['vvar']
uu=max(abs(u))
vv=max(abs(v))
'''