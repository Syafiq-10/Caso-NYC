import pandas as pd
import streamlit as st
import plotly.express as px

st.title("NYC CitiBikes")


@st.cache
def load_data(nrows):
    data = pd.read_csv('citibike-tripdata.csv', nrows=nrows)
    data['started_at'] = pd.to_datetime(data['started_at'])
    return data


data = load_data(500)


sidebar = st.sidebar
sidebar.title("Sofía Almeraya")
sidebar.subheader('A01283713')

if sidebar.checkbox("Mostrar todos los datos",value=True):
    st.dataframe(data)


viajes = data['started_at'].dt.hour.reset_index(name='started_at')
viajes=viajes.groupby(['started_at']).size().reset_index(name='cantidad')


if sidebar.checkbox('Recorridos por Hora'):
    fig8 = px.bar(viajes, x='started_at', y='cantidad',
             hover_data=['started_at','cantidad'], color='cantidad',
             color_continuous_scale="Brwnyl",
             height=400)
             
    st.plotly_chart(fig8, use_container_width=True)

lat = data.rename(columns={'start_lat':'lat','start_lng':'lon'})

hour_to_filter = st.sidebar.slider('Hora', 0, 23, 12)
filtered_data = lat[lat['started_at'].dt.hour == hour_to_filter]

st.subheader('Los viajes a las %s:00' % hour_to_filter)
st.map(lat)