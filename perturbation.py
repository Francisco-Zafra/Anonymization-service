import pandas as pd
import numpy as np

def parse_currency_string(currency_string):
    if type(currency_string) == type(1) or type(currency_string) == type(1.0):
        return currency_string
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


def noise_addition(df, numeric_cols):
    # Aplicamos la perturbación a las columnas numéricas
    perturbed_data = df.copy()
    perturbed_data[numeric_cols] = perturbed_data[numeric_cols].applymap(perturb)

    # Redondeamos los valores perturbados a 2 decimales para mayor legibilidad
    perturbed_data[numeric_cols] = perturbed_data[numeric_cols].round(2)

    return perturbed_data


def micro_aggregation(df, numeric_cols, k=3):
        
    # Crear una copia de la base de datos a modificar
    df_anon = df.copy()
    
    # Para cada columna numérica, calcular las medias y desviaciones estándar
    # de los k vecinos más cercanos de cada registro
    for col in numeric_cols:
        means = []
        stds = []
        for i in range(len(df_anon)):
            # Calcular las distancias a todos los demás registros
            distances = np.sqrt(np.sum((df_anon[numeric_cols].iloc[i] - df_anon[numeric_cols])**2, axis=1))
            # Obtener los índices de los k vecinos más cercanos
            k_nn_idx = np.argsort(distances)[1:k+1]
            # Calcular la media y desviación estándar de los k vecinos más cercanos
            means.append(np.mean(df_anon[col].iloc[k_nn_idx]))
            stds.append(np.std(df_anon[col].iloc[k_nn_idx]))
        # Perturbar cada registro sumando un ruido aleatorio extraído de una distribución normal
        # con media 0 y desviación estándar igual al promedio de las desviaciones estándar de los vecinos
        df_anon[col] = np.random.normal(loc=df_anon[col], scale=np.mean(stds)).round(2)
    
    return df_anon


# Cargamos los datos originales desde un archivo CSV
# original_data = pd.read_csv('500 richest people 2021.csv',delimiter=";")

# numeric_cols = ["$ Last Change", "$ YTD Change"]
# fixed_data = original_data.copy()
# fixed_data[numeric_cols] = fixed_data[numeric_cols].applymap(parse_currency_string)
# fixed_data = fixed_data.iloc[:, :7]

# df_anon = micro_aggregation(fixed_data, numeric_cols)

# print(df_anon)