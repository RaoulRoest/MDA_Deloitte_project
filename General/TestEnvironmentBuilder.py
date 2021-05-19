import os
import sys
curDir = os.path.dirname(__file__)
sys.path.append(os.path.join(curDir, "..", "PreProcessing"))

from sklearn.model_selection import train_test_split

import pandas as pd
import numpy as np

import PathUtilities as pu
import ConsoleWriter as logger
import CsvWriter as csv

import DataSetBuilder as dataBuilder

class EnvVariables():
    EnvName = "TestEnvironment"
    
    TestName = "Test"
    TrainName = "Train"
    
def get_environment_path():
    dataDir = pu.get_data_dir()
    envFolder = os.path.join(dataDir, EnvVariables.EnvName)
    
    pu.make_directory_if_not_exists(envFolder) 
    return envFolder

def get_specific_env_path(specific):
    envFolder = get_environment_path()
    trainFolder = os.path.join(envFolder, specific)
    
    pu.make_directory_if_not_exists(trainFolder)
    return trainFolder

def get_test_env_path(filename, train=True):
    if(train):
        folderPath = get_specific_env_path(EnvVariables.TrainName)
        filename = f"Train_{filename}"
    else:
        folderPath = get_specific_env_path(EnvVariables.TestName)
        filename = f"Test_{filename}"
        
    return os.path.join(folderPath, filename) 

def main(years, ratio, sep, seed):
    logger.info("Load Data")
    dfOrig = dataBuilder.build_data_set(years, recalculate=True)
    
    logger.info(f"Divide data sets by ratio {ratio}", level=0)
    # Divide data set
    dfOrig.reset_index(inplace=True)
    origData = dfOrig.to_numpy()
    columns = np.array(dfOrig.columns.to_list())
    origTrain, origTest = train_test_split(origData, train_size=ratio, random_state=seed)
    
    # Write to csv
    logger.info(f"Write data sets to csv", level=0)
    years_addition = pu.get_years_addition(years=years)
    csv.write_numpy_to_csv(columns, get_test_env_path(f"columnNames_{years_addition}.csv", train=True), sep=sep)
    csv.write_numpy_to_csv(columns, get_test_env_path(f"columnNames_{years_addition}.csv", train=False), sep=sep)
    csv.write_numpy_to_csv(origTrain, get_test_env_path(f"OriginateData_{years_addition}.csv", train=True), sep=sep)
    csv.write_numpy_to_csv(origTest, get_test_env_path(f"OriginateData_{years_addition}.csv", train=False), sep=sep)

"""
======================
Parameters for script
======================
This script creates a test and train environment for modelling.
"""
# years = range(2013, 2021)
years = [2013]
ratio = 0.7
sep = ','
seed = 10

main(years=years, ratio=ratio, sep=sep, seed=seed)