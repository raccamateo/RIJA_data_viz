import pandas as pd
import plotly.express as px
import streamlit as st

# Load data
file_path = 'Mapeo_de_Casos_With_Coordinates.xlsx'
mapeo_de_casos = pd.read_excel(file_path)

# Add count column
mapeo_de_casos['Conteo'] = 1

# Streamlit layout
st.title("Treemap - Distribución de Iniciativas")

# Sidebar filters
st.sidebar.header("Filtros")
selected_countries = st.sidebar.multiselect("Seleccionar Países", sorted(mapeo_de_casos['País'].dropna().unique()))
selected_drivers = st.sidebar.multiselect("Seleccionar Impulsores", sorted(mapeo_de_casos['Impulsores'].dropna().unique()))

# Filter data
filtered_data = mapeo_de_casos.copy()
if selected_countries:
    filtered_data = filtered_data[filtered_data['País'].isin(selected_countries)]
if selected_drivers:
    filtered_data = filtered_data[filtered_data['Impulsores'].isin(selected_drivers)]

# Treemap
fig = px.treemap(
    filtered_data,
    path=['País', 'Type'],  # Adjust hierarchy as needed
    values='Conteo',
    title="Distribución de Iniciativas por País y Tipo",
    color='País',
    color_discrete_sequence=px.colors.qualitative.Safe,
    hover_data=['País', 'Type', 'Conteo']
)
st.plotly_chart(fig)
