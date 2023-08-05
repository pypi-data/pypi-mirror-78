
"""
Created on Sun Dec  2 21:03:02 2018

@author: fergal
"""

from __future__ import print_function
from __future__ import division

from pdb import set_trace as debug
import matplotlib.pyplot as plt
import numpy as np
from statistics import mode

import dave.diffimg.fastpsffit as ddf
from dave.misc.plateau import plateau
import dave.fileio.kplrfits as kplrfits
from astropy.coordinates import SkyCoord
from astroquery.mast import Tesscut
from astropy.wcs import WCS

def measurePerTransitCentroids(time, cube, period_days, epoch_days, duration_days, clip, plotFilePattern=None):#mask, hdr_tpf, plotFilePattern=None):#plotFilePattern):#
    """Measure difference image centroids for each transit in a data set
    
    For each transit, compute the centroid of a image reprsenting the the position of the star before transit,
    after transit, and the difference image. 

    Not working yet. Before and After centroids are in the wrong place
    
    Inputs
    --------
    time
        (1d np array) Times of cadences
    cube
        (3d np array) Contents of TPF file for this target
    period_days
        (float) Period of transit
    epoch_days
        (float) Time of first transit
    duration_days
        (float) Duration of transit. Results aren't strongly dependent on whether you choose total
        transit time, or just from end of ingress to start of egress, but the latter is preferable
        
    Optional Inputs
    -------------
    plotFilePattern
        If **None**, genereate no diagnostic plots. Otherwise, save plots to this path and file root
        
    Returns
    ---------
    A dictionary.
    """
    plot = True
    if plotFilePattern is None:
        plot = False
    
#    if plotFilePattern is not None:
#        raise NotImplementedError("Plots not implemented yet")
               
#    flux = clip['detrend.detrendFlux']
    isnan = np.isnan(time)
    time = time[~isnan]
#    flux = flux[~isnan]
    cube = cube[~isnan]

#    print(time.shape, flux.shape, cube.shape)

    out = dict()
    transits = getIngressEgressCadences(time, period_days, epoch_days, duration_days)
    
    good_transit_flags_ = []
    bad_transit_flags_ = np.zeros(len(transits), dtype = bool)

    for ii in range(len(transits)):
        cin = transits[ii]

        res = measureCentroidShift(cube, cin, ii, clip, plot)#mask, hdr_tpf, plot)
#            if res['errorCode'] < 7:
        out['transit-%04i' %(ii)] = res
#                good_transit_flags_.append(ii)
#            else:
#                bad_transit_flags_[ii] = True
#                print('Transit', str(ii), 'bad')

        if plotFilePattern is not None:
#             print(plotFilePattern)
#             plt.suptitle('%s-trans%02i' %(plotFilePattern , ii))
#             plt.savefig('%s-trans%02i.png' %(plotFilePattern , ii), transparent=True)
#             plt.savefig('%s-trans%02i.jpg' %(plotFilePattern , ii), bbox_inches='tight', pad_inches=0)

#             print(str(tic_[ii]), ',ExoFOP-TESS,','https://exofop.ipac.caltech.edu/tess/target.php?id=', str(tic_[ii]), ',RA=',ra_[0], ',Dec=', dec_[0])
             plt.savefig('%s-trans%02i.jpg' %(plotFilePattern , ii), bbox_inches='tight', pad_inches=0)
             plt.show()
             plt.close()

    results = np.zeros((len(transits), 6))#np.zeros((len(good_transit_flags_), 6))#
    for i in range(len(transits)):
        key = 'transit-%04i' %(i)
        results[i,:2] = out[key]['beforeCentroid']
        results[i,2:4] = out[key]['diffCentroid']
        results[i,4:6] = out[key]['afterCentroid']

    out['results'] = results
    return out
##
##
##
def getIngressEgressCadences(time, period_days, epoch_btjd, duration_days):
    """Get a list of transit start and end times in units of cadence number
    
    Inputs
    ----------
    
    
    Returns
    ----------
    A 2d numpy array. zeroth column is cadence number of transit starts, first column is cadence
    number of transit ends.
    """

    assert np.all(np.isfinite(time))

    idx = kplrfits.markTransitCadences(time, period_days, epoch_btjd, duration_days)
    transits = np.array(plateau(idx, .5))

    return transits
