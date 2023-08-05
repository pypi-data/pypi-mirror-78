# Kornpob Bhirombhakdi
# kbhirombhakdi@stsci.edu

from astropy.io import fits
import pandas as pd
import numpy as np
import copy
from .confreader import ConfReader

class ComputeXYREF:
    """
    ComputeXYREF is a class to compute xyref before computing trace and wavelength of a grism. If xyref is known, user can skip this process.
    - xyd = (x,y) from associated direct image of the source
    - xydiff = (dx,dy) for the relative position shift between direct and grism images. For HST images, this can be computed as xydiff = f(POSTARG1_d,POSTARG2_d,SCALE_d,POSTARG1_g,POSTARG2_g,SCALE_g) = (POSTARG1_g,POSTARG2_g) / SCALE_g - (POSTARG1_d,POSTARG2_d) / SCALE_d for *_d and *_g for values of direct and grism images, respectively
    - xyoff = (x,y) = h(confile,beam) or user specifies (Note: xyoff can be used as an manual adjustment)
    Use method compute() to compute xyref, which is accessible through self.xyref.
    Use method save() to save ./savefolder/saveprefix_xyref.csv; container must be specified.
    #####
    For convenience, 
    - if xydiff = 'default', user must specify gfile and dfile, and a method will be called to compute xydiff.
        gfile and dfile = (filepath, extension) for grism and direct images respectively.
        We assume POSTARG1,POSTARG2 in zeroth extension header, and IDCSCALE in the specified extension header.
        These values will be used to compute xydiff.
        A fits image from HST observation (e.g., MAST archive) should be already satisfied this assumption.
    - if xyoff = 'default', user must specify confile and beam, and a method will be called to retrieve xyoff from the confile.
        confile = filepath to configuration file
        beam = beam order
        We assume aXe configuration file with 'XOFF_A' and 'YOFF_A' for the xyoff given beam 'A' (for example)
    """
    def __init__(self,xyd,xydiff,xyoff,confile=None,beam=None,gfile=None,dfile=None,container=None):
        self.container = container
        self.data = {'xyd':xyd,
                     'xydiff':xydiff,
                     'xyoff':xyoff,
                     'confile':confile,
                     'beam':beam,
                     'gfile':gfile,
                     'dfile':dfile,
                     'xyref':'None'
                    }
        if xyoff == 'default':
            if confile is None or beam is None:
                raise ValueError('confile and beam must be specified for xyoff = "default"')
            self.data['xyoff'] = self._xyoff()
        if xydiff == 'default':
            if gfile is None or dfile is None:
                raise ValueError('gfile and dfile must be specified for xydiff = "default"')
            self.data['xydiff'] = self._xydiff()
    def _xyoff(self):
        confile = self.data['confile']
        beam = self.data['beam']
        conf = ConfReader(confile,beam)
        self.conf = conf
        confbeam = self.conf.beam
        return (confbeam['XOFF_'+beam].astype(float)[0],confbeam['YOFF_'+beam].astype(float)[0])
    def _xydiff(self):
        gfile = self.data['gfile']
        dfile = self.data['dfile']
        tmpg = fits.open(gfile[0])
        tmpd = fits.open(dfile[0])
        self.postarg_g= np.array([tmpg[0].header['POSTARG1'],tmpg[0].header['POSTARG2'],tmpd[gfile[1]].header['IDCSCALE']])
        self.postarg_d= np.array([tmpd[0].header['POSTARG1'],tmpd[0].header['POSTARG2'],tmpd[dfile[1]].header['IDCSCALE']])
        POSTARG1_g,POSTARG2_g,SCALE_g = self.postarg_g
        POSTARG1_d,POSTARG2_d,SCALE_d = self.postarg_d
        xydiff = np.array([POSTARG1_g,POSTARG2_g]) / SCALE_g - np.array([POSTARG1_d,POSTARG2_d]) / SCALE_d
        return xydiff
    ##########
    ##########
    ##########
    def compute(self):
        xyd,xydiff,xyoff = self.data['xyd'],self.data['xydiff'],self.data['xyoff']
        self.data['xyref'] = xyd + xydiff + xyoff
    ##########
    ##########
    ##########
    def save(self):
        if self.container is None:
            raise ValueError('container must be specified for saving. See hstgrism.container.Container class')
        saveprefix = self.container.data['saveprefix']
        savefolder = self.container.data['savefolder']
        string = './{1}/{0}_xyref.csv'.format(saveprefix,savefolder)
        tmp = copy.deepcopy(self.data)
        tmp['confile'] = (tmp['confile'],None)
        tmp['beam'] = (tmp['beam'],None)
        tmp = pd.DataFrame.from_dict(tmp, orient='index').T
        tmp.to_csv(string) 
        print('Save {0}'.format(string))
    