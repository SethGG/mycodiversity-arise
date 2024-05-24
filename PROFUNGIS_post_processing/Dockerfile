FROM python:3.9.6-slim

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN apt-get update
RUN apt-get -y install gcc
RUN pip install biopython

COPY generate_zotu_ref1.py generate_zotu_ref1.py
COPY SRR1502226_zotus_final.fa SRR1502226_zotus_final.fa
ENTRYPOINT ["python", "generate_zotu_ref1.py"]
