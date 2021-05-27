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

from DataLoader import DataLoader
import PrepaymentInfoProvider as ppm
import PreprocessMonthlyData as preProcess

import DataSetBuilder as dataBuilder

class EnvVariables():
    EnvName = "TestEnvironment"
    
    TestName = "Test"
    TrainName = "Train"
    
    # last time step in the data set
    LastYear = 2020 
    LastMonth = 9
    
    # first time step in the data set
    FirstYear = 2013 
    FirstMonth = 2

def get_months(year1, year2, month1, month2):
    if(year2 > year1):
        return (year2 - year1) * 12 + (month2 - month1)
    else:
        return (year1 - year2) * 12 + (month1 - month2)      

def get_time_step_by_year(year, month):
    return get_months(year, EnvVariables.FirstYearm, month, EnvVariables.FirstMonth)

def get_time_step_by_ratio(ratio):
    diff = get_months(EnvVariables.LastYear, EnvVariables.FirstYear, 
                      EnvVariables.LastMonth, EnvVariables.FirstMonth)
    return int(diff * ratio)

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

def main(years, ratio, ppm_th, ppm_skip_mnths, sep, seed):
    logger.info("Load Data")
    dl = DataLoader()
    dfOrigClean, dfMonthlyClean = dl.get_data_set(years=years)
    dfPPM = ppm.calculate_prepayment_info(dfOrig=dfOrigClean, 
                                          dfMonthly=dfMonthlyClean, 
                                          threshold_percentage=ppm_th, 
                                          timeSkip=ppm_skip_mnths)
    dfMonthly = dfMonthlyClean.reset_index().merge(dfPPM[["id_loan", "svcg_cycle", "prepayment_type"]], 
                                                   how="left", 
                                                   on=["id_loan", "svcg_cycle"]).set_index(["id_loan", 
                                                                                            "svcg_cycle"])
    
    timeStep = get_time_step_by_ratio(ratio)                                               
    dfOrig = dataBuilder.build_data_set(years, recalculate=True, timeStep=timeStep, dfPPM=dfPPM)
    dfMonthly = preProcess.preprocess_monthly_data(dfMonthly=dfMonthly, current_time_step=timeStep)
    dfOrig = preProcess.add_monthly_data_to_orig_data(dfMonthly=dfMonthly, dfOrig=dfOrig)

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
# ys = range(2013, 2021)
ys = [2013]
ratio = 0.7

ppm_threshold = 0.1
ppm_months_to_skip = 6

sep = ','
seed = 10

for y in ys:
    years = [y]

    main(years=years, 
         ratio=ratio, 
         ppm_th=ppm_threshold, 
         ppm_skip_mnths=ppm_months_to_skip, 
         sep=sep, 
         seed=seed)