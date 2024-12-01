# !/bin/bash

input_dir="$(realpath $1)"
cd phylogenetic_placement
./run_blast.sh $input_dir