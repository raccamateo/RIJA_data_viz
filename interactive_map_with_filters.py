import pandas as pd
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static
import streamlit as st

# Load data
file_path = 'Mapeo_de_Casos_With_Coordinates.xlsx'
mapeo_de_casos = pd.read_excel(file_path)

# Round years in the dataset
if 'Año de Inicio' in mapeo_de_casos.columns:
    mapeo_de_casos['Año de Inicio'] = mapeo_de_casos['Año de Inicio'].round(0).astype(int)

# Streamlit layout
st.title("Mapa Interactivo de Iniciativas Ciudadanas")

# Sidebar filters with compact styling
with st.sidebar:
    st.header("Filtros")
    st.markdown("<style>.sidebar .widget {font-size: 0.9rem;}</style>", unsafe_allow_html=True)
    selected_countries = st.multiselect("Seleccionar Países", sorted(mapeo_de_casos['País'].dropna().unique()))
    selected_drivers = st.multiselect("Seleccionar Impulsores", sorted(mapeo_de_casos['Impulsores'].dropna().unique()))
    selected_years = st.multiselect("Seleccionar Años", sorted(mapeo_de_casos['Año de Inicio'].dropna().unique()))

# Filter data
filtered_data = mapeo_de_casos.copy()
if selected_countries:
    filtered_data = filtered_data[filtered_data['País'].isin(selected_countries)]
if selected_drivers:
    filtered_data = filtered_data[filtered_data['Impulsores'].isin(selected_drivers)]
if selected_years:
    filtered_data = filtered_data[filtered_data['Año de Inicio'].isin(selected_years)]

# Center map with panoramic view
if not filtered_data.empty:
    avg_lat = filtered_data['Latitude'].mean()
    avg_lon = filtered_data['Longitude'].mean()
else:
    avg_lat, avg_lon = 0, 0  # Default center for empty data

# Create map with infinite scrolling and panoramic initial view
m = folium.Map(location=[avg_lat, avg_lon], zoom_start=2, tiles="CartoDB positron", scrollWheelZoom=True)
marker_cluster = MarkerCluster().add_to(m)

# Add markers
for _, row in filtered_data.iterrows():
    if pd.notna(row['Latitude']) and pd.notna(row['Longitude']):
        popup_content = f"""
        <b>Nombre:</b> {row['Nombre']}<br>
        <b>País:</b> {row['País']}<br>
        <b>Impulsores:</b> {row['Impulsores']}<br>
        <b>Año:</b> {row['Año de Inicio']}<br>
        <b><a href="{row['Links / Recursos']}" target="_blank">Ficha técnica</a></b>
        """
        folium.Marker(
            location=[row['Latitude'], row['Longitude']],
            popup=folium.Popup(popup_content, max_width=300),
            icon=folium.Icon(color="blue", icon="info-sign")
        ).add_to(marker_cluster)

# Display map
folium_static(m)
