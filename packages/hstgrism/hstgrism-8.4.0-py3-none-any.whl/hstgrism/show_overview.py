# Kornpob Bhirombhakdi
# kbhirombhakdi@stsci.edu

from astropy.io import fits
import matplotlib.pyplot as plt
import numpy as np

def show_overview(gfile,dfile,xyd,xyref,xh,yh,ww,objname,save=False,container=None,
         params={'figsize':(10,10),
                 '221':{'minmax':(5.,99.),'cmap':'viridis','s':30,'facecolor':'None','edgecolor':'red','fontsize':12,'title':'default'},
                 '222':{'minmax':(5.,99.),'cmap':'viridis','s':30,'facecolor':'None','edgecolor':'red','padxy':(50,50),'fontsize':12,'title':'default'},
                 '223':{'minmax':(5.,99.),'cmap':'viridis','s':30,'facecolor':'None','edgecolor':'red','color':'red','ls':'-','lw':4,'alpha':0.6,'fontsize':12,'title':'default'},
                 '224':{'minmax':(5.,99.),'cmap':'viridis','s':30,'facecolor':'None','edgecolor':'red','color':'red','ls':'-','lw':4,'alpha':0.6,'padxy':(50,50),'tickperx':50,'annotate_marker':'ro','annotate_color':'red','annotate_fontsize':8,'annotate_rotation':30.,'fontsize':12,'title':'default'},
                }
        ):
    """
    show_overview plots 2x2 of direct and grism images with zoom-in to the object location.
    - gfile = (path to grism file, extension)
    - dfile = (path to direct file, extension)
    - xyd = (pixX,pixY) of the object in the direct image
    - xyref = (xref,yref) of the object in the grism image
    - xh,yh,ww = trace and wavelength map
    - objname = object name which will be used for the plot title
    - save = True if user wants an output file for the plot, given container
    - params = customizable plot parameters
    """
    pixx,pixy = xyd
    xref,yref = xyref
    xg,yg = xh+xref,yh+yref
    plt.figure(figsize=params['figsize'])
    # 221
    ax1 = plt.subplot(2,2,1)
    fontsize = params['221']['fontsize']
    tmpdata = fits.open(dfile[0])[dfile[1]].data
    m = np.isfinite(tmpdata)
    vmin,vmax = np.percentile(tmpdata[m],params['221']['minmax'][0]),np.percentile(tmpdata[m],params['221']['minmax'][1])
    ax1.imshow(tmpdata,origin='lower',cmap=params['221']['cmap'],vmin=vmin,vmax=vmax)
    ax1.scatter(pixx,pixy,s=params['221']['s'],facecolor=params['221']['facecolor'],edgecolor=params['221']['edgecolor'])
    if params['221']['title'] == 'default':
        tmpheader = fits.open(dfile[0])[0].header
        string = '{0} {1} {2} {3}'.format(objname,tmpheader['ROOTNAME'],tmpheader['DATE-OBS'],tmpheader['FILTER'])
        string += '\nEXPSTART={0:.3f} EXPTIME={1:.3f}'.format(tmpheader['EXPSTART'],tmpheader['EXPTIME'])
    else:
        string = params['221']['title']
    ax1.set_title(string,fontsize=fontsize)
    # 222
    ax2 = plt.subplot(2,2,2)
    fontsize = params['222']['fontsize']
    dx,dy = params['222']['padxy']
    tmpdata = fits.open(dfile[0])[dfile[1]].data
    m = np.isfinite(tmpdata)
    vmin,vmax = np.percentile(tmpdata[m],params['222']['minmax'][0]),np.percentile(tmpdata[m],params['222']['minmax'][1])
    ax2.imshow(tmpdata,origin='lower',cmap=params['222']['cmap'],vmin=vmin,vmax=vmax)
    ax2.scatter(pixx,pixy,s=params['222']['s'],facecolor=params['222']['facecolor'],edgecolor=params['222']['edgecolor'])
    ax2.set_xlim(pixx-dx,pixx+dx)
    ax2.set_ylim(pixy-dy,pixy+dy)
    if params['222']['title'] == 'default':
        string = 'xyd = {0:.1f},{1:.1f}'.format(pixx,pixy)
    else:
        string = params['222']['title']
    ax2.set_title(string,fontsize=fontsize)
    # 223
    ax3 = plt.subplot(2,2,3)
    fontsize = params['223']['fontsize']
    tmpdata = fits.open(gfile[0])[gfile[1]].data
    m = np.isfinite(tmpdata)
    vmin,vmax = np.percentile(tmpdata[m],params['223']['minmax'][0]),np.percentile(tmpdata[m],params['223']['minmax'][1])
    ax3.imshow(tmpdata,origin='lower',cmap=params['223']['cmap'],vmin=vmin,vmax=vmax)
    ax3.plot(xg,yg,color=params['223']['color'],ls=params['223']['ls'],lw=params['223']['lw'],alpha=params['223']['alpha'])
    if params['223']['title'] == 'default':
        tmpheader = fits.open(gfile[0])[0].header
        string = '{0} {1} {2} {3}'.format(objname,tmpheader['ROOTNAME'],tmpheader['DATE-OBS'],tmpheader['FILTER'])
        string += '\nEXPSTART={0:.3f} EXPTIME={1:.3f}'.format(tmpheader['EXPSTART'],tmpheader['EXPTIME'])
    else:
        string = params['223']['title']   
    ax3.set_title(string,fontsize=fontsize)
    # 224
    ax4 = plt.subplot(2,2,4)
    fontsize = params['224']['fontsize']
    tickperx = params['224']['tickperx']
    dx,dy = params['224']['padxy']
    annotate_marker = params['224']['annotate_marker']
    annotate_color = params['224']['annotate_color']
    annotate_fontsize = params['224']['annotate_fontsize']
    annotate_rotation = params['224']['annotate_rotation']
    tmpdata = fits.open(gfile[0])[gfile[1]].data
    m = np.isfinite(tmpdata)    
    vmin,vmax = np.percentile(tmpdata[m],params['224']['minmax'][0]),np.percentile(tmpdata[m],params['224']['minmax'][1])
    ax4.imshow(tmpdata,origin='lower',cmap=params['224']['cmap'],vmin=vmin,vmax=vmax)
    ax4.plot(xg,yg,color=params['224']['color'],ls=params['224']['ls'],lw=params['224']['lw'],alpha=params['224']['alpha'])
    for i,ii in enumerate(xg):
        if (i in {0,len(xg)-1}) or (np.mod(i,tickperx)==0):
            label = '{0}A'.format(int(ww[i]))
            ax4.plot(xg[i],yg[i],annotate_marker)
            ax4.annotate(label,(xg[i],yg[i]),
                         textcoords='offset points',
                         xytext=(0,10),
                         ha='center',
                         fontsize=annotate_fontsize,
                         rotation=annotate_rotation,
                         color=annotate_color
                        )
    ax4.set_xlim(xg.min()-dx,xg.max()+dx)
    ax4.set_ylim(yg.min()-dy,yg.max()+dy)  
    if params['224']['title'] == 'default':
        string = 'xyref = {0:.1f},{1:.1f}'.format(xref,yref)        
    else:
        string = params['224']['title']   
    ax4.set_title(string,fontsize=fontsize)
    plt.tight_layout()
    if save:
        if container is None:
            raise ValueEror('container must be specified to save.')
        saveprefix = container.data['saveprefix']
        savefolder = container.data['savefolder']
        saveformat = container.data['plotformat']
        string = './{2}/{0}_overview.{1}'.format(saveprefix,saveformat,savefolder)
        plt.savefig(string,format=saveformat,bbox_inches='tight')
        print('Save {0}\n'.format(string))


