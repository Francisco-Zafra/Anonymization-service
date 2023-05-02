import pandas as pd
import numpy as np

# Cargamos los datos originales desde un archivo CSV
original_data = pd.read_csv('500 richest people 2021.csv',delimiter=";")

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


# Definimos la función de perturbación para aplicar a las columnas numéricas
def perturb(x):
    # Definimos la magnitud máxima de perturbación como el 5% del valor original
    max_perturbation = 0.05 * parse_currency_string(x)
    # Generamos un valor aleatorio de perturbación dentro del rango permitido
    perturbation = np.random.uniform(low=-max_perturbation, high=max_perturbation)
    # Devolvemos el valor original más la perturbación
    return parse_currency_string(x) + perturbation

# Seleccionamos las columnas numéricas a perturbar
numeric_cols = ['$ Last Change', '$ YTD Change']

# Aplicamos la perturbación a las columnas numéricas
perturbed_data = original_data.copy()
perturbed_data[numeric_cols] = perturbed_data[numeric_cols].applymap(perturb)

# Redondeamos los valores perturbados a 2 decimales para mayor legibilidad
perturbed_data[numeric_cols] = perturbed_data[numeric_cols].round(2)

# Definimos el valor de k
k = 10

# Definimos una función que toma un dataframe y realiza una operación en el grupo de 10 elementos
def operate_on_group(df):
    # Realizamos una operación en el grupo de 10 elementos, por ejemplo, calculamos la suma de la columna A
    result = df['Total Net Worth'].apply(parse_currency_string)
    # Devolvemos el resultado como un dataframe
    return pd.DataFrame({'result': [result]})

result = perturbed_data.groupby(perturbed_data.index // k).apply(operate_on_group)

print(result)

# # Seleccionamos y reordenamos las columnas que queremos incluir en el archivo anonimizado
# anon_data = anon_data[['Rank', 'Name', 'Total Net Worth', '$ Last Change', '$ YTD Change', 'Country', 'Industry']]

# # Guardamos los datos anonimizados en un archivo CSV
# anon_data.to_csv('datos_anonimizados.csv', index=False)
