import numpy as np
import pandas as pd
import streamlit as st
from streamlit.elements.arrow import Data
from streamlit.type_util import data_frame_to_bytes

import app_functions as appf
import calculation_functions as cf

###############################################################################
# Initial Page Config
st.set_page_config(
     page_title='Race Time Calculator',
     layout="wide",
     initial_sidebar_state="expanded",
)

###############################################################################
# Sidebar

#Header
st.sidebar.header('Race Time Calculator')

#---------------------------------------
#File upload

help_input_csv = """Please upload a CSV File that has your time and distance measurem
ents"""

#Upload CSV File
uploaded_file = st.sidebar.file_uploader(
    label='Upload Race Time Data', help=help_input_csv)

#---------------------------------------
#Given inputs

help_input = """just input stuff dude"""

#car_mass
car_mass = st.sidebar.number_input(
    label='Car Mass', help=help_input)

#friction_u or friction coeffe (subject to change as experiments improve)
friction_u = st.sidebar.number_input(
    label='friction_u', help=help_input)

start = False
if car_mass and friction_u != 0:
    start = True

#drag_force (subject to change as experiment improve)
# drag_force = st.sidebar.number_input(
#     label='drag_force', help=help_input)

###############################################################################
# Main body

#---------------------------------------
#Introduction

introduction = st.empty()
with introduction.container():
    st.title("Roosevelt Racer's Race Time Calculator")
    st.header("Welcome")
    st.write("""
        This is the Roosevelts Racer's Race Time Calculator created by the
        team's R&D team. The goal of the R&D team is to improve and
        accelerate the proccess of creating our dragster. The purpose of the
        race time calculator is the evaluate if a dragster model is worthy 
        enough to be manufactured.""")

    st.header("How To Use")
    st.write("""
        To use this calculator you must have a csv to input. The csv should
        have stuff in it. An example input csv can be downloaded below.
    """)

    st.download_button(
        label="Example CSV",
        data= appf.example_csv(),
        file_name='RR_example.csv',
        mime='text/csv',)


if uploaded_file is not None and start == True:
    introduction.empty()
    st.title("Calculations")

#---------------------------------------
# Calculations
    dataframe = pd.read_csv(uploaded_file)

    #Talkes in all the data and outputs only Time, Total Mass, and Fnet
    dva_dataframe = cf.dataframe_to_dva(dataframe, car_mass, friction_u)

    #Calculate accerlation (here cause it can be done in one line)
    dva_dataframe['Acceleration (a)'] = (dva_dataframe['Fnet']/dva_dataframe['Total Mass'])*1000

    #Find Continuous
    dva_dataframe = cf.find_continuous_time(dva_dataframe)

    #Calculate speed change
    dva_dataframe = cf.cal_speed_change(dva_dataframe)

    #Caluculate speed
    dva_dataframe = cf.cal_speed(dva_dataframe)

    #Calculate distance change
    dva_dataframe = cf.cal_distance_change(dva_dataframe)

    #Caluculate distance
    dva_dataframe = cf.cal_distance(dva_dataframe)

    #DVA Columns Only 
    dva_dataframe = dva_dataframe[['Continuous Time', 'Acceleration (a)', 'Speed (v)', 'Distance (d)']]
    #Calculating End Time
    dva_dataframe = dva_dataframe[dva_dataframe['Distance (d)'] <= 20]  

