# Kornpob Bhirombhakdi
# kbhirombhakdi@stsci.edu

from hstphot.photapcorr import PhotApCorr
import numpy as np
import pandas as pd

class Phot2ABmag:
    """
    Phot2ABmag is a class to convert from photometric counts/sec (cps) to AB magnitude.
    The code will grab aperture correction from a table specified by instrument, filterobs, and aperture_radius. The table is recorded in hstphot.photapcorr.PhotApCorr class.
    - self.available_instrument and self.available_filterobs after instantiation with any mock parameters will provide available support.
    - aperture_radius must be in pixel.
    Use self.compute() method to compute AB magnitude and its error:
    - ABmag = -2.5 * np.log10(cps / apcorr) + zp
    - emag = 2.5 * np.sqrt(error**2) / (cps * np.log(10.))
    - self.mag = (ABmag,emag)
    - self.wavelength and self.zp provide the effective wavelength and zeropoint.
    - self.apcorr provides aperture correction value.
    Use self.save(container) to save output to ./savefolder/saveprefix_mag.csv given Container.
    """
    def __init__(self,instrument,filterobs,aperture_radius,cps,error):
        self.instrument = instrument
        self.filterobs = filterobs
        self.aperture_radius = aperture_radius
        self.cps = cps
        self.error = error
        self.available_instrument = self._available_instrument()
        self.available_filterobs = self._available_filterobs()
    def compute(self):
        t = PhotApCorr(self.instrument)
        self.wavelength,self.zp = t.table['ZP'][self.filterobs]
        self.scale = t.table['scale']        
        apsize = self.aperture_radius * self.scale
        t = PhotApCorr(self.instrument,apsize,self.wavelength)
        t.compute()
        self.apcorr = t.apcorr[0]
        tm = -2.5 * np.log10(self.cps / self.apcorr) + self.zp
        tem = 2.5 * np.sqrt(self.error**2) / (self.cps * np.log(10.))
        self.mag = (tm,tem)
    def save(self,container=None):
        if container is None:
            raise ValueError('container must be specified to save.')
        sfolder = container.data['savefolder']
        sprefix = container.data['saveprefix']
        string = './{0}/{1}_mag.csv'.format(sfolder,sprefix)
        t = {'wavelength':self.wavelength,'ABmag':self.mag[0],'emag':self.mag[1],'zp':self.zp}
        pd.DataFrame(t,index=[0]).to_csv(string)
        print('Save {0}'.format(string))
    def _available_instrument(self):
        return PhotApCorr().available_instrument
    def _available_filterobs(self):
        try:
            t = PhotApCorr(self.instrument).table['ZP'].keys()
            return t
        except:
            string = 'instrument must be specified when instantiate. Use self.available_instrument to see support.'
            return string
        