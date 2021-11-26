import numpy as np
import pandas as pd
from streamlit import cache

import calculation_functions as cf


@cache
def example_csv():
    """This calls the example csv file"""
    example_csv = pd.read_csv('./data/experimental_data.csv')
    example_csv = example_csv.to_csv().encode('utf-8')

    return example_csv


    # example_csv = pd.DataFrame(
    #     {'Time (s)':[
    #             7.9917,
    #             7.9934,
    #             7.9951,
    #             7.9968,
    #             7.9985,
    #             8.0002,
    #             8.0019,
    #             8.0036,
    #             8.0053,
    #             8.007,
    #             8.0087,
    #             8.0104,],
    #         'Force (N)':[
    #             10.20665628,
    #             14.61394447,
    #             19.78110993,
    #             25.2522263,
    #             29.53793412,
    #             32.09112176,
    #             32.91178922,
    #             31.84796103,
    #             28.96042739,
    #             24.40116375,
    #             19.23399829,
    #             14.70512974,],
    #         'CO2 Mass (Mco2)':[
    #             29.85,
    #             29.85,
    #             29.85,
    #             29.85,
    #             29.85,
    #             29.85,
    #             29.85,
    #             29.85,
    #             29.85,
    #             29.85,
    #             29.85,
    #             29.85,],
    #         'Drag (FD)':[
    #             0.243,
    #             0.243,
    #             0.243,
    #             0.243,
    #             0.243,
    #             0.243,
    #             0.243,
    #             0.243,
    #             0.243,
    #             0.243,
    #             0.243,
    #             0.243,
    #         ]
    #     }
    # )
