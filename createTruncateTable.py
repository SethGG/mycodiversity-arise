import os
import sys
import re
import pandas as pd


def main(input_dir, output_dir):
    pattern_zotutab = re.compile(r"^(NBCLAB\d+?)_zotutab.txt$")
    df_trunc_mapping = pd.DataFrame(columns=['srr_name', 'zotu_id', 'trunc_mapping'])

    df_filter_mapping_trunc = pd.DataFrame(columns=['srr_name', 'zotu_id', 'passed_abun', 'passed_contam'])
    df_filter_mapping_full = pd.DataFrame(columns=['srr_name', 'zotu_id', 'passed_abun', 'passed_contam'])
    df_filter_mapping = {"": df_filter_mapping_trunc, "_full": df_filter_mapping_full}

    for suffix in df_filter_mapping:
        zotus_dir = os.path.join(input_dir, f"ZOTUS{suffix}")
        for filename in sorted(os.listdir(zotus_dir)):
            match = pattern_zotutab.match(filename)
            if match:
                srr_name = match.groups()[0]

                if suffix == "":
                    trunc_mapping_path = os.path.join(zotus_dir, f"{srr_name}_zotus_trunc_mapping.txt")
                    df = pd.read_csv(trunc_mapping_path, sep="\t", usecols=[0, 1], names=["zotu_id", "trunc_mapping"])
                    df['srr_name'] = srr_name
                    df_trunc_mapping = pd.concat([df_trunc_mapping, df])

                zotutab_path = os.path.join(zotus_dir, filename)
                df_zotutab = pd.read_csv(zotutab_path, sep="\t", usecols=[0], names=["zotu_id"], header=0)

                abun_path = os.path.join(zotus_dir, 'abundant', f"{srr_name}_zotutab_af.txt")
                contam_path = os.path.join(input_dir, f"FINAL{suffix}", f"{srr_name}_zotutab_final.txt")
                df_abun = pd.read_csv(abun_path, sep="\t", usecols=[0], names=["zotu_id_abun"], header=0)
                df_contam = pd.read_csv(contam_path, sep="\t", usecols=[0], names=["zotu_id_contam"], header=0)

                df_merged_abun = df_zotutab.merge(df_abun, how="left", left_on="zotu_id", right_on="zotu_id_abun")
                df_merged_contam = df_zotutab.merge(df_contam, how="left", left_on="zotu_id", right_on="zotu_id_contam")
                df_zotutab['passed_abun'] = df_merged_abun["zotu_id_abun"].notna()
                df_zotutab['passed_contam'] = df_merged_contam["zotu_id_contam"].notna()

                print(df_zotutab)

    df_trunc_mapping.to_csv(os.path.join(output_dir, "truncate_mapping.csv"))


if __name__ == "__main__":
    input_dir = sys.argv[1]
    output_dir = os.path.join("output_tables", os.path.basename(input_dir))
    os.makedirs(output_dir, exist_ok=True)

    main(input_dir, output_dir)
