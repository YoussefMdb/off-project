import streamlit as st
import pandas as pd
from pathlib import Path
import re

st.set_page_config(page_title="OFF Project", layout="wide")
st.title("OFF Project — Clean MVP Explorer")

data_dir = Path("data/curated/off_mvp_clean_parquet")
files = sorted(data_dir.glob("clean-part-*.parquet"))

st.write(f"Clean parquet parts found: {len(files)}")

if not files:
    st.warning("Aucun parquet clean trouvé (normal sur Streamlit Cloud).")
    st.info("Exécute le script de cleaning en local puis relance l’app.")
    st.stop()

# ---------- Choix de la part ----------
part_idx = st.selectbox(
    "Choisir une part (200k lignes chacune environ)",
    list(range(len(files))),
    format_func=lambda i: files[i].name,
)

@st.cache_data(show_spinner=False)
def load_part(path: Path) -> pd.DataFrame:
    return pd.read_parquet(path)

df = load_part(files[part_idx])

# ---------- Filtre countries tags ----------
st.subheader("Filtre (countries tags OFF)")

countries_series = df.get("countries")
if countries_series is None:
    st.error("Colonne 'countries' introuvable dans ce parquet.")
    st.stop()

countries_series = countries_series.dropna().astype(str)

all_country_tags = sorted(
    set(tag for s in countries_series for tag in s.split("|") if tag)
)

selected_tags = st.multiselect(
    "Pays (tags OFF) — ex: en:france, en:canada, en:brazil",
    options=all_country_tags,
)

reset = st.button("Reset filtre")
if reset:
    selected_tags = []

def filter_by_countries_tags(df_: pd.DataFrame, tags: list[str]) -> pd.DataFrame:
    if not tags:
        return df_
    pattern = r"(^|\|)(" + "|".join(re.escape(t) for t in tags) + r")(\||$)"
    mask = df_["countries"].fillna("").astype(str).str.contains(pattern, regex=True)
    return df_[mask].copy()

dff = filter_by_countries_tags(df, selected_tags)

# ---------- KPIs ----------
st.subheader("KPIs (sur cette part)")
c1, c2, c3 = st.columns(3)
c1.metric("Rows", f"{len(dff):,}".replace(",", " "))

nutri_rate = (dff["nutriscore_grade"].notna().mean() * 100) if "nutriscore_grade" in dff.columns else 0.0
nova_rate = (dff["nova_group"].notna().mean() * 100) if "nova_group" in dff.columns else 0.0

c2.metric("Produits avec Nutri-Score", f"{nutri_rate:.1f}%")
c3.metric("Produits avec NOVA", f"{nova_rate:.1f}%")

# ---------- Qualité ----------
st.subheader("Qualité rapide (sur cette part filtrée)")
missing_pct = (dff.isna().mean() * 100).round(2).sort_values(ascending=False)

st.markdown("**Top 10 colonnes les plus manquantes (%)**")
st.dataframe(
    missing_pct.head(10).reset_index().rename(columns={"index": "column", 0: "missing_%"}),
    width="stretch",
)

st.markdown("**Top 10 colonnes les plus complètes (%)**")
st.dataframe(
    missing_pct.tail(10).sort_values().reset_index().rename(columns={"index": "column", 0: "missing_%"}),
    width="stretch",
)

# ---------- Aperçu ----------
st.subheader("Aperçu (50 lignes)")
st.dataframe(dff.head(50), width="stretch")
