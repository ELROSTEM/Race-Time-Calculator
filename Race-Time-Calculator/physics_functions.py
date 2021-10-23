import numpy as np
import pandas as pd

###############################################################################
# ^Python standard line length



###############################################################################

#Friciton Force (Ff)

def friction_f(car_mass, co2_mass, friction_u):
    Ff = (car_mass+co2_mass)/1000*9.81*friction_u
    return Ff

#---------------------------------------

#Friction Coeffe (u)

def friction_u(friction_u):
    return friction_u

###############################################################################

#Net force (Fnet)
def force_net(force, friction_force, drag_force):
    Fnet = force - friction_force - drag_force
    return Fnet

###############################################################################

#CO2 Mass [will be added to car mass which is give to us]

def co2_mass(co2_mass):
    return co2_mass

###############################################################################

#Acceleration (a)

#---------------------------------------
#Speed Change (delta v)  [Calculated using acceleration]

###############################################################################

#Speed (v)   [Calculated using delta v]

#---------------------------------------
#distance change (delta d) [calculated using speed]


###############################################################################

#distance (d)  [calculated using delta d]

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
