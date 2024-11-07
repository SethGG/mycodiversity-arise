# !/bin/bash

input_dir="$(realpath $1)"
cd taxonomic_assignment
./run_ublast.sh $input_dir