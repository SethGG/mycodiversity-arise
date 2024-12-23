# !/bin/bash

input_dir="$(realpath $1)"
pplacer_out_dir=$input_dir/pplacer

query_dir=query_files
query_align_dir=query_align_files

chunk_dir=MDDB-phylogeny/l0.2_s3_4_1500_o1.0_a0_constr_localpair/chunks/aligned
tree_dir=regen_trees
refpkg_dir=refpkg_files

mkdir -p $query_align_dir
mkdir -p $refpkg_dir
mkdir -p $pplacer_out_dir

export LC_ALL=C

for input_query_file in $query_dir/*.fasta; do
    base_name=$(basename "$input_query_file" .fasta)
    base_name_num=${base_name::3}

    taxit create -l its -P $refpkg_dir/$base_name.refpkg --aln-fasta $chunk_dir/$base_name.fasta --tree-stats $tree_dir/RAxML_info.$base_name_num.out --tree-file $tree_dir/RAxML_bestTree.$base_name_num.out
    mafft-linux64/mafft.bat --addfragments $input_query_file --keeplength $chunk_dir/$base_name.fasta > $query_align_dir/$base_name.fasta
    pplacer-Linux-v1.1.alpha19/pplacer -c $refpkg_dir/$base_name.refpkg $query_align_dir/$base_name.fasta -o $pplacer_out_dir/$base_name.jplace
    #pplacer-Linux-v1.1.alpha19/guppy to_csv $pplacer_out_dir/$base_name.jplace -o $pplacer_out_dir/$base_name.csv
    #pplacer-Linux-v1.1.alpha19/guppy tog $pplacer_out_dir/$base_name.jplace -o $pplacer_out_dir/$base_name.tog.tre
done

rm -r $query_align_dir
rm -r $refpkg_dir