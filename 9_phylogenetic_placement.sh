# !/bin/bash

input_dir="$(realpath $1)"
cd phylogenetic_placement
python generate_query_files.py $input_dir
./regenerate_chunk_trees.sh
./phylogenetic_placement.sh