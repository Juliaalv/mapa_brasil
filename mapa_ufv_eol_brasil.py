import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static

@st.cache_data
def load_data():
    return pd.read_csv("df_geracao_ufv_eol.csv")  

df = load_data()

# Converter Latitude e Longitude para float
df["Latitude"] = df["Latitude"].str.replace(",", ".", regex=True).astype(float)
df["Longitude"] = df["Longitude"].str.replace(",", ".", regex=True).astype(float)

# Remover linhas com Latitude ou Longitude ausente
df = df.dropna(subset=["Latitude", "Longitude"])

# Título do App
st.title("Geração de Energia Eólica e Solar no Brasil")

# Filtro interativo
tipos_disponiveis = ["EOL", "UFV"]
selecionados = st.multiselect("Selecione os tipos que deseja visualizar no mapa:", tipos_disponiveis, default=tipos_disponiveis)

# Criar o mapa
m = folium.Map(location=[-14.2350, -51.9253], zoom_start=4, tiles="cartodbpositron")

# Criar grupos para cada tipo de geração
if "EOL" in selecionados:
    eol_group = folium.FeatureGroup(name="Eólica (EOL)", show=True)
    for _, row in df[df["Tipo de Geração"] == "EOL"].iterrows():
        folium.CircleMarker(
            location=[row["Latitude"], row["Longitude"]],
            radius=1.5,
            color="blue",
            fill=True,
            fill_color="blue",
            fill_opacity=0.7,
            popup=row["Empreendimento"],
        ).add_to(eol_group)
    eol_group.add_to(m)

if "UFV" in selecionados:
    ufv_group = folium.FeatureGroup(name="Solar (UFV)", show=True)
    for _, row in df[df["Tipo de Geração"] == "UFV"].iterrows():
        folium.CircleMarker(
            location=[row["Latitude"], row["Longitude"]],
            radius=1.5,
            color="orange",
            fill=True,
            fill_color="orange",
            fill_opacity=0.7,
            popup=row["Empreendimento"],
        ).add_to(ufv_group)
    ufv_group.add_to(m)

# Adicionar controle de camadas (legenda interativa)
folium.LayerControl(collapsed=False).add_to(m)

# Legenda fixa
legend_html = """
<div style="position: fixed; 
            bottom: 50px; left: 50px; width: 200px; height: 90px; 
            background-color: white; z-index:9999; padding: 10px;
            border-radius: 10px; box-shadow: 2px 2px 5px rgba(0,0,0,0.3);
            font-size:14px;">
    <strong>Legenda:</strong><br>
    <span style="color:blue;">⬤</span> Eólica (EOL) <br>
    <span style="color:orange;">⬤</span> Solar (UFV)
</div>
"""
st.markdown(legend_html, unsafe_allow_html=True)

# Mostrar o mapa
folium_static(m, width=800, height=750)
