import numpy as np
import pandas as pd
from streamlit import cache

import calculation_functions as cf


def example_csv():
    example_csv = 'https://raw.githubusercontent.com/Roosevelt-Racers/Race-Time-Calculator/master/Race-Time-Calculator/data/experimental_data.csv'
    example_csv = pd.read_csv(example_csv).to_csv().encode('utf-8')
    return example_csv