##
##
##
def measureCentroidShift(cube, cin, ii, clip, plot=True):
    """
        
    Todo
    ---------
    * Adapt this code so it can be parameterised to accept different fitting algorithms, instead
      of hard coding fastGaussianPrf
    """
    
    before, after, diff = generateDiffImg(cube, cin, plot=plot)

#    print(before.min(), after.min(), diff.min())
#    before -= before.min()
#    after -= after.min()
#    diff -= diff.min()

#    before[np.isnan(before)] = 0.
#    after[np.isnan(after)] = 0.
#    diff[np.isnan(diff)] = 0.

#    print(before.min(), after.min(), diff.min())
#    print(diff)

#    if (np.isnan(np.nanmean(before)) == True) or (np.isnan(np.nanmean(after)) == True) or (np.isnan(np.nanmean(diff)) == True):
#        print('Transit bad')

    if (np.isnan(np.nanmean(diff)) == False):

        guess = pickInitialGuess(before)
        beforeSoln = ddf.fastGaussianPrfFit(before, guess)

        guess = pickInitialGuess(diff)
        diffSoln = ddf.fastGaussianPrfFit(diff, guess)

        guess = pickInitialGuess(after)
        afterSoln = ddf.fastGaussianPrfFit(after, guess)

#    plot = True
        if plot:
#             generateDiffImgOnlyPlot(diff, beforeSoln, diffSoln, afterSoln, clip)#mask, hdr_tpf)
#             print('AAAA')            
             generateDiffImgPlanetPatrol(diff, beforeSoln, diffSoln, afterSoln, clip)#mask, hdr_tpf)

#    print(beforeSoln.success, diffSoln.success, afterSoln.success)

        out = dict()
        error = 0
        error += 1 * (not beforeSoln.success)
        error += 2 * (not diffSoln.success)
        error += 4 * (not afterSoln.success)
        out['errorCode'] = error

        out['beforeCentroid'] = beforeSoln.x[:2]
        out['diffCentroid'] = diffSoln.x[:2]
        out['afterCentroid'] = afterSoln.x[:2]

    else:
        out = dict()
        out['errorCode'] = 999
        out['beforeCentroid'], out['diffCentroid'], out['afterCentroid'] = 0., 0., 0.

    return out
##
##
##
def generateDiffImg(cube, transits, offset_cadences=3, plot=False):
    """Generate a difference image.

    Also generates an image for each the $n$ cadedences before and after the transit,
    where $n$ is the number of cadences of the transit itself

    Inputs
    ------------
    cube
        (np 3 array) Datacube of postage stamps
    transits
        (2-tuples) Indices of the first and last cadence

    Optional Inputs
    -----------------
    offset_cadences
        (int) How many cadences gap should be inserted between transit and before and after images 
        Bryson et al. suggest 3 is a good number.
    plot
        (Bool) If true, generate a diagnostic plot


    Returns
    -------------
    Three 2d images,

    before
        The sum of the n cadences before transit (where n is the number of in-transit cadences
    after
        The sum of the n cadences after transit
    diff
        The difference between the flux in-transit and the average of the flux before and after

    Notes
    ---------
    * When there is image motion, the before and after images won't be identical, and the difference
    image will show distinct departures from the ideal prf.
    
    Todo
    ---------
    * This function belongs more properly in diffimg.py. I should port it there.
    """

    dur  = transits[1] - transits[0]
    s0, s1 = transits - dur - offset_cadences
    e0, e1 = transits + dur + offset_cadences

    before = np.nanmean(cube[s0:s1], axis = 0)#cube[s0:s1].sum(axis=0)
    during = np.nanmean(cube[transits[0]:transits[1]], axis = 0)#cube[transits[0]:transits[1]].sum(axis=0)
    after = np.nanmean(cube[e0:e1],axis = 0)#cube[e0:e1].sum(axis=0)
    diff = .5 * (before + after) - during

#    print(np.nanmean(cube[e0:e1],axis = 0))

#    if (np.isnan(np.nanmean(diff)) == False):
    return before, after, diff


#    print(np.isnan(np.nanmean(before)), np.isnan(np.nanmean(during)), np.isnan(np.nanmean(after)))
#    if (np.isnan(np.nanmean(before)) == True) or (np.isnan(np.nanmean(after)) == True) or (np.isnan(np.nanmean(diff)) == True):
#        print('Transit bad')
#    return before, after, diff    
##
##
##
def pickInitialGuess(img):
    """Pick initial guess of params for `fastGaussianPrfFit`
    
    Inputs
    ---------
    img
        (2d np array) Image to be fit
        
    Returns
    ---------
    An array of initial conditions for the fit
    """
    r0, c0 = np.unravel_index( np.argmax(img), img.shape)

    guess = [c0+.5, r0+.5, .5, np.max(img), np.median(img)]
    return guess
