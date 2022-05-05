# AmpWrapper - Python Scripts for AmpTools Analysis

## Overview
---
AmpWrapper is designed to consolidate the tools provided by the [AmpTools](https://github.com/mashephe/AmpTools) library into a few easy-to-use Python scripts. Among these are scripts for running multiple fits through a SLURM interface, generating configuration files for partial wave analysis in both mass-dependent and model-independent fits, plotting results from fits, and bootstrapping fit results, along with utilities which wrap AmpTools fit results files. This code was designed to be used on the CMU MEG cluster and some of the job-submission code is formatted for our specific queue structure.

## Scripts
---
In general, scripts have the naming format `amptools-<script name>` to allow for them to be easily selected through tab completion.
### amptools-activate
```
usage: amptools-activate [-h] [-d DIRECTORY]

optional arguments:
  -h, --help            show this help message and exit
  -d DIRECTORY, --directory DIRECTORY
                        (optional) path to new environment directory (default
                        is current directory)
```
- Activates an AmpWrapper environment in the specified `DIRECTORY` (uses current working directory if none is supplied). This involves creating folders for flattrees and an `.env.json` file which is populated with useful information for other scripts. It also creates a file `~/.amptoolstools` which just points all programs to the currently activated environment (this allows scripts to be run from anywhere without having to be in the environment directory).

### amptools-convert
```
usage: amptools-convert [-h] [--version] [--merge-only]
                        [--exclude EXCLUDE [EXCLUDE ...]] [-w WEIGHT]
                        [-f FORMAT [FORMAT ...]] [-p PREFIX] [--force]
                        [--no-pol]
                        input output

Convert ROOT analysis trees to AmpTools flat trees

positional arguments:
  input                 Directory containing either:
                        1. ROOT files with run numbers in their names
                        2. ROOT files with any of the following keywords
                           in their names (this will skip the merging step!)
                        3. Directories whose names contain the following
                           keywords and whose contents are ROOT files
                        Keywords: AMO, PARA_0, PERP_45, PERP_90, PARA_135
                        
                        In the case of input directories which contain a mix of the
                        above formats, the program will chose a method in the given order.
  output                Directory to store any output files

optional arguments:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  --merge-only          Merge files by polarization without conversion
  --exclude EXCLUDE [EXCLUDE ...]
                        Exclude polarizations from merging/conversion
                        e.g. "--exclude AMO PERP_45 PERP_90" to only
                        process PARA polarizations
  -w WEIGHT, --weight WEIGHT
                        Specify a weighting factor (positive, even
                        for background trees)
                        Default: 1.0
                        If a path is supplied, weights will be pulled from CSVs with columns of
                        | EventNumber | ComboNumber | Signal Weight | ... |
                        This file must have a header line with at least these column names and no
                        index column. The filename must contain the run number.
  -f FORMAT [FORMAT ...]
                        Specify format for final state (run without
                        this option for more information)
  -p PREFIX, --prefix PREFIX
                        Specify output prefix
  --force               Force recreation of new merged ROOT files if they already exist
  --no-pol              Don't include energy-dependent polarization information in the beam 4-momentum
  --no-accidental-subtraction
                        Skip accidental weighting
  ```
  - converts GlueX analysis TTrees into AmpTools flattree format after merging them according to polarization
  - a flat weight can be specified by `-w`. Alternatively, a directory can be supplied containing multiple CSVs whose file names contain a run number and whose header is EventNumber,ComboNumber,Signal Weight,...
    - For example:
`some_weighting/some_weights_030499.csv`:

| EventNumber | ComboNumber| Signal Weight |
|---|---|---|
|493208|0|0.5432|
|495834|1|0.9982|
|...|...|...|

would be accessed by `-w some_weighting`.
- The `-f FORMAT` option can be used when you already know the particles which you want in the final state. Running the script without this argument will give you a dialog to specify the particles and a string of numbers which can be used in future script calls to skip the dialog step.
### amptools-link
```
usage: amptools-link [-h] [-d | -b | -g | -a] [-s | -c] [-f]
                     ROOT file [ROOT file ...]

positional arguments:
  ROOT file    file(s) to add

optional arguments:
  -h, --help   show this help message and exit
  -d, --data   add as data (default)
  -b, --bkg    add as background
  -g, --gen    add as generated/thrown MC
  -a, --acc    add as accepted/reconstructed MC
  -s, --soft   soft symlink to file (default is hard symlink)
  -c, --copy   copy file rather than symlink
  -f, --force  force overwrite of file if it already exists in the environment
```
- This script adds flattrees to the proper folders in an AmpWrapper environment. By default, these files are hard linked, which means a label is added to the file which points to the directory in the AmpWrapper environment. Deleting the file in that directory does not delete it in the original location and vice-versa, but it only takes up one spot in disk memory. Alternatively a `-s` can be used to create a soft symlink which just points to the original location on disk, but this link is broken if the original file is deleted or moved. `-c` can alternatively be used to copy the file, but this will take up two different locations on disk (although modifying files in one location will not effect the others, unlike in a hard symlink).
### amptools-study
```
usage: amptools-study [-h] [-d DATA [DATA ...]] [-g GEN [GEN ...]]
                      [-a ACC [ACC ...]] [-b BKG [BKG ...]] [--use-background]
                      [-n NBINS] [--low LOW] [--high HIGH]
                      name

positional arguments:
  name                  study name

optional arguments:
  -h, --help            show this help message and exit
  -d DATA [DATA ...], --data DATA [DATA ...]
                        path(s) to data files (optional)
  -g GEN [GEN ...], --gen GEN [GEN ...]
                        path(s) to generated MC files (optional)
  -a ACC [ACC ...], --acc ACC [ACC ...]
                        path(s) to accepted MC files (optional)
  -b BKG [BKG ...], --bkg BKG [BKG ...]
                        path(s) to background files (optional)
  --use-background      prompt for file selector if -b/--bkg option is left
                        blank
  -n NBINS, --nbins NBINS
                        number of bins (set to 1 for an unbinned study)
  --low LOW             lower edge for data selection
  --high HIGH           lower edge for data selection
  ```
  - The only required argument is a name for the study. If none of the file paths are provided, a dialog will allow the user to select files which have been `amptools-link`ed into the environment directory.
  - Additionally, if no binning information is provided, a command line interface will load weighted data files and display a histogram with binning that can be modified by user input keys. This is helpful if you don't exactly know what binning you want to use and don't want to create a bunch of plots with static histograms.
 
### amptools-generate
```
usage: amptools-generate [-h] [-b] [-o OUTPUT] [--amo] [-n NAME]
                         [--add-pol-info] [--sym]
                         amplitudes [amplitudes ...]

positional arguments:
  amplitudes            list of amplitudes to include, formatted as L/M/R

optional arguments:
  -h, --help            show this help message and exit
  -b, --background      use a separate set of background files
  -o OUTPUT, --output OUTPUT
                        name for output configuration file
  --amo                 include amorphous runs
  -n NAME, --name NAME  reaction name
  --add-pol-info        polarization information is NOT included in the ROOT
                        file's beam photon four-vector
  --sym                 symmetrize the two (non-recoil) particles (use this
                        for identical particles)
```
- This script is used to generate AmpTools configuration files with proper bookkeeping on all the amplitudes (specifically for Zlm amplitudes).
- `amplitudes` is a list of strings of the format `L/M/R` (L = total spin = {0, 1, 2, ...}, M = orbital quantum number = {-L, ..., +L}, R = reflectivity = {-1, +1} or {+, -}). Excluding one of these numbers generates all possibilities (except for `L` of course), so `1//` generates P waves with M = -1, 0, +1 and both positive and negative reflectivity (six waves total).
- Currently, it must at least generate Zlm amplitudes, but other amplitudes can be tacked on to those Zlms using @tags:
    - `2/0/1@my_Dwave_1 2/0/1@my_Dwave_2` would create two positive-reflectivity D waves with M = 0 which are distinct amplitudes in the config file. By itself, this would not make much sense, but it can be extended with `L/M/R@<name>@<Amplitude>@args@args@...` to additionally create named amplitudes which are not Zlms.
    - `2/1/1@my_f21270@BreitWigner@1.2755@0.1867@2@2@3` would create a positive-reflectivity D wave with M = +1 as well as a Breit-Wigner amplitude with a mass of 1.2755 MeV and a width of 0.1867 MeV (see the specific amplitude for the required arguments)
- If no `-o OUTPUT` option is included, the file will be printed to the terminal rather than saved in the `configs` directory inside the AmpWrapper environment.
### amptools-generate-from-json
```
usage: amptools-generate-from-json [-h] [-n NAME] [-o OUTPUT] [--amo] [--sym]
                                   [--add-pol-info] [-b]
                                   input

positional arguments:
  input                 input JSON file to turn into amptools-generate command

optional arguments:
  -h, --help            show this help message and exit
  -n NAME, --name NAME  reaction name
  -o OUTPUT, --output OUTPUT
                        name for output configuration file
  --amo                 include amorphous runs
  --sym                 symmetrize the two (non-recoil) particles (use this
                        for identical particles)
  --add-pol-info        polarization information is NOT included in the ROOT
                        file's beam photon four-vector
  -b, --background      use a separate set of background files
```
- This script has mostly the same arguments as `amptools-generate` but takes a `JSON`-formatted file as input rather than a list of amplitude strings. An example `JSON` file is provided in the repository (`amplitudes.json`).
- Running the script without `-o OUTPUT` will print a valid command for `amptools-generate` to the terminal followed by `--output`, allowing the user to copy-paste the command and add a name to generate the configuration manually.
### amptools-fit
```
usage: amptools-fit [-h] [-s STUDY] [-c CONFIG] [-i ITERATIONS] [-a]
                    [--seed SEED] [--skip-fit]
                    [-q {red,green,blue}] [--no-mem]

optional arguments:
  -h, --help            show this help message and exit
  -s STUDY              name of AmpTools study to fit
  -c CONFIG             name of AmpTools config to use in fit
  -i ITERATIONS, --iterations ITERATIONS
                        number of fits to do for each bin (randomized
                        bootstrap replication)
  -a, --append          append these iterations to any existing fits rather
                        than rerunning
  --seed SEED           seed for randomization
  --skip-fit            skip fitting and just collect available results from
                        any previous fits
  -q {red,green,blue}, --queue {red,green,blue}
                        SLURM queue for jobs
  --no-mem              don't set a memory cap in the SLURM script (use for
                        large bins where the generated MC is a huge file)
```
- This script actually runs the `fit` command provided by `halld_sim`. The study and configuration names are optional and a dialog will allow the user to select them if they aren't provided.
### amptools-fit-[bootstrap, stability, chain]
- These scripts all share similar functionality to `amptools-fit` but slightly modify the randomization process. While `amptools-fit` starts all amplitudes in a random spot in parameter space, `amptools-fit-chain` fits the first bin (the lowest mass bin) a specified number of times in random starting locations, selects the fit with the best likelihood, and starts each subsequent bin fit from the minimized value of the previous one. This significantly reduces the amount of fits which are done, but it can be unstable if the first bin isn't a great minimum or if the fit ends up on the wrong branch of minima somewhere along the fit.
- `amptools-fit-bootstrap` must be run after running `amptools-fit` or `amptools-fit-chain`, as it takes the best likelihood fit in each bin and then runs a specified number of fits starting at that minimum with a bootstrapped dataset.
- `amptools-fit-stability` is a different way of selectingg the best minimum. Rather than relying on the best likelihood, each individual iteration within each bin is bootstrapped and the best iteration is selected based on the bootstrap-t, which is related to the distance of the fit from the mean of the bootstraps normalized by the variance of the bootstraps. Fits with the lowest distance are selected because they represent a minimum which won't change much if the data is modified or if new data is obtained.
### amptools-plot(-[bootstrap, chain, stability, angles])
```
usage: amptools-plot [-h] [-s STUDY]

optional arguments:
  -h, --help            show this help message and exit
  -s STUDY, --study STUDY
                        study name
```
- All of these scripts generate plots for their respective fitting scripts. A dialog will allow the user to select the study along with the configuration that was fit. The script generates plots for the amplitudes of each wave, phase plots, complex amplitude plots (for some scripts), and violin plots that show the distribution of fits in each bin (for some scripts). The bootstrap version also does a simple bias-correction calculation (WIP).
- `amptools-plot-angles` creates plots for the angular distributions of particles in each bin for each type of data (accepted MC, generated MC, acceptance-corrected data) and doesn't require a fit to be run first.
### amptools-select-thrown-topology, amptools-view-thrown-topologies, amptools-search
- These scripts are used to select a specific thrown topology based on the particles you want in your final state. Generators like `gen_amp` can create unwanted decays which are difficult to deal with in the `amptools-convert` script, so it is useful to only select one topology at a time in an AmpTools analysis.
### amptools-info
- This script is still a work in progress. The intent is for it to display useful information about a particular study or configuration.
### boost_flattree.py
- A simple script to boost flattrees to the center-of-momentum frame. This is largely not required because AmpTools already does this by default, but might be useful for other testing purposes.
### utils.py
- This file is not a script, but it contains most of the helper functions used by the rest of the scripts.

## Example Usage
---
Here I demonstrate a typical workflow starting from some processed data/MC GlueX analysis trees located at `~/data_trees/`, `~/recon_trees/` (reconstructed/accepted MC), and `~/gen_trees/` (thrown/generated MC). I exclude most of the output/all dialogs from the programs:
```csh
$ tree ~/data_trees/
/home/<username>/data_trees/
├── tree_ksks__B4_050685.root
├── tree_ksks__B4_050697.root
├── tree_ksks__B4_050698.root
...
└── tree_ksks__B4_051768.root
$ tree ~/gen_trees/
/home/<username>/gen_trees/
├── tree_ksks__B4_PARA_0.root
├── tree_ksks__B4_PARA_135.root
├── tree_ksks__B4_PERP_45.root
└── tree_ksks__B4_PERP_90.root
$ tree ~/recon_trees/
/home/<username>/recon_trees/
├── tree_ksks__B4_PARA_0.root
├── tree_ksks__B4_PARA_135.root
├── tree_ksks__B4_PERP_45.root
└── tree_ksks__B4_PERP_90.root
```
First, we convert the GlueX analysis trees to AmpTools flattrees:
```csh
$ amptools-convert -p data --exclude AMO ~/data_trees/ ~/data_merged/
$ amptools-convert -p gen ~/gen_trees/ ~/gen_merged/
$ amptools-convert -p acc ~/recon_trees/ ~/recon_merged/
```
Next, activate a new AmpWrapper environment and link the flattrees:
```csh
$ amptools-activate ~/pwa_analysis/
$ amptools-link ~/data_merged/flattrees/*
$ amptools-link --gen ~/gen_merged/flattrees/*
$ amptools-link --acc ~/recon_merged/flattrees/*
```
Next, we will make a configuration file. For this demonstration, we'll just add all possible S and D waves (probably overkill but we could use the results of such a fit to decide which waves to get rid of). Because is is a channel with two identical kaons in the final state, we should symmetrize them in the fit:
```csh
$ amptools-generate --sym -n ksks_fit -o all_waves 0// 2//
```
Next, we create a study. Our study here will span the 1-2 GeV range, so 25 bins will give us a bin-width of 40 MeV:
```csh
$ amptools-study -n 25 --low 1.000 --high 2.000 my_study
```
Now let's fit the data with the configuration we just made, creating 30 randomly initialized fits in each bin, and submit it to the `red` SLURM queue:
```csh
$ amptools-fit -s my_study -c all_waves -i 30 -q red
```
Next, let's generate a plot:
```csh
$ amptools-plot -s my_study
```
This will create a PDF at `~/pwa_analysis/my_study/plot_all_waves_results.pdf`. Suppose we like these results and want to get a better interpretation of the error/bias through bootstrapping. We then do the following:
```csh
$ amptools-fit-bootstrap -s my_study -c all_waves -i 50 -q red
$ amptools-plot-bootstrap -s my_study
```
This will generate a PDF at `~/pwa_analysis/my_study/plot_all_waves_results_bootstrap.pdf`.

## Installing
---
The following code will install everything in one line:
```csh
$ python -m pip install git+https://github.com/denehoffman/AmpToolsTools.git
```
If you want to have an easily-accessible cloned version of the source, you can also do
```csh
$ git clone https://github.com/denehoffman/AmpToolsTools.git
$ cd AmpToolsTools
$ python -m pip install .
```
or
```csh
$ python -m pip install -e .
```
to soft symlink the repo (so that you can modify it without having to reinstall each time to test it).

## Future Plans
---
- Possibly a wrapper for more AmpPlotter functionality (right now the plot scripts will only really work for mass/model-independent fits, although you can still create studies with one bin and fit mass-dependent models).
- Clean up code, help strings, and documentation
