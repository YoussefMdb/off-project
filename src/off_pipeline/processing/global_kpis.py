import argparse
from pathlib import Path

import pandas as pd


def compute_global_missing(input_dir: Path) -> pd.DataFrame:
    files = sorted(input_dir.glob("clean-part-*.parquet"))
    if not files:
        raise SystemExit(f"No parquet files found in: {input_dir}")

    total_rows = 0
    non_null_counts = None  # pd.Series

    for fp in files:
        df = pd.read_parquet(fp)

        # init once with all columns
        if non_null_counts is None:
            non_null_counts = pd.Series(0, index=df.columns, dtype="int64")

        total_rows += len(df)
        non_null_counts = non_null_counts.add(df.notna().sum().astype("int64"), fill_value=0)

        print(f"scanned {fp.name} rows={len(df)}")

    if total_rows == 0:
        raise SystemExit("Total rows = 0 (unexpected)")

    missing_pct = (1 - (non_null_counts / total_rows)) * 100
    out = (
        pd.DataFrame({"column": missing_pct.index, "missing_%": missing_pct.values})
        .sort_values("missing_%", ascending=False)
        .reset_index(drop=True)
    )
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--input-dir",
        type=str,
        default="data/curated/off_mvp_clean_parquet",
        help="Folder with clean-part-*.parquet",
    )
    ap.add_argument(
        "--output-csv",
        type=str,
        default="data/curated/global_kpis.csv",
        help="Output CSV path",
    )
    args = ap.parse_args()

    input_dir = Path(args.input_dir)
    output_csv = Path(args.output_csv)
    output_csv.parent.mkdir(parents=True, exist_ok=True)

    df_stats = compute_global_missing(input_dir)
    df_stats.to_csv(output_csv, index=False, encoding="utf-8")

    print("\n✅ Wrote:", output_csv)
    print("Top 10 missing:")
    print(df_stats.head(10).to_string(index=False))
    print("\nTop 10 complete:")
    print(df_stats.tail(10).sort_values("missing_%").to_string(index=False))


if __name__ == "__main__":
    main()
