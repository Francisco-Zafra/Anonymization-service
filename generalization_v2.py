import pandas as pd
import numpy as np
import json

def get_division(dataframe, columns_to_convert):
    num_inter = 9999999999999999999999999999999999999

    for col in columns_to_convert:
        col_max = dataframe[col].max()
        col_min = dataframe[col].min()
        intervals = col_max - col_min
        #print(col + " Col_Max: " + str(col_max) + " Col_Min: " + str(col_min) + " Intervals: " + str(intervals))
        if (intervals < num_inter):
            num_inter = intervals

    return num_inter/100000000


def generalize_numeric_data(dataframe, columns_to_convert, k):
    df = dataframe.copy()

    for col in columns_to_convert:
        unique_values = sorted(df[col].unique())
        col_intervals = []
        pointer = 0
        interval_size = 1
        num_rows = df.shape[0]
        print(unique_values)
        print("Calculating intervals...")
        print(col)
        while(num_rows > 0):#hacer un while que mientras no se cambien la cantidad de filas siga adelante, tambien evaluar si la cantidad de datos que quedan son mayor a k    
            if (num_rows > k + interval_size):
                while(pointer + interval_size < len(unique_values)):
                    print("pointer: " + str(pointer) + " "+ str(len(unique_values)) + " " + str(interval_size))
                    interval_min = unique_values[pointer]
                    interval_max = unique_values[pointer+interval_size]
                    print("current interval: ["+ str(interval_min) + ", " + str(interval_max) + "]")
                    mask = np.logical_and(df[col] >= interval_min, df[col] <= interval_max)
                    count = np.sum(mask)

                    if (count >= k):
                        print("add a new interval..." + str(interval_min) + " count: " + str(count))
                        col_intervals.append((interval_min, interval_max))
                        pointer = pointer + interval_size + 1
                        num_rows = num_rows - count
                        interval_size = 1
                        print("fal_num_rows: " + str(num_rows))
                    else:
                        interval_size = interval_size + 1
            else:
                print("num_rows <= k......")
                col_intervals.append(unique_values[-1])
                pointer = len(unique_values)
                num_rows = 0
            
        print(col_intervals)
        df[col] = pd.cut(df[col], [interval[0]-1e-9 for interval in col_intervals] + [col_intervals[-1][1]], labels=[f"[{interval[0]}-{interval[1]}]" for interval in col_intervals])
        
    print(df)
    return df

                
                

        




    return df

def generalize_categorical_data(dataframe, columns_to_map, categories):
    with open('categories.json', 'r') as f:
        categories_data = json.load(f)

    df = dataframe.copy()

    for col, cat in zip(columns_to_map, categories):
        #df['continent'] = df['country'].map(continent_dict) Crear otra columna si no funciona y luego hacer drop
        category = categories_data[cat]
        df[col] = df[col].map(category)

    return df


def gen_kanony_data(dataframe, numeric_col, cat_col, categories):
    df = dataframe.copy()
    k=2
    chunk =int(get_division(dataframe, numeric_col))
    print("chunk i: " + str(chunk))
    #return 0
    while(chunk >= 2 ):
        df = dataframe.copy()
        print("chunk: " + str(chunk))
        df = generalize_numeric_data(df, numeric_col, chunk)
        #df = generalize_categorical_data(df, cat_col, categories)

        counts = df.groupby(numeric_col).size()
        counts_df = counts.reset_index(name='count')
        counts_df = counts_df.loc[counts_df['count'] > 0]
        print(counts_df)
        if (counts_df['count'] >= k).all():
            k_f= counts_df['count'].min()
            
            print("k-anonymation process successfull with k= " + str(k_f))
            return df
        
        if (chunk > chunk +2 ):
            chunk = chunk - 1*10**(len(str(chunk))-1)
        else:
            chunk = chunk - 1
        
        print("················································································")
    print("Error in k-anonymation process")
    
