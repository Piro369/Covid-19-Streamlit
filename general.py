import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from calendar import month_name as mn
import plotly.express as px


class General():
    def __init__(self,dataset):
        self.data = dataset
        self.data.drop(columns=['new_deaths_smoothed','hosp_patients','weekly_icu_admissions',
                        'weekly_hosp_admissions','new_cases_smoothed'],inplace=True)

    def showmetrics(self):

        countries = self.data['country'].unique().tolist()
        country_selected = st.selectbox('Select a Country',options=countries)

        st.write(country_selected)
        self.df = self.data[self.data['country']==country_selected]
        col1 ,col2 = st.columns(2)
        col1.metric('Total Deaths',self.df['new_deaths'].sum())
        col2.metric('Total Cases',self.df['new_cases'].sum())

    def show_line(self):
        months = mn[1:]

        self.df['date'] = pd.to_datetime(self.df['date'])
        self.df['Month'] = self.df['date'].dt.month_name()
        self.df['Year'] = self.df['date'].dt.year

        option = st.selectbox('Select any ',['Cases','Deaths'])

        if option =='Cases':
            selected = 'new_cases'
        else:
            selected = 'new_deaths'
        st.write(selected)
        df_grpby = self.df.groupby(['Year','Month'])[selected].sum().reset_index()

        df_grpby['Month'] = pd.Categorical(df_grpby['Month'],categories=months,ordered=True)

        fig = px.line(data_frame=df_grpby,x='Month',y=selected,color='Year')

        st.plotly_chart(fig)


