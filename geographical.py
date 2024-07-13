import folium.features
import folium.map
import streamlit as st
import folium
from streamlit_folium import folium_static
import pandas as pd
import json
from urllib.request import urlopen
from datetime import timedelta

# Reading Json file where the coordinates of all the Countries are
url  = 'https://raw.githubusercontent.com/python-visualization/folium/master/examples/data/world-countries.json'
res = urlopen(url)
data_json = json.loads(res.read())

class Geo():
    def __init__(self,dataset):
        self.df = dataset
        self.data_json = data_json

    # Initialize analysis option and date range
        self.analysisoption()
        self.date_range()

    #  Method to select the basis of analysis (Total Cases or Total Deaths)
    def analysisoption(self):
        self.anaoption = st.selectbox('Select on which Basis you want Analysis',
            ['Total Cases','Total Deaths'])

        # Set the option based on user selection
        if self.anaoption == 'Total Cases':
            self.option = 'new_cases'
        else:
            self.option = 'new_deaths'
        
    # Method to add the date range
    def date_range(self):
        start_date = self.df['date'].min()
        end_date = self.df['date'].max()

        st_col,end_col = st.columns(2)
        # Input for Date
        start_date= st_col.date_input('Start Date',start_date,min_value=start_date,
                            max_value=end_date-timedelta(days=1))

        end_date = end_col.date_input('End Date',min_value=start_date+timedelta(days=1),
                            max_value=end_date)

        # Filtering Data on the basis of Dates Selected 
        filtered_df = self.df[(self.df['date']>start_date) & (self.df['date']<end_date)]

        self.actual_df = filtered_df.groupby(['iso_code','country'])[self.option].sum().reset_index()
        self.actual_df[self.option] = self.actual_df[self.option]/1000
        
    # Show the Map
    def showmap(self):

        map = folium.Map(zoom_start=1,title='CartoDB positron',max_bounds=True)
        # Add Choropleth layer to the map
        choropleth = folium.Choropleth(
            geo_data=self.data_json,
            name='chorpleth',
            data=self.actual_df,
            columns=['iso_code',self.option],
            key_on='feature.id',
            fill_color='OrRd',
            legend_name=f'{self.anaoption} (Thousands)',
            highlight=True,
            zoom_start=1,min_zoom=1
        ).add_to(map)

        # Showing the Country + Total Cases/Total Deaths upon Hovering
        for features in choropleth.geojson.data['features']:
            count_name = features['properties']['name']
            if self.actual_df[self.actual_df['country'] == count_name][self.option].empty:
                features['properties']['data'] = '0'
            else:
                features['properties']['data'] = '' + str(
                    self.actual_df[self.actual_df['country'] == count_name][self.option].values[0]
                )

        choropleth.geojson.add_child(
            folium.features.GeoJsonTooltip(['name','data'],labels=False)
        )

        choropleth.geojson.add_to(map)
        folium_static(map,width=750, height=500)
