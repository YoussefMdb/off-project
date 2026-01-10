import pandas as pd
from pathlib import Path

sample_path = Path("data/raw/off_sample_10k.tsv")
mvp_path = Path("src/off_pipeline/ingestion/mvp_columns.txt")

mvp = [c.strip() for c in mvp_path.read_text(encoding="ascii").splitlines() if c.strip()]

df = pd.read_csv(sample_path, sep="\t", usecols=mvp, low_memory=False)
print("Rows:", len(df), "Cols:", df.shape[1])
