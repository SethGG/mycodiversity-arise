# mycodiversity-arise
This is a fork of the mycodiversity repository aimed at extending the PROFUNGIS pipeline to accept raw fungal ITS data from the Naturalis ARISE project (which is not retreived from the SRA). New scripts have been written for extracting the data to the correct file structure for the PROFUNGIS pipeline and several changes have been made to the PROFUNGIS pipeline in order to work with more up to date dependancies.

## New scripts
- **extractARISEDATA.py**: This script requires the ARISE data to be present in the diretory called "ARISE_data". First the checksums for all the compressed reads are checked. The reads are then extracted in the "PROFUNGIS/samples" directory where every sample gets named by their unique NBCLAB identifier. Finally, sample list files are generated in the "PROFUNGIS" directory for each geographic location of the study samples (A and B). These sample lists can be used as input for the PROFUNGIS pipeline.

## Modifications to PROFUNGIS
- Forward and reverse primers used for the ARISE data have been added to **deps/primers.data**.
- "--cores" argument added to the snakemake call in **startPROFUNGIS.py** as this is required for newer versions of Snakemake.
- Invalid calls to dependancies have been fixed in **Snakefile**:
    - "flash" to "./deps/flash"
    - "vsearch" to "./deps/vsearch"
- Fixed an error in the "filter_contamination_filter" rule in **Snakefile** where the BLAST directory could not be created because it already exists. Fixed by adding the "-p" flag to "mkdir".
- Fixed to log output of the "filter_primers" rule in **Snakefile** being written to stdout instead of the log file. Fixed by changing the redirect from "2>" to ">".
- Added the "-n 2" argument to the flash call in the "filter_primers" rule in **Snakefile**. This allows both the forward and reverse primer to be cut from a single read. The [DADA2 based pipeline](https://github.com/naturalis/arise-metabarcoding-biodiversity/blob/main/src/DADA2.R#L37-L42) developed by Naturalis for the same data also uses this option.
- The output of the "filter_primers" rule in **Snakefile** has been marked as temporary to save disk space. For the reverse reads this effect was achieved by calling "rm" on the filtered read file after merging.
- The **requirements.txt** file has been replaced with my currect Python environment (Python 3.10.12).

# Generating ZOTUs
1. Run **extractARISEDATA.py** from the root project directory
    ```shell
    python extractARISEDATA.py
    ```
2. Run **startPROFUNGIS** from the PROFUNGIS directory using either sample list (A or B)
    ```shell
    python startPROFUNGIS.py -f ARISEF1 -r ARISER -p illumina -l -m sample_list_A.txt
    ```
    Only one of the five forward primers can be used. The above mentioned [DADA2 based pipeline](https://github.com/naturalis/arise-metabarcoding-biodiversity/blob/main/src/DADA2.R#L37-L42) assures us however that the error rate default of 0.1 in cutadapt takes out all forward reads when selecting the first primer.
3. PROFUNGIS_post_processing: TODO


(original README)
# mycodiversity
Pipelines for analysing fungal diversity data

## repository structure
The repository is structured as followed:
- **PROFUNGIS** : Pipeline for processing raw Fungal ITS Sequences markers obtained from SRA to unique ZOTUs sequences.
- **PROFUNGIS_post_processing** : incorporation of new ZOTUs sequences into MDDB reference table "ref_sequence" and update of mapping table ZOTU reference SRA
- **ncbi_data_aquistion** : automatic pipeline for retrieving sequence read archive metadata that is associated to open source publication linked to metabarcoding studies.

## method

please read the README files for each pipeline for running the relevant pipelines.

