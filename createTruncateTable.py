import os
import sys
import re
import csv
from collections import defaultdict


def zotutab_to_dict(input_path, type, skip_header=True):
    output_dict = defaultdict(type)
    header = not (skip_header)
    with open(input_path, "r") as f:
        for line in f:
            if not header:
                header = True
            else:
                parts = line.strip().split()
                zotu, map = parts[0], type(parts[1])
                output_dict[zotu] = map
    return output_dict


def main(input_dir, output_dir):
    pattern = re.compile(r"^(NBCLAB\d+?)_zotutab.txt$")

    with open(os.path.join(output_dir, "truncate_mapping.csv"), "w") as tm_out, \
            open(os.path.join(output_dir, "filter_mapping_full.csv"), "w") as fmf_out, \
            open(os.path.join(output_dir, "filter_mapping_trunc.csv"), "w") as fmt_out:

        csv_writer_tm = csv.writer(tm_out)
        csv_writer_tm.writerow(['srr_name', 'zotu_id', 'trunc_zotu_id', 'passed_trunc'])

        csv_writer_fmf = csv.writer(fmf_out)
        csv_writer_fmf.writerow(['srr_name', 'zotu_id', 'passed_abun', 'passed_contam'])

        csv_writer_fmt = csv.writer(fmt_out)
        csv_writer_fmt.writerow(['srr_name', 'zotu_id', 'passed_abun', 'passed_contam'])

        suffix_csv_map = {"": csv_writer_fmt, "_full": csv_writer_fmf}
        for suffix in suffix_csv_map:
            zotus_dir = os.path.join(input_dir, f"ZOTUS{suffix}")
            zotus_abun_dir = os.path.join(zotus_dir, "abundant")
            zotus_final_dir = os.path.join(input_dir, f"FINAL{suffix}")

            for filename in sorted(os.listdir(zotus_dir)):
                zotutab_path = os.path.join(zotus_dir, filename)
                match = pattern.match(filename)
                if match:
                    srr_name = match.group(1)

                    abun_path = os.path.join(zotus_abun_dir, f"{srr_name}_zotutab_af.txt")
                    abun_dict = zotutab_to_dict(abun_path, bool)

                    contam_path = os.path.join(zotus_final_dir, f"{srr_name}_zotutab_final.txt")
                    contam_dict = zotutab_to_dict(contam_path, bool)

                    if suffix == "_full":
                        trunc_path = os.path.join(input_dir, "ZOTUS", f"{srr_name}_zotus_trunc_mapping.txt")
                        trunc_dict = zotutab_to_dict(trunc_path, str, skip_header=False)

                    header = False
                    with open(zotutab_path, "r") as f:
                        for line in f:
                            if not header:
                                header = True
                            else:
                                parts = line.strip().split()
                                zotu = parts[0]

                                suffix_csv_map[suffix].writerow([srr_name, zotu, abun_dict[zotu], contam_dict[zotu]])

                                if suffix == "_full":
                                    csv_writer_tm.writerow([srr_name, zotu, trunc_dict[zotu], bool(trunc_dict[zotu])])


if __name__ == "__main__":
    input_dir = os.path.normpath(sys.argv[1])
    output_dir = os.path.join("output_tables", os.path.basename(input_dir))
    os.makedirs(output_dir, exist_ok=True)

    main(input_dir, output_dir)
