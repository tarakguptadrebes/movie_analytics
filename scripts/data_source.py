
import pandas as pd

url = "https://datasets.imdbws.com/title.basics.tsv.gz"
df = pd.read_csv(url, sep="\t")

print(df.keys())

