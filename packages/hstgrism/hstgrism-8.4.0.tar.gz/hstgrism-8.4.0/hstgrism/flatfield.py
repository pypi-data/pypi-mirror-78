# Kornpob Bhirombhakdi
# kbhirombhakdi@stsci.edu

from astropy.io import fits
import copy
import numpy as np
import pandas as pd

class FlatField:
    '''
    FlatField computes a flatfield image in aXe definition.
    This requires flatfile produced for aXe, and trace.csv produced by hstgrism package.
    - container = Container object
    - xyref and dldp can be found in trace.csv
    Use method compute() to generate flatfield image, which is accessible through self.flatfield.
    Use method save() to save the flatfield image in full frame as ./savefolder/saveprefix_fullflate.fits
    - if save(do_cutout=True), this will also save a cutout, given bbx0x,bb1x,bb0y,bb1y (which can be found in bbcorner.csv if produced by earlier step).
        The cutout is saved as ./savefolder/saveprefix_cutflat.fits
    '''
    def __init__(self,container,flatfile,xyref,dldp):
        self.container = container
        self.flatfile = flatfile
        self.xyref = xyref
        self.dldp = dldp
        self.data = {'WMIN':None,
                     'WMAX':None,
                     'FLAT':None,
                     'NAX1':None,
                     'NAX2':None,
                     'WW':None
                    }
        self.flatfield = None
        self._get()
    def _get(self):
        # basic info
        tmp = fits.open(self.flatfile)
        wmin,wmax = tmp[0].header['WMIN'],tmp[0].header['WMAX']
        nax1,nax2 = tmp[0].header['NAXIS1'],tmp[0].header['NAXIS2']
        self.data['WMIN'] = wmin
        self.data['WMAX'] = wmax
        self.data['NAX1'] = nax1
        self.data['NAX2'] = nax2
        # flat
        n = len(tmp)
        tmpp = {}
        for i in range(n):
            tmpp[i] = tmp[i].data.copy()
        self.data['FLAT'] = copy.deepcopy(tmpp)
        # wavelength
        dldp = self.dldp
        m = np.isfinite(dldp)
        dldp = dldp[m].values
        xg = np.arange(self.data['NAX1'])
        xref = int(self.xyref[0])
        xh = xg-xref
        ww = np.full_like(xh,0.,dtype=float)
        for i,ii in enumerate(dldp):
            ww += ii * np.power(xh,i)
        self.data['WW'] = ww
        self.data['XG'] = xg
        self.data['XREF'] = xref
    ##########
    ##########
    ##########
    def compute(self):
        # dimension test
        if self.data['WW'].shape[0] != self.data['NAX1']:
            raise ValueError('Dimension of WW != NAX1')
        # set parametric wavelength [0,1]
        wmin,wmax,ww = self.data['WMIN'],self.data['WMAX'],self.data['WW']
        paramww = (ww-wmin)/(wmax-wmin)
        paramww[paramww<0.] = 0.
        paramww[paramww>1.] = 1.
        paramww,_ = np.meshgrid(paramww,np.arange(self.data['NAX2']))
        # compute
        tmp = self.data['FLAT']
        tmpp = np.full_like(paramww,0.,dtype=float)
        for i in tmp:
            tmpp += tmp[i] * np.power(paramww,i)
        self.flatfield = tmpp.copy()
    ##########
    ##########
    ##########
    def save(self,
             do_cutout=False,bb0x=None,bb1x=None,bb0y=None,bb1y=None
            ):
        if self.container is None:
            raise ValueError('container must be specified to save')
        savefolder = self.container.data['savefolder']
        saveprefix = self.container.data['saveprefix']
        # fullflat
        phdu = fits.PrimaryHDU()
        imhdu = fits.ImageHDU()
        hdul = fits.HDUList([phdu,imhdu])
        hdul[1].data = self.flatfield
        string = './{0}/{1}_fullflat.fits'.format(savefolder,saveprefix)
        hdul.writeto(string,overwrite=True)
        print('Save {0}'.format(string))
        # cutflat
        if do_cutout:
            if bb0x is None or bb1x is None or bb0y is None or bb1y is None:
                raise ValueError('bb0x,bb1x,bb0y,bb1y must be specified to save cutout')
            phdu = fits.PrimaryHDU()
            imhdu = fits.ImageHDU()
            hdul = fits.HDUList([phdu,imhdu])
            hdul[1].data = self.flatfield[bb0y:bb1y,bb0x:bb1x]
            string = './{0}/{1}_cutflat.fits'.format(savefolder,saveprefix)
            hdul.writeto(string,overwrite=True)
            print('Save {0}'.format(string))
        