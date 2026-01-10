import gzip

path = "data/raw/en.openfoodfacts.org.products.csv.gz"

with gzip.open(path, "rt", encoding="utf-8", errors="replace") as f:
    header = f.readline().strip()

cols = header.split("\t")
print(f"Columns: {len(cols)}")
print("First 30 columns:")
for c in cols[:30]:
    print("-", c)
