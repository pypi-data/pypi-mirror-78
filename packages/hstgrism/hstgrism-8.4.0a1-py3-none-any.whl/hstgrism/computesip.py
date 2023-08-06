# Kornpob Bhirombhakdi
# kbhirombhakdi@stsci.edu

from polynomial2d.polynomial2d import Polynomial2D

class ComputeSIP:
    '''
    ComputeSIP compute SIP given (x1,x2) as xyref, and coef2d from ConfReader. Note: x1 is the leading term in SIP.
    Polynomial2D is used (pip install polynomial2d).
    Use method compress() to compute the 1D coefficients using SIP model, which is accessible through self.coef1d.
    '''
    def __init__(self,coef2d,xyref):
        self.coef2d = coef2d
        x1,x2 = xyref
        self.x1 = x1
        self.x2 = x2
    def compress(self):
        out = {}
        for i in self.coef2d:
            tmp = self.coef2d[i]   
            obj = Polynomial2D()
            obj.model['NORDER'] = tmp['NORDER']
            obj.model['COEF'] = tmp['COEF']
            obj.data['X1'] = self.x1
            obj.data['X2'] = self.x2
            obj.compute(rescale=False)
            out[i] = obj.model['YFIT']
        self.coef1d = out           
