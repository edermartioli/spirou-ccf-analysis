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
parser.add_option("-o", "--output", dest="output", help="Output plot file name (end with .png)",type='string',default="")
parser.add_option("-f", action="store_true", dest="fit", help="fit", default=False)
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

if options.fit :
    rv_func = lambda t, shift : mean_rv + shift

for i in range(len(rv_files)):
    basename = os.path.basename(rv_files[i])
    
    if options.fit :
        guess = [0.0001]
        pfit, pcov = curve_fit(rv_func, bjd[i], rv[i], p0=guess)
        rv_fit = rv_func(bjd[i], *pfit)
        rv_calib = rv[i] - pfit[0]
    
        plt.errorbar(bjd[i], rv_calib, yerr=rverr[i], linestyle="None", fmt='o', alpha = 0.5, label="{0}: RV{1:+.3f} km/s".format(basename,pfit[0]))
    else :
        plt.errorbar(bjd[i], rv[i], yerr=rverr[i], linestyle="None", fmt='o', alpha = 0.5, label="{}".format(basename))

plt.xlabel('BJD')
plt.ylabel('Velocity [km/s]')
plt.legend()

if options.output != "":
    plt.savefig(options.output)

plt.show()



