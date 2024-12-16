import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest

def run_classic_threshold(df):
    idf = df

    comparing_df = idf.shift(-1) / idf
    comparing_df = comparing_df[:-1]

    pred_anomalies = ((comparing_df > 1.1) | (comparing_df < 0.9)).any(axis=1).astype(int).values
    pred_anomalies = np.append(pred_anomalies, [0])

    return pred_anomalies

def run_iforest(df):
    idf = df
    # Aplicar Isolation Forest
    model = IsolationForest(contamination=0.03)  
    idf['anomaly'] = model.fit_predict(idf)
    
    pred_labels = idf['anomaly'].apply(lambda x: 0 if x == 1 else 1)

    return pred_labels.to_numpy()

import numpy as np
import matplotlib.pyplot as plt
from sklearn.neighbors import LocalOutlierFactor

def run_LOF(df):
    idf = df
    # Ajustar el modelo LOF
    model = LocalOutlierFactor(n_neighbors=20, contamination=0.03)
    idf['anomaly_lof'] = model.fit_predict(idf)

    pred_labels = idf['anomaly_lof'].apply(lambda x: 0 if x == 1 else 1)

    return pred_labels.to_numpy()


def majority_vote(predictions):
    arrays = []
    for p in predictions:
        arrays.append(predictions[p])
    # Stack the arrays along a new dimension
    stacked_arrays = np.stack(arrays, axis=0)
    
    # Calculate the sum along the new dimension
    sum_arrays = np.sum(stacked_arrays, axis=0)
    
    # Determine the majority vote (more than half of the arrays should have a 1)
    majority_threshold = len(arrays) / 2
    
    # If the sum is greater than the threshold, the majority is 1, otherwise 0
    majority_vote_result = (sum_arrays >= majority_threshold).astype(int)
    
    return majority_vote_result

def detect_anomalies_by_columnn(X):
    vote_all = {}

    for column in X.columns[1:]:
        print(column)
        predictions_all = {}

        cont = 0
        vote = []
        values_count = len(X)
        while cont < values_count:
            data = X[[X.columns[1], column]].iloc[cont:cont+100]
            cont += 100

            predictions_all['IForest'] = list(run_iforest(data.copy()))
            predictions_all['LOF'] = list(run_LOF(data.copy()))
            predictions_all['Classic_Threshold'] = list(run_classic_threshold(data.copy()))
            vote += list(majority_vote(predictions_all))
        vote_all[column] = vote

    # Initialize the result with the first array
    result = vote_all[next(iter(vote_all))]

    # Perform AND operation across all arrays
    for array in vote_all.values():
        result = [x | y for x, y in zip(result, array)]
    
    return result

def run(X, Y):
    return detect_anomalies_by_columnn(X)