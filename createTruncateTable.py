import os
import sys
import re
import csv
from collections import defaultdict


def main(input_dir, output_dir):
    pattern = re.compile(r"^(NBCLAB\d+?)_zotus_trunc_mapping.txt$")
    with open(os.path.join(output_dir, "truncate_mapping.csv"), "w") as tm_out, \
            open(os.path.join(output_dir, "filter_mapping_full.csv"), "w") as fmf_out, \
            open(os.path.join(output_dir, "filter_mapping_trunc.csv"), "w") as fmt_out:

        csv_writer_tm = csv.writer(tm_out)
        csv_writer_tm.writerow(['srr_name', 'zotu_id', 'trunc_zotu_id'])

        csv_writer_fmf = csv.writer(fmf_out)
        csv_writer_fmf.writerow(['srr_name', 'zotu_id', 'passed_abun', 'passed_contam'])

        csv_writer_fmt = csv.writer(fmt_out)
        csv_writer_fmt.writerow(['srr_name', 'zotu_id', 'passed_abun', 'passed_contam'])

        srr_names = []

        for filename in sorted(os.listdir(f"{input_dir}/ZOTUS")):
            input_path = os.path.join(input_dir, "ZOTUS", filename)
            match = pattern.match(filename)
            if match:
                srr_name = match.groups()[0]
                srr_names.append(srr_name)

                with open(input_path, "r") as f:
                    for line in f:
                        parts = line.strip().split()
                        zotu, cluster = parts[0], parts[1]
                        csv_writer_tm.writerow([srr_name, zotu, cluster])

        suffix = {"": csv_writer_fmt, "_full": csv_writer_fmf}
        for srr_name in srr_names:
            passed_abun = {s: defaultdict(bool) for s in suffix}
            passed_contam = {s: defaultdict(bool) for s in suffix}
            for s in suffix:
                abun_path = f"ZOTUS{s}/abundant/{srr_name}_zotutab_af.txt"
                contam_path = f"FINAL{s}/{srr_name}_zotutab_final.txt"
                abun = (abun_path, passed_abun)
                contam = (contam_path, passed_contam)
                for filter in (abun, contam):
                    header = None
                    with open(f"{input_dir}/{filter[0]}", "r") as f:
                        for line in f:
                            if header is None:
                                header = line
                            else:
                                parts = line.strip().split()
                                zotu = parts[0]
                                filter[1][s][zotu] = True

                zotu_path = f"ZOTUS{s}/{srr_name}_zotutab.txt"
                header = None
                with open(f"{input_dir}/{zotu_path}", "r") as f:
                    for line in f:
                        if header is None:
                            header = line
                        else:
                            parts = line.strip().split()
                            zotu = parts[0]
                            suffix[s].writerow([srr_name, zotu, passed_abun[s][zotu], passed_contam[s][zotu]])


if __name__ == "__main__":
    input_dir = sys.argv[1]
    output_dir = os.path.join("output_tables", os.path.basename(input_dir))
    os.makedirs(output_dir, exist_ok=True)

    main(input_dir, output_dir)
