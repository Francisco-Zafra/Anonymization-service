import pandas as pd
import numpy as np

def generalize_numeric_data(dataframe, columns_to_convert, k):

    df = dataframe.copy()

    for col in columns_to_convert:
        print(col)
        col_min = df[col].min()
        col_max = df[col].max()
        interval_size = np.ceil((col_max - col_min + 1) / k)
        print("Calculating intervals...")
        print("Max: " + str(col_max)  + ", Min: " + str(col_min) + ", Interval: " + str(interval_size))

        col_intervals = []
        
        #Create intervals for k-anonymization
        for i in range(k):
            interval_min = col_min + i * interval_size
            interval_max = min(col_max, interval_min + interval_size - 1)
            print("Interval " + str(i) + " ["+ str(interval_min) + ", " + str(interval_max) + "]")
            col_intervals.append((interval_min, interval_max))
        
        #Applying k-anonymization dor numeric-data
        df[col] = pd.cut(df[col], [interval[0]-1e-9 for interval in col_intervals] + [col_intervals[-1][1]], labels=[f"[{interval[0]}-{interval[1]}]" for interval in col_intervals])

    return df