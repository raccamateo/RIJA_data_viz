import pandas as pd
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static
import streamlit as st

# Load data
file_path = 'Mapeo_de_Casos_With_Coordinates.xlsx'
mapeo_de_casos = pd.read_excel(file_path)

# Handle NaN values and round years
if 'Año de Inicio' in mapeo_de_casos.columns:
    mapeo_de_casos['Año de Inicio'] = mapeo_de_casos['Año de Inicio'].fillna(0).round(0).astype(int)
    mapeo_de_casos.loc[mapeo_de_casos['Año de Inicio'] == 0, 'Año de Inicio'] = None  # Replace 0 with None for clarity

# Streamlit layout
st.set_page_config(layout="wide")  # Set layout to wide for better screen utilization
st.title("Mapa Interactivo de Iniciativas Ciudadanas")

# Filters placed above the map
st.markdown(
    """
    <style>
    .filter-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 20px;
    }
    .filter-container div {
        flex: 1;
        margin: 0 10px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
st.markdown('<div class="filter-container">', unsafe_allow_html=True)

# Create filters
col1, col2, col3 = st.columns([1, 1, 1], gap="small")
with col1:
    selected_countries = st.multiselect(
        "Seleccionar Países", sorted(mapeo_de_casos['País'].dropna().unique()), help="Filtra por país"
    )
with col2:
    selected_drivers = st.multiselect(
        "Seleccionar Impulsores", sorted(mapeo_de_casos['Impulsores'].dropna().unique()), help="Filtra por impulsores"
    )
with col3:
    selected_years = st.multiselect(
        "Seleccionar Años", sorted(mapeo_de_casos['Año de Inicio'].dropna().unique()), help="Filtra por años"
    )

st.markdown('</div>', unsafe_allow_html=True)

# Filter data
filtered_data = mapeo_de_casos.copy()
if selected_countries:
    filtered_data = filtered_data[filtered_data['País'].isin(selected_countries)]
if selected_drivers:
    filtered_data = filtered_data[filtered_data['Impulsores'].isin(selected_drivers)]
if selected_years:
    filtered_data = filtered_data[filtered_data['Año de Inicio'].isin(selected_years)]

# Center map with bounds
if not filtered_data.empty:
    map_bounds = [[filtered_data['Latitude'].min(), filtered_data['Longitude'].min()],
                  [filtered_data['Latitude'].max(), filtered_data['Longitude'].max()]]
else:
    map_bounds = [[-90, -180], [90, 180]]  # Default global bounds for empty data

# Create map with appropriate size and bounds
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
        <b><a href="{row['Links / Recursos']}" target="_blank">Ficha técnica</a></b>
        """
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
