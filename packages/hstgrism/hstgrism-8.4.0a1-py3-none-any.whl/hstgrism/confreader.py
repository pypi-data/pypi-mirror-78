# Kornpob Bhirombhakdi
# kbhirombhakdi@stsci.edu

import numpy as np

class ConfReader:
    '''
    ConfReader is a class to read aXe configuration file.
    - confile = path to aXe configuration file
    - beam = beam order
    Use method readall() to read every line in the file.
    Use self.beam to access extracted beam information.
    Use self.coef2d to access extracted coefficients.
    NOTE: use np.astype(type) to convert after extraction
    NOTE: can feed coef2d into Polynomial2D package (pip install polynomial2d) for further analysis
        (i.e., given X1,X2 arrays and obj.coef2d, Polynomial2D().fit() can decompress from 2D coef to 1D coef)
    '''
    def __init__(self,confile,beam):
        self.confile = confile
        self.beam = self._getbeam(beam)
        self.coef2d = self._make_coef2d()
    ##########
    ##########
    ##########
    def _getbeam(self,beam):
        #####
        # prepare keywords to read
        KEY = ['BEAM'+beam,'MMAG_EXTRACT_'+beam,'MMAG_MARK_'+beam,
               'DYDX_ORDER_'+beam,
               'XOFF_'+beam,'YOFF_'+beam,
               'DISP_ORDER_'+beam
              ]
        #####
        # open file and record value for each keyword
        f = open(self.confile,'r')
        tmpp = {}
        tmpp['BEAM'] = beam
        for i,ii in enumerate(f.readlines()):
            tmp = ii.split(' ')[0]
            if tmp in KEY:
                tmppp = np.array(ii.split()[1:])
                tmpp[tmp] = tmppp
        f.close()
        #####
        # get DYDX_{beam}_{order} and DLDP_{beam}_{order}
        tmpkey = {'DYDX_ORDER_'+beam:'DYDX_{0}_'.format(beam),
                  'DISP_ORDER_'+beam:'DLDP_{0}_'.format(beam)
                 }
        for i in tmpkey:
            order = int(tmpp[i][0])
            for j in np.arange(order+1):
                string = tmpkey[i]+str(j)
                f = open(self.confile,'r')
                for k,kk in enumerate(f.readlines()):
                    if string in kk.split(' '):
                        tmpp[string] = np.array(kk.split()[1:])
        #####
        # keep in self
        return tmpp
    ##########
    ##########
    ##########
    def _make_coef2d(self):
        beam = self.beam['BEAM']
        KEY = {'DYDX_ORDER_'+beam:'DYDX_{0}_'.format(beam),
               'DISP_ORDER_'+beam:'DLDP_{0}_'.format(beam)
              }
        tmpp = {}
        for i in KEY:
            order = int(self.beam[i][0])
            for j in np.arange(order+1):
                string = KEY[i]+str(j)
                tmp = self.beam[string]
                tmpp[string] = self._make_coef(tmp)
        return tmpp
    def _make_coef(self,coef):
        tmp = np.array(coef).astype(float)
        px1,px2,order = 0,0,0 # initialize
        out = {}
        out['NORDER'] = None
        out['COEF'] = {}
        for i in tmp:
            out['COEF'][(px1,px2)] = i
            px1-=1
            px2+=1
            if px1 < 0:
                order += 1
                px1 = order
                px2 = 0
        out['NORDER'] = order - 1
        return out
    ##########
    ##########
    ##########
    def readall(self):
        f = open(self.confile,'r')
        for i,ii in enumerate(f.readlines()):
            print(i,ii.split())
    
