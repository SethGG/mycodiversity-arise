#!/bin/bash
# Parameters: ZOTU fasta input, blast output and final fasta output
ZOTUS=${1}
OUTPUT=${2}
OUTZOTU=${3}

NAMES_CONTAM="${OUTPUT%blast.txt}names_contam.tmp"
NAMES="${OUTPUT%blast.txt}names.tmp"
TEMPOUT="${OUTPUT%blast.txt}tempout.tmp"


# A BLAST against the UNITE database is performed, minimal identity is 70%
blastn -query ${ZOTUS} -db ./deps/Unite/unite -outfmt 6 -out ${OUTPUT} -perc_identity 70 -max_target_seqs 3

# All hits without kingdom: Fungus are selected and stored as contamination
egrep "k__[^F]" ${OUTPUT} | cut -f 1 | sort | uniq > ${NAMES_CONTAM}
# All other hits are stored as correct names
egrep "k__F" ${OUTPUT} | cut -f 1 | sort | uniq > ${NAMES}


# All sequences with a hit are selected from the ZOTU file
./deps/faSomeRecords ${ZOTUS} ${NAMES} ${TEMPOUT}
# All sequences in the contamination file are removed from the zotu file
./deps/faSomeRecords ${TEMPOUT} ${NAMES_CONTAM} ${OUTZOTU} -exclude

# Remove temp files
#rm names.tmp tempout.tmp names_contam.tmp
rm ${TEMPOUT}
