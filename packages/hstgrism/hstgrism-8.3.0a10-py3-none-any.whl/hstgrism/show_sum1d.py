# Kornpob Bhirombhakdi
# kbhirombhakdi@stsci.edu

import matplotlib.pyplot as plt
import numpy as np

def show_sum1d(gdata,objname,mdata=None,
               do_zero=True,
               params = {'figsize':(10,10),
                         'cmap':'viridis',
                         'minmax':(5.,90.),
                         'fontsize':12,
                         'title':'default',
                         'xlabel':'default',
                         'ylabel':'default'
                        },
               save=False,container=None):
    """
    show_sum1d takes a 2D data (i.e., gdata), computes summation along x and y axes, and plots.
    - do_zero = True will plot a zero line for reference.
    - mdata = mask with True for being excluded (i.e., set to np.nan)
    Use method save() to save the plot as ./savefolder/saveprefix_sum1d.plotformat, given container.
    """
    figsize = params['figsize']
    fontsize = params['fontsize']
    minmax = params['minmax']
    cmap = params['cmap']
    if mdata is None:
        mdata = np.full_like(gdata,False,dtype=bool)
    tmpdata = gdata.copy()
    tmpdata[mdata] = np.nan
    fig = plt.figure(figsize=figsize)
    # 221
    ax = fig.add_subplot(2,2,1)
    m = np.isfinite(tmpdata)
    vmin,vmax = np.percentile(tmpdata[m],minmax[0]),np.percentile(tmpdata[m],minmax[1])
    ax.imshow(tmpdata,origin='lower',cmap=cmap,vmin=vmin,vmax=vmax)
    string_title = objname if params['title'] == 'default' else params['title']
    string_xlabel = 'pixX' if params['xlabel'] == 'default' else params['xlabel']
    string_ylabel = 'pixY' if params['ylabel'] == 'default' else params['ylabel']
    ax.set_title(string_title,fontsize=fontsize)
    ax.set_xlabel(string_xlabel,fontsize=fontsize)
    ax.set_ylabel(string_ylabel,fontsize=fontsize)
    # 222
    ax2 = fig.add_subplot(2,2,2,sharey=ax)
    ny,nx = tmpdata.shape
    ax2.plot(np.nansum(tmpdata,axis=1),np.arange(ny))
    # 223
    ax3 = fig.add_subplot(2,2,3,sharex=ax)
    ny,nx = tmpdata.shape
    ax3.plot(np.arange(nx),np.nansum(tmpdata,axis=0))
    # do_zero
    if do_zero:
        ax2.plot(np.full_like(np.arange(ny),0.,dtype=float),np.arange(ny),'r:')
        ax3.plot(np.arange(nx),np.full_like(np.arange(nx),0.,dtype=float))
    fig.tight_layout()
    if save:
        if container is None:
            raise ValueError('container must be specified to save')
        saveprefix = container.data['saveprefix']
        savefolder = container.data['savefolder']
        plotformat = container.data['plotformat']
        string = './{2}/{0}_sum1d.{1}'.format(saveprefix,plotformat,savefolder)
        fig.savefig(string,format=plotformat,bbox_inches='tight')
        print('Save {0}'.format(string))
