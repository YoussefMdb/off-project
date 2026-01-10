import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(page_title="OFF Project", layout="wide")
st.title("OFF Project — MVP Explorer")

data_dir = Path("data/curated/off_mvp_parquet")
files = sorted(data_dir.glob("part-*.parquet"))

st.write(f"Parquet parts found: {len(files)}")

if len(files) == 0:
    st.warning("Aucun fichier parquet local trouvé (normal sur Streamlit Cloud).")
    st.info("Pour voir les données : exécute l’ingestion en local puis relance l’app.")
    st.stop()

df = pd.read_parquet(files[0])
st.write("Preview (first parquet part):")
st.dataframe(df.head(50))
