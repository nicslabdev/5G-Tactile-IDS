#################################################################
#
# MODULE TO MANAGE DIFERENT INPUT INTERFACES
#
#################################################################

import pandas as pd
import numpy as np

def modificar_dataframe(df, pct_filas = 0.03, pct_cambio = 0.2):
    # Número de filas y columnas del DataFrame
    num_filas = len(df)
    num_columnas = len(df.columns[:-1])
    
    # Seleccionar aleatoriamente el 10% de las filas
    num_filas_modificar = int(num_filas * pct_filas)
    filas_modificar = np.random.choice(df.index, size=num_filas_modificar, replace=False)
    
    # Seleccionar aleatoriamente un número de columnas (entre 1 y el número total de columnas)
    num_columnas_modificar = np.random.randint(1, num_columnas + 1)
    columnas_modificar = np.random.choice(df.columns[:-1], size=num_columnas_modificar, replace=False)
    
    # Modificar los valores de las filas y columnas seleccionadas en un 15%
    for fila in filas_modificar:
        for columna in columnas_modificar:
            df.at[fila, columna] = int(df.at[fila, columna] * (1 + pct_cambio))
            df.at[fila, 'label'] = 1

    df.to_csv('tmp.csv')
            
    return df

#######################################################################

def source_example():
    dataframe = pd.read_csv('example/datasets/TimeSeries.csv')
    dataframe_labels = pd.read_csv('example/datasets/labelsTimeSeries.csv')
    
    dataframe['label'] = dataframe_labels['label']

    return dataframe

def vicomtech_data():
    dataframe = pd.read_csv('data/RecFile_1_20240712_095926_CAM_Generator_output_list.csv')
    dataframe = dataframe.head(100)
    dataframe['label'] = 0
    dataframe = dataframe.drop('Timestamp (UNIX) ', axis=1)
    dataframe = dataframe.drop('Unnamed: 0', axis=1)

    modificar_dataframe(dataframe, pct_cambio=10)

    return dataframe

def simple_random_data(size=100, n_columns=5):
    # Generar datos aleatorios para las columnas
    data = np.random.rand(size, n_columns)
    
    # Crear el DataFrame con los datos aleatorios
    df = pd.DataFrame(data, columns=[f'col_{i}' for i in range(n_columns)])
    
    # Agregar la columna 'label' con valores 0 o 1
    df['label'] = np.random.choice([0, 1], size=size, p=[0.7, 0.3])
    
    return df