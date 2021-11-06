from os import name

import numpy as np
import pandas as pd
import streamlit as st
from streamlit.elements.arrow import Data
from streamlit.type_util import data_frame_to_bytes

import physics_functions as pf

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
    label='car_mass', help=help_input)

#friction_u or friction coeffe (subject to change as experiments improve)
friction_u = st.sidebar.number_input(
    label='friction_u', help=help_input)

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
        data='experimental_data',
        file_name='large_df.csv',
        mime='text/csv',)


if uploaded_file is not None:
    introduction.empty()
    st.title("Calculations")

#---------------------------------------
# Calculations
    dataframe = pd.read_csv(uploaded_file)

    #Get Total Mass
    dataframe["Total Mass"] = dataframe["CO2 Mass (Mco2)"] + car_mass
    
    #Get Friction_u (subject to change cause friction coeffe changes)
    dataframe["Friction Coeffe (u)"] = friction_u

    #Get Friction Force (Ff)
    dataframe["Friction Force (Ff)"] = pf.friction_f(dataframe["Total Mass"], dataframe["Friction Coeffe (u)"])

    #Get Force net (Fnet)
    dataframe["Fnet"] = pf.force_net(dataframe["Force (N)"], dataframe["Friction Force (Ff)"], dataframe["Drag (FD)"])

#---------------------------------------
#dva Calculations
    #Create DataFrame
    dva_dataframe = dataframe[["Time (s)", "Total Mass", "Fnet"]]

    #Replace all negative with 0 (for covinence at this moment)
    dva_dataframe[dva_dataframe < 0] = 0

    #Calculate accerlation
    dva_dataframe['Acceleration (a)'] = (dva_dataframe['Fnet']/dva_dataframe['Total Mass'])*1000

    # Find where to start
    for index,row in dva_dataframe.iterrows():
        if row['Fnet'] > 0:
            # row_above = dva_dataframe.iloc[[index-1]]
            # row_above_diff = 0-row_above['Fnet']
            # row_diff = 0-row['Fnet']
            # if abs(row_above_diff) < abs(row_diff):
            #     dva_dataframe = dva_dataframe.iloc[index-1:]
            #     break
            dva_dataframe = dva_dataframe.iloc[index:]
            break
    dva_dataframe = dva_dataframe.reset_index(drop=True)

    #Find Continuous
    sec = []
    for index, row in dva_dataframe.iterrows():
        first_row = dva_dataframe.iloc[[0]]
        sec.append(row['Time (s)'] - first_row['Time (s)'])
    df = pd.concat(sec).reset_index(drop=True)
    dva_dataframe = pd.concat([dva_dataframe, df], axis=1)
    # dva_dataframe = dva_dataframe.iloc[: , 1:]
    dva_dataframe = dva_dataframe.set_axis([*dva_dataframe.columns[:-1], 'Continuous Time'], axis=1, inplace=False)

    #Calculate speed change
    ser = pd.Series({0:0}, name='Speed Change (delta v)')
    delta_v = []
    for index, row in dva_dataframe.iterrows():
        row_above = dva_dataframe.iloc[[index-1]]
        if index == 0:
            row_above['Acceleration (a)'] = 0
        delta_v.append((row['Time (s)'] - row_above['Time (s)'])*(row_above['Acceleration (a)']+row['Acceleration (a)'])/2)
    delta_v[0] = ser
    df = pd.concat(delta_v).reset_index(drop=True)
    dva_dataframe = pd.concat([dva_dataframe, df], axis=1)
    dva_dataframe = dva_dataframe.set_axis([*dva_dataframe.columns[:-1], 'Speed Change (delta v)'], axis=1, inplace=False)
    # dva_dataframe = dva_dataframe[:-1]

    #Caluculate speed
    ser = pd.Series({0:0}, name='Speed (v)')
    v = [ser]
    for index, row in dva_dataframe.iterrows():
        row_above = dva_dataframe.iloc[[index-1]]
        v.append(v[-1]+row['Speed Change (delta v)'])
    del v[0]
    df = pd.concat(v).reset_index(drop=True)
    dva_dataframe = pd.concat([dva_dataframe, df], axis=1)
    dva_dataframe = dva_dataframe.set_axis([*dva_dataframe.columns[:-1], 'Speed (v)'], axis=1, inplace=False)


    #Calculate distance change
    ser = pd.Series({0:0}, name='Distance Change (delta d)')
    delta_d = []
    for index, row in dva_dataframe.iterrows():
        row_above = dva_dataframe.iloc[[index-1]]
        delta_d.append((row['Time (s)'] - row_above['Time (s)'])*(row_above['Speed (v)']+row['Speed (v)'])/2)
    delta_d[0] = ser
    df = pd.concat(delta_d).reset_index(drop=True)
    dva_dataframe = pd.concat([dva_dataframe, df], axis=1)
    dva_dataframe = dva_dataframe.set_axis([*dva_dataframe.columns[:-1], 'Distance Change (delta d)'], axis=1, inplace=False)


    #Caluculate distance
    ser = pd.Series({0:0}, name='Distance (d)')
    d = [ser]
    for index, row in dva_dataframe.iterrows():
        row_above = dva_dataframe.iloc[[index-1]]
        d.append(d[-1]+row['Distance Change (delta d)'])
    del d[0]
    df = pd.concat(d).reset_index(drop=True)
    dva_dataframe = pd.concat([dva_dataframe, df], axis=1)
    dva_dataframe = dva_dataframe.set_axis([*dva_dataframe.columns[:-1], 'Distance (d)'], axis=1, inplace=False)


    #DVA Columns Only 
    dva_dataframe = dva_dataframe[['Continuous Time', 'Acceleration (a)', 'Speed (v)', 'Distance (d)']]
    #Calculating End Time
    dva_dataframe = dva_dataframe[dva_dataframe['Distance (d)'] <= 20]  


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

###############################################################################

