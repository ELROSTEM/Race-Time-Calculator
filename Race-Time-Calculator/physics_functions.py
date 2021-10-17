import numpy as np
import pandas as pd

###############################################################################
# ^Python standard line length


###############################################################################

#d-t, v-t, a-t calculator
def calculate_dva_t(dataframe):
    """This function calculates the v-t and a-t using the d-t table"""
    # get differences for time values
    count_t_vals = dataframe['time'].values
    diffs_t = count_t_vals[:-1] - count_t_vals[1:] 

    # get differences for displacement values
    count_d_vals = dataframe['displacement'].values
    diffs_d = count_d_vals[:-1] - count_d_vals[1:] 

    # create velocity column and calculte it
    velocity = diffs_d / diffs_t
    dataframe['velocity']= np.insert(velocity,0,0)

    # calculate difference in velocity
    count_v_vals = dataframe['velocity'].values
    diffs_v = count_v_vals[:-1] - count_v_vals[1:]
    diffs_v=np.round(diffs_v,1)

    # calculate accelertaion
    accel= diffs_v / diffs_t
    dataframe['acceleration']=np.append(accel,0)
    return dataframe


###############################################################################

#Fnet Calculator
def calculate_fnet(dataframe, friction, mass, drag):
    return None

###############################################################################