#---------------------------------------
#Graphs

    #Acceleration Graph
    acc_dataframe = dva_dataframe[['Continuous Time', 'Acceleration (a)']]
    st.header('Acceleration Over Time')
    acc_col1, acc_col2 = st.columns([3, 1])
    acc_col1.subheader('Acceleration Over Time Chart')
    acc_col1.line_chart(acc_dataframe.rename(columns={'Continuous Time':'index'}).set_index('index'))
    acc_col2.subheader('DVA DataFrame')
    acc_col2.write(acc_dataframe)

    #Acceleration Expander
    acc_expander = st.expander('What did we do?')
    acc_expander.write("We did these calculation:")
    acc_expander.image("https://static.streamlit.io/examples/dice.jpg")
    acc_expander.latex(r'''
    ...     a + ar + a r^2 + a r^3 + \cdots + a r^{n-1} =
    ...     \sum_{k=0}^{n-1} ar^k =
    ...     a \left(\frac{1-r^{n}}{1-r}\right)
    ...     ''')

    #Velocity Graph
    v_dataframe = dva_dataframe[['Continuous Time', 'Speed (v)']]
    st.header('Velocity Over Time')
    v_col1, v_col2 = st.columns([3, 1])
    v_col1.subheader('Velocity Over Time Chart')
    v_col1.line_chart(v_dataframe.rename(columns={'Continuous Time':'index'}).set_index('index'))
    v_col2.subheader('DVA DataFrame')
    v_col2.write(v_dataframe)

    #Velocity Expander
    v_expander = st.expander('What did we do?')
    v_expander.write("We did these calculation:")
    v_expander.image("https://static.streamlit.io/examples/dice.jpg")
    v_expander.latex(r'''
    ...     a + ar + a r^2 + a r^3 + \cdots + a r^{n-1} =
    ...     \sum_{k=0}^{n-1} ar^k =
    ...     a \left(\frac{1-r^{n}}{1-r}\right)
    ...     ''')
    
    #Distance Graph
    d_dataframe = dva_dataframe[['Continuous Time', 'Distance (d)']]
    st.header('Distance Over Time')
    d_col1, d_col2 = st.columns([3, 1])
    d_col1.subheader('Distance Over Time Chart')
    d_col1.line_chart(d_dataframe.rename(columns={'Continuous Time':'index'}).set_index('index'))
    d_col2.subheader('DVA DataFrame')
    d_col2.write(d_dataframe)

    d_expander = st.expander('What did we do?')
    d_expander.write("We did these calculation:")
    d_expander.image("https://static.streamlit.io/examples/dice.jpg")
    d_expander.latex(r'''
    ...     a + ar + a r^2 + a r^3 + \cdots + a r^{n-1} =
    ...     \sum_{k=0}^{n-1} ar^k =
    ...     a \left(\frac{1-r^{n}}{1-r}\right)
    ...     ''')
    


    dva_dataframe

    dva_csv = dva_dataframe.to_csv().encode('utf-8')
    st.download_button(
        label="Download DVA data as CSV",
        data=dva_csv,
        file_name='dva_data.csv',
        mime='text/csv',)




    #Thrust Graph This is wrong reason down below however thrust doesnt need to be graphed cause
    #its always canstant anyways... this can go in our introduciton
    # thrust_dataframe = dva_dataframe[['Continuous Time', 'Fnet']]#Fnet is wrong its supposed to be Fn
    # st.header('Thrust Over Time')
    # thrust_col1, thrust_col2 = st.columns([3, 1])
    # thrust_col1.subheader('Thrust Over Time Chart')
    # thrust_col1.line_chart(thrusttdataframe.rename(columns={'Continuous Time':'index'}).set_index('index'))
    # thrust_col2.subheader('DVA DataFrame')
    # thrust_col2.write(acc_dataframe)

#---------------------------------------
# Metric

    top_speed = (dva_dataframe['Speed (v)'].max())*(18/5)
    end_time = dva_dataframe['Continuous Time'].values[-1]

    #I made these values up but obv they would be real in the future
    metric_col1, metric_col2, metric_col3 = st.columns(3)
    metric_col1.metric("Top Speed (km/hr)", round(top_speed, 4), "5 km/hr")
    metric_col2.metric("End time", round(end_time, 4), "-8%")
    metric_col3.metric("Efficiency", "86%", "4%")

else:
    st.sidebar.error('Please input all your information including Car Mass and Friction')

##############################################################################
