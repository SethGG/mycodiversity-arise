import pandas as pd
import os
import sys

if __name__ == "__main__":
    input_dir = os.path.normpath(sys.argv[1])

    df_refseq_full = pd.read_csv(os.path.join(input_dir, "refseq_table_pk_full.csv"))
    df_refseq = pd.read_csv(os.path.join(input_dir, "refseq_table_pk.csv"))

    df_refseq_tax_full = pd.read_csv(os.path.join(input_dir, "tax_refseq_table_pk_full.csv"))
    df_refseq_tax = pd.read_csv(os.path.join(input_dir, "tax_refseq_table_pk.csv"))

    df_phylo_blast_full = pd.read_csv(os.path.join(input_dir, "phylo_blast_refseq_table_pk_full.csv"))
    df_phylo_blast = pd.read_csv(os.path.join(input_dir, "phylo_blast_refseq_table_pk.csv"))

    df_full = df_refseq_tax_full.merge(df_phylo_blast_full, how="inner")
    df_full = df_full.merge(df_refseq_full, how="inner")

    df_trunc = df_refseq_tax.merge(df_phylo_blast, how="inner")
    df_trunc = df_trunc.merge(df_refseq, how="inner")

    df_full["sequence_trunc"] = df_full["sequence"].str[:250]
    df_full = df_full.merge(
        df_trunc.rename(columns={"sequence": "sequence_trunc"})[["refsequence_pk", "sequence_trunc"]],
        on="sequence_trunc", suffixes=("_full", "_trunc"), how="left"
    )

    df_full["refsequence_pk"] = df_full['refsequence_pk_full'] + \
        "_full->" + df_full['refsequence_pk_trunc'] + "_trunc"
    df_trunc["refsequence_pk"] = df_trunc["refsequence_pk"] + "_trunc"

    df_all = pd.concat(
        [df_full[['refsequence_pk', 'sequence', 'maj_chunk']],
         df_trunc[['refsequence_pk', 'sequence', 'maj_chunk']]],
    )

    output_dir = "query_files"
    os.makedirs(output_dir, exist_ok=True)

    for chunk_name, group in df_all.groupby('maj_chunk'):
        fasta_file = os.path.join(output_dir, f"{chunk_name}.fasta")

        with open(fasta_file, 'w') as f:
            for _, row in group.iterrows():
                refsequence_pk = row['refsequence_pk']
                sequence = row['sequence']
                f.write(f">{refsequence_pk}\n{sequence}\n")
