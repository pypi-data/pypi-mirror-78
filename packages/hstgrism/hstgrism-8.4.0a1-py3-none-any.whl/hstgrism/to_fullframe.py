# Kornpob Bhirombhakdi
# kbhirombhakdi@stsci.edu

from astropy.io import fits
import os

def to_fullframe(cutdata,fullfile,bb0x,bb1x,bb0y,bb1y,savesuffix,container):
    """
    to_fullframe replaces cutdata back to fullfile given bbcorner (bb0x,bb1x,bb0y,bb1y).
    The new file is created to ./savefolder/saveprefix_savesuffix.fits, given container and savesuffix.
    """
    saveprefix = container.data['saveprefix']
    savefolder = container.data['savefolder']
    # make a copy of fullfile to fullfile_new
    string = './{0}/{1}_{2}.fits'.format(savefolder,saveprefix,savesuffix)
    fullfile_new = (string,fullfile[1])
    os.system('cp {0} {1}'.format(fullfile[0],fullfile_new[0]))
    print('Make a copy of {0} to {1}'.format(fullfile[0],fullfile_new[0]))
    # replace
    tmp = fits.open(fullfile_new[0])
    tmp[fullfile_new[1]].data[bb0y:bb1y,bb0x:bb1x] = cutdata
    # save
    tmp.writeto(fullfile_new[0],overwrite=True)
    