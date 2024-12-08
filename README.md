# Support for FBMN with MSDIAL5

## Usage 1

- Launch the notebook by clicking on this button [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/lfnothias/FBMN_MSDIAL5/main?labpath=FBMN_MSDIAL_v5.ipynb)

- Add your files to the jupyter lab (drag and drop in the left column).

- Specify your filename for input and output.

- Run the notebook cells.

- Download the output converted files (left column, right-click on the items).

- Use those output for a FBMN job on GNPS and select 'MZMINE' as workflow type.


## Usage 2

```bash
conda create -n FBMN_MSDIAL5 python3 pandas
conda activate FBMN_MSDIAL5

# git clone this repo
git clone https://github.com/BioGavin/FBMN_MSDIAL5.git

# navigate to the FBMN_MSDIAL5 directory
cd FBMN_MSDIAL5

# view help info
python3 msdial5_formatter.py -h

# usage example
python3 msdial5_formatter.py -q input_quant.txt -m input.mgf -Q converted_quant.csv -M converted.mgf
```