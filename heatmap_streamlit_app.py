import streamlit as st
import folium
from folium.plugins import HeatMap
import pandas as pd
from streamlit_folium import st_folium

# Título da aplicação
st.title("Inundações por Ano, Mês e Natureza")

# Carregar os dados
@st.cache_data
def carregar_dados():
    df = pd.read_excel("Inundacoes_2014_2025_Normalizado.xlsx")
    df["Ano"] = pd.to_datetime(df["Data/hora"]).dt.year
    df["Mês"] = pd.to_datetime(df["Data/hora"]).dt.month_name()
    return df

df = carregar_dados()

# Filtros
anos = sorted(df["Ano"].unique())
naturezas = sorted(df["Natureza ANPC"].unique())

ano_escolhido = st.selectbox("Seleciona o Ano", anos)
natureza_escolhida = st.selectbox("Seleciona a Natureza da Ocorrência", naturezas)

meses_disponiveis = sorted(df[df["Ano"] == ano_escolhido]["Mês"].unique())
mes_escolhido = st.selectbox("Seleciona o Mês (opcional)", ["Todos"] + meses_disponiveis)

# Filtrar os dados
df_filtrado = df[(df["Ano"] == ano_escolhido) & (df["Natureza ANPC"] == natureza_escolhida)]
if mes_escolhido != "Todos":
    df_filtrado = df_filtrado[df_filtrado["Mês"] == mes_escolhido]

# Gerar mapa
if df_filtrado.empty:
    st.warning("Não existem dados para os filtros selecionados.")
else:
    m = folium.Map(location=[df_filtrado["Latitude"].mean(), df_filtrado["Longitude"].mean()], zoom_start=11)
    pontos = df_filtrado[["Latitude", "Longitude"]].dropna().values.tolist()
    HeatMap(pontos, radius=10, blur=15).add_to(m)
    st_folium(m, width=700, height=500)
