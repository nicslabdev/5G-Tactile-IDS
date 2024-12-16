#################################################################
#
# MODULE TO MANAGE WORKERS INPUTS/OUTPUTS
#
# INPUT PIPELINE:   INPUT > PRE_PROCESING > MAIN > WORKERS
# OUTPUT PIPELINE:  WORKERS > MAIN > POST-PROCESING > OUTPUT
#
#################################################################

#################################################################
# CUSTOM MODULES IMPORTS
#################################################################
import pre_processing
import post_processing
import input_module
import output_module
import main_process
from store_module import save_to_influxdb

#################################################################
# PYTHON IMPORTS
#################################################################
import os
import glob
import sys

#################################################################
#################################################################
from matplotlib import pyplot as plt
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from sklearn.metrics import roc_auc_score

def evaluate(Y, Y_pred):

    roc_auc = roc_auc_score(Y, Y_pred)
    print(f'ROC: {roc_auc}')

    # Compute confusion matrix
    cm = confusion_matrix(Y, Y_pred)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm)
    disp.plot()
    plt.show()
    return roc_auc

def run(mode='basic'):
    if mode == 'basic':
        #################################################################
        # GET DATA DATAFRAMES
        #################################################################
        df = pre_processing.basic_clean(input_module.vicomtech_data())
        X = df.iloc[:, :-1]
        Y = df.iloc[:, -1]

        #################################################################
        # SELECT AND RUN WORKERS
        #################################################################
        # Get a list of all Python files in the directory
        sys.path.insert(0, 'workers')
        python_files = glob.glob(os.path.join('workers', '*.py'))

        # Import all Python files and run modules
        results = {}
        for py_file in python_files:
            print(f'Running {py_file}')
            module_name = os.path.splitext(os.path.basename(py_file))[0]
            module = __import__(module_name)
            results[module_name] = module.run(X, Y)


        print("Processing results...")

        #################################################################
        # PROCESS AND OUTPUT RESULTS
        #################################################################
        # TODO CREATE PROCESS RESULTS FUNCTION
        output = main_process.process_results(results)
        # Upload data to database
        save_to_influxdb(X, output)
        if output_module.print_output(post_processing.basic_post_processing(output)) == 0:
            print('Success')

        roc_auc = evaluate(Y, output)

        return roc_auc
    
    if mode == 'test':
        #################################################################
        # GET DATA DATAFRAMES
        #################################################################
        df = pre_processing.basic_clean(input_module.vicomtech_data())
        X = df.iloc[:, :-1]
        Y = df.iloc[:, -1]

        #################################################################
        # SELECT AND RUN WORKERS
        #################################################################
        # Get a list of all Python files in the directory
        sys.path.insert(0, 'workers')
        python_files = glob.glob(os.path.join('workers', '*.py'))

        # Import all Python files and run modules
        results = {}
        for py_file in python_files:
            print(f'Running {py_file}')
            module_name = os.path.splitext(os.path.basename(py_file))[0]
            module = __import__(module_name)
            results[module_name] = module.run(X, Y)


        print("Processing results...")

        #################################################################
        # PROCESS AND OUTPUT RESULTS
        #################################################################
        # TODO CREATE PROCESS RESULTS FUNCTION
        output = main_process.process_results(results)
        # Upload data to database
        save_to_influxdb(X, output)
        if output_module.print_output(post_processing.basic_post_processing(output)) == 0:
            # print('Success')
            pass

        roc_auc = evaluate(Y, output)

        return roc_auc

if __name__ == "__main__":
    run()
    print("Finished")
    sys.exit(0)