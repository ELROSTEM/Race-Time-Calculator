import pandas as pd
import streamlit as st

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

#Upload CSV File
uploaded_file = st.sidebar.file_uploader(label='Upload Race Time Data')
if uploaded_file is not None:
    dataframe = pd.read_csv(uploaded_file)
    st.write(dataframe)


# get difference for time values
st.write(dataframe)

count_t_vals = dataframe['time'].values
diffs_t = count_t_vals[:-1] - count_t_vals[1:]

# get differences for distance values
count_d_vals = dataframe['displacement'].values
diffs_d = count_d_vals[:-1] - count_d_vals[1:]

# create velocity column and calculte it
dataframe['Velocity'] = ''
dataframe['Velocity'] = dataframe.loc[diffs_d / diffs_t]

st.write(dataframe)

# # calculate difference in velocity
# count_v_vals = dataframe['Velocity'].values
# diffs_v = count_v_vals[:-1] - count_v_vals[1:]

# # calculate accelertaion
# dataframe['Acceleration'] = dataframe.loc[diffs_v / diffs_t]
# st.write(dataframe)


###############################################################################
# Main body



###############################################################################

