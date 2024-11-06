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
st.title("Dashboard de Iniciativas Ciudadanas")

# 1. Initiatives Over Time with Year Filter
st.header("1. Iniciativas a lo Largo del Tiempo")
selected_years = st.multiselect("Seleccionar Años para Iniciativas a lo Largo del Tiempo", 
                                sorted(mapeo_de_casos['Año de Inicio'].unique()))

yearly_data = mapeo_de_casos[mapeo_de_casos['Año de Inicio'].isin(selected_years)] if selected_years else mapeo_de_casos
yearly_counts = yearly_data['Año de Inicio'].value_counts().reset_index()
yearly_counts.columns = ['Año', 'Conteo']
yearly_counts = yearly_counts.sort_values(by='Año')

fig1 = px.bar(yearly_counts, x='Año', y='Conteo', title="Número de Iniciativas a lo Largo del Tiempo",
              labels={'Año': 'Año', 'Conteo': 'Número de Iniciativas'},
              color='Conteo', color_continuous_scale='Viridis')
fig1.update_layout(xaxis_title="Año", yaxis_title="Conteo de Iniciativas")
st.plotly_chart(fig1)

# 2. Initiatives by Country with Country Filter
st.header("2. Iniciativas por País")
selected_countries = st.multiselect("Seleccionar Países para Iniciativas por País", 
                                    sorted(mapeo_de_casos['País'].unique()))

country_data = mapeo_de_casos[mapeo_de_casos['País'].isin(selected_countries)] if selected_countries else mapeo_de_casos
country_counts = country_data['País'].value_counts().reset_index()
country_counts.columns = ['País', 'Conteo']

fig2 = px.bar(country_counts, x='País', y='Conteo', title="Número de Iniciativas por País",
              labels={'País': 'País', 'Conteo': 'Número de Iniciativas'},
              color='Conteo', color_continuous_scale='Plasma')
fig2.update_layout(xaxis_title="País", yaxis_title="Conteo de Iniciativas")
st.plotly_chart(fig2)

# 3. Drivers of Initiatives with Driver Filter
st.header("3. Iniciativas por Impulsores Principales")
selected_drivers = st.multiselect("Seleccionar Impulsores para Iniciativas por Impulsores",
                                  sorted(mapeo_de_casos['Impulsores'].unique()))

driver_data = mapeo_de_casos[mapeo_de_casos['Impulsores'].isin(selected_drivers)] if selected_drivers else mapeo_de_casos
driver_counts = driver_data['Impulsores'].value_counts().reset_index()
driver_counts.columns = ['Impulsor', 'Conteo']

fig3 = px.bar(driver_counts, x='Impulsor', y='Conteo', title="Número de Iniciativas por Impulsores",
              labels={'Impulsor': 'Impulsor Principal', 'Conteo': 'Número de Iniciativas'},
              color='Conteo', color_continuous_scale='Cividis')
fig3.update_layout(xaxis_title="Impulsor Principal", yaxis_title="Conteo de Iniciativas")
st.plotly_chart(fig3)

# 4. Initiatives by Type with Type Filter (if applicable)
if 'Type' in mapeo_de_casos.columns:  # Check if there's a 'Type' column
    st.header("4. Iniciativas por Tipo")
    selected_types = st.multiselect("Seleccionar Tipos para Iniciativas por Tipo",
                                    sorted(mapeo_de_casos['Type'].unique()))

    type_data = mapeo_de_casos[mapeo_de_casos['Type'].isin(selected_types)] if selected_types else mapeo_de_casos
    type_counts = type_data['Type'].value_counts().reset_index()
    type_counts.columns = ['Tipo', 'Conteo']

    fig4 = px.bar(type_counts, x='Tipo', y='Conteo', title="Número de Iniciativas por Tipo",
                  labels={'Tipo': 'Tipo de Iniciativa', 'Conteo': 'Número de Iniciativas'},
                  color='Conteo', color_continuous_scale='Inferno')
    fig4.update_layout(xaxis_title="Tipo de Iniciativa", yaxis_title="Conteo de Iniciativas")
    st.plotly_chart(fig4)

# Show filtered data preview without "Description (Homogenized)", "Latitude", and "Longitude" columns
columns_to_display = mapeo_de_casos.drop(columns=["Description (Homogenized)", "Latitude", "Longitude"], errors='ignore')
st.dataframe(columns_to_display)
