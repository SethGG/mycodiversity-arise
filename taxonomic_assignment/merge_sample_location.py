import pandas as pd

refseq = pd.read_csv("refseq_table_up2.csv")
refseq_tax = pd.read_csv("refseq_tax.csv")
refseq_sample_zotu = pd.read_csv("updated_mapping_pk_srr_zotu.csv")
sample_mapping = pd.read_csv("sample_mapping.csv")

merged_df_refseq = refseq.merge(refseq_tax, how="outer")
merged_df_refseq["tax_missing"] = merged_df_refseq["identity"].isnull()
merged_df_refseq.to_csv("merged_output_refseq.csv", index=False)

merged_df_samples = refseq_sample_zotu.merge(merged_df_refseq)
merged_df_samples = merged_df_samples.merge(sample_mapping)
merged_df_samples.to_csv("merged_output_samples.csv", index=False)
