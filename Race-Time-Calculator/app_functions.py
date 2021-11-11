import numpy as np
import pandas as pd
from streamlit import cache

import calculation_functions as cf


@cache
def example_csv():
    example_csv = pd.read_csv('experimental_data.csv')
    example_csv = example_csv.to_csv().encode('utf-8')
    return example_csv
