import os
import numpy as np 
import pandas as pd

# Custom modules
import DataInformation as datInfo 

class DataLoader():
    """
    DataLoader class for importing the data in the Deloitte project. 
    Note that by default the data directory is given by: 
    
    \\Data
    
    Otherwise, an alternative directory for the data can be given 
    by wrkdir.
    """ 
    
    def __init__(self, wrkdir=None):
        if(wrkdir is None):
            self._dataDir = self.get_data_directory()
        else:
            self._dataDir = wrkdir
        
    def get_data_directory(self):
        curDir = os.path.dirname(__file__)
        
        return os.path.join(curDir, "..", "Data")
    
    def load_origination_data_file(self, year):
        filepath = os.path.join(self._dataDir, f"sample_orig_{year}.txt")
        headers = datInfo.get_origination_data_headers()
        dtypes = datInfo.get_orig_dtypes()
        typeDict = {k : v for k, v in zip(headers, dtypes)}
        
        df = self._load_general_data_file_as_df(filepath=filepath, headers=headers, dtypes=typeDict)
            
        return df
    
    def load_monthly_performance_data_file(self, year):
        filepath = os.path.join(self._dataDir, f"sample_svcg_{year}.txt")
        headers = datInfo.get_monthly_performance_headers()
        dtypes = datInfo.get_monthly_dtypes()
        typeDict = {k : v for k, v in zip(headers, dtypes)}
        
        df = self._load_general_data_file_as_df(filepath=filepath, headers=headers, dtypes=typeDict)

        return df
    
    def _load_general_data_file_as_df(self, filepath, headers, dtypes):        
        if(os.path.exists(filepath)):
            df = pd.read_csv(filepath, sep="|", header=None, names=headers, dtype=dtypes)
            
            return df
        else:
            raise Exception(f"The file {filepath} does not exist.") 
    
    def _get_multiple_files(self, years, dfProviderFunction):
        indexer = 0 
        for year in years:
            if(indexer == 0):
                df = dfProviderFunction(year)
            
            else:
                df.append(dfProviderFunction(year))

            indexer += 1
            
        return df
    
    def get_all_originate_years(self, years):
        return self._get_multiple_files(years, self.load_origination_data_file)
    
    def get_all_monthly_performance_years(self, years):    
        return self._get_multiple_files(years, self.load_monthly_performance_data_file)
