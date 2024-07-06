import folium.features
import folium.map
import streamlit as st
import folium
from streamlit_folium import folium_static
import pandas as pd

class Geo():
    def __init__(self,dataset,data_json,anaoption,option):
        self.df = dataset
        self.data_json = data_json
        self.anaoption = anaoption
        self.option = option


    def showmap(self):
        self.df[self.option] = pd.to_numeric(self.df[self.option], errors='coerce').fillna(0)

        map = folium.Map(zoom_start=1,title='CartoDB positron',max_bounds=True)
        # Add Choropleth layer to the map
        choropleth = folium.Choropleth(
            geo_data=self.data_json,
            name='chorpleth',
            data=self.df,
            columns=['iso_code',self.option],
            key_on='feature.id',
            fill_color='OrRd',
            legend_name=f'{self.anaoption} (Lakhs)',
            highlight=True,
            zoom_start=1,min_zoom=1
        ).add_to(map)

        # Showing the Country + Total Cases/Total Deaths upon Hovering
        for features in choropleth.geojson.data['features']:
            count_name = features['properties']['name']
            if self.df[self.df['country'] == count_name][self.option].empty:
                features['properties']['data'] = '0'
            else:
                features['properties']['data'] = '' + str(
                    self.df[self.df['country'] == count_name][self.option].values[0]
                )

        choropleth.geojson.add_child(
            folium.features.GeoJsonTooltip(['name','data'],labels=False)
        )

        choropleth.geojson.add_to(map)
        folium_static(map,width=700,height=450)
