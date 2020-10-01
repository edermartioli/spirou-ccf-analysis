# -*- coding: iso-8859-1 -*-
"""
    Created on September 29 2020
    
    Description: This routine performs the CCF analysis for a series of SPIRou CCF data products to obtain optimal radial velocities
    
    @author: Eder Martioli <martioli@iap.fr>
    
    Institut d'Astrophysique de Paris, France.
    
    Simple usage example:
    
    python spirou_ccf_analysis.py --pattern=data/TOI-1452/*.fits --bandpass="HK" --snr_min=20
    """

__version__ = "1.0"

__copyright__ = """
    Copyright (c) ...  All rights reserved.
    """

from optparse import OptionParser
import os,sys

import glob
import ccf2rv

parser = OptionParser()
parser.add_option("-i", "--pattern", dest="pattern", help="Input CCF data pattern",type='string',default="")
parser.add_option("-m", "--method", dest="method", help="Method to calculate RVs",type='string',default="template")
parser.add_option("-b", "--bandpass", dest="bandpass", help="Bandpass",type='string',default="YJHK")
parser.add_option("-e", "--exclude_orders", dest="exclude_orders", help="List of orders to exclude in the analysis ",type='string',default="-1")
parser.add_option("-s", "--min_snr", dest="min_snr", help="Minimum SNR",type='string',default="0")
parser.add_option("-a", action="store_true", dest="save_all_subproducts", help="Save all sub-products", default=False)
parser.add_option("-f", action="store_true", dest="force", help="force overwriting", default=False)
parser.add_option("-p", action="store_true", dest="plot", help="plot", default=False)
parser.add_option("-v", action="store_true", dest="verbose", help="verbose", default=False)

try:
    options,args = parser.parse_args(sys.argv[1:])
except:
    print("Error: check usage with spirou_ccf_analysis.py -h ")
    sys.exit(1)

if options.verbose:
    print('Input CCF data pattern: ', options.pattern)
    print('Method to calculate RVs: ', options.method)
    print('Bandpass: ', options.bandpass)
    print('List of orders to exclude in the analysis: ', options.exclude_orders)
    print('Minimum SNR: ', options.min_snr)

if options.verbose:
    print("Creating list of CCF data files...")
ccf_files = sorted(glob.glob(options.pattern))

#[0,11,12,13,15,16,20,21,22,47,48]
exclude_orders = options.exclude_orders.split(",")

for i in range(len(exclude_orders)) :
    exclude_orders[i] = int(exclude_orders[i])

# detect and organize collection of files based on: object, ccfmask, sanitize, and DRS version
ccf_collections = ccf2rv.create_collections(ccf_files)

for key in ccf_collections["modes"]:
    list_of_files = ccf_collections[key]

    if options.verbose:
        print("Processing collection {0} containing {1} files".format(key, len(list_of_files)))

    tbl = ccf2rv.get_object_rv(list_of_files, collection_key=key, method=options.method, force=options.force, exclude_orders = exclude_orders, snr_min=float(options.min_snr), bandpass = options.bandpass, save_subproducts=options.save_all_subproducts, showplots=options.plot, verbose=options.verbose)
