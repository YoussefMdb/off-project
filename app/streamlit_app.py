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
missing_pct = (df.isna().mean() * 100).round(2).sort_values(ascending=False)

st.write("Rows (this part):", len(df))

st.markdown("**Top 10 colonnes les plus manquantes (%)**")
st.dataframe(missing_pct.head(10).reset_index().rename(columns={"index":"column", 0:"missing_%"}))

st.markdown("**Top 10 colonnes les plus complètes (%)**")
st.dataframe(missing_pct.tail(10).sort_values().reset_index().rename(columns={"index":"column", 0:"missing_%"}))
