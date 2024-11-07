from PROFUNGIS_post_processing import generate_zotu_ref1
from PROFUNGIS_post_processing import update_ref_map
import sys
import os


def main(input_dir_list, output_dir):
    fasta_count = 0
    input_dir_list = [os.path.abspath(input_dir) for input_dir in input_dir_list]
    os.makedirs(output_dir, exist_ok=True)
    os.chdir(output_dir)
    for input_dir in input_dir_list:
        for filename in sorted(os.listdir(input_dir)):
            if filename.endswith(".fa"):
                input_path = os.path.join(input_dir, filename)
                if fasta_count == 0:
                    generate_zotu_ref1.Main(input_path, "Y")
                elif fasta_count == 1:
                    update_ref_map.Main(input_path, "refseq_table_pk.csv", "mapping_table_pk_zotu_srr.csv")
                else:
                    update_ref_map.Main(input_path, "refseq_table_up2.csv", "updated_mapping_pk_srr_zotu.csv")
                fasta_count += 1


if __name__ == "__main__":
    post_process_output_dir = os.path.join("output_tables", sys.argv[1])
    profungis_output_dirs = sys.argv[2:]

    main(profungis_output_dirs, post_process_output_dir)
