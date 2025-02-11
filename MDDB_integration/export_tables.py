import pandas as pd
import pymonetdb
import numpy as np
import os

# set export dir
export_dir = "export_tables"
os.makedirs(export_dir, exist_ok=True)

# direct database import
con = pymonetdb.connect(username="monetdb", password="monetdb", hostname="localhost", database="MDDB4", port="9999")

cursor = con.cursor()

cursor.execute("SELECT tables.name FROM tables WHERE tables.system=false;")
tables = [row[0] for row in cursor]

for table in tables:
    print(f"Exporting table: {table}")
    cursor.execute(f'SELECT * FROM "{table}";')
    df = pd.DataFrame(cursor.fetchall(), columns=[c.name for c in cursor.description])
    df = df.replace('', np.nan)
    df.to_csv(os.path.join(export_dir, f"{table}.csv"), index=False)
