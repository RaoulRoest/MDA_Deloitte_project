import sys 
import os 
cleanerPath = os.path.join(os.path.dirname(__file__), "..", "..", "PreProcessing")
sys.path.append(cleanerPath)

from DataCleaner import DataCleaner 

from DataLoader import DataLoader

dl = DataLoader()
dc = DataCleaner()

dfOriginate = dl.load_origination_data_file(2020)
print(dfOriginate.iloc[2])

ids = dc.get_ids_to_remove(dfOriginate)

print(ids)
# dfMonthly = dl.load_monthly_performance_data_file(2020)
# print(dfMonthly.iloc[0])