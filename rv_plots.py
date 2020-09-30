# -*- coding: iso-8859-1 -*-
"""
    Created on September 30 2020
    
    Description: This routine runs a basic analysis and do plots of RV data
    
    @author: Eder Martioli <martioli@iap.fr>
    
    Institut d'Astrophysique de Paris, France.
    
    Simple usage example:
    
    python rv_plots.py --pattern=*.rdb --output=
    """

__version__ = "1.0"

__copyright__ = """
    Copyright (c) ...  All rights reserved.
    """


from optparse import OptionParser
import os,sys

import glob
import ccf2rv
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

parser = OptionParser()
parser.add_option("-i", "--pattern", dest="pattern", help="Input RV data pattern",type='string',default="")
parser.add_option("-o", "--output", dest="output", help="Output RV file name (end with .rdb)",type='string',default="")
parser.add_option("-c", action="store_true", dest="calib", help="calibrate data sets", default=False)
parser.add_option("-f", action="store_true", dest="fit_orbit", help="fit orbit", default=False)
parser.add_option("-v", action="store_true", dest="verbose", help="verbose", default=False)

try:
    options,args = parser.parse_args(sys.argv[1:])
except:
    print("Error: check usage with rv_plots.py -h ")
    sys.exit(1)

if options.verbose:
    print('Input RV data pattern: ', options.pattern)
    print('Output plot file name: ', options.output)

if options.verbose:
    print("Creating list of RV data files...")
rv_files = sorted(glob.glob(options.pattern))

bjd, rv, rverr = [], [], []
for i in range(len(rv_files)):
    loc_bjd, loc_rv, loc_rverr = ccf2rv.read_rv_time_series(rv_files[i])
    bjd.append(loc_bjd)
    rv.append(loc_rv)
    rverr.append(loc_rverr)
bjd = np.array(bjd)
rv = np.array(rv)
rverr = np.array(rverr)

mean_rv = np.mean(rv, axis=0)
rvdiff = rv - mean_rv

if options.calib :
    rv_func = lambda t, shift : mean_rv + shift

rvs_calib = []
for i in range(len(rv_files)):
    basename = os.path.basename(rv_files[i])
    
    if options.calib :
        guess = [0.0001]
        pfit, pcov = curve_fit(rv_func, bjd[i], rv[i], p0=guess)
        rv_fit = rv_func(bjd[i], *pfit)
        rv_calib = rv[i] - pfit[0]
        
        plt.errorbar(bjd[i], rv_calib, yerr=rverr[i], linestyle="None", fmt='o', alpha = 0.5, label="{0}: RV{1:+.3f} km/s".format(basename,pfit[0]))
    
        if options.fit_orbit :
            fit = ccf2rv.fitorbit(bjd[i], rv_calib, rverr[i], plot=False, verbose=False)
            plt.plot(fit["bjd_long_model"], fit["rv_long_model"],':')
            print("{0}: P={1:.2f}+-{2:.2f}d K={3:.3f}+-{4:.3f}km/s rms={5:.1f}m/s mad={6:.1f}m/s".format(basename,fit["period"],fit["perioderr"],fit["K"],fit["Kerr"],fit["rms_residuals"],fit["mad_residuals"]))

    else :
        rv_calib = rv[i]
        plt.errorbar(bjd[i], rv[i], yerr=rverr[i], linestyle="None", fmt='o', alpha = 0.5, label="{}".format(basename))

        if options.fit_orbit :
            fit = ccf2rv.fitorbit(bjd[i], rv[i], rverr[i], plot=False, verbose=False)
            plt.plot(fit["bjd_long_model"], fit["rv_long_model"],':')
            print("{0}: P={1:.2f}+-{2:.2f}d K={3:.3f}+-{4:.3f}km/s rms={5:.1f}m/s mad={6:.1f}m/s".format(basename,fit["period"],fit["perioderr"],fit["K"],fit["Kerr"],fit["rms_residuals"],fit["mad_residuals"]))
                
    rvs_calib.append(rv_calib)

rvs_calib = np.array(rvs_calib)

median_rv_calib = np.median(rvs_calib, axis=0)
mad_rv_calib = np.median(np.abs(rvs_calib - median_rv_calib), axis=0) / 0.67449

plt.errorbar(bjd[0], median_rv_calib, yerr=mad_rv_calib, linestyle="None", fmt='o', color='k', label="Mean RV")

plt.xlabel('BJD')
plt.ylabel('Velocity [km/s]')
plt.legend()

if options.output != "":
    
    ccf2rv.save_rv_time_series(options.output, bjd[0], median_rv_calib, mad_rv_calib, time_in_rjd=True, rv_in_mps=False)
    
    plt.savefig((options.output).replace(".rdb",".png"))

plt.show()



