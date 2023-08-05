# Kornpob Bhirombhakdi
# kbhirombhakdi@stsci.edu

import numpy as np
from scipy.integrate import quad

class ComputeTraceNWavelength:
    '''
    ComputeTraceNWavelength computes trace and wavelength in HST/aXe definition.
    This class can be easily used following ComputeSIP, and ConfReader.
    - coef1d can be computed through ComputeSIP.
    - xyref = (xref,yref) can be computed through ComputeXYREF. Assuming the trace runs along x.
    - xgbound = (xleft,xright) specifying the computing grid which is np.arange(xleft, xright).
    Use method compute() to compute trace and wavelength, which is access ible through self.output
    - output['dydx'],output['dldp'] are coefficients for calculating trace and wavelength respectively.
    - output['xh'] is the computing grid, which is related to grism frame by xg = xref + xh.
    - output['yh'] is the trace, which is related to grism frame by yg = yref + yh.
    - output['ww'] is wavelength in A.
    '''
    def __init__(self,coef1d,xyref,xgbound):
        self.data = {'coef1d':coef1d,
                     'xyref':xyref,
                     'xgbound':xgbound
                    }
        self.output = {'xyref':xyref,
                       'xgbound':xgbound,
                       'dydx':None,
                       'dldp':None,
                       'xh':None,
                       'yh':None,
                       'ww':None
                      }
    ##########
    ##########
    ##########
    def compute(self):
        coef1d = self.data['coef1d']
        xyref = self.data['xyref']
        xgbound = self.data['xgbound']
        dydx = self._get_coef('DYDX')
        dldp = self._get_coef('DLDP')
        xh = np.arange(xgbound[0],xgbound[1])
        # trace
        yh = 0.
        for i,ii in enumerate(dydx):
            yh += ii * np.power(xh,i)
        # wavelength
        varclength = np.vectorize(self._arclength)
        arc,earc = np.array(varclength(xh,*dydx))
        ww = 0.
        for i,ii in enumerate(dldp):
            ww += ii * np.power(arc,i)
        # output
        self.output['dydx'] = dydx.copy()
        self.output['dldp'] = dldp.copy()
        self.output['xh'] = xh.copy()
        self.output['yh'] = yh.copy()
        self.output['ww'] = ww.copy()
    def _get_coef(self,key):
        coef1d = self.data['coef1d']
        tmp = {}
        for i in coef1d:
            if i.split('_')[0] == key:
                tmp[int(i.split('_')[2])] = coef1d[i]
        n = len(tmp)
        dydx = []
        for i in range(n):
            dydx.append(tmp[i])
        return dydx
    def _arclength_integrand(self,Fa,*coef):
        # compute np.sqrt(1 + np.power(dydx,2))
        # dy = sum(i=0,i=n,DYDX_A_i*np.power(dx,i))
        # dydx = (dy/dx) = sum(i=0,i=n,i*DYDX_A_i*np.power(dx,i-1))
        # Fa = dx
        # coef = [DYDX_A_0,DYDX_A_1,...]
        s = 0
        for i,ii in enumerate(coef):
            if i==0:
                continue
            s += i * ii * np.power(Fa,i-1)
        return np.sqrt(1. + np.power(s,2))
    def _arclength(self,Fa,*coef):
        # compute integrate(from 0,to Fa,integrand np.sqrt(1 + np.power(dydx,2)))
        integral,err = quad(self._arclength_integrand, 0., Fa, args=coef)
        return integral,err 
