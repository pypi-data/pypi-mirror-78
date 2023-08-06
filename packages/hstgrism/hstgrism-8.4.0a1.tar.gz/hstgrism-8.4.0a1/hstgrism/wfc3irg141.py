# Kornpob Bhirombhakdi
# kbhirombhakdi@stsci.edu

import pandas as pd
import copy
from .confreader import ConfReader
from .computesip import ComputeSIP
from .computetracenwavelength import ComputeTraceNWavelength

class WFC3IRG141:
    """
    WFC3IRG141 is a class for a grism object HST/WFC3/IR/G141. Call this to initiate computing trace and wavelength.
    - confile = path to aXe configuration file
    - beam = beam order
    - xyref = (x,y) for the reference pixel location (Note: use can use hstgrism.ComputeXYREF class to compute this)
    xgbound is a preset to optimize the extraction region to be about 9900 to 18000 A for HST/WFC3/IR/G102, beam 'A'. Set xgbound will change the region.
    Use method compute() to compute trace and wavelength.
    Use method save() to save file saveprefix_trace.csv, given container.
    """
    def __init__(self,confile,beam,xyref,xgbound=(20,195),container=None):
        self.container = container
        self.data = {'confile':confile,
                     'beam':beam,
                     'xyref':xyref,
                     'xgbound':xgbound
                    }
        self.conf = self._conf()
    def _conf(self): 
        confile = self.data['confile']
        beam = self.data['beam']
        conf = ConfReader(confile,beam)
        return conf
    ##########
    ##########
    ##########
    def compute(self):
        xyref = self.data['xyref']
        xgbound = self.data['xgbound']
        conf = self.conf
        obj = ComputeSIP(conf.coef2d,xyref)
        obj.compress()
        newobj = ComputeTraceNWavelength(obj.coef1d,xyref,xgbound)
        newobj.compute()
        self.output = newobj.output
    ##########
    ##########
    ##########
    def save(self):
        if self.container is None:
            raise ValueError('container must be specified for saving. See hstgrism.container.Container class')
        saveprefix = self.container.data['saveprefix']
        savefolder = self.container.data['savefolder']
        string = './{1}/{0}_trace.csv'.format(saveprefix,savefolder)
        tmp = copy.deepcopy(self.output)
        tmp = pd.DataFrame.from_dict(tmp, orient='index').T
        tmp.to_csv(string) 
        print('Save {0}'.format(string))
        