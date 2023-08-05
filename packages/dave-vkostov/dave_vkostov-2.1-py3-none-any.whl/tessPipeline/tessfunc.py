"""
Created on Tue Nov 27 21:44:04 2018

@author: fergal
"""

from __future__ import division

from pdb import set_trace as debug
import matplotlib.pyplot as plt
import matplotlib.patches as mpatch
import matplotlib as mpl
import pandas as pd
import numpy as np
from astroquery.mast import Tesscut
from astropy.coordinates import SkyCoord
from dave.tessPipeline.tessio import TessDvtLocalArchive
from dave.tessPipeline.tessmastio import TessAstroqueryArchive
import os
import eleanor
import lightkurve as lk

def serve(sector, tic, planetNum, localPath, source_):
    
    ar = TessAstroqueryArchive(localPath)
#    ar = TessDvtLocalArchive(localPath)
        
    if source_ == "tess_2min":
#        if planetNum > 1:
#            planetNum = 1
        try:
            dvt, hdr = ar.getDvt(tic, sector, ext=planetNum, header=True)
        except:
            dvt, hdr = ar.getLightcurve(tic, sector, ext=1, header=True)
#        dvt, hdr = ar.getLightcurve(tic, sector, ext=planetNum, header=True)
        tpf, hdr_tpf = ar.getTPF(tic, sector, ext=1, header=True)

        mask, mask_hdr = ar.getTPF(tic, sector, ext=2, header=True)

    return dvt, hdr, tpf, hdr_tpf, mask, mask_hdr

#    elif source_ == "tess_FFI_eleanor":
#        star = eleanor.Source(tic=int(tic), tc = True, sector = sector)
#        data = eleanor.TargetData(star, do_psf = False, do_pca = True)
        
#        flags = data.quality == 0
#        time = data.time[flags]
#        lc = data.pca_flux[flags]/np.nanmean(data.pca_flux[flags])
#        hdr  = data.header
#        tpf = data.tpf

#        return flags, time, lc, hdr, tpf

def serve_TESS_FFI(sector_, tic_):
    star = eleanor.Source(tic=tic_, tc = True, sector = sector_)
    data = eleanor.TargetData(star, do_psf = False, do_pca = False)
        
    flags = data.quality == 0
    time = data.time
    lc = data.corr_flux/np.nanmedian(data.corr_flux)
    hdr  = data.header
    tpf = data.tpf

    mask = np.ones(data.aperture.shape, dtype=bool)
    mask[data.aperture != 0.] = False

#    print(flags.shape, time.shape, lc.shape, tpf.shape)
#    xxxx

    return flags, time, lc, hdr, tpf, mask, hdr

def getOutputBasename(basePath, tic):
    """Get the output basename for any files a task creates

    Inputs:
    ----------
    basePath
        (string) Path where all files should be output
    epic
        (int or string) Epic number of star


    Returns:
    -----------
    (string) a basename for files.


    Outputs:
    ----------
    Function attempts to create output directory if it doesn't exist.

    Example:
    -------------
    >>> getOutputBasename("/home/dave/c6", 123456789)
    "/home/dave/c6/123456789/123456789"

    The calling task can then create a bunch files like
    "/home/dave/c6/123456789/123456789-file1.txt"
    "/home/dave/c6/123456789/123456789-image1.png" etc.
    """

    ticStr = str(int(tic))
    path = os.path.join(basePath, ticStr)

    if not os.path.exists(path):
        os.mkdir(path)
    if not (os.access(path, os.W_OK)):
        raise IOError("Can't write to output directory %s" %path)

    return os.path.join(path, ticStr)
