from collections import Counter
import pandas as pd
import sys


def aggregate_chunk_info(group):
    chunk_counts = Counter(group["chunk"])
    majority_chunk, majority_count = chunk_counts.most_common(1)[0]

    return pd.Series({
        "num_hits": len(group),
        "avg_identity": group["identity"].mean(),
        "num_chunks": len(chunk_counts),
        "maj_chunk": majority_chunk,
        "maj_chunk_count": majority_count
    })


if __name__ == "__main__":
    input_csv = sys.argv[1]
    output_csv = sys.argv[2]

    df = pd.read_csv(input_csv)

    df_out = df.groupby("refsequence_pk").apply(aggregate_chunk_info, include_groups=False).reset_index()

    df_out.to_csv(output_csv, index=False)
