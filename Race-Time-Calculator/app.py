import pandas as pd
import streamlit as st
from streamlit.elements.arrow import Data

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

#------------------------------------------------------------------------------
#D-t V-t A-t inputs or DVA inputs

help_dva = """Please upload a CSV File that has your time and distance measurem
ents"""

#Upload CSV File
uploaded_file = st.sidebar.file_uploader(
    label='Upload Race Time Data', help=help_dva)

#------------------------------------------------------------------------------
#Fnet inputs

help_fnet = """Please input your old measurements"""

#Friction data input (old)
friction_data_old = st.sidebar.number_input(
    label='Friction Data Old (stff)', help=help_fnet)

#Mass data input (old)
mass_data_old = st.sidebar.number_input(
    label='Mass Data Old (KG?)', help=help_fnet)

#Drag data input (old)
drag_data_old = st.sidebar.number_input(
    label='Drag Data Old (stuff)', help=help_fnet)

###############################################################################
# Main body

#------------------------------------------------------------------------------
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
#------------------------------------------------------------------------------

# Dva calc
    dataframe = pd.read_csv(uploaded_file)
    dataframe = pf.calculate_dva_t(dataframe)

    st.header('DVA')
    dva_col1, dva_col2 = st.columns([3, 1])
    dva_col1.subheader('DVA Chart')
    dva_col1.line_chart(dataframe.rename(columns={'time':'index'}).set_index('index'))
    dva_col2.subheader('DVA DataFrame')
    dva_col2.write(dataframe)

    dva_expander = st.expander('What did we do?')
    dva_expander.write("We did these calculation:")
    dva_expander.image("https://static.streamlit.io/examples/dice.jpg")

#------------------------------------------------------------------------------

#Fnet Calc
    fnet = pf.calculate_fnet(dataframe, friction_data_old, mass_data_old, drag_data_old)



#------------------------------------------------------------------------------
# Metric
    #I made these values up but obv they would be real in the future
    col1, col2, col3 = st.columns(3)
    col1.metric("Speed", "100 mph", "5 mph")
    col2.metric("End time", "0.98 sec", "-8%")
    col3.metric("Efficiency", "86%", "4%")

###############################################################################

