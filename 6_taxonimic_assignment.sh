# !/bin/bash

input_dir="$(realpath $1)"
cd taxonomic_assignment
./run_usearch.sh $input_dir