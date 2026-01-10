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

st.subheader("Filtre (countries tags)")
countries_series = df["countries"].dropna().astype(str)

# on garde uniquement les tokens de type en:xxx (tags OFF)
all_tokens = []
for s in countries_series:
    for tok in s.split("|"):
        tok = tok.strip().lower()
        if tok.startswith("en:"):
            all_tokens.append(tok)

all_countries = sorted(set(all_tokens))
selected = st.selectbox("Pays (tag OFF)", ["(Tous)"] + all_countries)

if selected != "(Tous)":
    mask = df["countries"].fillna("").str.contains(rf"(^|\|){selected}(\||$)", regex=True)
    dff = df[mask].copy()
else:
    dff = df

st.subheader("KPIs (sur cette part)")
col1, col2, col3 = st.columns(3)
col1.metric("Rows", f"{len(dff):,}".replace(",", " "))
col2.metric("Produits avec Nutri-Score", f"{dff['nutriscore_grade'].notna().mean()*100:.1f}%")
col3.metric("Produits avec NOVA", f"{dff['nova_group'].notna().mean()*100:.1f}%")

st.subheader("Qualité rapide")
missing_pct = (dff.isna().mean() * 100).round(2).sort_values(ascending=False)

st.markdown("**Top 10 colonnes les plus manquantes (%)**")
st.dataframe(missing_pct.head(10).reset_index().rename(columns={"index":"column", 0:"missing_%"}))

st.markdown("**Aperçu**")
st.dataframe(dff.head(50))
