import streamlit as st

# Streamlit page configuration must be the first command
st.set_page_config(layout="wide", page_title="Mapa Interactivo de Iniciativas", page_icon="🌍")

import pandas as pd
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static

# Load data
file_path = 'Mapeo_de_Casos_With_Coordinates.xlsx'
base_url = 'https://github.com/raccamateo/RIJA_data_viz/raw/main/'  # Use 'raw' to link directly to the files
mapeo_de_casos = pd.read_excel(file_path)

# Complete mapping of initiatives to fichas
initiative_to_ficha = {
    "Capacitación en DDHH": "Capacitaciones Especializadas",
    "Reforma Judicial 2022": "Fortalecimiento Institucional",
    "Acceso a la Justicia para Todos": "Acceso Universal a la Justicia",
    "Mejoras en el Sistema Penal": "Modernización del Sistema Penal",
    "Digitalización de Expedientes": "Transformación Digital",
    "Capacitación en Género": "Capacitaciones Especializadas",
    "Justicia Comunitaria en Acción": "Justicia Comunitaria",
    "Protección de los Derechos de los Niños": "Derechos de los Niños",
    "Fortalecimiento de la Mediación": "Mediación y Resolución de Conflictos",
    "Iniciativa de Acceso Inclusivo": "Acceso Inclusivo",
    "Reformas Penales Modernas": "Modernización del Sistema Penal",
    "Digitalización Judicial 2021": "Transformación Digital",
    "Descentralización de Servicios Legales": "Justicia Comunitaria",
    "Fortalecimiento del Estado de Derecho": "Fortalecimiento Institucional",
    "Acceso a Justicia en Zonas Rurales": "Acceso Universal a la Justicia",
    "Capacitación sobre Ley de Género": "Capacitaciones Especializadas",
    "Desarrollo de Centros de Mediación": "Mediación y Resolución de Conflictos",
    "Programas para Protección Infantil": "Derechos de los Niños",
    "Capacitación en Resolución de Conflictos": "Capacitaciones Especializadas",
    "Acceso Digital a Expedientes": "Transformación Digital",
    "Reforma Legal Transparente": "Fortalecimiento Institucional",
    "Participación Ciudadana en Reformas": "Acceso Inclusivo",
}

# Map initiatives to fichas
mapeo_de_casos['Ficha'] = mapeo_de_casos['Nombre'].map(initiative_to_ficha)
mapeo_de_casos['Ficha Link'] = mapeo_de_casos['Ficha'].apply(
    lambda x: f"{base_url}Ficha%20-%20{x}.pdf" if pd.notna(x) else None
)

# Handle NaN values and round years
if 'Año de Inicio' in mapeo_de_casos.columns:
    mapeo_de_casos['Año de Inicio'] = mapeo_de_casos['Año de Inicio'].fillna(0).round(0).astype(int)
    mapeo_de_casos.loc[mapeo_de_casos['Año de Inicio'] == 0, 'Año de Inicio'] = None  # Replace 0 with None for clarity

# Streamlit layout
st.title("Mapa Interactivo de Iniciativas Ciudadanas")

# Filters
st.subheader("Filtros")
col1, col2, col3 = st.columns(3)

with col1:
    selected_countries = st.multiselect("Seleccionar Países", sorted(mapeo_de_casos['País'].dropna().unique()))

with col2:
    selected_drivers = st.multiselect("Seleccionar Impulsores", sorted(mapeo_de_casos['Impulsores'].dropna().unique()))

with col3:
    selected_years = st.multiselect("Seleccionar Años", sorted(mapeo_de_casos['Año de Inicio'].dropna().unique()))

# Filter data
filtered_data = mapeo_de_casos.copy()
if selected_countries:
    filtered_data = filtered_data[filtered_data['País'].isin(selected_countries)]
if selected_drivers:
    filtered_data = filtered_data[filtered_data['Impulsores'].isin(selected_drivers)]
if selected_years:
    filtered_data = filtered_data[filtered_data['Año de Inicio'].isin(selected_years)]

# Map bounds
if not filtered_data.empty:
    map_bounds = [[filtered_data['Latitude'].min(), filtered_data['Longitude'].min()],
                  [filtered_data['Latitude'].max(), filtered_data['Longitude'].max()]]
else:
    map_bounds = [[-90, -180], [90, 180]]  # Default bounds

# Create map
m = folium.Map(location=[0, 0], zoom_start=2, tiles="CartoDB positron", scrollWheelZoom=True, max_bounds=True)
marker_cluster = MarkerCluster().add_to(m)

# Add markers
for _, row in filtered_data.iterrows():
    if pd.notna(row['Latitude']) and pd.notna(row['Longitude']):
        popup_content = f"""
        <b>Nombre:</b> {row['Nombre']}<br>
        <b>País:</b> {row['País']}<br>
        <b>Impulsores:</b> {row['Impulsores']}<br>
        <b>Año:</b> {row['Año de Inicio'] if row['Año de Inicio'] else 'N/A'}<br>
        <b>Descripción:</b> {row['Description'] if 'Description' in row else 'Sin descripción disponible'}<br>
        """
        if pd.notna(row['Ficha Link']):
            popup_content += f"""<b><a href="{row['Ficha Link']}" target="_blank">Ficha técnica</a></b>"""
        
        folium.Marker(
            location=[row['Latitude'], row['Longitude']],
            popup=folium.Popup(popup_content, max_width=300),
            icon=folium.Icon(color="blue", icon="info-sign")
        ).add_to(marker_cluster)

# Fit map to bounds
m.fit_bounds(map_bounds)

# Display map
st.write("Mapa interactivo:")
folium_static(m, width=1400, height=800)
