from PROFUNGIS_post_processing import update_ref_map
import sys
import os
import tempfile
import shutil


def main(mddb_dir, input_dir, output_dir):
    input_dir = os.path.abspath(input_dir)
    output_dir = os.path.abspath(output_dir)

    mddb_refseq = os.path.abspath(os.path.join(mddb_dir, "refseq_table_pk.csv"))
    mddb_mapping = os.path.abspath(os.path.join(mddb_dir, "mapping_table_pk_zotu_srr.csv"))

    os.makedirs(output_dir, exist_ok=True)

    fasta_count = 0
    with tempfile.TemporaryDirectory(dir=output_dir) as tmp_output_dir:
        os.chdir(tmp_output_dir)
        zotus_dir = os.path.join(input_dir, "FINAL")
        for filename in sorted(os.listdir(zotus_dir)):
            if filename.endswith(".fa"):
                input_path = os.path.join(zotus_dir, filename)
                if fasta_count == 0:
                    update_ref_map.Main(input_path, mddb_refseq, mddb_mapping)
                else:
                    update_ref_map.Main(input_path, "refseq_table_up2.csv", "updated_mapping_pk_srr_zotu.csv")
                fasta_count += 1

        refseq_table_path = os.path.join(tmp_output_dir, "refseq_table_up2.csv")
        refseq_table_dest = os.path.join(output_dir, "refseq_table_pk.csv")
        shutil.move(refseq_table_path, refseq_table_dest)

        zotu_srr_table_path = os.path.join(tmp_output_dir, "updated_mapping_pk_srr_zotu.csv")
        zotu_srr_table_dest = os.path.join(output_dir, "mapping_table_pk_zotu_srr.csv")
        shutil.move(zotu_srr_table_path, zotu_srr_table_dest)

        record_track_path = os.path.join(tmp_output_dir, "record_track.csv")
        record_track_dest = os.path.join(output_dir, "record_track.csv")
        shutil.move(record_track_path, record_track_dest)


if __name__ == "__main__":
    mddb_dir = "MDDB_tables"
    input_dir = os.path.normpath(sys.argv[1])
    output_dir = os.path.join(os.path.join(mddb_dir, "update_output"), os.path.basename(input_dir))

    main(mddb_dir, input_dir, output_dir)
