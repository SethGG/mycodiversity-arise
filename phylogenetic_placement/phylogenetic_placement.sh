# !/bin/bash

query_dir=query_files
query_align_dir=query_align_files
query_placement_dir=query_placement_files

chunk_dir=MDDB-phylogeny/l0.2_s3_4_1500_o1.0_a0_constr_localpair/chunks/aligned
tree_dir=MDDB-phylogeny/l0.2_s3_4_1500_o1.0_a0_constr_localpair/chunks/trees
refpkg_dir=refpkg_files

mkdir -p $query_align_dir
mkdir -p $query_placement_dir
mkdir -p $refpkg_dir

export LC_ALL=C

for input_query_file in $query_dir/*.fasta; do
    base_name=$(basename "$input_query_file" .fasta)

    taxit create -l its -P $refpkg_dir/$base_name.refpkg --aln-fasta $chunk_dir/$base_name.fasta --tree-stats dummy_tree_stats --tree-file $tree_dir/$base_name.tre
    mafft-linux64/mafft.bat --addfragments $input_query_file --keeplength $chunk_dir/$base_name.fasta > $query_align_dir/$base_name.fasta
    pplacer-Linux-v1.1.alpha19/pplacer -c $refpkg_dir/$base_name.refpkg $query_align_dir/$base_name.fasta $placement_dir/$base_name.jplace
    break
done