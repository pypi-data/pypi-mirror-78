# Kornpob Bhirombhakdi
# kbhirombhakdi@stsci.edu

import numpy as np

def mag2flux(mag,emag,wave):
    """
    mag2flux is a function to convert AB magnitude to flam.
    This is essentially the same as legacy mag2flux used widely in astronomy (e.g., https://www.harrisgeospatial.com/docs/mag2flux.html).
    """
    flam = 10**(-0.4 * (mag + 2.406 + 5.*np.log10(wave)))
    eflam = flam * np.log(10.) * 0.4 * emag
    return flam,eflam
