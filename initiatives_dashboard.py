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
st.title("Dashboard de Datos de Iniciativas")

# Sidebar Filters in Spanish
st.sidebar.header("Filtros")
selected_countries = st.sidebar.multiselect("Seleccionar Países", sorted(mapeo_de_casos['País'].dropna().unique()))
selected_drivers = st.sidebar.multiselect("Seleccionar Impulsores", sorted(mapeo_de_casos['Impulsores'].dropna().unique()))
selected_years = st.sidebar.multiselect("Seleccionar Años", sorted(mapeo_de_casos['Año de Inicio'].dropna().unique()))

# Apply filters to the data
filtered_data = mapeo_de_casos.copy()
if selected_countries:
    filtered_data = filtered_data[filtered_data['País'].isin(selected_countries)]
if selected_drivers:
    filtered_data = filtered_data[filtered_data['Impulsores'].isin(selected_drivers)]
if selected_years:
    filtered_data = filtered_data[filtered_data['Año de Inicio'].isin(selected_years)]

# 1. Initiatives Over Time
st.header("1. Iniciativas a lo Largo del Tiempo")
yearly_counts = filtered_data['Año de Inicio'].value_counts().reset_index()
yearly_counts.columns = ['Año', 'Conteo']
yearly_counts = yearly_counts.sort_values(by='Año')

fig1 = px.bar(yearly_counts, x='Año', y='Conteo', title="Número de Iniciativas a lo Largo del Tiempo",
              labels={'Año': 'Año', 'Conteo': 'Número de Iniciativas'},
              color='Conteo', color_continuous_scale='Viridis')
fig1.update_layout(xaxis_title="Año", yaxis_title="Conteo de Iniciativas")
st.plotly_chart(fig1)

# 2. Initiatives by Country
st.header("2. Iniciativas por País")
country_counts = filtered_data['País'].value_counts().reset_index()
country_counts.columns = ['País', 'Conteo']

fig2 = px.bar(country_counts, x='País', y='Conteo', title="Número de Iniciativas por País",
              labels={'País': 'País', 'Conteo': 'Número de Iniciativas'},
              color='Conteo', color_continuous_scale='Plasma')
fig2.update_layout(xaxis_title="País", yaxis_title="Conteo de Iniciativas")
st.plotly_chart(fig2)

# 3. Drivers of Initiatives
st.header("3. Iniciativas por Impulsores Principales")
driver_counts = filtered_data['Impulsores'].value_counts().reset_index()
driver_counts.columns = ['Impulsor', 'Conteo']

fig3 = px.bar(driver_counts, x='Impulsor', y='Conteo', title="Número de Iniciativas por Impulsores",
              labels={'Impulsor': 'Impulsor Principal', 'Conteo': 'Número de Iniciativas'},
              color='Conteo', color_continuous_scale='Cividis')
fig3.update_layout(xaxis_title="Impulsor Principal", yaxis_title="Conteo de Iniciativas")
st.plotly_chart(fig3)

# 4. Initiatives by Type (if applicable)
if 'Type' in filtered_data.columns:  # Check if there's a 'Type' column
    st.header("4. Iniciativas por Tipo")
    type_counts = filtered_data['Type'].value_counts().reset_index()
    type_counts.columns = ['Tipo', 'Conteo']

    fig4 = px.bar(type_counts, x='Tipo', y='Conteo', title="Número de Iniciativas por Tipo",
                  labels={'Tipo': 'Tipo de Iniciativa', 'Conteo': 'Número de Iniciativas'},
                  color='Conteo', color_continuous_scale='Inferno')
    fig4.update_layout(xaxis_title="Tipo de Iniciativa", yaxis_title="Conteo de Iniciativas")
    st.plotly_chart(fig4)

# Show preview of data if needed
st.dataframe(filtered_data)
