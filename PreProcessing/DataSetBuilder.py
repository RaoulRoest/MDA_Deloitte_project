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
    FolderName = "AdjustedDataSet"
    Prefix = "Adjusted"
    OrigFileName = "OrigData"

def build_data_set(years, recalculate=False, timeStep=None, dfPPM=None):
    """
    Reads data file if it is available, otherwise it
    reads the corresponding info from file. 
    If recalculate == True, then the info is always recalculated. 
    """
    filename = get_filename(years=years)
    filename = pu.check_extension(filename, ext="csv")

    if(recalculate):
        logger.info("Recalculating adjusted data files")
        dfOrig = recalculate_data_set(years, timeStep=timeStep, dfPPM=dfPPM).reset_index()
        csv.write_to_csv(dfOrig, filename=filename, specific=EnvironmentVariables.FolderName, sep=',')                
    
    else:
        if check_if_file_exists(filename=filename):
            logger.info("Reading adjusted data files")
            dfOrig = get_data_from_file(years=years)
        else:
            logger.warning(f"File {filename} was nog found, recalculating adjusted data files.")
            dfOrig = recalculate_data_set(years, timeStep=timeStep, dfPPM=dfPPM).reset_index()
            csv.write_to_csv(dfOrig, filename=filename, specific=EnvironmentVariables.FolderName, sep=',')                
    
    return dfOrig

def get_filename(years):
    yearText = pu.get_years_addition(years=years)
    return f"{EnvironmentVariables.Prefix}_{EnvironmentVariables.OrigFileName}_{yearText}"

def check_if_file_exists(filename):
    filename = pu.check_extension(filename, ext="csv")
    folder = pu.get_specific_path(EnvironmentVariables.FolderName)
    filepath = os.path.join(folder, filename)

    return os.path.exists(filepath)

def get_data_from_file(years):
    filename = get_filename(years=years)
    filename = pu.check_extension(filename, ext="csv")
    folder = pu.get_specific_path(EnvironmentVariables.FolderName)
    
    filepath = os.path.join(folder, filename)
    
    if check_if_file_exists(filepath):
        return pd.read_csv(filepath, delimiter=',', header=0)

def recalculate_data_set(years, timeStep=None, dfPPM=None):
    logger.info("Read raw data", level=1)
    loader = DataLoader()
    logger.info("Read Originate and Monthly data", level=1)
    dfOrig, dfMonthly = loader.get_data_set(years=years)
    
    if dfPPM is None:
        logger.info("Retrieve prepayment info", level=1)
        dfPPM = ppm.calculate_prepayment_info(dfOrig=dfOrig, dfMonthly=dfMonthly)
    
    logger.info("Combine data sets", level=1)
    dfOrig = prepare_orig_data(dfOrig=dfOrig)
    dfOrig = add_prepayment_info(dfOrig=dfOrig, dfPPM=dfPPM, timeStep=timeStep)
    
    return dfOrig

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
    _, nonNumerics = Helpers.check_dtypes(dfOrig, dfOrig.columns)
    
    for column in nonNumerics:
        if not (column in exclude):
            dfOrig = add_numeric_dummies(dfOrig, column=column)
    
    return dfOrig

def add_prepayment_info(dfOrig, dfPPM, timeStep=None):
    columns_to_merge = [
        "prepayment_time_step",
        # "prepayment_type_FullPrepayment",
        # "prepayment_type_No Prepayment",
        # "prepayment_type_PartialPrepayment",
        # "prepayment_flag_False",
        # "prepayment_flag_True",
        "prepayment_flag",
        "prepayment_type",
    ]
    
    if timeStep is not None:
        timeStepColumns = [
            f"prepayment_before_timestep_{timeStep}",
            f"prepayment_type_before_timestep_{timeStep}",
            f"prepayment_type_after_timestep_{timeStep}",
        ]
        columns_to_merge = columns_to_merge + timeStepColumns
    
    dfToMerge = prepare_ppm(dfPPM=dfPPM, timeStep=timeStep)
    dfOrig = dfOrig.merge(dfToMerge[columns_to_merge], on="id_loan")

    return dfOrig
    
def prepare_ppm(dfPPM, timeStep=None):
    """
    Add dummy columns for: 
        - prepayment_type
        - prepayment_flag
        
    Get time value for prepayment flag
    """
    dfPPM["prepayment_time_step"] = 0
    dfPPM.loc[dfPPM["prepayment_flag"] == True, "prepayment_time_step"] = dfPPM.loc[dfPPM["prepayment_flag"] == True, "time"]    

    ppm_map = {"No Prepayment" : 0, "PartialPrepayment" : 1, "FullPrepayment" : 2}
    dfPPM["prepayment_type"] = dfPPM["prepayment_type"].map(ppm_map)
    
    if timeStep is not None:
        dfPPM[f"prepayment_before_timestep_{timeStep}"] = (dfPPM["prepayment_flag"] == True) & (dfPPM["time"] <= timeStep)
        dfPPM[f"prepayment_type_before_timestep_{timeStep}"] = dfPPM[f"prepayment_before_timestep_{timeStep}"] * dfPPM["prepayment_type"]
        dfPPM[f"prepayment_type_after_timestep_{timeStep}"] = (1 - dfPPM[f"prepayment_before_timestep_{timeStep}"]) * dfPPM["prepayment_type"]
    
        
    return dfPPM.groupby("id_loan").max()

def add_numeric_dummies(df, column):
    return pd.concat([df.drop(column, axis=1), pd.get_dummies(df[column], prefix=column)], axis=1)

"""
EXAMPLE
"""
if __name__ == "__main__":
    ys = range(2013, 2021)
    for y in ys:
        years=[y]
        recalc = True
        
        dfOrig = build_data_set(years=years, recalculate=recalc)
        
    dfOrig = build_data_set(years=ys, recalculate=True)
