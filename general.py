import streamlit as st
import pandas as pd
from calendar import month_name as mn
import plotly.express as px

st.set_page_config(layout='wide',page_title='Covid19')
class General():
    def __init__(self,dataset):
        self.data = dataset

    # Show Total Cases & Deaths
    def showmetrics(self):

        countries = self.data['country'].unique().tolist()
        country_selected = st.selectbox('Select a Country',options=countries)

        self.df = self.data[self.data['country']==country_selected]
        col1 ,col2 = st.columns(2)
        col1.metric('Total Deaths',self.df['new_deaths'].sum())
        col2.metric('Total Cases',self.df['new_cases'].sum())

    # Plot Plotly Line Chart
    def show_line(self):

        # List of all the Months
        months = mn[1:]

        # Changing data type and Adding new Columns
        self.df['date'] = pd.to_datetime(self.df['date'])
        self.df['Month'] = self.df['date'].dt.month_name()
        self.df['Year'] = self.df['date'].dt.year

        option = st.selectbox('Select any ',['Cases','Deaths'])

        if option =='Cases':
            selected = 'new_cases'
        else:
            selected = 'new_deaths'
        df_grpby = self.df.groupby(['Year','Month'])[selected].sum().reset_index()

        # Making sure that Month is in Order
        df_grpby['Month'] = pd.Categorical(df_grpby['Month'],categories=months,ordered=True)
        df_grpby = df_grpby.sort_values(['Year','Month']).reset_index(drop=True)

        # Plotly Chart
        fig = px.line(data_frame=df_grpby,x='Month',y=selected,color='Year',
                      labels={selected:f'No of {option}'},markers=True)

        st.plotly_chart(fig)


