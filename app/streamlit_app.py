import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(page_title="OFF Project", layout="wide")
st.title("OFF Project — Clean MVP Explorer")

data_dir = Path("data/curated/off_mvp_clean_parquet")
files = sorted(data_dir.glob("clean-part-*.parquet"))

st.write(f"Clean parquet parts found: {len(files)}")

if len(files) == 0:
    st.warning("Aucun parquet clean trouvé (normal sur Streamlit Cloud).")
    st.info("Exécute le script de cleaning en local puis relance l’app.")
    st.stop()

df = pd.read_parquet(files[0])

st.subheader("Aperçu")
st.dataframe(df.head(50))

st.subheader("Qualité rapide")
st.write("Rows (this part):", len(df))
st.write("Missing % (this part):")
st.write((df.isna().mean() * 100).round(2))
