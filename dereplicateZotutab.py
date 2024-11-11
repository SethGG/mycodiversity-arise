import sys
from collections import defaultdict


def main(derep_input, zotutab_input, zotutab_output):
    old_zotutab = {}
    header = None
    with open(zotutab_input, "r") as f:
        for line in f:
            if header is None:
                header = line
            else:
                parts = line.strip().split()
                zotu, count = parts[0], int(parts[1])
                old_zotutab[zotu] = count

    cluster_counts = defaultdict(int)
    with open(derep_input, "r") as f:
        for line in f:
            parts = line.strip().split()
            zotu, cluster = parts[0], parts[1]
            cluster_counts[cluster] += old_zotutab[zotu]

    with open(zotutab_output, "w") as f:
        f.write(header)
        for cluster, count in cluster_counts.items():
            f.write(f"{cluster}\t{count}\n")


if __name__ == "__main__":
    derep_input = sys.argv[1]
    zotutab_input = sys.argv[2]
    zotutab_output = sys.argv[3]
    main(derep_input, zotutab_input, zotutab_output)
