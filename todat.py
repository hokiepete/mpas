# -*- coding: utf-8 -*-
"""
Created on Fri Jun 01 14:25:19 2018

@author: pnola
"""
from netCDF4 import Dataset
#import matplotlib.pyplot as plt
import numpy as np
#import matplotlib.pyplot as plt

for t in range(9):
    ncfile="outfile_"+str(t)+".nc"

    vars = Dataset(ncfile,'r').variables #read the data
    u = np.squeeze(vars['U_925mb'][:])
    v = np.squeeze(vars['V_925mb'][:])
    lon = np.squeeze(vars['lon'][:])
    lat = np.squeeze(vars['lat'][:])
    
    f = open('roms%04d.dat' % t, 'w')
    #f.write("Surface Velocity ROMS data (m/s)\n")	
    f.write("Surface Velocity ROMS data (km/hr)\n")	
    #f.write("Domain Center 36.7964N,-120.822E\n")
    #f.write("Domain Center "+str(Lat)+"N,"+str(Lon)+"E\n")
    f.write("#Data_XMin = "+str(lon.min())+"\n")
    f.write("#Data_XMax = "+str(lon.max())+"\n")
    f.write("#Data_XRes = "+str(lon.size)+"\n")
    f.write("#Data_YMin = "+str(lat.min())+"\n")
    f.write("#Data_YMax = "+str(lat.max())+"\n")
    f.write("#Data_YRes = "+str(lat.size)+"\n")
    f.write("ZONE T=\"%04d\" I=" % (t+1) +str(lat.size)+" J="+str(lon.size)+"\n")
    for i in range(lat.size):
        for j in range(lon.size):
            #f.write(str(u[i,j])+" "+str(v[i,j])+"\n")
            f.write(str(3.6*u[i,j])+" "+str(3.6*v[i,j])+"\n")
            #f.write(str(lon[j])+" "+str(lat[i])+" "+str(u[i,j])+" "+str(v[i,j])+"\n")
    f.close()