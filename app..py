import streamlit as st
import pandas as pd
import json
from urllib.request import urlopen
from datetime import timedelta
from geographical import Geo


st.header('COVID19 Dashboard')

# Reading Json file where the coordinates of all the Countries are
def openjsonfile():
    url  = 'https://raw.githubusercontent.com/python-visualization/folium/master/examples/data/world-countries.json'
    res = urlopen(url)
    data_json = json.loads(res.read())
    return data_json

coviddata = pd.read_csv('cleaned.csv')

# Removing Unnecessary Columns
remove_cols = [i for i in coviddata.columns if 'Unnamed' in i]
coviddata.drop(columns=remove_cols,inplace=True)

coviddata['date'] = pd.to_datetime(coviddata['date']).dt.date

# Side bar Options 
st.sidebar.title('Select any')
overalloption = st.sidebar.selectbox('Select Any',
            ['Geographical','Comparison','General'])

# Analysi on which Basis
analysisoption = st.selectbox('Select on on Basis you want Analysis',
            ['Total Cases','Total Deaths'])


# Below is the code to select the Date Range for 
# which range you want analysis
start_date = coviddata['date'].min()
end_date = coviddata['date'].max()

st_col,end_col = st.columns(2)

start_date= st_col.date_input('Enter the Start Date',min_value=start_date,
                    max_value=end_date-timedelta(days=1))

end_date = end_col.date_input('Enter the Start Date',min_value=start_date+timedelta(days=1),
                    max_value=end_date)


# Filtering Data on the basis of Dates Selected 
filtered_df = coviddata[(coviddata['date']>start_date) & (coviddata['date']<end_date)]

# Showing the Dashboard based on User Input
if overalloption == 'Geographical':
    if analysisoption == 'Total Cases':
        option = 'total_cases'
    else:
        option = 'total_deaths'
    actual_df = filtered_df.groupby(['iso_code','country'])[option].sum().reset_index()
    actual_df[option] = actual_df[option]/100000
    app = Geo(actual_df,openjsonfile(),analysisoption,option)
    app.showmap()
    print(actual_df.info())
    
