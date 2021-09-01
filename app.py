from numpy.core.shape_base import block
import streamlit as st
from streamlit_folium import folium_static
import plotly.express as px
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import folium
import os

files = os.listdir('data')

@st.cache
def load_data(name):
    df = pd.read_csv('data/'+name, parse_dates=['Date'])
    df.replace('Bihar****','Bihar',inplace=True)
    return df

def plot_ts(df, title, x_title, y_title, width, height):
    fig = px.line(df, title=title, width=width, height=height)
    fig.update_layout(
        xaxis_title=x_title,
        yaxis_title=y_title,
    )
    return fig

df = load_data(files[0])

# menu
options = [
            'Introduction',
            'Geo Visualization',
            'Graphical Representation',
            'Vaccine Data',
            'Testing Data'
        ]

menu = st.sidebar.radio("Select a variable", options)
states_df = df.groupby("State/UnionTerritory")[['Deaths','Cured','Confirmed']].sum().reset_index()


if menu == options[0]:
    st.title("Data Analysis of Covid 19 in India")
    st.image("images/corona.jfif",width=500)
    st.markdown('COVID-19 is an infectious disease caused by a newly discovered coronavirus. Most people infected with the COVID-19 virus will experience mild to moderate respiratory illness and recover without requiring special treatment.')

if menu == options[1]:
    st.title("Geo Visualization")
    
    fiop = st.sidebar.slider("fill color opacity", 0.0, 1.0, value=0.7) 
    if st.checkbox("View Data"):
        st.write(states_df)

    map = folium.Map(location=[25,80], zoom_start=4)
    map.choropleth(
        geo_data='data/Indian_States.json',
        name='choropleth',
        data=states_df,
        columns=['State/UnionTerritory', 'Deaths','Cured','Confirmed'],
        key_on='feature.properties.NAME_1',
        fill_color='YlOrRd',
        fill_opacity=fiop,
        line_opacity=0.2,
        legend_name='Deaths,Cured,Confirmed'
    )
    folium_static(map)


if menu == options[2]:
    options1 = ['Bar Plot','Violin plot','joint plot','Scatter Plot']
    menu1 = st.sidebar.selectbox("Select a Plot",options1)
    state = st.selectbox("Select any State or Union Territory ",states_df)
    statewise = df[df['State/UnionTerritory'] == state]
    
    if menu1 == options1[0]:
        st.title("Bar Plot")
        fig = px.bar(statewise, x='Date', y='Confirmed', hover_data=['Cured','Deaths'], height=800, width=800)
        st.write("This plot shows  Cured and Deaths of Confirmed Patients by Date.")
        st.plotly_chart(fig)

    if menu1 == options1[1]:
        st.title("Violin plot")
        fig = px.violin(statewise, x="Date", y="Confirmed")
        st.write("This plot shows State-wise Confirmed Patients by Dates.")
        st.plotly_chart(fig,use_container_width=True)

    if menu1 == options1[2]:
        st.title("joint plot")
        fig = sns.jointplot(data = statewise, x='Cured', y='Deaths')
        st.write("This plot shows Cured Patients by Deaths.")
        st.pyplot(fig)
        
    if menu1 == options1[3]:
        st.title("scatter")
        fig = px.scatter(statewise, x="Cured", y="Deaths", height=600, width=800)
        st.write("This plot shows Cured Patients by Deaths.")
        st.plotly_chart(fig)
    

if menu == options[3]:
    df_vaccine = pd.read_csv('data/'+files[1])
    st.title("Male and Female Vaccinated ratio for Covid19")
    male = df_vaccine["Male(Individuals Vaccinated)"].max() 
    female = df_vaccine["Female(Individuals Vaccinated)"].max()  
    trans = df_vaccine["Transgender(Individuals Vaccinated)"].max()
    st.plotly_chart(px.pie(names=["Male Vaccinated","Female Vaccinated","Trans Gender"],values=[male,female,trans]))

    st.title("People who are vaccinated with Covaxin or Covishield Vaccines")
    Covaxin = df_vaccine["Total Covaxin Administered"].max()
    Covishield = df_vaccine["Total CoviShield Administered"].max()
    st.plotly_chart(px.pie(names=["Covaxin Vaccinated","Covishield Vaccinated"],values=[Covaxin,Covishield]))

    st.title("Doses Administered vs People Vaccinated")
    Doses = df_vaccine["Total Doses Administered"].max() 
    Vaccinated = df_vaccine["Total Individuals Vaccinated"].max()  
    st.plotly_chart(px.pie(names=["Doses Administered","People Vaccinated"],values=[Doses,Vaccinated]))

if menu == options[4]:
    ICMRTestingDF = pd.read_csv('data/'+files[3])
    ICMRTestingDF['Date'] = pd.to_datetime(ICMRTestingDF['Date'],format='%Y-%m-%d')
    ICMRTestingDF = ICMRTestingDF[ICMRTestingDF['Date']<pd.to_datetime('today')]
    ICMRTestingDF.sort_values('Date',inplace=True)
    ICMRTestingDF = ICMRTestingDF.groupby('Date').sum().reset_index()
    ICMRTestingDF['Cases/Total Tested Ratio'] = ICMRTestingDF['Positive']*100/ICMRTestingDF['TotalSamples']

    fig = px.line(ICMRTestingDF,
                  x = 'Date',
                  y = 'Cases/Total Tested Ratio',
                  template = 'plotly_dark',
                  title = 'Positive cases/Total Tested Ratio')
    st.plotly_chart(fig)