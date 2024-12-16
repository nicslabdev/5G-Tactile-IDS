#################################################################
#
# MODULE TO MANAGE PRE-PROCESING INPUT DATA
#
#################################################################

import pandas as pd

def basic_clean(source):
    df = source
        # Convert all values to numeric, coerce non-numeric values to NaN
    df_numeric = df.apply(pd.to_numeric, errors='coerce')
        # Drop columns with only NaN values
    df_clean = df_numeric.dropna(axis=1, how='all').dropna()
        # Drop all rows with NaN values
    df_clean = df_clean.dropna()

    return df_clean