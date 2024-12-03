# !/bin/bash

input_dir="$(realpath $1)"
cd phylogenetic_placement
#./run_usearch.sh $input_dir
./run_blast.sh $input_dir