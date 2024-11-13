# !/bin/bash

source .venv/bin/activate
outdir=$(realpath $1)

python createFilterTable.py $outdir