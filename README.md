# spirou-ccf-analysis

Wrapper to perform radial velocity measurements on SPIRou CCF data using the CCF-tools developed by E. Artigau and the SPIRou DRS team. 

To start using this tool for a given CCF data set saved in a given directory `SOME_PATH/TARGET/`, one can run the following example:

```
python spirou_ccf_analysis.py --pattern=SOME_PATH/TARGET/*.fits
```
The following input options are available:

```
--pattern for input data pattern (e.g., *.fits or *_ccf_masque_sept18_andres_trans50_AB.fits)
--method for selecting which method to use in the CCF analysis. Current methods available: "gaussian", "bisector", or "template" (default)
--bandpass for selecting NIR band pass. Current options available are: 'Y', 'J', 'H', 'K', or 'YJHK' (default)
-a for saving all sub-products, including csv tables and plot files. By default it generates only the RV time-series in .rdb format.
-f force overwriting
-p for plotting
-v for verbose
```
Notice that more than one type of reduced data can be included in the input files. The CCF analysis will be performed on each data set separately with one output RV time-series file for each of them. The collections are arranged by matching the combination of the following criteria: object name, ccf mask, sanitize option, and DRS version.

The tools `rv_plots.py` can be used to plot all RV time series together, as in the following example:

```
python rv_plots.py --pattern=data/TOI-1278/*.rdb -f
```

which generates the following plot:

![Alt text](Figures/TOI-1278.png?raw=true "Title")
