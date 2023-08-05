# Kornpob Bhirombhakdi
# kbhirombhakdi@stsci.edu

from photutils import CircularAperture
from photutils import aperture_photometry
from photutils.utils import calc_total_error
import pandas as pd

class ApPhot:
    """
    ApPhot is a class to perform circular aperture photometry. The code uses photutils, and follows closely to its instruction (https://photutils.readthedocs.io/en/stable/aperture.html).
    - aperture unit must be in pixel.
    - data = 2D image to be measured
    - ebkg, effgain = error from additional component such as background, and effective gain.
      - These values are used in computing total errors by using photutils.utils.calc_total_error.
      - If unknown, a user can set ebkg = 0 and effgain = 1.
    - center = (pixX,pixY) of centroid
    - aperture_radius = aperture radius in pixel unit
    Use self.compute() method after instantiation to perform the photometry.
    - self.apphot contains the outputs from computation including
      - apphot['error'] = total error. If ebkg = 0, this is equivalent to poisson error from the data scaled by effective gain.
      - apphot['aperture'] = photutils.CircularAperture object given center and aperture_radius
      - apphot['phot_table'] = photometry as the main output for this routine.
    Use self.save(container) method to save output to ./savefolder/saveprefix_apphot.csv given Container.
    """
    def __init__(self,data,ebkg,effgain,center,aperture_radius):
        self.data = data
        self.ebkg = ebkg
        self.effgain = effgain
        self.center = center
        self.aperture_radius = aperture_radius
    def compute(self):
        error = calc_total_error(self.data,self.ebkg,self.effgain)
        aperture = CircularAperture(self.center,r=self.aperture_radius)
        phot_table = aperture_photometry(self.data,aperture,error=error)
        self.apphot = {'error':error,'aperture':aperture,'phot_table':phot_table}
    def save(self,container=None):
        if container is None:
            raise ValueError('container must be specified to save.')
        sf = container.data['savefolder']
        sp = container.data['saveprefix']
        string = './{0}/{1}_apphot.csv'.format(sf,sp)
        t = {'aperture_radius':self.aperture_radius,
             'aperture_sum':self.apphot['phot_table']['aperture_sum'],
             'aperture_sum_err':self.apphot['phot_table']['aperture_sum_err']
            }
        pd.DataFrame(t).to_csv(string)
        print('Save {0}'.format(string))
        