##
##
##
def generateDiffImgPlot(before, diff, after, beforeSoln, diffSoln, afterSoln):
    """Generate a difference image plot"""
#    
    kwargs = {'origin':'bottom', 'interpolation':'nearest', 'cmap':plt.cm.YlGnBu_r}
#
#    
    plt.clf()
    plt.subplot(221)
    plt.imshow(before, **kwargs)
    plt.title("Before")
    plt.colorbar()
#
#
    plt.subplot(222)
    plt.imshow(after, **kwargs)
    plt.title("After")
    plt.colorbar()
#
#
    plt.subplot(223)
    kwargs['cmap'] = plt.cm.RdBu_r
    img = after - before
#    img = 0.5*(after + before)
#    oot = 0.5*(afterSoln.x[:2] + beforeSoln.x[:2])
#    plt.plot(oot[1], oot[0], 'ms', ms=8, label="OOT")
    plt.imshow(img, **kwargs)
    plt.title("After - Before")
    vm = max( np.fabs([np.min(img), np.max(img)]) )
#    plt.clim(-vm, vm)
    plt.colorbar()
#
#
    plt.subplot(224)
    plt.imshow(diff, **kwargs)
    vm = max( np.fabs([np.min(diff), np.max(diff)]) )
#    plt.clim(-vm, vm)

    plotCentroidLocation(beforeSoln, 's', ms=8, label="Before")
    plotCentroidLocation(afterSoln, '^', ms=8, label="After")
    plotCentroidLocation(diffSoln, 'o', ms=12, label="Diff")
    
#    plt.legend()
    plt.title("Diff")
    plt.colorbar()
    plt.pause(1)
##
##
##
def generateDiffImgOnlyPlot(diff, beforeSoln, diffSoln, afterSoln, clip):#mask, hdr_tpf):
    """Generate a difference image plot"""
#    
    ss_ = diff.shape
    kwargs = {'origin':'bottom', 'interpolation':'nearest', 'cmap':plt.cm.YlGnBu_r, 'extent':[0, ss_[1],0, ss_[0]]}
#   kwargs = {'origin':'bottom', 'interpolation':'nearest', 'cmap':plt.cm.gray, 'extent':[0, ss_[1],0, ss_[0]]}

    plt.imshow(diff, **kwargs)
    vm = max( np.fabs([np.min(diff), np.max(diff)]) )
#    plt.clim(-vm, vm)
    plt.xticks([])
    plt.yticks([])
 
    col, row = diffSoln.x[:2]

#    print([col], [row])

    plt.plot([col], [row], 'ro', ms=12, mec = 'r', mew = 2)

#    plt.plot(hdr_tpf['1CRPX4']-0.5, hdr_tpf['2CRPX4']-0.5, 'r*', mfc = "None", ms = 30, mew = 3.)
#    if clip['config.detrendType'] == "tess_2min":
#        TIC_x, TIC_y = hdr_tpf['1CRPX4']-0.5, hdr_tpf['2CRPX4']-0.5

    if clip['config.detrendType'] == "tess_2min":
        aperture_mask = np.ones(clip['serve.mask'].shape, dtype=bool)
        aperture_mask[clip['serve.mask'] != mode(clip['serve.mask'].flatten()) + 10] = False
    elif clip['config.detrendType'] == "tess_FFI_eleanor":
        aperture_mask = clip['serve.mask']

    ra_, dec_ = clip.serve.param.RA, clip.serve.param.DEC
    wcs = clip.serve.param.wcs
    starloc = wcs.all_world2pix([[ra_, dec_]],0)  #Second is origin
    TIC_x,TIC_y=starloc[0,0]+0.5, starloc[0,1]+0.5
      
    plt.plot(TIC_x, TIC_y, 'r*', mfc = "None", ms = 30, mew = 1.5, label = 'TIC')

    f = lambda x,y: aperture_mask[int(y),int(x)]
    g = np.vectorize(f)
    x = np.linspace(0, aperture_mask.shape[1], aperture_mask.shape[1]*100)
    y = np.linspace(0, aperture_mask.shape[0], aperture_mask.shape[0]*100)
    X, Y= np.meshgrid(x[:-1],y[:-1])
    Z = g(X[:-1],Y[:-1])
    plt.contour(Z[::-1], [0.5], colors = 'w', linestyles = 'dashed', alpha = 1.0, linewidths=[2], \
               extent=[0-0., x[:-1].max()-0.,0-0., y[:-1].max()-0.], origin = 'upper')


