# !/bin/bash

source .venv/bin/activate
cd PROFUNGIS

python startPROFUNGIS.py -f ARISEF1 -r ARISER -p illumina -l -s NBCLAB4119
outdir=$(awk -v field="outdir" -F': ' '$1 == field {print $2}' config.yml)
mv config.yml $outdir