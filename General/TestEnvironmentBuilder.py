import os
import sys
from pandas.io import excel
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

def get_years_addition(years):
    if(len(years) > 1):
        return f"{years[0]}-{years[-1]}"
    else:
        return f"{years[0]}"

def prepare_orig_data(dfOrig):
    """
    We make the orig data numeric. This includes: 
        - removing the msa, zipcode, dt_matr and dt_first_pi (as it is not compatible)
        - Change the flags to True/False values {0,1}
        - get dummies for large categoric values
    """
    # map to bool : ppmt_pnlty, flag_sc,
    # exclude : zipcode
    # dummy the rest
    exclude = [
        "zipcode",
        "dt_first_pi",
        "dt_matr",
        "cd_msa",
        "index",
    ]
    yesNoMap = {"N" : 0, "Y" : 1}
    
    # Map
    dfOrig["flag_sc"] = dfOrig["flag_sc"].map(yesNoMap)
    dfOrig["ppmt_pnlty"] = dfOrig["ppmt_pnlty"].map(yesNoMap)
    
    # del msa
    for column in exclude:
        dfOrig.drop(column, axis=1, inplace=True)
    
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

def main(years, ratio, sep, seed):
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
    dfOrig.reset_index(inplace=True)
    origData = dfOrig.to_numpy()
    columns = np.array(dfOrig.columns.to_list())
    origTrain, origTest = train_test_split(origData, train_size=ratio, random_state=seed)
    
    logger.info(f"Write data sets to csv", level=0)
    # Write to csv
    years_addition = get_years_addition(years=years)
    write_numpy_to_csv(columns, f"columnNames_{years_addition}.csv", train=True, sep=sep)
    write_numpy_to_csv(columns, f"columnNames_{years_addition}.csv", train=False, sep=sep)
    write_numpy_to_csv(origTrain, f"OriginateData_{years_addition}.csv", train=True, sep=sep)
    write_numpy_to_csv(origTest, f"OriginateData_{years_addition}.csv", train=False, sep=sep)

"""
======================
Parameters for script
======================
"""
# years = range(2013, 2021)
years = [2013]
ratio = 0.7
sep = ','
seed = 10

main(years=years, ratio=ratio, sep=sep, seed=seed)