import pandas as pd
from pathlib import Path
import math

src_path = Path("data/raw/en.openfoodfacts.org.products.csv.gz")
out_dir = Path("data/curated/off_mvp_parquet")
mvp_path = Path("src/off_pipeline/ingestion/mvp_columns.txt")

mvp = [c.strip() for c in mvp_path.read_text(encoding="ascii").splitlines() if c.strip()]

out_dir.mkdir(parents=True, exist_ok=True)

reader = pd.read_csv(
    src_path,
    sep="\t",
    compression="gzip",
    usecols=mvp,
    chunksize=200_000,
    low_memory=False,
)

total = 0
part = 0

for chunk in reader:
    chunk.columns = [c.strip() for c in chunk.columns]
    total += len(chunk)
    part += 1
    out_path = out_dir / f"part-{part:04d}.parquet"
    chunk.to_parquet(out_path, index=False)
    print("wrote", out_path, "rows", len(chunk))

print("Done. total rows:", total, "parts:", part)
