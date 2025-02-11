import pandas as pd
import os
import re

# set export dir
export_dir = "export_tables"
df_sample = pd.read_csv(os.path.join(export_dir, "Sample.csv"))

# set profungis output
zotus_dir = os.path.join("..", "PROFUNGIS", "2024_11_18_16_07_output", "FINAL")
for filename in sorted(os.listdir(zotus_dir)):
    if filename.endswith(".fa"):
        input_path = os.path.join(zotus_dir, filename)
        sample_id = filename.split("_")[0]
        if sample_id not in df_sample["sample_id"]:
            last_pk = df_sample.iloc[-1]["sample_pk"]
            new_pk = re.sub(r'[0-9]+$',
                            lambda x: f"{str(int(x.group())+1).zfill(len(x.group()))}",
                            last_pk)
            new_entry = {
                "sample_pk": new_pk,
                "sample_id": sample_id,
                "sample_type": "soil",
                "sample_link": f"https://mycodiversity.liacs.nl/arise-samples/{sample_id}",
                "sampl_collect_device": "PVC tube 32 mm diam.",
                "collection_date": "2021",
                "collection_year": "2021",
                "sampl_size": "Samples to 100 mm depth from 100-m2 area",
                "env_material": "soil",
                "country_geonames_continent": "Europe",
                "country_parent": "Western Europe",
                "country_geoname_pref_en": "The Netherlands",
                "country_geonamesname": "Kingdom of the Netherlands",
                "country_geoname_abbrev": "NL",
                "country_geoname_url": "https://www.geonames.org/2750405/kingdom-of-the-netherlands.html",
                "country_geoname_id": 2750405
            }
            df_sample.loc[df_sample.shape[0]] = new_entry

print(df_sample.loc[211])
