# !/bin/bash

source .venv/bin/activate
cd PROFUNGIS
outdir=$1

cp -r "$outdir/ZOTUS" "$outdir/ZOTUS_full"
rm -r "$outdir/ZOTUS/abundant"
mv "$outdir/BLAST" "$outdir/BLAST_full"
mv "$outdir/FINAL" "$outdir/FINAL_full" 

for zotus in $outdir/ZOTUS/*.fa; do
    zotus_full="${zotus%.fa}_full.fa"
    zotus_trunc="${zotus%.fa}_trunc.fa"
    zotus_derep="${zotus%.fa}_trunc_mapping.txt"
    mv $zotus $zotus_full
    ./deps/usearch11 -fastx_truncate $zotus_full -trunclen 250 -fastaout $zotus_trunc
    ./deps/usearch11 -fastx_uniques $zotus_trunc -fastaout $zotus -tabbedout $zotus_derep
    zotutab="${zotus%zotus.fa}zotutab.txt"
    zotutab_full="${zotutab%.txt}_full.txt"
    mv $zotutab $zotutab_full
    python dereplicate_zotutab.py $zotus_derep $zotutab_full $zotutab
    rm $zotus_full $zotus_trunc $zotutab_full
done

snakemake --cores 4 --config $outdir/config.yml
