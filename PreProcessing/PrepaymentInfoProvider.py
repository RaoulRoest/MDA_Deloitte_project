# Import modules
# General modules
import sys 
import os
# Adding path variables for custom modules.
preProcessing_dir = os.path.join(os.path.abspath(""), "PreProcessing")
general = os.path.join(os.path.dirname(os.path.abspath("")), "General")
sys.path.append(preProcessing_dir)
sys.path.append(general)

# Calculation modules.
import pandas as pd 
import numpy as np 

# Custom modules
from DataLoader import DataLoader
from DataCleaner import DataCleaner

# Helper modules
import ConsoleWriter as logger
import Helpers

"""
Functions for making a prepayment info
dataframe. 
"""
def get_orig_columns():
    """
    Columns to use from dfOrig
    """
    return [
        "dt_matr",
        "orig_upb",
        "ppmt_pnlty",
        "orig_loan_term",
    ]

def get_monthly_columns():
    """
    Columns to use from dfMonthly
    """
    return [
        "current_upb",
        "mths_remng",
        "flag_mod",
    ]
    
def initialize(dfOrig, dfMonthly):
    """
    Create new dataframe with columns from dfOrig and dfMonthly, 
    specified as: 
    dfOrig ::  
        - dt_matr,
        - orig_upb,
        - ppmt_pnlty,
        - orig_loan_term,
    
    dfMonthly :: 
        - current_upb,
        - mths_remng,
        - flag_mod,
    """
    dfInit = dfOrig[get_orig_columns()].merge(dfMonthly[get_monthly_columns()], 
                                                          how="inner", 
                                                          on="id_loan")
    return dfInit
    
def calculate_monthly_upb_percentages(upbs, orig_upbs):
    """
    Calculate :: 
    (shifted_current_upb - current_upb) / orig_upb
    """
    
    upbs_shifted = Helpers.shift_numpy_array(upbs, 1) # shift the array one position to the right
    upbs_shifted[np.isnan(upbs_shifted)] = 0 # set NaN's entries equal to zero
    
    # return calculation of
    # (shifted_current_upb - current_upb) / orig_upb
    return np.divide(upbs_shifted - upbs, orig_upbs, out=np.ones_like(upbs)) 
    
def calculate_monthly_upb_fullprepayment(dfOrig,dfMonthly):
    dfPPM=initialize(dfOrig, dfMonthly)
    columnName = "FlagFullPrepayment"
    condition1 = dfPPM["current_upb"] == 0 #If zero, full loan paid
    condition2 = dfPPM["mths_remng"] != 0 #If zero, contract ended
    dfPPM[columnName] = False
    dfPPM.loc[condition1&condition2, columnName] = True
    return dfPPM
    
    
def calculate_prepayment_info(dfOrig, dfMonthly):
    """
    Function to make a dataframe with specific prepayment 
    info. It uses columns:
    
    dfOrig ::  
        - dt_matr,
        - orig_upb,
        - ppmt_pnlty,
        - orig_loan_term,
    
    dfMonthly :: 
        - current_upb,
        - mths_remng,
        - flag_mod,

    and derives the column 'upb_perc' ::
    (shifted_current_upb - current_upb) / orig_upb
    """
    
    logger.info("Prepaymentprovider :: Initialize Prepayment info dataframe.", level=1)
    dfPPM = initialize(dfOrig, dfMonthly) #Get columns from dfs
    
    logger.info("Prepaymentprovider :: Calculate payment percentages of the original upb.", level=1)
    # Get the upb_perc
    dfPPM["upb_perc"] = calculate_monthly_upb_percentages(upbs=dfPPM["current_upb"].to_numpy(),
                                                          orig_upbs=dfPPM["orig_upb"].to_numpy())
    
    return dfPPM

def set_prepayment_flag(dfPPM, perc):
    """
    Sets a prepayment flag corresponding to a prepayment of 
    at least 'perc' percent. 
    Hence if (shifted_current_upb - current_upb) / orig_upb > perc => True
    """
    newColumnName = f"ppm_flag_{perc}"
    
    ppm = dfPPM.reset_index()[["id_loan", "upb_perc"]].to_numpy() # Get matrix of id_loan and upb_perc
    # Calculate which id's of the values of the second column (upb_perc) > perc (1)
    ppm_ids = ppm[ppm[:, 1] > perc][:, 0]  
    dfPPM[newColumnName] = False # pre allocate column with default False values 
    dfPPM.loc[ppm_ids, newColumnName] = True # Set values of id's from (1) equal to True
    
"""
=====================
Data retrieving function
=====================
Not part of the original 
code for calculating the prepayments. 
"""
def get_data(years):
    """
    
    """
    dl = DataLoader()
    dc = DataCleaner()
    
    dfOrig = dl.get_all_originate_years(years)
    dfMonthly = dl.get_all_monthly_performance_years(years)
    
    dfOrigClean, dfMonthlyClean = dc.clean_data(dfOrig, dfMonthly)
        
    # Set indexes for faster searches
    dfMonthlyClean.set_index(["id_loan", "svcg_cycle"], inplace=True) #Index on loan index, and timestep. 
    dfOrigClean.set_index("id_loan", inplace=True) #Index on loan index
        
    return dfOrigClean, dfMonthlyClean


"""
=====================
Test Outcomes with simple
visualizing script
=====================
Output will be printed in the console,
here one can check if the functions 
work. 
"""

logger.info("Retrieve data")
dfOrig, dfMonthly = get_data([2013])

logger.info("Calculate Prepayment")
dfPPM = calculate_prepayment_info(dfOrig, dfMonthly)

logger.info("Set Prepayment flag")
set_prepayment_flag(dfPPM, 0.1)

print(dfPPM[dfPPM["ppm_flag_0.1"] == True])