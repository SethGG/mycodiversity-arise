# !/bin/bash

input_dir="$(realpath $1)"

for input_refseq in $input_dir/refseq_table_pk*.csv; do
    base_name=$(basename "$input_refseq" .csv)
    output_fasta="${base_name}.fasta"
    output_usearch="${base_name}_hits.txt"
    output_taxonomy="${input_dir}/tax_${base_name}.csv"

    awk -F',' 'NR > 1 {print ">" $1 "\n" $2}' $input_refseq > $output_fasta
    ./usearch11 -usearch_global $output_fasta -db Unite/sh_general_release_dynamic_04.04.2024.fasta -strand plus -id 0.70 -userout $output_usearch -userfields query+id+target

    echo "refsequence_pk,identity,UNITE_id,kingdom,phylum,class,order,family,genus,species" > $output_taxonomy
    awk -F'\t' '{
        refsequence_pk = $1
        identity = $2

        # Split the third field by the | character
        split($3, fields, "|")

        # Extract UNITE ID
        unite_id = fields[3]

        # Split the taxonomy part (5th element) by ;
        split(fields[5], taxonomy, ";")

        # Extract taxonomic levels by removing "k__", "p__", etc.
        kingdom = taxonomy[1]
        phylum = taxonomy[2]
        class = taxonomy[3]
        order = taxonomy[4]
        family = taxonomy[5]
        genus = taxonomy[6]
        species = taxonomy[7]

        # Print CSV row
        print refsequence_pk "," identity "," unite_id "," kingdom "," phylum "," class "," order "," family "," genus "," species
    }' $output_usearch >> $output_taxonomy

    rm $output_fasta $output_usearch
done