# -*- coding: iso-8859-1 -*-
"""
    Created on September 25 2020
    
    Description: This routine fits a simple orbit model to RV data
    
    @author: Eder Martioli <martioli@iap.fr>
    
    Institut d'Astrophysique de Paris, France.
    
    Simple usage example:
    
    python fit_orbit.py --input=TOI-1278.rdb
    """

__version__ = "1.0"

__copyright__ = """
    Copyright (c) ...  All rights reserved.
    """

from optparse import OptionParser
import os,sys

import matplotlib.pyplot as plt
import numpy as np

import ccf2rv

from astropy.io import ascii

parser = OptionParser()
parser.add_option("-i", "--input", dest="input", help="Input RV file",type='string',default="")
parser.add_option("-v", action="store_true", dest="verbose", help="verbose", default=False)

try:
    options,args = parser.parse_args(sys.argv[1:])
except:
    print("Error: check usage with fit_orbit.py -h ")
    sys.exit(1)

if options.verbose:
    print('Input RV file: ', options.input)


data = ascii.read(options.input,data_start=2)
#bjd = np.array(data['rjd']) + 2400000.
bjd = np.array(data['rjd'])
rvs = np.array(data["vrad"])
rverrs = np.array(data["svrad"])

fit = ccf2rv.fitorbit(bjd, rvs, rverrs, plot=True, verbose=True)


