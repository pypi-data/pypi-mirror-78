# Kornpob Bhirombhakdi
# kbhirombhakdi@stsci.edu

from astropy.io import fits
import pandas as pd

class HeaderSummary:
    """
    header_summary is a class reading fits headers, and extracting relevant information regarding to HSTGRISM flow.
    - fits_file = (path_to_file, sci_extension)
    - params = dictionary with keyword = extension number, and values = keyword to look for in the header. If None, a preset params will be assigned.
      - Set self.params until satisfied.
    Use self.fetch() to fetch the information from headers, which can be access by self.table.
    Use self.save(Container) to save self.table to ./savefolder/saveprefix_hsum.csv given Container class object.
    For mutiple fits, use x = HeaderSummary(fits_file=None).combine(header_summary_list) where
    - header_summary_list = [x1,x2,x3,...] for each xi as HeaderSummary object.
    - This will return a dictionary of all HeaderSummary object tables. Use pandas.DataFrame to make it more readable.
    Use save(Container) method to output as ./savefolder/saveprefix_hsum.csv given Container object.
    - For multiple fits, use HeaderSummary(fits_file=None).save(Container,header_dict) where 
      - header_dict = HeaderSummary(fits_file=None).combine(header_summary_list)
    """
    def __init__(self,fits_file,params=None):
        self.fits_file = fits_file
        self.params = self._params() if params is None else params
        self.table = None
    ##################################################
    ##################################################
    ##################################################
    def save(self,container=None,header_dict=None):
        if container is None:
            raise ValueError('container must be specified to save.')
        folder,prefix = container.data['savefolder'],container.data['saveprefix']
        string = './{0}/{1}_hsum.csv'.format(folder,prefix)
        if self.fits_file is not None:
            pd.DataFrame(self.table,index=[0]).to_csv(string)
        else:
            pd.DataFrame(header_dict).to_csv(string)
        print('Save {0}'.format(string))
    ##################################################
    ##################################################
    ##################################################
    def combine(self,header_summary_list):
        """
        This function combines all HeaderSummary objects in the header_summary_list to a single object.
        To use, call HeaderSummary(fits_file=None).combine(header_summary_list).
        - header_summary_list = [x1,x2,x3,...] for each x as HeaderSummary object.
        It returns a ditionary combined
        """
        output_header = {}
        output_header['index'] = []
        output_header['filepath'] = []
        output_header['sci_ext_num'] = []
        for ii,i in enumerate(header_summary_list):
            index = ii
            header = header_summary_list[ii].table
            output_header['index'].append(index)
            output_header['filepath'].append(header_summary_list[ii].fits_file[0])
            output_header['sci_ext_num'].append(header_summary_list[ii].fits_file[1])
            for j in header:
                if j not in output_header.keys():
                    output_header[j] = []
                output_header[j].append(header[j])
        return output_header
    ##################################################
    ##################################################
    ##################################################
    def fetch(self):
        """
        Output a table given self.params
        """
        t = fits.open(self.fits_file[0])
        out = {}
        for i in self.params:
            try:
                h = t[i].header
            except:
                print('Cannot find extension {0} in file {1}'.format(i,self.fits_file[0]))
                continue
            for j in self.params[i]:
                try:
                    out[j] = h[j]
                except:
                    print('Cannot find keyword {0} in extension {1}.'.format(j,i))
                    out[j] = None
        self.table = out
    ##################################################
    ##################################################
    ##################################################
    def _params(self):
        """
        Output a dictionary as keyword = extension number, and values = keyword to look for in header.
        This function gives a preset.
        hdu = (extension_number,key1,key2,...)
        - sci extension number is given when instantiate.
        """
        try:
            phdu = (0,'ROOTNAME','DATE-OBS','FILTER','PA_V3','SUBARRAY','POSTARG1','POSTARG2','EXPSTART','EXPTIME',)
            shdu = (self.fits_file[1],'IDCSCALE','ORIENTAT')
            params = {phdu[0]:phdu[1:],shdu[0]:shdu[1:]}
            return params  
        except:
            return None
    