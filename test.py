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


df = pd.read_csv('AgeDataset-V4.csv', sep=',')
print(df.head(10))
print(df.shape)
df = gen_kanony_data(df, ['Birth year', 'Death year', 'Age of death'])
df = generalize_categorical_data(df, ['Short description','Country'], ['occupation','country'])
print(df.head(10))

print("----------------------------------------------------------------------------------------------")
df2 = pd.read_csv('500 richest people 2021 decrypted2.csv', delimiter=';')
print(df2.head(10))
print(df2.shape)
numeric_cols = ['$ Last Change', '$ YTD Change']
fixed_data = df.copy()
fixed_data[numeric_cols] =  fixed_data[numeric_cols].applymap(parse_currency_string)
fixed_data = fixed_data.iloc[:,:7]
print(fixed_data.head(10))
df2 = gen_kanony_data(fixed_data, ['$ YTD Change'], ['Country'], ['country'])
df2 = generalize_categorical_data(df, ['Country'], ['country'])
print(df2.head(10))






