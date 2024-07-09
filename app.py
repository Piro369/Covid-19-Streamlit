import streamlit as st
import pandas as pd
from geographical import Geo


st.header('COVID19 Dashboard')

def read_data():
    coviddata = pd.read_csv('cleaned.csv')

    # Removing Unnecessary Columns
    remove_cols = [i for i in coviddata.columns if 'Unnamed' in i]
    coviddata.drop(columns=remove_cols,inplace=True)

    # Changing Datatype
    coviddata['date'] = pd.to_datetime(coviddata['date']).dt.date

    return coviddata

# Side bar Options 
st.sidebar.title('Select any')
overalloption = st.sidebar.selectbox('Select Any',
            ['Geographical','General'])

# Showing the Dashboard based on User Input
if overalloption == 'Geographical':
    app = Geo(read_data())
    app.showmap()

else:
    st.subheader('General Analysis')

    
