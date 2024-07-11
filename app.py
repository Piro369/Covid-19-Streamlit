import streamlit as st
import pandas as pd
from geographical import Geo
from general import General

# Load the data and cache it to improve performance
@st.cache_data
def read_data():
    coviddata = pd.read_csv('cleaned.csv',index_col=0)
    coviddata['date'] = pd.to_datetime(coviddata['date']).dt.date
    coviddata['country'].replace('United States','United States of America',inplace=True)
    return coviddata

df = read_data()

# Sidebar for navigation
st.header('COVID19 Dashboard')
overalloption = st.sidebar.selectbox('Select a Page',['Geographical','General'])


# Conditional rendering based on the selected page
if overalloption == 'Geographical':
    app = Geo(df)
    app.showmap()
else:
    app = General(df)
    app.showmetrics()
    app.show_line()

    
