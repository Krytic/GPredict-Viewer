# -*- coding: utf-8 -*-
"""
Created on Wed Mar 13 14:43:36 2019

@author: sric560
"""

from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt
import sys
import datetime

if len(sys.argv) == 1:
    sys.exit('Incorrect usage. Correct usage is: python {f} file-to-analyse'.format(f=sys.argv[0]))

plt.close('all')

filename = sys.argv[1] + ".txt"

data = np.genfromtxt(filename, dtype='U10,U8,f,f,f,f,f,f')

print(type(data[0]))

lat, long = data[:,5], data[:,6]

fl = data[0]

i = filename.rfind("-")
j = filename.rfind('/')
if j > 0:
    satellite = filename[j+1:i] # located in subfolder like demos
else:
    satellite = filename[:i] # located in same dir as this file

map = Basemap(projection='ortho',lat_0=-36.8535,lon_0=174.7684,resolution='l')

# draw lat/lon grid lines every 30 degrees.
map.drawmeridians(np.arange(0,360,30))
map.drawparallels(np.arange(-90,90,30))
map.bluemarble()

y, x = lat, long
llat, llong = lat[-1], long[-1]

map.plot(x,y,zorder=100,latlon=True,marker=None,color='y',markersize=2)

plt.title('Pass by {} (date: {}, AOS: {})'.format(satellite.upper(), fl[0], fl[1]))

name = filename[:-4]
plt.savefig(name + '-pass.png', dpi=500)

headertext = "  Pass report for {}  ".format(satellite)
headerlen = len(headertext)
header = "=" * headerlen

filedata = """{header}
{headertext}
{header}

Pass date: {date}
AOS: ({lat}, {long}) @ {starttime}
LOS: ({llat}, {llong})

Report generated at {ctime}
""".format(header=header,headertext=headertext,date=fl[0],starttime=fl[1],lat=fl[5],long=fl[6], ctime=datetime.datetime.now(), llat=llat, llong=llong)

with(open('{}-pass-report.txt'.format(name), 'w')) as f:
    f.writelines(filedata)

print('Analysis completed.')