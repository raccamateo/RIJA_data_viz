# Import necessary libraries
import streamlit as st
import pandas as pd
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static

# Load data including coordinates (replace 'path_to_file' with actual path)
file_path = 'Mapeo_de_Casos_With_Coordinates.xlsx'
mapeo_de_casos = pd.read_excel(file_path)

# Function to create a filtered map based on selected description type and filters
def create_filtered_map(description_type, year_filter, country_filter, drivers_filter, save_path="filtered_map.html"):
    # Apply filters
    filtered_data = mapeo_de_casos.copy()
    if year_filter:
        filtered_data = filtered_data[filtered_data['Año de Inicio'].isin(year_filter)]
    if country_filter:
        filtered_data = filtered_data[filtered_data['País'].isin(country_filter)]
    if drivers_filter:
        filtered_data = filtered_data[filtered_data['Impulsores'].isin(drivers_filter)]

    # Determine map center based on filtered data
    if not filtered_data.empty:
        avg_lat = filtered_data['Latitude'].mean()
        avg_lon = filtered_data['Longitude'].mean()
        map_center = [avg_lat, avg_lon]
    else:
        map_center = [4.0, -74.0]  # Default center if no filters selected

    m = folium.Map(location=map_center, zoom_start=4, tiles='CartoDB positron')
    marker_cluster = MarkerCluster().add_to(m)

    # Add markers based on filtered data
    for _, row in filtered_data.iterrows():
        if pd.notna(row['Latitude']) and pd.notna(row['Longitude']):
            coordinates = [row['Latitude'], row['Longitude']]
            description = row['Description'] if description_type == "Full" else row['Description (Homogenized)']

            # Create pop-up content
            popup_content = f"""
            <b>Initiative:</b> {row['Nombre']}<br>
            <b>Country:</b> {row['País']}<br>
            <b>Year:</b> {row['Año de Inicio']}<br>
            <b>Drivers:</b> {row['Impulsores']}<br>
            <b>Description:</b> {description}<br>
            <b><a href='{row['Links / Recursos']}' target='_blank'>Technical Sheet</a></b>
            """
            folium.Marker(
                location=coordinates,
                popup=folium.Popup(popup_content, max_width=300),
                icon=folium.Icon(color='blue', icon='info-sign')
            ).add_to(marker_cluster)

    # Save the map as an HTML file
    m.save(save_path)
    return m

# Streamlit app structure
st.title("Interactive Map of Citizen Participation Initiatives")
st.write("Select options to explore initiatives based on Year, Country, Drivers, and Description Type.")

# Sidebar toggle to switch between Full and Homogenized descriptions
description_type = st.sidebar.radio("Description Type", ["Full", "Homogenized"])

# Sidebar filters
years = sorted(mapeo_de_casos['Año de Inicio'].dropna().unique())
countries = sorted(mapeo_de_casos['País'].dropna().unique())
drivers = sorted(mapeo_de_casos['Impulsores'].dropna().unique())

year_filter = st.sidebar.multiselect("Filter by Year", years)
country_filter = st.sidebar.multiselect("Filter by Country", countries)
drivers_filter = st.sidebar.multiselect("Filter by Drivers", drivers)

# Create and display the filtered map
filtered_map = create_filtered_map(description_type, year_filter, country_filter, drivers_filter)
folium_static(filtered_map)

# Add a download button for the HTML map
if st.button("Download Map as HTML"):
    create_filtered_map(description_type, year_filter, country_filter, drivers_filter, save_path="filtered_map.html")
    with open("filtered_map.html", "rb") as file:
        btn = st.download_button(
            label="Download HTML file",
            data=file,
            file_name="filtered_map.html",
            mime="text/html"
        )

