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

    #Get rid of negative values in Fnet
    dva_dataframe_acc = dva_dataframe[dva_dataframe.Fnet > 0]

    
    # count_t_vals = dva_dataframe['Time (s)'].values
    # diffs_t = count_t_vals[:-1] - count_t_vals[1:]
    
    # dataframe["Time"]= diffs_t

    dva_dataframe_acc

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

