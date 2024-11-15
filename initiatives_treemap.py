import pandas as pd
import plotly.express as px
import streamlit as st

# Load data
file_path = 'Mapeo_de_Casos_With_Coordinates.xlsx'
mapeo_de_casos = pd.read_excel(file_path)

# Add count column
mapeo_de_casos['Conteo'] = 1

# Streamlit layout
st.title("Dashboard de Iniciativas Ciudadanas - Treemap")

# Sidebar filters
st.sidebar.header("Filtros")
selected_countries = st.sidebar.multiselect(
    "Seleccionar Países", sorted(mapeo_de_casos['País'].dropna().unique())
)
selected_types = st.sidebar.multiselect(
    "Seleccionar Tipos de Iniciativa", sorted(mapeo_de_casos['Type'].dropna().unique())
)
selected_drivers = st.sidebar.multiselect(
    "Seleccionar Impulsores", sorted(mapeo_de_casos['Impulsores'].dropna().unique())
)

# Apply filters independently
filtered_data = mapeo_de_casos.copy()
if selected_countries:
    filtered_data = filtered_data[filtered_data['País'].isin(selected_countries)]
if selected_types:
    filtered_data = filtered_data[filtered_data['Type'].isin(selected_types)]
if selected_drivers:
    filtered_data = filtered_data[filtered_data['Impulsores'].isin(selected_drivers)]

# Check if filtered data is empty
if filtered_data.empty:
    st.warning("No se encontraron datos con los filtros seleccionados.")
else:
    # Treemap
    fig = px.treemap(
        filtered_data,
        path=['País', 'Type'],  # Hierarchy: Country > Type
        values='Conteo',
        title="Distribución de Iniciativas por País y Tipo",
        color='País',  # Use País for coloring
        color_continuous_scale='Viridis',  # Apply Viridis palette
        hover_data={
            'País': True,  # Show Country
            'Type': True,  # Show Initiative Type
            'Conteo': True  # Show Count
        }
    )

    # Customize hover details for clarity
    fig.update_traces(
        hovertemplate='<b>País:</b> %{customdata[0]}<br>' +
                      '<b>Tipo de Iniciativa:</b> %{customdata[1]}<br>' +
                      '<b>Número de Iniciativas:</b> %{value}<br>'
    )

    # Display treemap
    st.plotly_chart(fig)
