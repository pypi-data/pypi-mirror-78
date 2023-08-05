import numpy as np

def read_ds9region(ds9regfile):
    """
    Assume ds9regfile in the format as ds9, and coordinate system as image
    """
    out = {}
    f = open(ds9regfile,'r')
    for i,ii in enumerate(f.readlines()):
        if i < 3:
            continue
        x,y,_ = np.array(ii.split('(')[1].split(')')[0].split(',')).astype(float)
        z = ii.split('{')[1].split('}')[0]
        out[z] = (x,y)
    return out
