import pandas as pd
from generalization import *

def parse_currency_string(currency_string):
    # Eliminamos el símbolo '$' y cualquier espacio en blanco, y convertimos la cadena en minúsculas
    currency_string = currency_string.replace('$', '').replace(' ', '').replace(' ', '').lower()
    # Extraemos el signo (si existe)
    sign = -1 if currency_string[0] == '-' else 1
    # Eliminamos el signo de la cadena (si existe)
    currency_string = currency_string[1:] if sign == -1 else currency_string
    # Extraemos la cantidad en dólares y centavos
    dollars_cents = currency_string[:-1]
    # Convertimos la cantidad en dólares y centavos a un valor de punto flotante
    if(dollars_cents == ''):
        return 0
    dollars_cents_float = float(dollars_cents)
    # Extraemos el orden de magnitud
    magnitude_char = currency_string[-1]
    # Convertimos el orden de magnitud a un factor multiplicativo
    if magnitude_char == 'b':
        magnitude_factor = 1e9
    elif magnitude_char == 'm':
        magnitude_factor = 1e6
    elif magnitude_char == 'k':
        magnitude_factor = 1e3
    else:
        raise ValueError("Invalid magnitude character")
    # Multiplicamos la cantidad en dólares y centavos por el factor multiplicativo
    currency_float = dollars_cents_float * magnitude_factor * sign
    # Devolvemos el valor resultante
    return currency_float


#df = pd.DataFrame({'Age': [30, 93, 18, 13, 95, 34, 87, 81, 85, 40, 21, 63, 28, 66, 23, 79, 45, 53, 68, 11,
#             95, 24, 23, 62, 37, 11, 72, 85, 70, 60, 1, 52, 84, 23, 35, 19, 41, 31, 55, 47, 
#             90, 3, 95, 51, 39, 89, 15, 56, 23, 78, 95, 51, 89, 64, 67, 61, 63, 71, 74, 64, 
#             44, 31, 19, 14, 77, 8, 36, 76, 47, 87, 1, 84, 26, 95, 1, 12, 35, 72, 70, 9, 70, 
#             48, 90, 18, 82, 1, 52, 59, 39, 58, 45, 66, 80, 74, 72, 33, 38, 2, 13, 25],
#            'Income': [150000, 850000, 820000, 630000, 620000, 620000, 130000, 630000, 
#                       260000, 340000, 300000, 640000, 160000, 370000, 980000, 190000, 
#                       720000, 780000, 780000, 720000, 870000, 610000, 370000, 300000, 
#                       60000, 490000, 360000, 670000, 610000, 190000, 490000, 130000, 
#                       790000, 60000, 630000, 890000, 740000, 930000, 760000, 130000, 
#                       950000, 350000, 980000, 990000, 80000, 920000, 560000, 210000, 
#                       580000, 750000, 950000, 810000, 160000, 180000, 120000, 780000, 
#                       310000, 290000, 180000, 570000, 610000, 890000, 80000, 680000, 
#                       640000, 320000, 70000, 80000, 270000, 520000, 620000, 110000, 
#                       730000, 630000, 30000, 320000, 170000, 780000, 750000, 980000, 
#                       110000, 600000, 80000, 240000, 830000, 470000, 680000, 890000, 
#                       460000, 850000, 270000, 340000, 30000, 590000, 910000, 920000, 
#                       970000, 200000, 280000, 90000], 
#            'Country':['United States', 'United States', 'Philippines', 'China', 'China', 'Germany', 'Germany', 'Germany',
#                        'United States', 'Russia', 'Taiwan', 'Nigeria', 'China', 'United States', 'Russia', 'Russia', 'Canada',
#                        'Argentina', 'Sweden', 'Singapore', 'China', 'Russia', 'France', 'Colombia', 'Netherlands', 'China', 'United States',
#                        'United States', 'Hong Kong', 'Germany', 'Sweden', 'United States', 'United States', 'Hong Kong', 'Norway', 'Australia',
#                        'United States', 'United States', 'Mexico', 'United Kingdom', 'Spain', 'United States', 'China', 'China', 'Singapore', 'Germany',
#                        'United States', 'United States', 'United States', 'Austria', 'United States', 'United States', 'France', 'China', 'United States',
#                        'United States', 'Sweden', 'China', 'India', 'United States', 'United States', 'Denmark', 'China', 'Hong Kong', 'Russia', 'Canada',
#                        'Australia', 'India', 'Japan', 'Switzerland', 'India', 'United States', 'Australia', 'United States', 'United States', 'United States',
#                        'South Africa', 'United States', 'China', 'Kazakhstan', 'Singapore', 'Monaco', 'United States', 'India', 'Russia', 'United States',
#                        'Switzerland', 'United States', 'Denmark', 'Germany', 'United States', 'China', 'Italy', 'China', 'Korea', 'Canada', 'Germany', 'United States',
#                        'Saudi Arabia', 'United Kingdom']})
#generalized_df = generalize_numeric_data(df, ['Age', 'Income'], 3)
#generalized_df = generalize_categorical_data(df, ['Country'], ['country'])
#print(generalized_df)


# Mostrar el resultado
#print(counts_df)

#gen_kanony_data(df, ['Age', 'Income'], ['Country'], ['country'])
#df = pd.read_csv('AgeDataset-V3.csv', sep=',')
df = pd.read_csv('500 richest people 2021.csv', delimiter=';')
print(df.dtypes)
print(df.head(10))

#gen_kanony_data(df, ['Birth year', 'Death year', 'Age of death'], ['Country'], ['country'])
numeric_cols = ['$ Last Change', '$ YTD Change']
fixed_data = df.copy()
fixed_data[numeric_cols] =  fixed_data[numeric_cols].applymap(parse_currency_string)
fixed_data = fixed_data.iloc[:,:7]
#df['Total Net Worth'].apply(parse_currency_string)
#df[].apply(parse_currency_string)
#df[].apply(parse_currency_string)
print(fixed_data.head(10))

df['$ Last Change'] = df['$ Last Change'].astype(int)
df['$ YTD Change'] = df['$ YTD Change'].astype(int)
gen_kanony_data(df, ['$ Last Change', '$ YTD Change'], ['Country'], ['country'])