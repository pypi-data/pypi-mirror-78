
import os

import numpy as np
import healpy as hp
import h5py
import astropy.io.fits
from astropy.table import Table
from astropy import units as u
from astropy.coordinates import SkyCoord

from matplotlib import rc
rc('text', usetex=False)
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 20})
from matplotlib.collections import LineCollection
from matplotlib.lines import Line2D
from mpl_toolkits.axes_grid1 import make_axes_locatable

filename = '../catalog/CLU_20170106_galexwise_DaveUpdate.fits'
filename = '../catalog/CLU_20181213V2.fits'
filename = '../catalog/CLU_20190406_filled.hdf5'
filename = '../catalog/CLU_20190708_marshalFormat.hdf5'

outputDir = '../output/CLU'
if not os.path.isdir(outputDir):
    os.makedirs(outputDir)

t = Table.read(filename)
columns = ['name', 'ra', 'dec', 'distmpc', 'sfr_fuv', 'mstar',
           'magb', 'a', 'b2a', 'pa', 'btc']
t.keep_columns(columns)

t['ra'].unit = u.deg
t['dec'].unit = u.deg
t['distmpc'].unit = u.Mpc

coord = SkyCoord(ra=t['ra'], dec=t['dec'])

nsamples = 1000
idx = np.random.choice(len(t), nsamples)
data_out = np.zeros((20,nsamples))
for jj, ii in enumerate(idx):
    coord1 = coord[ii]
    dist = coord1.separation(coord).deg
    idy = np.argsort(dist)[1:11]

    dist_train = t['distmpc'][idy] 
    data_out[0:-1:2,jj] = dist[idy]
    data_out[1::2,jj] = dist_train
data_out = np.vstack((data_out,np.atleast_2d(t['distmpc'][idx]))).T

# background setup
NSIDE = 64
NPIX = hp.nside2npix(NSIDE)
coordsys = ['C','C']
nest = True

ipix = hp.ang2pix(NSIDE, t['ra'],t['dec'], lonlat=True, nest=nest)

hist = np.zeros(hp.nside2npix(NSIDE))
#hist[ipix] = hist[ipix] + 1
for ii in ipix:
    hist[ii] = hist[ii] + 1
hist = hist / (hp.nside2pixarea(NSIDE)*3600)

# init figure
fig1 = plt.figure(figsize=(14,10))

# colormap
cm = plt.cm.get_cmap('viridis') # colorscale
cm.set_under('w')
cm.set_bad('w')

# plot the data in healpy
norm ='log'
hp.mollview(hist,fig=1,norm=norm,unit='Number of galaxies.',cbar=False,nest=nest,title='',coord=coordsys,notext=True,cmap=cm,flip='astro',nlocs=4,min=1,max=100)

#f = plt.gcf().get_children()
#HpxAx = f[1]
#CbAx = f[2]
#unit_text_obj = CbAx.get_children()[1]
#unit_text_obj.set_fontsize(28)

fig = plt.gcf()
ax = plt.gca()
image = ax.get_images()[0]

cbar = fig.colorbar(image, ax=ax, ticks=[1,10,100], fraction=0.15, pad=0.05, location='bottom')
cbar.set_label('Number of galaxies per square arcminute', size=24)
cbar.ax.tick_params(labelsize=24)

ax.tick_params(axis='both', which='major', labelsize=24)

# borders
lw = 3
pi = np.pi
dtor = pi/180.
theta = np.arange(0,181)*dtor
hp.projplot(theta, theta*0-pi,'-k',
                               lw=lw,direct=True)
hp.projplot(theta, theta*0+0.9999*pi,'-k',
                               lw=lw,direct=True)
phi = np.arange(-180,180)*dtor
hp.projplot(phi*0+1.e-10, phi,'-k',
                               lw=lw,direct=True)
hp.projplot(phi*0+pi-1.e-10, phi,'-k',
                               lw=lw,direct=True)

# galaxy
for gallat in [15,0,-15]:
    theta = np.arange(0., 360, 0.036)
    phi = gallat*np.ones_like(theta)
    hp.projplot(theta, phi, 'w-', coord=['G'],lonlat=True,lw=2)

# ecliptic
for ecllat in zip([0,-30,30],[2,1,1]):
    theta = np.arange(0., 360, 0.036)
    phi = gallat*np.ones_like(theta)
    hp.projplot(theta, phi, 'w-', coord=['E'],lonlat=True,lw=2,ls=':')

# graticule
hp.graticule(ls='-',alpha=0.1,lw=0.5)

# NWES
fig = plt.gcf()
ax = plt.gca()
plt.text(0.0,0.5,r'E',ha='right',transform=ax.transAxes,weight='bold')
plt.text(1.0,0.5,r'W',ha='left',transform=ax.transAxes,weight='bold')
plt.text(0.5,0.992,r'N',va='bottom',ha='center',transform=ax.transAxes,weight='bold')
plt.text(0.5,0.0,r'S',va='top',ha='center',transform=ax.transAxes,weight='bold')

plt.show()
plotName = os.path.join(outputDir,'coverage.pdf')
plt.savefig(plotName, bbox_inches='tight')
plt.close()

