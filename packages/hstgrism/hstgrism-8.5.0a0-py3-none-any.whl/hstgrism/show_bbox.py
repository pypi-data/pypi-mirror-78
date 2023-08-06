# Kornpob Bhirombhakdi
# kbhirombhakdi@stsci.edu

import matplotlib.pyplot as plt
import numpy as np

def show_bbox(cutoutdata,objname='No_object_name',
              maskdata=None,
              params = {'figsize':(10,10),
                        'cmap_cutout':'viridis',
                        'minmax':(5.,90.),
                        'cmap_mask':'Greys',
                        'alpha_mask':0.4,
                        'title':'default',
                        'fontsize':12
                       },
              do_trace=False,xcut=None,ycut=None,ww=None,
              tparams = {'tcolor':'red',
                         'tls':':',
                         'tlw':4,
                         'talpha':0.4
                        },
              aparams = {'axpertick':100,
                         'acolor_marker':'red',
                         'amarker':'o',
                         'afontsize':10,
                         'arotation':90.,
                         'acolor_text':'red'
                        },
              save=False,container=None
             ):
    """
    show_bbox plots Cutout2D object.
    - if maskdata is specified, maskdata will be plotted. Use params to set the parameters.
    - if d_trace is True, trace will be plotted. Use tparams and aparams to set parameters.
    - xcut = xg - bb0x and xg = xh + xref, and vice versa for ycut
    - if save is True, ./savefolder/saveprefix_bbox.plotformat is saved, given container.
    """
    figsize = params['figsize']
    cmap_cutout = params['cmap_cutout']
    minmax = params['minmax']
    plt.plot(figsize=figsize)
    m = np.isfinite(cutoutdata)
    vmin,vmax = np.percentile(cutoutdata[m],minmax[0]),np.percentile(cutoutdata[m],minmax[1])
    plt.imshow(cutoutdata,origin='lower',cmap=cmap_cutout,vmin=vmin,vmax=vmax)
    if maskdata is not None:
        cmap_mask = params['cmap_mask']
        alpha_mask = params['alpha_mask']
        plt.imshow(maskdata,origin='lower',cmap=cmap_mask,vmin=0.5,alpha=alpha_mask)
    if do_trace:
        if xcut is None or ycut is None or ww is None:
            raise ValueError('xcut,ycut,ww must be specified to plot trace')
        tcolor = tparams['tcolor']
        tls = tparams['tls']
        tlw = tparams['tlw']
        talpha = tparams['talpha']
        axpertick = aparams['axpertick']
        acolor_marker = aparams['acolor_marker']
        amarker = aparams['amarker']
        afontsize = aparams['afontsize']
        arotation = aparams['arotation']
        acolor_text = aparams['acolor_text']
        plt.plot(xcut,ycut,color=tcolor,ls=tls,lw=tlw,alpha=talpha)
        for i,ii in enumerate(xcut):
            if (i in {0,len(xcut)-1}) or (np.mod(i,axpertick)==0):
                label = '{0}A'.format(int(ww[i]))
                plt.plot(xcut[i],ycut[i],color=acolor_marker,marker=amarker)
                plt.annotate(label,(xcut[i],ycut[i]),
                             textcoords='offset points',
                             xytext=(0,10),
                             ha='center',
                             fontsize=afontsize,
                             rotation=arotation,
                             color=acolor_text
                            )
    if params['title'] == 'default':
        string = objname
    else:
        string = params['title']
    plt.title(string,fontsize=params['fontsize'])
    plt.tight_layout()
    if save:
        if container is None:
            raise ValueError('container must be specified to save')
        saveprefix = container.data['saveprefix']
        savefolder = container.data['savefolder']
        plotformat = container.data['plotformat']
        string = './{0}/{1}_bbox.{2}'.format(savefolder,saveprefix,plotformat)
        plt.savefig(string,format=plotformat,bbox_inches='tight')
        print('Save {0}'.format(string))
    