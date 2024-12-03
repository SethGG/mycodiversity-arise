# !/bin/bash

input_dir="$(realpath $1)"
unite_chunk_dir=MDDB-phylogeny/l0.2_s3_4_1500_o1.0_a0_constr_localpair/chunks/unaligned

for input_refseq in $input_dir/refseq_table_pk*.csv; do
    base_name=$(basename "$input_refseq" .csv)
    output_fasta="${base_name}.fasta"
    output_blast="${base_name}_hits.txt"
    output_blast_chunks="${base_name}_hits_chunks.csv"
    output_blast_chunks_agg="${input_dir}/phylo_blast_${base_name}.csv"

    awk -F',' 'NR > 1 {print ">" $1 "\n" $2}' $input_refseq > $output_fasta
    blastn -query $output_fasta -db backbone_blastdb/backbone -out $output_blast -outfmt 6 -max_target_seqs 10

    echo "refsequence_pk,identity,UNITE_id,chunk" > $output_blast_chunks
    awk -F'\t' -v chunk_dir="$unite_chunk_dir" '{
        refsequence_pk = $1
        identity = $3
        unite_id = $2

        # Find the chunk file the UNITE ID is in
        cmd = "grep -l \"" unite_id "\" " chunk_dir "/*.fasta"
        cmd | getline chunk_file
        close(cmd)

        # Extract only the file name
        chunk = (chunk_file != "" ? chunk_file : "discarded")
        gsub(".*/", "", chunk)
        gsub("\\.[^.]+$", "", chunk)

        # Print CSV row
        print refsequence_pk "," identity "," unite_id "," chunk
        }' $output_blast >> $output_blast_chunks

    python aggregate_chunk_info.py $output_blast_chunks $output_blast_chunks_agg

    rm $output_fasta $output_blast $output_blast_chunks
done