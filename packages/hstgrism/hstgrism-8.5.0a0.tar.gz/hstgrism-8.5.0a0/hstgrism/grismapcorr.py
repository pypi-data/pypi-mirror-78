# Kornpob Bhirombhakdi
# kbhirombhakdi@stsci.edu

import numpy as np
from scipy.interpolate import interp2d
import copy

class GrismApCorr:
    """
    GrismApCorr is a class containing tables for aperture correction (i.e., apcorr = f(wavelength, apsize)) in aXe reduction. These tables are from ISRs. Interpolaton model is also prepared.
    - Available instrument can be found by GrismApCorr().available_instrument.
    - apsize is an array with the same length as wave, and must be diameter in arcsec. This can be computed as apsize = (halfdyup + 1 + halfdylow) * scale where (halfdyup,halfdylow) can be found in tbox.csv (if generated from earlier process), and scale can be found from GrismApCorr().table[instrument]['scale'].
    - Note: halfdyup must be equal to halfdylow according to the ISRs.
    - wave is an array of wavelengths, and must be in Angstrom.
    Use method compute() after instantiating the GrismApCorr object correctly to return the aperture correction values, which is accessible through self.data['apcorr'].
    - Note: compute(fill_value='median') is the only implementation in this version. This will replace any out-of-bound values with median value calculated from in-bound values.
    ##########
    x = GrismApCorr()
    x.table = show apcorr tables with keys as intrument codes. Use x.instrument to check which instrument is available.
    x.instrument = show available instrument codes
    x.table[instrument]['model'](wave,apsize) = calculate apcorr given a model corresponding to its instrument, wavelength, and aperture size.
    ##########
    Note: to avoid crash, and to support wider wavelength, we manually added min and max wavelengths to the tables.
    - for HST-WFC3-IR-G102: we added 7000. and 12000.
    - for HST-WFC3-IR-G141: we added 11000. and 17000.
    - for HST-WFC3-UVIS1-G280: we added 2000. and 8000.
    - apcorr values for these additional columns were set to be the nearest available values.
    - This change would simply make the interpolation of apcorr outside the original bounds to be nearest neighbour.
    """    
    def __init__(self,instrument=None,apsize=None,wave=None,aptype='diameter',apunit='arcsec',waveunit='A'):
        self.table = self._get_table()
        self.available_instrument = self.table.keys()
        self.data = {'instrument':None,
                     'apsize':None,
                     'aptype':aptype,
                     'apunit':apunit,
                     'wave':None,
                     'waveunit':waveunit,
                     'apcorr':None
                    }
        if instrument is not None:
            self.data['instrument'] = instrument
        if apsize is not None:
            self.data['apsize'] = apsize
        if wave is not None:
            self.data['wave'] = wave
    def compute(self,fill_value='median'):
        if fill_value == 'median':
            fill = np.nan
        instrument = self.data['instrument']
        apsize = self.data['apsize']
        aptype = self.data['aptype']
        apunit = self.data['apunit']
        wave = self.data['wave']
        waveunit = self.data['waveunit']
        table = self.table[instrument]
        # check aptype
        if aptype != table['type']:
            raise ValueError('aptype not equal {0}'.format(table['type']))
        # check apunit
        if apunit != table['apunit']:
            if table['apunit'] == 'arcsec' and table['scaleunit'] == 'arcsec/pix' and apunit == 'pix':
                apsize = apsize * table['scale']
                apunit = 'arcsec'
                self.data['apsize'] = apsize
                self.data['apunit'] = apunit
                print('Scale apsize in {0} with {1} {2}'.format(apunit,table['scale'],table['scaleunit']))
            else:
                raise ValueError('apunit not equal {0} or pix'.format(table['apunit']))
        # check waveunit
        if waveunit != table['waveunit']:
            raise ValueError('waveunit not equal {0}'.format(table['waveunit']))
        model = self._model(table['wave'],table['apsize'],table['value'],fill)
        apcorr = model(wave,apsize).diagonal()
        if fill_value == 'median':
            tmp = apcorr.copy()
            m_good = np.argwhere(np.isfinite(tmp)).flatten()
            m_bad = np.argwhere(~np.isfinite(tmp)).flatten()
            median = np.median(tmp[m_good])
            tmp[m_bad] = median
            apcorr = tmp.copy()
            print('Replace bad apcorr values with median = {0:.3f}'.format(median))
        self.data['apcorr'] = apcorr
    def _model(self,wave,apsize,value,fill_value):
        model = interp2d(wave,apsize,value,kind='linear',copy=True,
                         bounds_error=False,fill_value=fill_value
                        )
        return model  
    def _get_table(self):
        ##########
        # Tables from ISRs
        TABLE = {'HST-WFC3-IR-G102': 
                 {'ref': 'ISR WFC3-2011-05'
                  ,'filter': 'G102'
                  ,'scale': 0.13
                  ,'scaleunit': 'arcsec/pix'
                  ,'type': 'diameter'
                  ,'row': 'apsize'
                  ,'col': 'wave'
                  ,'apunit': 'arcsec'
                  ,'apsize': np.array((0.128,0.385,0.641
                                       ,0.898,1.154,1.411
                                       ,1.667,1.924,3.719
                                       ,7.567,12.954,25.779
                                      ))
                  ,'waveunit': 'A'
                  ,'wave': np.array((7000.,8850.,9350.,9850.,10350.,10850.,11350.,12000.))
                  ,'value' : np.array(((0.459,0.459,0.391,0.414,0.464,0.416,0.369,0.369)
                                      ,(0.825,0.825,0.809,0.808,0.811,0.794,0.792,0.792)
                                      ,(0.890,0.890,0.889,0.887,0.880,0.875,0.888,0.888)
                                      ,(0.920,0.920,0.917,0.916,0.909,0.904,0.916,0.916)
                                      ,(0.939,0.939,0.937,0.936,0.930,0.925,0.936,0.936)
                                      ,(0.952,0.952,0.950,0.950,0.943,0.940,0.949,0.949)
                                      ,(0.962,0.962,0.961,0.961,0.954,0.951,0.958,0.958)
                                      ,(0.969,0.969,0.968,0.969,0.962,0.959,0.965,0.965)
                                      ,(0.985,0.985,0.984,0.986,0.982,0.980,0.983,0.983)
                                      ,(0.995,0.995,0.995,0.996,0.991,0.990,0.992,0.992)
                                      ,(0.999,0.999,0.999,0.999,0.997,0.996,0.995,0.995)
                                      ,(1.000,1.000,1.000,1.000,1.000,1.000,1.000,1.000)
                                     ))
                  ,'model': None
                 }
                 ,'HST-WFC3-IR-G141':
                 {'ref': 'ISR WFC3-2011-05'
                  ,'filter': 'G141'
                  ,'scale': 0.13
                  ,'scaleunit': 'arcsec/pix'
                  ,'type': 'diameter'
                  ,'row': 'apsize'
                  ,'col': 'wave'
                  ,'apunit': 'arcsec'
                  ,'apsize': np.array((0.128,0.385,0.641
                                       ,0.898,1.154,1.411
                                       ,1.667,1.924,3.719
                                       ,7.567,12.954,25.779
                                      ))   
                  ,'waveunit': 'A'
                  ,'wave': np.array((11000.,11300.,12300.,13300.,14300.,15300.,16300.,17000.))
                  ,'value': np.array(((0.442,0.442,0.444,0.395,0.344,0.342,0.376,0.376)
                                     ,(0.805,0.805,0.792,0.764,0.747,0.732,0.732,0.732)
                                     ,(0.866,0.866,0.877,0.865,0.863,0.850,0.859,0.859)
                                     ,(0.912,0.912,0.901,0.893,0.894,0.884,0.898,0.898)
                                     ,(0.933,0.933,0.924,0.914,0.913,0.903,0.913,0.913)
                                     ,(0.947,0.947,0.940,0.931,0.932,0.921,0.932,0.932)
                                     ,(0.958,0.958,0.950,0.942,0.944,0.934,0.945,0.945)
                                     ,(0.966,0.966,0.959,0.951,0.953,0.944,0.954,0.954)
                                     ,(0.985,0.985,0.984,0.981,0.985,0.980,0.985,0.985)
                                     ,(0.993,0.993,0.995,0.992,0.997,0.992,0.996,0.996)
                                     ,(0.996,0.996,0.998,0.997,1.000,0.997,1.000,1.000)
                                     ,(1.000,1.000,1.000,1.000,1.000,1.000,1.000,1.000)
                                    ))
                  ,'model': None
                 }
                 ,'HST-WFC3-UVIS1-G280':
                 {'ref': 'ISR WFC3-2009-01'
                  ,'filter': 'G280'
                  ,'scale': 0.04
                  ,'scaleunit': 'arcsec/pix'
                  ,'type': 'diameter'
                  ,'row': 'apsize'
                  ,'col': 'wave'
                  ,'apunit': 'arcsec'
                  ,'apsize': np.array((0.04,0.12,0.20,
                                       0.28,0.36,0.44,
                                       0.52,0.60,1.16,
                                       2.36,4.04,8.04
                                      ))   
                  ,'waveunit': 'A'
                  ,'wave': np.array((2000.,2275.,2825.,3375.,3925.,4475.,5025.,8000.))
                  ,'value': np.array(((0.312,0.312,0.312,0.276,0.258,0.261,0.241,0.241)
                                     ,(0.720,0.720,0.706,0.676,0.642,0.600,0.589,0.589)
                                     ,(0.856,0.856,0.848,0.839,0.815,0.767,0.769,0.769)
                                     ,(0.903,0.903,0.899,0.897,0.882,0.840,0.855,0.855)
                                     ,(0.926,0.926,0.926,0.926,0.913,0.875,0.895,0.895)
                                     ,(0.939,0.939,0.942,0.944,0.933,0.898,0.916,0.916)
                                     ,(0.947,0.947,0.951,0.956,0.947,0.915,0.931,0.931)
                                     ,(0.953,0.953,0.957,0.963,0.956,0.928,0.944,0.944)
                                     ,(0.974,0.974,0.978,0.983,0.978,0.960,0.973,0.973)
                                     ,(0.990,0.990,0.992,0.994,0.991,0.983,0.989,0.989)
                                     ,(0.995,0.995,0.997,0.998,0.997,0.994,0.996,0.996)
                                     ,(1.000,1.000,1.000,1.000,1.000,1.000,1.000,1.000)
                                    ))
                  ,'model': None
                 }
                }
        return TABLE
