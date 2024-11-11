from PROFUNGIS_post_processing import generate_zotu_ref1
from PROFUNGIS_post_processing import update_ref_map
import sys
import os
import tempfile
import shutil


def main(input_dir, output_dir):
    input_dir = os.path.abspath(input_dir)
    output_dir = os.path.abspath(output_dir)
    os.makedirs(output_dir, exist_ok=True)

    for suffix in ["", "_full"]:
        fasta_count = 0
        with tempfile.TemporaryDirectory(dir=output_dir) as tmp_output_dir:
            os.chdir(tmp_output_dir)
            zotus_dir = os.path.join(input_dir, f"FINAL{suffix}")
            for filename in sorted(os.listdir(zotus_dir)):
                if filename.endswith(".fa"):
                    input_path = os.path.join(zotus_dir, filename)
                    if fasta_count == 0:
                        generate_zotu_ref1.Main(input_path, "Y")
                    elif fasta_count == 1:
                        update_ref_map.Main(input_path, "refseq_table_pk.csv", "mapping_table_pk_zotu_srr.csv")
                    else:
                        update_ref_map.Main(input_path, "refseq_table_up2.csv", "updated_mapping_pk_srr_zotu.csv")
                    fasta_count += 1

            refseq_table_path = os.path.join(tmp_output_dir, "refseq_table_up2.csv")
            refseq_table_dest = os.path.join(output_dir, f"refseq_table_pk{suffix}.csv")
            shutil.move(refseq_table_path, refseq_table_dest)

            zotu_srr_table_path = os.path.join(tmp_output_dir, "updated_mapping_pk_srr_zotu.csv")
            zotu_srr_table_dest = os.path.join(output_dir, f"mapping_table_pk_zotu_srr{suffix}.csv")
            shutil.move(zotu_srr_table_path, zotu_srr_table_dest)

            record_track_path = os.path.join(tmp_output_dir, "record_track.csv")
            record_track_dest = os.path.join(output_dir, f"record_track{suffix}.csv")
            shutil.move(record_track_path, record_track_dest)


if __name__ == "__main__":
    input_dir = os.path.normpath(sys.argv[1])
    output_dir = os.path.join("output_tables", os.path.basename(input_dir))

    main(input_dir, output_dir)
