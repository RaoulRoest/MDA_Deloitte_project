"""
====================
Description
====================

"""
# General modules
import sys 
import os

# Adding path variables for custom modules.
preProcessing_dir = os.path.join(os.path.abspath(""), "PreProcessing")
general = os.path.join(os.path.abspath(""), "General")
sys.path.append(preProcessing_dir)
sys.path.append(general)

# Calculation modules.
import pandas as pd 
import numpy as np 

# Custom modules
from DataLoader import DataLoader

# Helper modules
import ConsoleWriter as logger
import Helpers

"""
Constants for column names
"""
class ColumnNames():
     PaymentName = "payments"
     ShiftedPaymentsName = "shifted_payments"
     FlagName = "prepayment_flag"
     PrepaymentTypeName = "prepayment_type"
     ScheduledPaymentsName = "scheduled_payments"
     PreviousPaymentFlag = "previous_payment_flag"

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
        "delq_sts",
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
        - delq_sts

    """
    dfInit = dfOrig[get_orig_columns()].merge(dfMonthly[get_monthly_columns()], 
                                                          how="inner", 
                                                          on="id_loan")
    return dfInit

def calculate_shifted_ubps(upb):
    return Helpers.shift_numpy_array(upb, 1, fill_value=0)

def calculate_prepayment_info(dfOrig, dfMonthly):    
    logger.info("Prepaymentprovider :: Initialize Prepayment info dataframe.", level=1)
    dfPPM = initialize(dfOrig, dfMonthly) #Get columns from dfs
    
    # Calculate payments
    upb = dfPPM["current_upb"].to_numpy()
    shiftedUpb = calculate_shifted_ubps(upb)
    payments = shiftedUpb - upb
    dfPPM[ColumnNames.PaymentName] = payments
    dfPPM[ColumnNames.ShiftedPaymentsName] = Helpers.shift_numpy_array(payments, 1, fill_value=0) 
    
    # Calculate scheduled payments
    dfPPM[ColumnNames.ScheduledPaymentsName] = dfPPM["orig_upb"].to_numpy() / dfPPM["orig_loan_term"].to_numpy()
    
    # Flag if previous payment is zero
    dfPPM[ColumnNames.PreviousPaymentFlag] = shiftedUpb == 0
    
    # Set prepayment flag
    set_prepayment_flag(dfPPM, shiftedUpb)
    classify_prepayments(dfPPM)
    
    return dfPPM

def set_prepayment_flag(dfPPM, shiftedUpb):
    condition_1 = shiftedUpb > 0
    condition_2 = dfPPM[ColumnNames.PaymentName] > 0
    condition_3 = (dfPPM[ColumnNames.PaymentName].to_numpy() - dfPPM[ColumnNames.ScheduledPaymentsName].to_numpy()) > 0
    condition_4 = dfPPM["mths_remng"] > 0
    condition_5 = dfPPM["delq_sts"] == "0"
    condition_6 = (dfPPM[ColumnNames.ShiftedPaymentsName] > 0) |\
        (dfPPM[ColumnNames.PaymentName] > 2 * dfPPM[ColumnNames.ScheduledPaymentsName])
    
    dfPPM[ColumnNames.FlagName] = condition_1 & condition_2 & condition_3 & condition_4 & condition_5 &\
        condition_6

def classify_prepayments(dfPPM):
    condition_ppm = dfPPM[ColumnNames.FlagName] == True
    condition_full_ppm = dfPPM["current_upb"] == 0
    condition_partial_ppm = dfPPM["current_upb"] != 0
    
    # Initialize
    dfPPM[ColumnNames.PrepaymentTypeName] = "No Prepayment"
    dfPPM.loc[condition_ppm & condition_full_ppm, ColumnNames.PrepaymentTypeName] = "FullPrepayment"
    dfPPM.loc[condition_ppm & condition_partial_ppm, ColumnNames.PrepaymentTypeName] = "PartialPrepayment"
    
"""
=====================
Test Outcomes with simple
visualizing script
=====================
Output will be printed in the console,
here one can check if the functions 
work. 
"""

if __name__ == "__main__":
    logger.info("Retrieve data")
    loader = DataLoader()
    dfOrig, dfMonthly = loader.get_data_set([2013])
    
    logger.info("Calculate Prepayment")
    dfPPM = calculate_prepayment_info(dfOrig, dfMonthly)
    
    print(dfPPM[dfPPM[ColumnNames.FlagName] == True])