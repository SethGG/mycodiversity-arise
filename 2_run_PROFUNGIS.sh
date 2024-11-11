# !/bin/bash

source .venv/bin/activate
cd PROFUNGIS

python startPROFUNGIS.py -f ARISEF1 -r ARISER -p illumina -l -m sample_list.txt
outdir=$(awk -v field="outdir" -F': ' '$1 == field {print $2}' config.yml)
mv config.yml $outdir