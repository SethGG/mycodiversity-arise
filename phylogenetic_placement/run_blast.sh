# !/bin/bash

input_dir="$(realpath $1)"

for input_refseq in $input_dir/refseq_table_pk*.csv; do
    base_name=$(basename "$input_refseq" .csv)
    output_fasta="${base_name}.fasta"
    output_blast="${base_name}_hits.csv"

    awk -F',' 'NR > 1 {print ">" $1 "\n" $2}' $input_refseq > $output_fasta
    blastn -query $output_fasta -db backbone_blastdb/backbone -out $output_blast -outfmt "7 qseqid sseqid pident evalue length qcovhsp" -max_target_seqs 10

    rm $output_fasta
done