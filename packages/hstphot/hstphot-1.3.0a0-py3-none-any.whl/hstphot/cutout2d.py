# Kornpob Bhirombhakdi
# kbhirombhakdi@stsci.edu

from astropy.io import fits
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class Cutout2d:
    """
    Cutout2d is a class facilitating making a 2D cutout of a 2D array by given center, dx, and dy.
    - center = np.array((xc,yc),dtype=int)
    - dx,dy = int, specifying size of the cutout to be 2*dx+1 and 2*dy+1.
    - cutout image = data[bb0y:bb1y,bb0x:bb1x] where
      - bb0y = center[1]-dy
      - bb1y = center[1]+1+dy
      - bb0x = center[0]-dx
      - bb1x = center[0]+1+dx
    Note: typically for a 2D image that the order of axis is (y,x).
    Use method show to plot the cutout image.
    - show(save=True,container) to save outputs with name convention ./savefolder/saveprefix_savesuffix.extention
      - savefolder, saveprefix are specified by container
      - plotformat in container specifies plotformat.
      - outputs include:
        - cutout.plotformat = plot image.
        - bbcorner.csv = corner definition including center relative to the original frame.
        - cutout.fits = fits image
    """
    def __init__(self,data,center,dx,dy):
        self.data = data
        self.center = np.array(center,dtype=int)
        self.dx = int(dx)
        self.dy = int(dy)
        xc,yc = self.center
        self.bb0x = xc - self.dx
        self.bb1x = xc + 1 + self.dx
        self.bb0y = yc - self.dy
        self.bb1y = yc + 1 + self.dy
        self.cut = self.data[self.bb0y:self.bb1y,self.bb0x:self.bb1x]
    def show(self,title,
             fontsize=12,
             figsize=(5,5),cmap='viridis',minmax=(5.,99.),
             scatter_size=30,marker_style='x',color='red',
             save=False,container=None):
        m = np.isfinite(self.cut)
        vmin,vmax = np.percentile(self.cut[m],minmax[0]),np.percentile(self.cut[m],minmax[1])
        plt.figure(figsize=figsize)
        plt.imshow(self.cut,origin='lower',cmap=cmap,vmin=vmin,vmax=vmax)
        tx,ty = self.center - np.array([self.bb0x,self.bb0y],dtype=int)
        plt.scatter(tx,ty,s=scatter_size,marker=marker_style,color=color)
        plt.title(title,fontsize=12)
        plt.tight_layout()
        if save:
            if container is None:
                raise ValueError('container must be specified to save.')
            saveprefix = container.data['saveprefix']
            savefolder = container.data['savefolder']
            plotformat = container.data['plotformat']
            string = './{0}/{1}_cutout.{2}'.format(savefolder,saveprefix,plotformat)
            plt.savefig(string,plotformat=plotformat,bbox_inches='tight')
            print('Save {0}'.format(string))
            self._save_bbcorner(savefolder,saveprefix)
            self._save_fits(savefolder,saveprefix)
    def _save_bbcorner(self,savefolder,saveprefix):
        t = {'xyd':self.center,'bbx':[self.bb0x,self.bb1x],'bby':[self.bb0y,self.bb1y]}
        string = './{0}/{1}_bbcorner.csv'.format(savefolder,saveprefix)
        pd.DataFrame(t).to_csv(string)
        print('Save {0}'.format(string))
    def _save_fits(self,savefolder,saveprefix):
        ph = fits.PrimaryHDU()
        ih = fits.ImageHDU()
        hdul = fits.HDUList([ph,ih])
        hdul[1].data = self.cut.copy() 
        string = './{0}/{1}_cutout.fits'.format(savefolder,saveprefix)
        hdul.writeto(string,overwrite=True)
        print('Save {0}'.format(string))
        