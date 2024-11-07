# !/bin/bash

input_refseq="refseq_table_up2.csv"
output_fasta="refseq.fasta"
output_usearch="hits.txt"
output_taxonomy="refseq_tax.csv"

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
    kingdom = substr(taxonomy[1], 4)
    phylum = substr(taxonomy[2], 4)
    class = substr(taxonomy[3], 4)
    order = substr(taxonomy[4], 4)
    family = substr(taxonomy[5], 4)
    genus = substr(taxonomy[6], 4)
    species = substr(taxonomy[7], 4)

    # Print CSV row
    print refsequence_pk "," identity "," unite_id "," kingdom "," phylum "," class "," order "," family "," genus "," species
}' $output_usearch >> $output_taxonomy
