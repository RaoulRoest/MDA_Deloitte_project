import os
import numpy as np 
import pandas as pd

# Custom modules
import DataInformation as datInfo 
import DataCleaner as cleaner

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
        
        self._origHeaderDictName = "OriginateHeaderMapping.xlsx"
        self._monthlyHeaderDictName = "MonthlyHeaderMapping.xlsx"
                
    def get_data_directory(self):
        curDir = os.path.dirname(__file__)
        
        return os.path.join(curDir, "..", "Data")
    
    def _get_header_dict(self, file="Orig"):
        if(file == "Orig"):
            if(not hasattr(self, '_origHeaderDict')):
                headerFilePath = os.path.join(self._dataDir, self._origHeaderDictName)
                self._origHeaderDict = datInfo.get_data_dict(headerFilePath)
            
            return self._origHeaderDict
        
        elif(file == "Monthly"):
            if(not hasattr(self, '_monthlyHeaderDict')):
                headerFilePath = os.path.join(self._dataDir, self._monthlyHeaderDictName)
                self._monthlyHeaderDict = datInfo.get_data_dict(headerFilePath)
            
            return self._monthlyHeaderDict            
    
    def load_origination_data_file(self, year):
        filepath = os.path.join(self._dataDir, f"sample_orig_{year}.txt")
        
        typeDict = self._get_header_dict(file="Orig")
        headers = [k for k, v in typeDict.items()]
        
        df = self._load_general_data_file_as_df(filepath=filepath, headers=headers, dtypes=typeDict)
            
        return df
    
    def load_monthly_performance_data_file(self, year):
        filepath = os.path.join(self._dataDir, f"sample_svcg_{year}.txt")

        typeDict = self._get_header_dict(file="Monthly")
        headers = [k for k, v in typeDict.items()]
        
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
                df = df.append(dfProviderFunction(year), ignore_index=True)

            indexer += 1
            
        return df
    
    def get_all_originate_years(self, years):
        return self._get_multiple_files(years, self.load_origination_data_file)
    
    def get_all_monthly_performance_years(self, years):    
        return self._get_multiple_files(years, self.load_monthly_performance_data_file)

    def get_fifteen_years_mortgage_rate(self):
        filepath = os.path.join(self._dataDir, "MORTGAGE15US_adjusted.xlsx")
        return pd.read_excel(filepath).set_index("observation_date")
    
    def get_data_set(self, years):
        """
        Function that provides the cleaned data set. 
        Moreover, indices on the dataframes are set to: 
        Originate data: 
            - id_loan
        Monthly data:
            - id_loan
            - svcg_cycle
        """
        dfOrig = self.get_all_originate_years(years)
        dfMonthly = self.get_all_monthly_performance_years(years)
        
        dfOrigClean, dfMonthlyClean = cleaner.clean_data(dfOrig, dfMonthly)
        
        # Set indexes for faster searches
        dfMonthlyClean.set_index(["id_loan", "svcg_cycle"], inplace=True) #Index on loan index, and timestep. 
        dfOrigClean.set_index("id_loan", inplace=True) #Index on loan index
            
        return dfOrigClean, dfMonthlyClean        