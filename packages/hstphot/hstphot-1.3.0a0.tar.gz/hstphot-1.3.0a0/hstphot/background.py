# Kornpob Bhirombhakdi
# kbhirombhakdi@stsci.edu

from polynomial2d.polynomial2d import Polynomial2D
from astropy.io import fits
import numpy as np

class Background:
    def __init__(self,gdata,norder,mdata=None,
                 rescale='default',
                 sigclip=(False,None,None),
                 container=None
                ):
        """
        Background is a class to facilitate background estimation. The routine uses Polynomial2D package (pip install polynomial2d).
        - gdata = data
        - norder = polynomial order
        - mdata = mask data with True for masking object
        - rescale, sigclip = parameters from Polynomial2D to perform rescaling of values (in order to improve the performance), and sigma clipping in iterative fitting process respectively.
            rescale = 'default' will set rescaling to be performed with method [-1,1] linear transformation of x1,x2,y.
            Note: Polynomial2D also uses rescalex.rescale.Rescale class (pip install rescalex) internally for rescaling.
        At the instantiation, self.poly2d is the Polynomial2D object.
        - Use self.poly2d.fit() to perform the background fitting.
        - Use self.poly2d.model['YFIT'] to access the estimated background.
        - Use self.poly2d.model['MASKFIT'] to access the final mask after iterations (with True for masked out data).
        Use method save(do_bkg,do_mask) to save outputs, given container.
        - Set do_bkg = True for saving self.poly2d.model['YFIT'] as ./savefolder/saveprefix_cutbkg.fits.
        - Set do_mask = True for saving self.poly2d.model['MASKFIT'] as ./savefolder/saveprefix_maskfit.fits.
        """
        self.gdata = gdata
        self.norder = norder
        self.container = container
        if mdata is None:
            self.mdata = np.full_like(gdata,False,dtype=bool)
        else: self.mdata = mdata
        if rescale == 'default':
            dor = True
            methodr = {'method':'linear','minmax':(-1.,1.)}
            self.rescale = (dor,methodr,methodr,methodr)
        else:
            self.rescale = rescale
        self.sigclip = sigclip
        self.poly2d = self._poly2d()
    def _poly2d(self):
        ny,nx = self.gdata.shape
        x1 = np.arange(nx)
        x2 = np.arange(ny)
        x1v,x2v = np.meshgrid(x1,x2)
        obj = Polynomial2D(x1=x1v,x2=x2v,y=self.gdata,mask=self.mdata,norder=self.norder,rescale=self.rescale,sigclip=self.sigclip)
        return obj
    ##########
    ##########
    ##########
    def save(self,do_bkg=True,do_maskfit=True):
        if self.container is None:
            raise ValueError('container must be specified to save')
        saveprefix = self.container.data['saveprefix']
        savefolder = self.container.data['savefolder']
        if do_yfit:
            phdu = fits.PrimaryHDU()
            imhdu = fits.ImageHDU()
            hdul = fits.HDUList([phdu,imhdu])
            hdul[1].data = self.poly2d.model['YFIT'].copy()
            string = './{0}/{1}_cutbkg.fits'.format(savefolder,saveprefix)
            hdul.writeto(string,overwrite=True)
            print('Save {0}'.format(string))
        if do_maskfit:
            phdu = fits.PrimaryHDU()
            imhdu = fits.ImageHDU()
            hdul = fits.HDUList([phdu,imhdu])
            hdul[1].data = self.poly2d.model['MASKFIT'].astype(int)
            string = './{0}/{1}_maskfit.fits'.format(savefolder,saveprefix)
            hdul.writeto(string,overwrite=True)
            print('Save {0}'.format(string))
