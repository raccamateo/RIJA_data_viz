# Import necessary libraries
import pandas as pd
import plotly.express as px
import streamlit as st

# Load data including coordinates (replace 'file_path' with the actual path to your Excel file)
file_path = 'Mapeo_de_Casos_With_Coordinates.xlsx'
mapeo_de_casos = pd.read_excel(file_path)

# Truncate data to start from 1996
mapeo_de_casos = mapeo_de_casos[mapeo_de_casos['Año de Inicio'] >= 1996]

# Streamlit dashboard layout
st.title("Dashboard de Iniciativas Ciudadanas - Treemap")

# Sidebar Filters
st.sidebar.header("Filtros")
selected_years = st.sidebar.multiselect("Seleccionar Años", sorted(mapeo_de_casos['Año de Inicio'].dropna().unique()))
selected_countries = st.sidebar.multiselect("Seleccionar Países", sorted(mapeo_de_casos['País'].dropna().unique()))
selected_types = st.sidebar.multiselect("Seleccionar Tipos de Iniciativa", sorted(mapeo_de_casos['Type'].dropna().unique()) if 'Type' in mapeo_de_casos.columns else [])
selected_drivers = st.sidebar.multiselect("Seleccionar Impulsores", sorted(mapeo_de_casos['Impulsores'].dropna().unique()))

# Apply the filters to the data
filtered_data = mapeo_de_casos.copy()
if selected_years:
    filtered_data = filtered_data[filtered_data['Año de Inicio'].isin(selected_years)]
if selected_countries:
    filtered_data = filtered_data[filtered_data['País'].isin(selected_countries)]
if selected_types:
    filtered_data = filtered_data[filtered_data['Type'].isin(selected_types)]
if selected_drivers:
    filtered_data = filtered_data[filtered_data['Impulsores'].isin(selected_drivers)]

# Drop rows with NaN values in required columns for the treemap
required_columns = ['Año de Inicio', 'País']
if 'Type' in filtered_data.columns:
    required_columns.append('Type')
filtered_data.dropna(subset=required_columns, inplace=True)

# Treemap Visualization
st.header("Distribución de Iniciativas - Treemap")

try:
    # Create treemap with hierarchical levels: Year > Country > Type (if available)
    if 'Type' in filtered_data.columns:
        fig = px.treemap(
            filtered_data,
            path=['Año de Inicio', 'País', 'Type'],  # Define the hierarchy
            values='Nombre',  # Using 'Nombre' as a placeholder for counting
            title="Distribución de Iniciativas por Año, País y Tipo",
            color='Año de Inicio',  # Color by Year for better contrast
            color_continuous_scale='Viridis',
            hover_data={
                'Año de Inicio': True,  # Show year
                'País': True,  # Show country
                'Type': True,  # Show initiative type (if applicable)
                'Nombre': 'count'  # Show count of initiatives
            }
        )
    else:
        fig = px.treemap(
            filtered_data,
            path=['Año de Inicio', 'País'],  # Define hierarchy without Type if unavailable
            values='Nombre',
            title="Distribución de Iniciativas por Año y País",
            color='Año de Inicio',
            color_continuous_scale='Viridis',
            hover_data={
                'Año de Inicio': True,
                'País': True,
                'Nombre': 'count'
            }
        )

    # Display the treemap with dynamic labels
    st.plotly_chart(fig)

except ValueError as e:
    st.error(f"Error al generar el treemap: {e}")

# Show a filtered data preview without specific columns
columns_to_display = filtered_data.drop(columns=["Description (Homogenized)", "Latitude", "Longitude"], errors='ignore')
st.dataframe(columns_to_display)