#    plt.scatter(col, row)#, c = 'r', m = 'o', s = 16)
#    plt.title('Col-Row = ' + str(col) + '-' + str(row))
#    plt.title(str(diffSoln.success))
##
##
##
def generateDiffImgPlanetPatrol(diff, beforeSoln, diffSoln, afterSoln, clip):#mask, hdr_tpf):
    """Generate a difference image plot"""
#    
    ss_ = diff.shape
    kwargs = {'origin':'bottom', 'interpolation':'nearest', 'cmap':plt.cm.YlGnBu_r, 'extent':[0, ss_[1],0, ss_[0]]}
#   kwargs = {'origin':'bottom', 'interpolation':'nearest', 'cmap':plt.cm.gray, 'extent':[0, ss_[1],0, ss_[0]]}

    plt.imshow(diff, **kwargs)
    vm = max( np.fabs([np.min(diff), np.max(diff)]) )
#    plt.clim(-vm, vm)
    plt.xticks([])
    plt.yticks([])
 
    col, row = diffSoln.x[:2]

    plt.plot([col], [row], 'ro', ms=12, mec = 'r', mew = 2)

    if clip['config.detrendType'] == "tess_2min":
        aperture_mask = np.ones(clip['serve.mask'].shape, dtype=bool)
        aperture_mask[clip['serve.mask'] != mode(clip['serve.mask'].flatten()) + 10] = False
    elif clip['config.detrendType'] == "tess_FFI_eleanor":
        aperture_mask = clip['serve.mask']

    ra_, dec_ = clip.serve.param.RA, clip.serve.param.DEC
    wcs = clip.serve.param.wcs
    starloc = wcs.all_world2pix([[ra_, dec_]],0)  #Second is origin
    TIC_x,TIC_y=starloc[0,0]+0.5, starloc[0,1]+0.5
      
    plt.plot(TIC_x, TIC_y, 'r*', mfc = "None", ms = 30, mew = 1.5, label = 'TIC')

    f = lambda x,y: aperture_mask[int(y),int(x)]
    g = np.vectorize(f)
    x = np.linspace(0, aperture_mask.shape[1], aperture_mask.shape[1]*100)
    y = np.linspace(0, aperture_mask.shape[0], aperture_mask.shape[0]*100)
    X, Y= np.meshgrid(x[:-1],y[:-1])
    Z = g(X[:-1],Y[:-1])
    plt.contour(Z[::-1], [0.5], colors = 'r', linestyles = 'dashed', alpha = 1.0, linewidths=[2], \
               extent=[0-0., x[:-1].max()-0.,0-0., y[:-1].max()-0.], origin = 'upper')


#    plt.scatter(col, row)#, c = 'r', m = 'o', s = 16)
#    plt.title('Col-Row = ' + str(col) + '-' + str(row))
#    plt.title(str(diffSoln.success))
##
##
##
def plotCentroidLocation(soln, *args, **kwargs):
    """Add a point to the a plot.
    
    Private function of `generateDiffImgPlot()`
    """
    col, row = soln.x[:2]
    ms = kwargs.pop('ms', 8)

    kwargs['color'] = 'w'
    plt.plot([col], [row], *args, ms=ms+1, **kwargs)

    color='orange'
    if soln.success:
        color='c'
    kwargs['color'] = color
    plt.plot([col], [row], *args, **kwargs)
##
##
##
def testSmoke():
    import dave.fileio.pyfits as pyfits
    import dave.fileio.tpf as tpf
    tic = 307210830
    sector = 2

    period_days = 3.69061
    epoch_btjd = 1356.2038
    duration_days = 1.2676/24.

    path = '/home/fergal/data/tess/hlsp_tess-data-alerts_tess_phot_%011i-s%02i_tess_v1_tp.fits'
    path = path %(tic, sector)
    fits, hdr = pyfits.getdata(path, header=True)
    
    time = fits['TIME']
    cube = tpf.getTargetPixelArrayFromFits(fits, hdr)
    cube = cube[:, 3:9, 2:8]
    
    measurePerTransitCentroids(time, cube, period_days, epoch_btjd, duration_days, "tmp")
##
##
##