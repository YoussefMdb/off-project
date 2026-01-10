import argparse
import pandas as pd
from pathlib import Path

def norm_text(x):
    if pd.isna(x):
        return None
    s = str(x).strip()
    return s if s else None

def norm_list_str(x):
    """Retourne une string normalisée séparée par | (ex: en:france|en:germany)."""
    if pd.isna(x):
        return None
    s = str(x).strip()
    if not s:
        return None
    parts = [p.strip() for p in s.split(",")]
    parts = [p for p in parts if p]
    # normalise: lower + enlève doubles
    seen = set()
    out = []
    for p in parts:
        p2 = p.lower()
        if p2 not in seen:
            seen.add(p2)
            out.append(p2)
    return "|".join(out) if out else None

def to_float(x):
    if pd.isna(x) or x == "":
        return None
    try:
        return float(x)
    except Exception:
        return None

def main(limit_parts: int):
    in_dir = Path("data/curated/off_mvp_parquet")
    out_dir = Path("data/curated/off_mvp_clean_parquet")
    out_dir.mkdir(parents=True, exist_ok=True)

    files = sorted(in_dir.glob("part-*.parquet"))
    if not files:
        raise SystemExit("No input parquet parts found in data/curated/off_mvp_parquet")

    files = files[:limit_parts]
    total = 0

    for i, fp in enumerate(files, start=1):
        df = pd.read_parquet(fp)

        # champs texte
        for c in ["code", "product_name", "quantity", "serving_size", "ingredients_text", "allergens", "traces"]:
            if c in df.columns:
                df[c] = df[c].map(norm_text)

        # champs tags/listes
        for c in ["brands", "categories", "countries", "pnns_groups_1", "pnns_groups_2", "nutriscore_grade"]:
            if c in df.columns:
                df[c] = df[c].map(norm_list_str)

        # champs numériques (float)
        num_cols = [
            "nova_group",
            "energy-kcal_100g",
            "fat_100g",
            "saturated-fat_100g",
            "carbohydrates_100g",
            "sugars_100g",
            "fiber_100g",
            "proteins_100g",
            "salt_100g",
            "sodium_100g",
        ]
        for c in num_cols:
            if c in df.columns:
                df[c] = df[c].map(to_float)

        out_path = out_dir / f"clean-{fp.name}"
        df.to_parquet(out_path, index=False)
        total += len(df)
        print("wrote", out_path, "rows", len(df))

    print("Done. parts:", len(files), "total rows:", total)

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit-parts", type=int, default=1, help="Nombre de parts à traiter pour valider")
    args = ap.parse_args()
    main(args.limit_parts)
