# spirou-ccf-analysis

This is a wrapper to perform radial velocity measurements on SPIRou CCF data using the CCF-tools developed by E. Artigau and the SPIRou DRS team. 

To start using this tool one needs a given CCF data set saved in the same directory, for example `data/TOI-1278/`.  Then one can run the analysis and generate the RV time series as in the following example:

```
python spirou_ccf_analysis.py --pattern=data/TOI-1278/*.fits
```

The following input options are available:
```
--pattern for input data pattern 
  (e.g., --pattern=*ccf_gl514_neg_AB.fits)
--method for selecting which method to use in the CCF analysis. 
  Current methods available are: "gaussian", "bisector", or "template" (default)
--bandpass for selecting the nIR band pass
  Current options available are: 'Y', 'J', 'H', 'K', or 'YJHK' (default)
--exclude_orders for selecting orders to exclude from the CCF analysis
  Order numbers must be separated by comma, e.g.: --exclude_orders="0,11,12,13,15,16,20,21,22,47,48"
-a for saving all sub-products, including csv tables and plot files
  By default it generates only the RV time-series in .rdb format.
-f force overwriting
-p for plotting
-v for verbose
```
Notice that more than one type of reduced data may be included in the input pattern, for example the CCFs from two different masks. The `spirou_ccf_analysis.py` tool will recognize each collection separately and will produce one RV time series file for each of them. The collections are selected by matching the combination of the following criteria: **object name**, **ccf mask**, **sanitize option**, and **DRS version**, from the information in the FITS header.

The tool `rv_plots.py` can be used to plot all RV time series together, as in the following example:

```
python rv_plots.py --pattern=data/TOI-1278/*.rdb -f -c --output=data/TOI-1278/TOI-1278.rdb
```

Note the following options:
```
--pattern for input data pattern 
  (e.g., --pattern=data/TOI-1278/*__HK__.rdb)
--output for providing a filename to save mean RVs
-f for fitting a sinusoidal orbit to each input data set
-c to calibrate RVs to match the average RV between all data sets.
```

which generates the following plot:

![Alt text](Figures/TOI-1278.png?raw=true "Title")
