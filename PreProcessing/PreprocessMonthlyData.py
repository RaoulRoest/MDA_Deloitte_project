# General modules
import sys 
import os
from enum import Enum

# Adding path variables for custom modules.
general = os.path.join(os.path.dirname(__file__), "..", "General")
sys.path.append(general)

import pandas as pd
import numpy as np

# Custom modules
from DataLoader import DataLoader
import DataSetBuilder as dataBuilder
import PrepaymentInfoProvider as ppm

# Helper modules
import ConsoleWriter as logger
import CsvWriter as csv
import Helpers

class Aggregations(Enum):
    Sum = 1
    


class InputVariables():
    def get_columns_to_preprocess_conditions(df):
        return [
            # (condition, aggregation, flagName)
            (df["defered_payment_plan"] == "Y", Aggregations.Sum, "defered_payment_plan_flag"),
            (df["prepayment_type"] == 2, Aggregations.Sum, "partial_prepayment_flag"),
            (df["current_upb"] == 200000, Aggregations.Sum, "cur_upb_greater_than_200000_flag"),
            (df["eltv"] > 140, Aggregations.Sum, "eltv_greater_than_140_flag"),  
            (df["repch_flag"] == "Y", Aggregations.Sum, "repch_flag"),
            (df["zeroPaymentFlag"] == False, Aggregations.Sum, "zeroPaymentFlag_count"),
        ]
    
    TimeStepColumn = "t"

def set_time_steps(dfMonthly):
    return dfMonthly.groupby('id_loan').cumcount()

def preprocess_monthly_data(dfMonthly, current_time_step=None):
    
    
    # Create time steps, if needed
    if current_time_step is not None:
        dfMonthly[InputVariables.TimeStepColumn] = set_time_steps(dfMonthly=dfMonthly)
    
    for condition, _, flagName in InputVariables.get_columns_to_preprocess_conditions(dfMonthly):
        
        # Add time constraint
        if current_time_step is not None:
            condition = condition & (dfMonthly[InputVariables.TimeStepColumn] <= current_time_step)
        
        # Initialize flags in monthly data
        dfMonthly[flagName] = 0
        
        # Set flag based on condition
        dfMonthly.loc[condition, flagName] = 1
                
    return dfMonthly

def add_monthly_data_to_orig_data(dfMonthly, dfOrig):
    
    for _, agg, flagName in InputVariables.get_columns_to_preprocess_conditions(dfMonthly):

        # Aggregate over the aggregation level
        if(agg == Aggregations.Sum):
            dfAgg = dfMonthly[flagName].groupby("id_loan", observed=True).sum()
        
        
        # Merge the found data to the Originate data
        dfOrig = dfOrig.merge(dfAgg, how="left", on="id_loan")
    
    return dfOrig

if __name__ == "__main__":
    years = [2013]
    dl = DataLoader()
    dfOrigOld, dfMonthly = dl.get_data_set(years=years)
    dfOrig = dataBuilder.build_data_set(years=years)
    dfPPM = ppm.calculate_prepayment_info(dfOrig=dfOrigOld, dfMonthly=dfMonthly)
    
    dfMonthly = dfMonthly.reset_index().merge(dfPPM[["id_loan", "svcg_cycle", "prepayment_type","zeroPaymentFlag"]], 
                                how="left", 
                                on=["id_loan", "svcg_cycle"]).set_index(["id_loan", "svcg_cycle"])
    dfMonthly = preprocess_monthly_data(dfMonthly=dfMonthly, current_time_step=100)
    dfOrig = add_monthly_data_to_orig_data(dfMonthly=dfMonthly, dfOrig=dfOrig)
    
    csv.write_to_csv(dfOrig, "TestFile_preprocessedMonthlyData.csv", "Tests")