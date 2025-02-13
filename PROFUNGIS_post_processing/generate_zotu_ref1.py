"""**********************************************************"""
"""
SCRIPT 1/2 of post_profungis script: 
USAGE: Setting up an initial reference ZOTU set from FASTA file
the file can be appended in MDDB reference list and uploaded in the MDDB.
- script functions for checking if coming in sequence is on the reference list
- script can also be used for generating the first reference ZOTU table of personal use ZOTU reference table obtained from a PROFUNGIS pipeline
- Please read the README file for getting support in running the script
"""

"""**********************************************************"""


"""
keep track of FASTA seq label for mapping
"""




import os
import csv
import pandas
import re
from Bio import SeqIO
import random
from random import randint
def generate_header_track(recordtrackfile):
    track_header = ['update_srr', 'seq_fasta', 'previous_seq', 'update_seq']
    with open(recordtrackfile, "a") as fp:
        writer = csv.writer(fp)
        writer.writerow(track_header)
    fp.close()


def save_record_track(trackfile, tracker):
    with open(trackfile, 'a') as f:
        tracker.to_csv(f, header=False, index=False)
    f.close()


def Main(fastafiletest, generatepktest):
    # df = pd.DataFrame(columns=list('A'))
    # df.loc[0] = ['Hello']
    # print (df)
    print("testing")
    otu_id = []
    otu_sequence = []
    sequence_table = "refseq_table_zotus.csv"
    mapping_table_zotu_srr = "mapping_table_zotu_srr.csv"
    sequence_table_pk = "refseq_table_pk.csv"
    otuseq_mapping_toupdatepk = 'otu_seq_mapping_to_update.csv'
    mapping_table_pk_zotu_srr = "mapping_table_pk_zotu_srr.csv"
    record_track = "record_track.csv"
    index_of_key_column = 0
    index_of_marker_column = 2
    index_of_refseqlength_column = 3

    """
    parse FASTA file
    """
    for record in SeqIO.parse(fastafiletest, 'fasta'):
        otu_id.append(record.id)
        otu_sequence.append(record.seq)

    its2 = 'ITS2'  # type of marker used
    srr_filename = os.path.basename(fastafiletest)  # split the file pathname for fetching the SRR id
    srr_label = os.path.splitext(srr_filename)[0]
    srr_output_parse = srr_label.split("_")
    srr_name = srr_output_parse[0]
    record_list = [list(item) for item in list(zip(otu_id, otu_sequence))]
    """
    OPTION == "N" is CASE NO, then keep original IDs
    """
    if generatepktest == 'N':
        header_columns = ["seq_id", "sequence"]
        with open(sequence_table, "a") as fp:
            writer = csv.writer(fp)  # upload original fasta file into csv
            writer.writerow(header_columns)
            writer.writerows(record_list)
        fp.close()
        values_to_map = pandas.read_csv(sequence_table, header=0)
        values_to_map.insert(loc=index_of_key_column, column='srr_name', value=srr_name)
        map_zotu_srr = values_to_map.drop('sequence', axis=1)
        map_zotu_srr.to_csv(mapping_table_zotu_srr, encoding='utf-8', index=False)
    elif generatepktest == 'Y':
        header_columns_refseq_pk = ["otuseq_id", "sequence"]
        """
        OPTION == "Y" is CASE YES: generate primary keys
        """
        with open(otuseq_mapping_toupdatepk, "a") as fp:
            writer = csv.writer(fp)
            writer.writerow(header_columns_refseq_pk)
            writer.writerows(record_list)
        generatedids = []
        sample_suffix = 'ZOTU'  # suffix for pk
        suffix_primarykey = 'MDDBOTU'  # label for entity table "ref_zotus"
        index_of_key_column = 0

        """
        Replace original ZOTU id labels and replace with PKs
        """
        zotu_labels_to_fetch = pandas.read_csv(otuseq_mapping_toupdatepk, header=0)
        refseq_length = zotu_labels_to_fetch.sequence.str.len()
        """
        This keeps track of how many new reference ZOTUs are generated.
        Initially it will count how many PKs need to be generated
        constraint: LIM set up to 10^6 ZOTUs (aka PKs)
        """
        total_rows_in_input = len(zotu_labels_to_fetch)
        zotusequence_key_list = []
        for record in range(1, total_rows_in_input+1):
            generate_primary_key = "0" * (6 - len(str(record))) + str(record)
            zotusequence_key_list.append(suffix_primarykey+str(generate_primary_key))
        append_keys = pandas.Series(zotusequence_key_list)
        zotu_labels_to_fetch.insert(loc=index_of_key_column, column='refsequence_pk', value=append_keys)
        zotu_labels_to_fetch.insert(loc=index_of_key_column, column='srr_name', value=srr_name)
        """
        BACKUP: generate mapping for relation tables 
        copy the mapping srr_name | otu_label | pk assigned | sequence to new mapping file
        """
        zotu_labels_to_fetch.to_csv(mapping_table_pk_zotu_srr, encoding='utf-8', index=False)
        newupdate_remove_otuid = zotu_labels_to_fetch.drop('otuseq_id', axis=1)
        newupdate_remove_srrid = newupdate_remove_otuid.drop('srr_name', axis=1)
        """
        METADATA FILE extension
        Append attributes on csv file
        """
        newupdate_remove_srrid.insert(loc=index_of_marker_column, column='marker_type', value=its2)
        newupdate_remove_srrid.insert(loc=index_of_refseqlength_column, column='refseq_length', value=refseq_length)
        newupdate_remove_srrid.to_csv(sequence_table_pk, encoding='utf-8', index=False)
        generate_header_track(record_track)
        amount_fasta_seq1 = newupdate_remove_srrid.shape[0]
        first_srr = [[srr_name, amount_fasta_seq1, 0, amount_fasta_seq1]]
        update_record = pandas.DataFrame(first_srr)
        save_record_track(record_track, update_record)
        print("complete")


# Interaction with the user: Ask the user the fasta file
if __name__ == '__main__':
    import sys
    try:
        Filename = sys.argv[1]  # fasta file
        Sequence = sys.argv[2]  # option generate primary keys
    except:
        print("Usage: CreateCsvFromFasta3.py <filename>.fa Y/N')")
        print("Please provide a fasta file followed by Y if you want primary keys, else N for keep original label names as ids")
        raise SystemExit
    else:
        if Sequence == "Y" or Sequence == "N" and len(sys.argv) == 3:  # check if value is provided
            Main(Filename, Sequence)
        else:
            print("Please specify if you want to generate primary keys for your sequence.")
            raise SystemExit
