import os 
import sys

curDir = os.path.dirname(__file__)
sys.path.append(os.path.join(curDir, "..", "General"))

import pandas as pd 
import numpy as np

from DataLoader import DataLoader
import PrepaymentInfoProvider as ppm

import PathUtilities as pu
import CsvWriter as csv
import ConsoleWriter as logger
import Helpers

"""
==========================================
SEE BELOW FOR AN EXAMPLE HOW TO USE
==========================================
"""


class EnvironmentVariables():
    FolderName = "CleanedDataSet"
    Prefix = "Clean"
    OrigFileName = "OrigData"
    MonthlyFileName = "MonthlyData"

def build_data_set(years, recalculate=False):
    """
    Reads data file if it is available, otherwise it
    reads the corresponding info from file. 
    If recalculate == True, then the info is always recalculated. 
    """
    filenameMonthly = get_monthly_filename(years=years)
    filenameMonthly = pu.check_extension(filenameMonthly, ext="csv")

    fileNameOrig = get_orig_filename(years=years)
    fileNameOrig = pu.check_extension(fileNameOrig, ext="csv")

    if(recalculate):
        logger.info("Recalculating adjusted data files")
        dfOrig, dfMonthly = recalculate_data_set(years)
        csv.write_to_csv(dfOrig, filename=fileNameOrig, specific=EnvironmentVariables.FolderName, sep=',')                
        csv.write_to_csv(dfMonthly, filename=filenameMonthly, specific=EnvironmentVariables.FolderName, sep=',')                
    
    else:
        if (check_if_file_exists(filename=filenameMonthly)) & (check_if_file_exists(filename=fileNameOrig)):
            logger.info("Reading adjusted data files")
            dfMonthly = get_monthly_data_from_file(years=years)
            dfOrig = get_orig_data_from_file(years=years)
        else:
            logger.warning(f"File {filenameMonthly} was nog found, recalculating adjusted data files.")
            dfOrig, dfMonthly = recalculate_data_set(years)
        csv.write_to_csv(dfOrig, filename=fileNameOrig, specific=EnvironmentVariables.FolderName, sep=',')                
        csv.write_to_csv(dfMonthly, filename=filenameMonthly, specific=EnvironmentVariables.FolderName, sep=',')                
    
    return dfOrig, dfMonthly

def get_monthly_filename(years):
    filename = get_filename(years=years)
    return f"{filename}_{EnvironmentVariables.MonthlyFileName}"

def get_orig_filename(years):
    filename = get_filename(years=years)
    return f"{filename}_{EnvironmentVariables.OrigFileName}"

def get_filename(years):
    yearText = pu.get_years_addition(years=years)
    return f"{EnvironmentVariables.Prefix}_{EnvironmentVariables.OrigFileName}_{yearText}"

def check_if_file_exists(filename):
    filename = pu.check_extension(filename, ext="csv")
    folder = pu.get_specific_path(EnvironmentVariables.FolderName)
    filepath = os.path.join(folder, filename)

    return os.path.exists(filepath)

def get_monthly_data_from_file(years):
    filename = get_monthly_filename(years=years)
    filename = pu.check_extension(filename, ext="csv")
    folder = pu.get_specific_path(EnvironmentVariables.FolderName)
    
    filepath = os.path.join(folder, filename)
    
    return pd.read_csv(filepath, delimiter=',', header=0)

def get_orig_data_from_file(years):
    filename = get_orig_filename(years=years)
    filename = pu.check_extension(filename, ext="csv")
    folder = pu.get_specific_path(EnvironmentVariables.FolderName)
    
    filepath = os.path.join(folder, filename)
    
    return pd.read_csv(filepath, delimiter=',', header=0)

def recalculate_data_set(years):
    logger.info("Read raw data", level=1)
    loader = DataLoader()
    logger.info("Read Originate and Monthly data", level=1)
    dfOrig, dfMonthly = loader.get_data_set(years=years)
    
    return dfOrig, dfMonthly


"""
EXAMPLE
"""
if __name__ == "__main__":
    ys = range(2013, 2021)
    for y in ys:
        years=[y]
        recalc = False

        dfOrig, dfMonthly = build_data_set(years=years, recalculate=recalc)
    
    dfOrig, dfMonthly = build_data_set(years=ys, recalculate=recalc)
    
    print(dfOrig)