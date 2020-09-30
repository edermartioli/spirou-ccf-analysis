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
-a for saving all sub-products, including csv tables and plot files
  By default it generates only the RV time-series in .rdb format.
-f force overwriting
-p for plotting
-v for verbose
```
Notice that more than one type of reduced data may be included, for example the CCF data obtined with two different masks. The `spirou_ccf_analysis.py` tool will recognize each collection separately and will produce one RV time series file for each of them. The collections are selected by matching the combination of the following criteria: **object name**, **ccf mask**, **sanitize option**, and **DRS version**, from the information in the FITS header.

The tool `rv_plots.py` can be used to plot all RV time series together, as in the following example:

```
python rv_plots.py --pattern=data/TOI-1278/*.rdb -f
```

which generates the following plot:

![Alt text](Figures/TOI-1278.png?raw=true "Title")
