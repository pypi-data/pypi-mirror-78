# Kornpob Bhirombhakdi
# kbhirombhakdi@stsci.edu

from hstgrism.objectmask import ObjectMask
from astropy.io import fits
import numpy as np
import pandas as pd

class Cutout2D:
    """
    Cutout2D is a class to make a 2D cutout of an image.
    - tbox['xg'] and tbox['yg'] specifies the trace.
    - tbox['halfdyup'] and tbox['halfdylow'] specified the aperture width (up and down respectively) from the trace. Note: Total width is halfdylow + 1 + halfdyup.
    - tbox defines the trace region. Only max and min of xg and yg (together with halfdyup and halfdylow) would be used to define the trace box. 
    - However, complete arrays of xg and yg are necessary when creating an object mask. Otherwise, only min and max of xg and yg are necessary to specify the cutout region.
    - bbox specifies an outer box surrounding the trace region. 
    - Note: Total x width is padxleft + (max_xg - min_xg + 1) + padxright, and total y width is padylow + halfdylow + (max_yg - min_yg + 1) + halfdyup + padyup.
    - image = full image to be cut.
    - self.bbcorner provides the left-bottom corner (bb0x,bb0y) and right-upper corner (bb1x,bb1y) computed using the specified tbox and bbox.
    Use method compute() to make a 2D cutout, which is accessible through self.cutout.
    - Set compute(do_mask = True) if user also wants an object mask, which is accessible through self.mask.
    - self.mask = True in the trace region.
    Use method save() to save the output to files, given container.
    - save(tbox,bbox,bbcorner,cutout,mask) are switches to turn on/off what user would like to save. By default, save everything.
    """
    def __init__(self,
                 tbox = {'xg':None,
                         'yg':None,
                         'halfdyup':None,
                         'halfdylow':None
                        },
                 bbox = {'padxleft':15,
                         'padxright':15,
                         'padyup':15,
                         'padylow':15
                        },
                 image = None,
                 container = None
                ):
        if tbox['xg'] is None or tbox['yg'] is None or tbox['halfdyup'] is None or tbox['halfdylow'] is None:
            raise ValueError('tbox must be specified')
        self.tbox = tbox
        self.bbox = bbox
        self.bbcorner = self._bbcorner()
        self.image = image
        self.container = container
        self.cutout = None
        self.mask = None
    def _bbcorner(self):
        minxg,maxxg = self.tbox['xg'].min(),self.tbox['xg'].max()
        minyg,maxyg = self.tbox['yg'].min(),self.tbox['yg'].max()
        bb0x = int(minxg - self.bbox['padxleft'])
        bb1x = int(maxxg + 1 + self.bbox['padxright'])
        bb0y = int(minyg - self.tbox['halfdylow'] - self.bbox['padylow'])
        bb1y = int(maxyg + 1 + self.tbox['halfdyup'] + self.bbox['padyup'])
        return {'bb0x':bb0x,'bb1x':bb1x,'bb0y':bb0y,'bb1y':bb1y}
    ##########
    ##########
    ##########
    def compute(self,do_mask=True):
        if self.image is None:
            raise ValueError('image must be specified')
        bb0x,bb1x = self.bbcorner['bb0x'],self.bbcorner['bb1x']
        bb0y,bb1y = self.bbcorner['bb0y'],self.bbcorner['bb1y']
        self.cutout = self.image[bb0y:bb1y,bb0x:bb1x].copy()
        if do_mask:
            self.mask = self._mask()
    def _mask(self):
        bb0x,bb1x = self.bbcorner['bb0x'],self.bbcorner['bb1x']
        bb0y,bb1y = self.bbcorner['bb0y'],self.bbcorner['bb1y']
        ny,nx = self.image.shape
        tx,ty = self.tbox['xg'],self.tbox['yg']
        halfdyup,halfdylow = self.tbox['halfdyup'],self.tbox['halfdylow']
        maskobj = ObjectMask(nx,ny,tx,ty,halfdyup,halfdylow)
        maskobj.compute()
        return maskobj.mask[bb0y:bb1y,bb0x:bb1x]    
    ##########
    ##########
    ##########
    def save(self,tbox=True,bbox=True,bbcorner=True,cutout=True,mask=True):
        if self.container is None:
            raise ValueError('container must be specified')
        saveprefix = self.container.data['saveprefix']
        savefolder = self.container.data['savefolder']
        if tbox:
            string = './{0}/{1}_tbox.csv'.format(savefolder,saveprefix)
            tmp = pd.DataFrame(self.tbox)
            tmp.to_csv(string)
            print('Save {0}'.format(string))
        if bbox:
            string = './{0}/{1}_bbox.csv'.format(savefolder,saveprefix)
            tmp = pd.DataFrame.from_dict(self.bbox, orient='index').T
            tmp.to_csv(string)
            print('Save {0}'.format(string))
        if bbcorner:
            string = './{0}/{1}_bbcorner.csv'.format(savefolder,saveprefix)
            tmp = pd.DataFrame.from_dict(self.bbcorner, orient='index').T
            tmp.to_csv(string)
            print('Save {0}'.format(string))
        if cutout:
            phdu = fits.PrimaryHDU()
            imhdu = fits.ImageHDU()
            hdul = fits.HDUList([phdu,imhdu])
            hdul[1].data = self.cutout
            string = './{0}/{1}_cutout.fits'.format(savefolder,saveprefix)
            hdul.writeto(string,overwrite=True)
            print('Save {0}'.format(string))
        if mask:
            phdu = fits.PrimaryHDU()
            imhdu = fits.ImageHDU()
            hdul = fits.HDUList([phdu,imhdu])
            hdul[1].data = self.mask.astype(int)
            string = './{0}/{1}_mask.fits'.format(savefolder,saveprefix)
            hdul.writeto(string,overwrite=True)
            print('Save {0}'.format(string))
                    