# !/bin/bash

source .venv/bin/activate
cd PROFUNGIS

python startPROFUNGIS.py -f ARISEF$1 -r ARISER -p illumina -l -m sample_list.txt
outdir="$(awk -v field="outdir" -F': ' '$1 == field {print $2}' config.yml)/FINAL"
mv config.yml $outdir