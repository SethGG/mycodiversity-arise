# !/bin/bash

input_dir="$(realpath $1)"
unite_chunk_dir=MDDB-phylogeny/l0.2_s3_4_1500_o1.0_a0_constr_localpair/chunks/unaligned

for input_refseq in $input_dir/refseq_table_pk*.csv; do
    base_name=$(basename "$input_refseq" .csv)
    output_fasta="${base_name}.fasta"
    output_usearch="${base_name}_hits.txt"
    output_taxonomy="${input_dir}/phylo_tax_${base_name}.csv"

    awk -F',' 'NR > 1 {print ">" $1 "\n" $2}' $input_refseq > $output_fasta
    ./usearch11 -usearch_global $output_fasta -db Unite/sh_refs_qiime_ver8_97_10.05.2021.fasta -strand plus -id 0.80 -userout $output_usearch -userfields query+id+target

    echo "refsequence_pk,identity,UNITE_id,chunk" > $output_taxonomy
    awk -F'\t' -v chunk_dir="$unite_chunk_dir" '{
        refsequence_pk = $1
        identity = $2
        unite_id = $3

        # Find the chunk file the UNITE ID is in
        cmd = "grep -l \"" unite_id "\" " chunk_dir "/*.fasta"
        cmd | getline chunk_file
        close(cmd)

        # Extract only the file name
        chunk_file = (chunk_file != "" ? chunk_file : "discarded")
        gsub(".*/", "", chunk_file)

        # Print CSV row
        print refsequence_pk "," identity "," unite_id "," chunk_file
    }' $output_usearch >> $output_taxonomy

    rm $output_fasta $output_usearch
done
