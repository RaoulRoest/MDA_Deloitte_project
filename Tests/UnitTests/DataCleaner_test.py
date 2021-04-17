import sys 
import os 
cleanerPath = os.path.join(os.path.dirname(__file__), "..", "..", "PreProcessing")
sys.path.append(cleanerPath)

from DataCleaner import DataCleaner 

from DataLoader import DataLoader

dl = DataLoader()
dc = DataCleaner()

dfOrig = dl.load_origination_data_file(2020)
dfMonthly = dl.load_monthly_performance_data_file(2020)

dfMonthlyClean, dfOrigClean = dc.clean_data(dfOrig, dfMonthly)

all_years = range(2013, 2021)
print([y for y in all_years])