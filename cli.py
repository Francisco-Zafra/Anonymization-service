import tkinter as tk
import os
import pandas as pd
from generalization import *
from Pseudonymisation_2 import deidentify, undo_deidentify

from perturbation import micro_aggregation, noise_addition

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


class CheckboxGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Anonymization Service')

        self.csv_files = self.get_csv_files("databases")
        self.selected_file = tk.StringVar(value=self.csv_files[0])
        self.file_selector = tk.OptionMenu(self.root, self.selected_file, *self.csv_files)
        self.file_selector.pack()

        self.checkbox_gen_num = tk.BooleanVar(value=False)
        self.checkbox = tk.Checkbutton(self.root, text='Activar generalizacion numérica', variable=self.checkbox_gen_num)
        self.checkbox.pack()

        self.checkbox_gen_cat = tk.BooleanVar(value=False)
        self.checkbox = tk.Checkbutton(self.root, text='Activar generalizacion categórica', variable=self.checkbox_gen_cat)
        self.checkbox.pack()

        self.checkbox_per_agr = tk.BooleanVar(value=False)
        self.checkbox = tk.Checkbutton(self.root, text='Activar perturbacion con micro agregaciones', variable=self.checkbox_per_agr)
        self.checkbox.pack()
     
        self.checkbox_per_noise = tk.BooleanVar(value=False)
        self.checkbox = tk.Checkbutton(self.root, text='Activar perturbacion con ruido', variable=self.checkbox_per_noise)
        self.checkbox.pack()

        self.checkbox_deidentify = tk.BooleanVar(value=False)
        self.checkbox = tk.Checkbutton(self.root, text='Activar deidentificacion', variable=self.checkbox_deidentify)
        self.checkbox.pack()

        self.submit_button = tk.Button(self.root, text='Anonimizar', command=self.submit)
        self.submit_button.pack()

    def get_csv_files(self, dir):
        csv_files = []
        for file in os.listdir(dir):
            if file.endswith('.csv'):
                csv_files.append(file)
        return csv_files
    
    def submit(self):

        if(self.selected_file.get() == "AgeDataset-V1.csv"):
            df = pd.read_csv('AgeDataset-V4.csv', sep=',')
            if self.checkbox_per_noise.get():
                print("noise_addition")
                df = noise_addition(df, ['Birth year', 'Death year', 'Age of death'])
            if self.checkbox_per_agr.get():
                print("micro_aggregation")
                df = micro_aggregation(df, ['Birth year', 'Death year', 'Age of death'])   
            if self.checkbox_gen_num.get():
                print("gen_kanony_data")
                df = gen_kanony_data(df, ['Birth year', 'Death year', 'Age of death'])
            if self.checkbox_gen_cat.get():
                print("generalize_categorical_data")
                df = generalize_categorical_data(df, ['Short description','Country'], ['occupation','country'])
            if self.checkbox_deidentify.get():
                print("deidentify")
                df = deidentify(df)

        if(self.selected_file.get() == "500 richest people 2021.csv"):
            df = pd.read_csv('500 richest people 2021.csv', delimiter=';')
            numeric_cols = ['$ Last Change', '$ YTD Change']
            df[numeric_cols] =  df[numeric_cols].applymap(parse_currency_string)
            df = df.iloc[:,:7]
            if self.checkbox_per_noise.get():
                print("noise_addition")
                df = noise_addition(df, numeric_cols)
            if self.checkbox_per_agr.get():
                print("micro_aggregation")
                df = micro_aggregation(df, numeric_cols)   
            if self.checkbox_gen_num.get():
                print("gen_kanony_data")
                df = gen_kanony_data(df, ['$ YTD Change'])
            if self.checkbox_gen_cat.get():
                print("generalize_categorical_data")
                df = generalize_categorical_data(df, ['Country'], ['country'])
            if self.checkbox_deidentify.get():
                print("deidentify")
                df = deidentify(df)

        file_name = self.selected_file.get().split(".")[0] + "_anonimized." + self.selected_file.get().split(".")[1]
        df.to_csv("output/" + file_name, index=False)  

        print("Done, file saved")      


    def run(self):
        self.root.mainloop()

if __name__ == '__main__':
    app = CheckboxGUI()
    app.run()
