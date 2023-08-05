# Kornpob Bhirombhakdi
# kbhirombhakdi@stsci.edu

import matplotlib.pyplot as plt
import numpy as np

def show_sources(image,sourcelist,
                 large_figsize=(10,10),zoom_figsize=(5,5),
                 minmax=(5.,99.),
                 cmap='viridis',
                 scatter_size=30,edgecolor='red',facecolor='None',
                 annotation_fontsize=10,annotation_color='red',
                 zoom_pad_xy=(50,50),
                 large_title='None',large_fontsize=12,
                 zoom_fontsize=12,
                 save_large=False,save_zoom=False,container=None
                ):
    """
    show_sources plots a large overview 2D image with marks of sources provided in sourcelist, together with zoom-in plot of each source.
    - image = 2D array of image
    - sourcelist = dict with (key,value) as (source_name, xyd) where xyd = (pixX,pixY)
     - Note: if reading from ds9 region file as image pixel coordinate, xyd = xyd - (1.,1.) must be computed separately.
    - save_large, save_zoom are switches to save plots to location ./savefolder/saveprefix_savesuffix.plotformat
     - savefolder,saveprefix,plotformat given by Container class (see hstgrism.container.Container)
     - savesuffix = large for large plot, and = source_name given in sourcelist for each zoom-in plot.
    """
    m = np.isfinite(image)
    vmin,vmax = np.percentile(image[m],minmax[0]),np.percentile(image[m],minmax[1])
    ##### large #####
    plt.figure(figsize=large_figsize)
    plt.imshow(image,origin='lower',cmap=cmap,vmin=vmin,vmax=vmax)
    for ii,i in enumerate(sourcelist):
        x,y = sourcelist[i]
        plt.scatter(x,y,s=scatter_size,edgecolor=edgecolor,facecolor=facecolor,label=i)
        plt.annotate(i,(x,y),fontsize=annotation_fontsize,color=annotation_color)    
    plt.title(large_title,fontsize=large_fontsize)
    plt.tight_layout()
    if save_large:
        if container is None:
            raise valueError('container must be specified to save')
        string = './{0}/{1}_large.{2}'.format(container.data['savefolder'],container.data['saveprefix'],container.data['plotformat'])
        plt.savefig(string,plotformat=container.data['plotformat'],bbox_inches='tight')
        print('Save {0}'.format(string))
    ##### zoom #####
    n = len(sourcelist)
    fig = plt.figure(figsize=(zoom_figsize[0]*n,zoom_figsize[1]))
    for i,ii in enumerate(sourcelist):
        x,y = sourcelist[ii]
        ax = fig.add_subplot(1,n,i+1)
        ax.imshow(image,origin='lower',cmap=cmap,vmin=vmin,vmax=vmax)
        ax.scatter(x,y,s=scatter_size,edgecolor=edgecolor,facecolor=facecolor,label=i)
        dx,dy = zoom_pad_xy
        ax.set_xlim(x-dx,x+dx)
        ax.set_ylim(y-dy,y+dy)
        string = '{0}'.format(ii)
        string += '\n{0:.2f},{1:.2f}'.format(x,y)
        ax.set_title(string,fontsize=zoom_fontsize)
        if save_zoom:
            if container is None:
                raise valueError('container must be specified to save')
            string = './{0}/{1}_{3}.{2}'.format(container.data['savefolder'],container.data['saveprefix'],container.data['plotformat'],ii)
            plt.savefig(string,plotformat=container.data['plotformat'],bbox_inches='tight')
            print('Save {0}'.format(string))
            