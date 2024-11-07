# !/bin/bash

source .venv/bin/activate
profungis_outdir=$1
post_process_outdir=$2
python createReferenceTable.py $post_process_outdir $profungis_outdir