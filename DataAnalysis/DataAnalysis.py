import sys 
import os
preProcessing_dir = os.path.join(os.path.dirname(__file__), "..", "PreProcessing")
sys.path.append(preProcessing_dir)

from DataLoader import DataLoader
from DataCleaner import DataCleaner

import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 

def get_data():
    years = range(2013, 2021) #Python uses 0-indexing, hence this will be [2013, 2020, steps=1]
    
    dl = DataLoader()
    dc = DataCleaner()
    
    dfOrig = dl.get_all_originate_years(years)
    dfMonthly = dl.get_all_monthly_performance_years(years)
    
    dfOrigClean, dfMonthlyClean = dc.clean_data(dfOrig, dfMonthly)
    
    return dfOrigClean, dfMonthlyClean

def main():
    dfOrig, dfMonthly = get_data()
    print(dfOrig.iloc[0])
    print(dfMonthly.iloc[0])
    
main()