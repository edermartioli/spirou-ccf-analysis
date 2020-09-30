# spirou-ccf-analysis

Wrapper to perform radial velocity measurements on SPIRou CCF data using the CCF-tools developed by E. Artigau and the SPIRou DRS team. 

To start using this tool for a given CCF data set saved in a given directory `SOME_PATH/TARGET/`, one can run the following example:

```
cd spirou-ccf-analysis/

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
