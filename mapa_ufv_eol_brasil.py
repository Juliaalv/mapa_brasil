import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static

@st.cache_data
def load_data():
    geracao_75 = pd.read_csv("df_ger_brasil_75_ufv_eol.csv")
    geracao_5 = pd.read_csv("df_ger_brasil_5_ufv_eol.csv")
    return geracao_75, geracao_5


geracao_75, geracao_5 = load_data()

# Sidebar para seleção do tipo de geração
st.sidebar.title("Opções de Visualização")
opcao_geracao = st.sidebar.radio("Selecione a faixa de geração:", ["Geração ≥ 75 kW", "Geração ≥ 5 MW"])

# Definir os dados conforme a opção escolhida
dados_geracao = geracao_75.copy() if opcao_geracao == "Geração ≥ 75 kW" else geracao_5.copy()

dados_geracao["Latitude"] = dados_geracao["Latitude"].astype(str).str.replace(",", ".", regex=True).astype(float)
dados_geracao["Longitude"] = dados_geracao["Longitude"].astype(str).str.replace(",", ".", regex=True).astype(float)

# Remover linhas com Latitude ou Longitude ausente
dados_geracao.dropna(subset=["Latitude", "Longitude"], inplace=True)

st.title("Geração de Energia Eólica e Solar no Brasil")

# Filtro 
tipos_disponiveis = ["EOL", "UFV"]
selecionados = st.multiselect("Selecione os tipos que deseja visualizar no mapa:", tipos_disponiveis, default=tipos_disponiveis)

# mapa
m = folium.Map(location=[-7.5, -36.5], zoom_start=7, tiles="cartodbpositron")

# Grupos por tipo de geração
if "EOL" in selecionados:
    eol_group = folium.FeatureGroup(name="Eólica (EOL)", show=True)
    for _, row in dados_geracao[dados_geracao["Tipo de Geração"] == "EOL"].iterrows():
        folium.CircleMarker(
            location=[row["Latitude"], row["Longitude"]],
            radius=2,
            color="blue",
            fill=True,
            fill_color="blue",
            fill_opacity=0.7,
            popup=row["Empreendimento"],
        ).add_to(eol_group)
    eol_group.add_to(m)

if "UFV" in selecionados:
    ufv_group = folium.FeatureGroup(name="Solar (UFV)", show=True)
    for _, row in dados_geracao[dados_geracao["Tipo de Geração"] == "UFV"].iterrows():
        folium.CircleMarker(
            location=[row["Latitude"], row["Longitude"]],
            radius=2,
            color="orange",
            fill=True,
            fill_color="orange",
            fill_opacity=0.7,
            popup=row["Empreendimento"],
        ).add_to(ufv_group)
    ufv_group.add_to(m)

# Adicionar controle de camadas
folium.LayerControl(collapsed=False).add_to(m)

legend_html = """
<div style="position: fixed; 
            bottom: 50px; right: 50px; width: 200px; height: 90px; 
            background-color: white; z-index:9999; padding: 10px;
            border-radius: 10px; box-shadow: 2px 2px 5px rgba(0,0,0,0.3);
            font-size:14px;">
    <strong>Legenda:</strong><br>
    <span style="color:blue;">⬤</span> Eólica (EOL) <br>
    <span style="color:orange;">⬤</span> Solar (UFV)
</div>
"""
st.markdown(legend_html, unsafe_allow_html=True)
folium_static(m, width=800, height=750)

