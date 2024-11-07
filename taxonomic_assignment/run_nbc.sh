# !/bin/bash

input_fasta="Unite/sh_general_release_dynamic_04.04.2024.fasta"
output_fasta="unite_tax_annotation.fasta"

awk '
BEGIN { FS="\\|"; OFS=";" }

# If the line starts with ">", its a header line
/^>/ {
    # Remove the ">" character at the start of the line
    header = substr($0, 2)

    # Split the line into parts by "|"
    split(header, parts, "|")

    # Extract components
    species = parts[1]          # e.g., "Gyroporus_purpurinus"
    accession = parts[2]        # e.g., "KX389110"
    unite_id = parts[3]         # e.g., "SH0879786.10FU"
    reps = parts[4]             # e.g., "reps"
    
    # Split the taxonomy part by ";"
    n = split(parts[5], taxonomy, ";")
    formatted_taxonomy = ""

    # Loop through taxonomy components and reformat
    for (i = 1; i <= n; i++) {
        if (taxonomy[i] != "") {
            # Extract the first letter for the prefix and the rest after "__"
            prefix = substr(taxonomy[i], 1, 1)
            taxon = substr(taxonomy[i], 4)
            formatted_taxonomy = formatted_taxonomy prefix ":" taxon (i < n ? "," : "")
        }
    }

    # Print the new header format
    print ">" species ";" accession ";" unite_id ";" reps ";tax=" formatted_taxonomy ";"
    next
}

# For non-header lines, just print them as they are
{ print }
' $input_fasta > $output_fasta

./usearch11 -sintax refseq.fasta -db unite_tax_annotation.fasta -strand plus -tabbedout nbc_tax.txt