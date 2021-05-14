import os
import sys
curDir = os.path.dirname(__file__)
sys.path.append(os.path.join(curDir, "..", "PreProcessing"))

import pandas as pd

import PathUtilities as pu
import PrepaymentInfoProvider as ppm
import ConsoleWriter as logger

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

def divide_data_set(df, ratio_train):
    """
    Ratio based on the train set. 
    Hence: 0.7 => 70% train and 30% test
    
    NOT RANDOM;
    Just first n rows for train and 
    rest for test.
    """
    if((ratio_train > 1) | (ratio_train < 0)):
        raise Exception("ratio_train should be between 0 and 1")
    
    n = len(df.index)
    trainAmount = int(n * ratio_train)
    testAmount = n - trainAmount
    
    dfTrain = df[:trainAmount]
    dfTest = df[trainAmount:testAmount+1]
    
    return dfTrain, dfTest

def get_years_addition(years):
    if(len(years) > 1):
        return f"{years[0]}-{years[-1]}"
    else:
        return f"{years[0]}"

def main(years, ratio, sep):
    logger.info("Read data", level=0)
    loader = DataLoader()
    logger.info("Read Originate and Monthly data", level=1)
    dfOrig, dfMonthly = loader.get_data_set(years=years)
    logger.info("Retrieve prepayment info", level=1)
    dfPPM = ppm.calculate_prepayment_info(dfOrig=dfOrig, dfMonthly=dfMonthly)
    
    logger.info("Combine data sets", level=0)
    # Combine monthly and dfPPM
    
    # 
    # Do some merging.
    # 
    
    # For the Orig data, combine the flags (if any is True --> flag is true)
    ppmOrigLevelSeries = dfPPM.groupby("id_loan").max()[ppm.ColumnNames.FlagName]
    dfOrig[ppm.ColumnNames.FlagName] = ppmOrigLevelSeries
    
    logger.info(f"Divide data sets by ratio {ratio}", level=0)
    # Divide data set
    dfOrigTrain, dfOrigTest = divide_data_set(dfOrig, ratio_train=ratio)
    dfMonthlyTrain, dfMonthlyTest = divide_data_set(dfMonthly, ratio_train=ratio)
    
    logger.info(f"Write data sets to csv", level=0)
    # Write to csv
    years_addition = get_years_addition(years=years)
    write_to_csv(dfOrigTrain, f"OriginateData_{years_addition}.csv", train=True, sep=sep)
    write_to_csv(dfOrigTest, f"OriginateData_{years_addition}.csv", train=False, sep=sep)

    write_to_csv(dfMonthlyTrain, f"MonthlyData_{years_addition}.csv", train=True, sep=sep)
    write_to_csv(dfMonthlyTest, f"MonthlyData_{years_addition}.csv", train=False, sep=sep)

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