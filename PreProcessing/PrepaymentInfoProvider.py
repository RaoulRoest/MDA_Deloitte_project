import sys 
import os
preProcessing_dir = os.path.join(os.path.abspath(""), "PreProcessing")
general = os.path.join(os.path.abspath(""), "General")
sys.path.append(preProcessing_dir)
sys.path.append(general)

import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 

# Custom modules
from DataLoader import DataLoader
from DataCleaner import DataCleaner

import ConsoleWriter as logger

def get_data(years):
    # years = range(2013, 2021) #Python uses 0-indexing, hence this will be [2013, 2020, steps=1]
    
    dl = DataLoader()
    dc = DataCleaner()
    
    dfOrig = dl.get_all_originate_years(years)
    dfMonthly = dl.get_all_monthly_performance_years(years)
    
    dfOrigClean, dfMonthlyClean = dc.clean_data(dfOrig, dfMonthly)
    
    # dfMonthlyClean.dropna(axis='columns', inplace=True) #Drop the columns with na values. 
    
    # Set indexes for faster searches
    dfMonthlyClean.set_index(["id_loan", "svcg_cycle"], inplace=True) #Index on loan index, and timestep. 
    dfOrigClean.set_index("id_loan", inplace=True) #Index on loan index
        
    return dfOrigClean, dfMonthlyClean


import os
import sys
curDir = os.path.dirname(__file__)
general = os.path.join(curDir, "..", "General")
sys.path.append(general)

import pandas as pd 
import numpy as np 

# Custom modules
import Helpers

class PrepaymentInfoProvider():
    
    def __init__(self):
        self._columns_of_interest_orig = [
            "dt_matr",
            "orig_upb",
            "ppmt_pnlty",
            "orig_loan_term",
        ]
        
        self._columns_of_interest_monthly = [
            "current_upb",
            "mths_remng",
            "flag_mod",
        ]
    
    def _initialize(self, dfOrig, dfMonthly):
        dfInit = dfOrig[self._columns_of_interest_orig].merge(dfMonthly[self._columns_of_interest_monthly], 
                                                              how="inner", 
                                                              on="id_loan")
        return dfInit
    
    def _calculate_monthly_upb_percentages(self, upbs):
        upbs_shifted = Helpers.shift_numpy_array(upbs, 1)
        upbs_shifted[np.isnan(upbs_shifted)] = 0
        return np.divide(upbs_shifted - upbs, upbs, out=np.ones_like(upbs), where=upbs!=0)
    
    def calculate_prepayment_info(self, dfOrig, dfMonthly):
        dfPPM = self._initialize(dfOrig, dfMonthly)
        dfPPM["upb_perc"] = self._calculate_monthly_upb_percentages(dfPPM["current_upb"].to_numpy())
        
        return dfPPM

    def set_prepayment_flag(self, dfPPM, perc):
        """
        Sets a prepayment flag corresponding to a prepayment of 
        at least 'perc' percent. 
        """
        newColumnName = f"ppm_flag_{perc}"
        
        ppm = dfPPM.reset_index()[["id_loan", "upb_perc"]].to_numpy()
        ppm_ids = ppm[ppm[:, 1] > perc][:, 0]
        dfPPM[newColumnName] = False
        dfPPM.loc[ppm_ids, newColumnName] = True
    



ppm = PrepaymentInfoProvider()

dfOrig, dfMonthly = get_data([2013])
dfPPM = ppm.calculate_prepayment_info(dfOrig, dfMonthly)
ppm.set_prepayment_flag(dfPPM, 0.1)

print(dfPPM[dfPPM["ppm_flag_0.1"] == True])