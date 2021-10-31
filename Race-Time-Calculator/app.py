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
drag_force = st.sidebar.number_input(
    label='drag_force', help=help_input)

###############################################################################
# Main body

#---------------------------------------
#Introduction

introduction = st.empty()
introduction.title("Roosevelt Racer's Race Time Calculator")
introduction.header('Welcome')
introduction.write("""
Please input your parameters, using the side bar, for calculating the car's race 
time. The csv file should have 2 columns one for time in sec and the other for di
stance in m. Do it you monkey. Also I need to figure out what to write here. S
hould be do like a run down or what we will calculate? or like how to use the app
or like idk. We will do the explaination inside the calculator no? i think we can just
make the slide here. Like tranfer the graph thing here. Also why does my header dis
appear!!!!!""")

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

    #Replace all negative with 0
    dva_dataframe[dva_dataframe < 0] = 0

    # Find where to start
    for index,row in dva_dataframe.iterrows():
        if row['Fnet'] > 0:
            # dva_dataframe = dva_dataframe.drop([index])
            dva_dataframe = dva_dataframe.iloc[index:]
            break
    dva_dataframe = dva_dataframe.reset_index(drop=True)

    #Find Time in sec
    sec = []
    for index, row in dva_dataframe.iterrows():
        first_row = dva_dataframe.iloc[[0]]
        sec.append(row['Time (s)'] - first_row['Time (s)'])
    df = pd.concat(sec).reset_index(drop=True)
    dva_dataframe = pd.concat([dva_dataframe, df], axis=1)
    dva_dataframe = dva_dataframe.iloc[: , 1:]

    #Calculate accerlation
    dva_dataframe['Acceleration (a)'] = (dva_dataframe['Fnet']/dva_dataframe['Total Mass'])*1000

    #Calculate speed change
    delta_v = []
    for index, row in dva_dataframe.iterrows():
        row_above = dva_dataframe.iloc[[index-1]]
        delta_v.append(row['Time (s)']*(row_above['Acceleration (a)']+row['Acceleration (a)'])/2)
    df = pd.concat(delta_v).reset_index(drop=True)
    dva_dataframe = pd.concat([dva_dataframe, df], axis=1)
    dva_dataframe = dva_dataframe.set_axis([*dva_dataframe.columns[:-1], 'Speed Change (delta v)'], axis=1, inplace=False)

    #Caluculate speed
    ser = pd.Series({0:0}, name='Speed (v)')
    v = [ser]
    st.write(v)
    for index, row in dva_dataframe.iterrows():
        row_above = dva_dataframe.iloc[[index-1]]
        v.append(v[-1]+row['Speed Change (delta v)'])
    del v[0]
    df = pd.concat(v).reset_index(drop=True)
    dva_dataframe = pd.concat([dva_dataframe, df], axis=1)
    dva_dataframe = dva_dataframe.set_axis([*dva_dataframe.columns[:-1], 'Speed (v)'], axis=1, inplace=False)

    dva_dataframe

    # dataframe = pf.calculate_dva_t(dataframe)

    # #Usable code template for the graphs
    # st.header('DVA')
    # dva_col1, dva_col2 = st.columns([3, 1])
    # dva_col1.subheader('DVA Chart')
    # dva_col1.line_chart(dataframe.rename(columns={'time':'index'}).set_index('index'))
    # dva_col2.subheader('DVA DataFrame')
    # dva_col2.write(dataframe)

    # dva_expander = st.expander('What did we do?')
    # dva_expander.write("We did these calculation:")
    # dva_expander.image("https://static.streamlit.io/examples/dice.jpg")


#---------------------------------------
# Metric
    #I made these values up but obv they would be real in the future
    col1, col2, col3 = st.columns(3)
    col1.metric("Speed", "100 mph", "5 mph")
    col2.metric("End time", "0.98 sec", "-8%")
    col3.metric("Efficiency", "86%", "4%")

###############################################################################

