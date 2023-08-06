# Kornpob Bhirombhakdi
# kbhirombhakdi@stsci.edu

from astropy.io import fits
import numpy as np

class ObjectMask:
    """
    ObjectMask is a class to generate an object mask, which is a 2D image of boolean for True = object.
    - nx,ny is the shape of the image
    - tx,ty is the trace
    - halfdyup,halfdylow is the aperture width from the trace (i.e., the total width is halfdylow + 1 + halfdyup)
    - Note: given (txi,tyi), image[tyi-halfdylow:tyi+1+halfdyup,txi] = True    
    Use method compute() to generate the object mask, which is accessible through self.mask.
    Use method save(container) to save the mask image as ./savefolder/saveprefix_mask.fits given container.
    - container is an object of hstgrism.container.Container class
    Note: if cutout.fits and bbcorner.csv was created from Cutout2D, together with trace.csv from earlier process, a simple way to create an object mask is:
    - Set ny,nx = gdata.shape where gdata is the image from cutout.fits
    - tx = trace.xh + trace.xyref[0] - bbcorner.bb0x[0] where trace from trace.csv and bbcorner from bbcorner.csv
    - ty is similar to tx
    - halfdyup, halfdylow are arbitrary
    """
    def __init__(self,nx,ny,tx,ty,halfdyup,halfdylow):
        self.nx = nx
        self.ny = ny
        self.tx = tx
        self.ty = ty
        self.halfdyup = halfdyup
        self.halfdylow = halfdylow
        self.mask = None
    def compute(self):
        tmp = np.arange(self.nx*self.ny).reshape(self.ny,self.nx)
        tmp = np.full_like(tmp,False,dtype=bool)
        for i,ii in enumerate(self.tx):
            xx,yy = self.tx[i],self.ty[i]
            if int(xx) < 0 or int(xx) > self.nx - 1:
                continue
            ymin = max(0,int(yy-self.halfdylow))
            ymax = min(self.ny,int(yy+1+self.halfdyup))
            tmp[ymin:ymax,int(xx)] = True        
        self.mask = tmp.copy()
    def save(self,container=None):
        if container is None:
            raise ValueError('container must be specified to save')
        savefolder = container.data['savefolder']
        saveprefix = container.data['saveprefix']
        phdu = fits.PrimaryHDU()
        imhdu = fits.ImageHDU()
        hdul = fits.HDUList([phdu,imhdu])
        hdul[1].data = self.mask.astype(int)
        string = './{0}/{1}_mask.fits'.format(savefolder,saveprefix)
        hdul.writeto(string,overwrite=True)
        print('Save {0}'.format(string))
    