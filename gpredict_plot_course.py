# -*- coding: utf-8 -*-
"""
Created on Wed Mar 13 14:43:36 2019

@author: sric560
"""

from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt
import sys

if len(sys.argv) == 1:
    sys.exit('Incorrect usage. Correct usage is: python {f} file-to-analyse'.format(f=sys.argv[0]))

plt.close('all')

filename = sys.argv[1] + ".txt"
skip = 0
with open(filename, 'r') as f:
    fl = f.readline()
    if fl[0] == "-":
        skip = 3
        f.readline()
        f.readline()
        fl = f.readline()

i = filename.rfind("-")
satellite = filename[:i]

data = np.genfromtxt(filename, skip_header=skip, dtype=float)
lat, long = data[:,5], data[:,6]

fl = list(filter(None, fl.split(" ")))

map = Basemap(projection='ortho',lat_0=-36.8535,lon_0=174.7684,resolution='l')
#map.drawcoastlines(linewidth=0.25)
#map.drawcountries(linewidth=0.25)
#map.fillcontinents(color='coral',lake_color='aqua',zorder=1)
# draw the edge of the map projection region (the projection limb)
#map.drawmapboundary(fill_color='aqua',zorder=0)
# draw lat/lon grid lines every 30 degrees.
map.drawmeridians(np.arange(0,360,30))
map.drawparallels(np.arange(-90,90,30))
map.bluemarble()

y, x = lat, long

map.plot(x,y,zorder=100,latlon=True,marker=None,color='y',markersize=2)

plt.title('Pass by {} (date: {}, start time: {})'.format(satellite.upper(), fl[0], fl[1]))

#plt.show()
name = filename[:-4]
plt.savefig(name + '-pass.png', dpi=500)

headertext = "  Pass report for {}  ".format(satellite)
headerlen = len(headertext)
header = "=" * headerlen

filedata = """
{header}
{headertext}
{header}

Pass date: {date}

Starts at: {starttime}

Lat/Long of first sighting: {lat} {long}
""".format(header=header,headertext=headertext,date=fl[0],starttime=fl[1],lat=fl[5],long=fl[6])

with(open('{}-pass-report.txt'.format(name), 'w')) as f:
    f.writelines(filedata)

print('Analysis completed.')