import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


data = pd.read_csv('cleaned.csv')
remove_cols = [i for i in data.columns if 'Unnamed' in i]
data.drop(columns=remove_cols,inplace=True)
data.drop(columns=['new_deaths_smoothed','hosp_patients','weekly_icu_admissions',
                'weekly_hosp_admissions','new_cases_smoothed'],inplace=True)
print(data.head())

countries = data['country'].unique().tolist()
country_selected = st.selectbox('Select a Country',options=countries)

st.write(country_selected)
country_grpby = data[data['country']==country_selected].groupby(['country'])

