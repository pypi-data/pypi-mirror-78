# Kornpob Bhirombhakdi
# kbhirombhakdi@stsci.edu

from astropy.io import fits
import numpy as np

class ObjectMask:
    """
    ObjectMask is a class to facilitate making an object mask (which is specified as True) given:
    - data = 2D image
    - center = np.array((xc,yc),dtype=int) is a center of the object.
    - dx,dy = int, specifying size of the object to be 2*dx+1 and 2*dy+1 from its center.
    - object mask is data[bb0y:bb1y,bb0x:bb1x] = True where
      - bb0y = center[1]-dy
      - bb1y = center[1]+1+dy
      - bb0x = center[0]-dx
      - bb1x = center[0]+1+dx
    Note: typically for a 2D image that the order of axis is (y,x).
    Use method compute to generate the mask after properly instantiated.
    Use save(container) to save ./savefolder/saveprefix_mask.fits given container
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
    def compute(self):
        t = np.full_like(self.data,False,dtype=bool)
        for i in np.arange(self.bb0x,self.bb1x):
            t[self.bb0y:self.bb1y,self.bb0x:self.bb1x] = True
        self.mask = t 
    def save(self,container=None):
        if container is None:
            raise ValueError('container must be specified to save.')
        sf = container.data['savefolder']
        sp = container.data['saveprefix']
        ph = fits.PrimaryHDU()
        ih = fits.ImageHDU()
        hdul = fits.HDUList([ph,ih])
        hdul[1].data = self.mask.astype(int).copy() 
        string = './{0}/{1}_mask.fits'.format(sf,sp)
        hdul.writeto(string,overwrite=True)
        print('Save {0}'.format(string))
        
        