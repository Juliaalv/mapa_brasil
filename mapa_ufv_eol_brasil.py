import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static


@st.cache_data
def load_data():
    return pd.read_csv("df_geracao_ufv_eol.csv")  

df = load_data()

# Converter Latitude e Longitude para float, corrigindo vírgulas
df["Latitude"] = df["Latitude"].str.replace(",", ".", regex=True).astype(float)
df["Longitude"] = df["Longitude"].str.replace(",", ".", regex=True).astype(float)

# Remover linhas com Latitude ou Longitude ausente
df = df.dropna(subset=["Latitude", "Longitude"])

# Criar um mapa centrado no Brasil
m = folium.Map(location=[-14.2350, -51.9253], zoom_start=4, tiles="cartodbpositron")

# Adicionar os pontos ao mapa
for _, row in df.iterrows():
    color = "blue" if row["Tipo de Geração"] == "EOL" else "orange"
    folium.CircleMarker(
        location=[row["Latitude"], row["Longitude"]],
        radius=1.5,
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=0.7,
        popup=row["Empreendimento"],
    ).add_to(m)

# Criar o app no Streamlit
st.title("Mapa de Empreendimentos UFV e EOL no Brasil")

# Exibir o mapa no Streamlit
folium_static(m, width=1400, height=750)
