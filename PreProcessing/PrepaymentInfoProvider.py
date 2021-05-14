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

# Custom modules
from DataLoader import DataLoader

# Helper modules
import ConsoleWriter as logger
import CsvWriter as csv
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
     AdjustedScheduledPaymentScheme = "adj_sched_paym"
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
        'int_rt',
        ColumnNames.ScheduledPaymentsName,
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
        - int_rt,
    
    dfMonthly :: 
        - current_upb,
        - mths_remng,
        - flag_mod,
        - delq_sts

    """
    # Calculate scheduled payments (over orig as this data contains all it needs)
    dfOrig[ColumnNames.ScheduledPaymentsName] = dfOrig.apply(lambda row: calculate_monthly_payments_df(row), axis=1)
    dfInit = dfOrig[get_orig_columns()].merge(dfMonthly[get_monthly_columns()], 
                                                          how="inner", 
                                                          on="id_loan")
    return dfInit.reset_index()

def calculate_shifted_ubps(upb):
    return Helpers.shift_numpy_array(upb, 1, fill_value=0)

def calculate_monthly_factor(interest, loan_term):
    factor = 1 - interest**(loan_term + 1)
    factor = factor / (1 -interest)
    return factor - 1

def calculate_monthly_payments(monthly_factor, loan):
    return loan / monthly_factor

def calculate_monthly_payments_df(row):
    interest = (1 + row['int_rt'] / 100)**(1/12)
    loan_term = row['orig_loan_term']
    factor = calculate_monthly_factor(interest=interest, loan_term=loan_term)
    
    loan = row['orig_upb']
    return calculate_monthly_payments(monthly_factor=factor, loan=loan)
    
def calculate_prepayment_info(dfOrig, dfMonthly, threshold_percentage=0.1):
    """
    threshold_percentage gives the threshold how far a payment may vary from 
    the scheduled payments to be a prepayment. 
    """    
    logger.info("Prepaymentprovider :: Initialize Prepayment info dataframe.", level=1)
    dfPPM = initialize(dfOrig, dfMonthly) #Get columns from dfs
    
    # Calculate payments
    upb = dfPPM["current_upb"].to_numpy()
    shiftedUpb = calculate_shifted_ubps(upb)
    payments = shiftedUpb - upb
    dfPPM[ColumnNames.PaymentName] = payments
    dfPPM[ColumnNames.ShiftedPaymentsName] = Helpers.shift_numpy_array(payments, 1, fill_value=0)
        
    # Calculate adjusted scheme
    dfPPM[ColumnNames.AdjustedScheduledPaymentScheme] = (1 + threshold_percentage) * dfPPM[ColumnNames.ScheduledPaymentsName]
    
    # Flag if previous payment is zero
    dfPPM[ColumnNames.PreviousPaymentFlag] = shiftedUpb == 0
    
    # Set prepayment flag
    set_prepayment_flag(dfPPM, shiftedUpb)
    classify_prepayments(dfPPM)
    
    return dfPPM

def set_prepayment_flag(dfPPM, shiftedUpb):
    condition_1 = shiftedUpb > 0
    condition_2 = dfPPM[ColumnNames.PaymentName] > 0
    condition_3 = (dfPPM[ColumnNames.PaymentName].to_numpy() - dfPPM[ColumnNames.AdjustedScheduledPaymentScheme].to_numpy()) > 0
    condition_4 = dfPPM["mths_remng"] > 0
    condition_5 = dfPPM["delq_sts"] == "0"
    condition_6 = (dfPPM[ColumnNames.ShiftedPaymentsName] > 0) |\
        (dfPPM[ColumnNames.PaymentName] > 2 * dfPPM[ColumnNames.ScheduledPaymentsName])
    
    # Only on same loan_id's
    shiftedLoans = Helpers.shift_numpy_array(dfPPM["id_loan"].to_numpy(), 1, "Empty")
    condition_7 = dfPPM["id_loan"] == shiftedLoans
    
    dfPPM[ColumnNames.FlagName] = condition_1 & condition_2 & condition_3 & condition_4 & condition_5 &\
        condition_6 & condition_7

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
    
    csv.write_to_csv(dfPPM, "TestFile", "Tests")
