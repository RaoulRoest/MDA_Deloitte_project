import os
import sys
curDir = os.path.dirname(__file__)
sys.path.append(os.path.join(curDir, "..", "PreProcessing"))

from sklearn.model_selection import train_test_split

import pandas as pd
import numpy as np

import PathUtilities as pu
import PrepaymentInfoProvider as ppm
import ConsoleWriter as logger
import Helpers

from DataLoader import DataLoader

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

def write_to_csv(df, filename, train=True, sep=','):
    if(train):
        folderPath = get_specific_env_path(EnvVariables.TrainName)
        filename = f"Train_{filename}"
    else:
        folderPath = get_specific_env_path(EnvVariables.TestName)
        filename = f"Test_{filename}"
    
    filePath = os.path.join(folderPath, filename)
    pu.check_extension(filePath=filePath, ext="csv")
    
    df.to_csv(filePath, sep=sep)

def write_numpy_to_csv(arr, filename, train=True, sep=','):
    if(train):
        folderPath = get_specific_env_path(EnvVariables.TrainName)
        filename = f"Train_{filename}"
    else:
        folderPath = get_specific_env_path(EnvVariables.TestName)
        filename = f"Test_{filename}"
    
    filePath = os.path.join(folderPath, filename)
    pu.check_extension(filePath=filePath, ext="csv")
    
    np.savetxt(filePath, arr, delimiter=sep, fmt='%s')

def divide_data_set(arr, ratio_train):
    """
    Ratio based on the train set. 
    Hence: 0.7 => 70% train and 30% test
    
    NOT RANDOM;
    Just first n rows for train and 
    rest for test.
    """
    if((ratio_train > 1) | (ratio_train < 0)):
        raise Exception("ratio_train should be between 0 and 1")
    
    # n = len(df.index)
    # trainAmount = int(n * ratio_train)
    # testAmount = n - trainAmount
    
    # dfTrain = df[:trainAmount]
    # dfTest = df[trainAmount:testAmount+1]
    
    return train_test_split(arr, test_size=ratio_train)

def get_years_addition(years):
    if(len(years) > 1):
        return f"{years[0]}-{years[-1]}"
    else:
        return f"{years[0]}"

def prepare_orig_data(dfOrig):
    """
    We make the orig data numeric. This includes: 
        - removing the msa (as it is not compatible)
        - Change the flags to True/False values
        - get dummies for large categoric values
    """
    # map to bool : ppmt_pnlty, flag_sc,
    # exclude : zipcode
    # dummy the rest
    exclude = [
        "zipcode",
        "dt_first_pi",
        "dt_matr,"
    ]
    yesNoMap = {"N" : False, "Y" : True}
    
    # Map
    dfOrig["flag_sc"] = dfOrig["flag_sc"].map(yesNoMap)
    dfOrig["ppmt_pnlty"] = dfOrig["ppmt_pnlty"].map(yesNoMap)
    
    # del msa
    dfOrig.drop("cd_msa", axis=1)
    
    # Get categorical
    numeric, nonNumerics = Helpers.check_dtypes(dfOrig, dfOrig.columns)
    
    for column in nonNumerics:
        if not (column in exclude):
            dfOrig = add_numeric_dummies(dfOrig, column=column)
    
    return dfOrig

def add_numeric_dummies(df, column):
    return pd.concat([df.drop(column, axis=1), pd.get_dummies(df[column], prefix=column)], axis=1)

def add_prepayment_info(dfOrig, dfPPM):
    columns_to_merge = [
        "prepayment_time_step",
        "prepayment_type_FullPrepayment",
        "prepayment_type_No Prepayment",
        "prepayment_type_PartialPrepayment",
        "prepayment_flag_False",
        "prepayment_flag_True",
    ]
    
    dfToMerge = prepare_ppm(dfPPM=dfPPM)
    dfOrig = dfOrig.merge(dfToMerge[columns_to_merge], on="id_loan")

    return dfOrig
    
def prepare_ppm(dfPPM):
    """
    Add dummy columns for: 
        - prepayment_type
        - prepayment_flag
        
    Get time value for prepayment flag
    """
    dfPPM["prepayment_time_step"] = 0
    dfPPM.loc[dfPPM["prepayment_flag"] == True, "prepayment_time_step"] = dfPPM.loc[dfPPM["prepayment_flag"] == True, "time"]    
    
    dummyColumns = [
        "prepayment_type",
        "prepayment_flag"
    ]
    for column in dummyColumns:
        dfPPM = add_numeric_dummies(dfPPM, column=column)
    
    return dfPPM.groupby("id_loan").max()

def main(years, ratio, sep):
    logger.info("Read data", level=0)
    loader = DataLoader()
    logger.info("Read Originate and Monthly data", level=1)
    dfOrig, dfMonthly = loader.get_data_set(years=years)
    logger.info("Retrieve prepayment info", level=1)
    dfPPM = ppm.calculate_prepayment_info(dfOrig=dfOrig, dfMonthly=dfMonthly)
    
    logger.info("Combine data sets", level=0)
    dfOrig = prepare_orig_data(dfOrig=dfOrig)
    dfOrig = add_prepayment_info(dfOrig=dfOrig, dfPPM=dfPPM)
    
    logger.info(f"Divide data sets by ratio {ratio}", level=0)
    # Divide data set
    origData = dfOrig.reset_index().to_numpy()
    columns = np.array(dfOrig.columns.to_list())
    origTrain, origTest = divide_data_set(origData, ratio_train=ratio)
    # dfMonthlyTrain, dfMonthlyTest = divide_data_set(dfMonthly, ratio_train=ratio)
    
    logger.info(f"Write data sets to csv", level=0)
    # Write to csv
    years_addition = get_years_addition(years=years)
    write_numpy_to_csv(columns, f"columnNames_{years_addition}.csv", train=True, sep=sep)
    write_numpy_to_csv(columns, f"columnNames_{years_addition}.csv", train=False, sep=sep)
    write_numpy_to_csv(origTrain, f"OriginateData_{years_addition}.csv", train=True, sep=sep)
    write_numpy_to_csv(origTest, f"OriginateData_{years_addition}.csv", train=False, sep=sep)

    # write_to_csv(dfMonthlyTrain, f"MonthlyData_{years_addition}.csv", train=True, sep=sep)
    # write_to_csv(dfMonthlyTest, f"MonthlyData_{years_addition}.csv", train=False, sep=sep)

"""
======================
Parameters for script
======================
"""
# years = range(2013, 2021)
years = [2013]
ratio = 0.7
sep = ','

main(years=years, ratio=ratio, sep=sep)