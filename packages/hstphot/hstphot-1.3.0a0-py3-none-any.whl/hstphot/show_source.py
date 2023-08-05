from astropy.io import fits
import numpy as np
import matplotlib.pyplot as plt

def show_source(dfile,xyd,title,figsize=(10,5),cmap='viridis',
                scatter_size=30,facecolor='None',edgecolor='red',
                minmax=(5.,99.5),
                dx=50,dy=50,
                save=False,container=None
               ):
    t = fits.open(dfile[0])[dfile[1]].data
    m = np.isfinite(t)
    vmin,vmax = np.percentile(t[m],minmax[0]),np.percentile(t[m],minmax[1])
    fig = plt.figure(figsize=figsize)
    ax1 = fig.add_subplot(1,2,1)
    ax2 = fig.add_subplot(1,2,2)
    ax1.imshow(t,origin='lower',cmap=cmap,vmin=vmin,vmax=vmax)
    ax1.scatter(*xyd,s=scatter_size,facecolor=facecolor,edgecolor=edgecolor)
    ax2.imshow(t,origin='lower',cmap=cmap,vmin=vmin,vmax=vmax)
    ax2.scatter(*xyd,s=scatter_size,facecolor=facecolor,edgecolor=edgecolor)
    ax2.set_xlim(xyd[0]-dx,xyd[0]+dx)
    ax2.set_ylim(xyd[1]-dy,xyd[1]+dy)
    ax1.set_title('{0}'.format(title),fontsize=12)
    ax2.set_title('xyd = ({0:.2f},{1:.2f})'.format(xyd[0],xyd[1]),fontsize=12)
    fig.tight_layout()
    if save:
        if container is None:
            raise ValueError('container must be speficified to save.')
        savefolder = container.data['savefolder']
        saveprefix = container.data['saveprefix']
        plotformat = container.data['plotformat']
        string = './{0}/{1}_source.{2}'.format(savefolder,saveprefix,plotformat)
        fig.savefig(string,plotformat=plotformat,bbox_inches='tight')
        print('Save {0}'.format(string))
        