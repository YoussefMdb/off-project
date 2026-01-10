import gzip
from pathlib import Path

src_path = Path("data/raw/en.openfoodfacts.org.products.csv.gz")
out_path = Path("data/raw/off_sample_10k.tsv")

with gzip.open(src_path, "rt", encoding="utf-8", errors="replace") as fin, \
     out_path.open("w", encoding="utf-8", newline="") as fout:
    header = fin.readline()
    fout.write(header)
    for i, line in enumerate(fin, start=1):
        fout.write(line)
        if i >= 10_000:
            break

print("Wrote:", out_path, "lines:", 10_001)
