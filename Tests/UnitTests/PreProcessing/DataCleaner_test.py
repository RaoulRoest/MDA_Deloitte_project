import sys 
import os 
cleanerPath = os.path.join(os.path.dirname(__file__), "..", "..", "..", "PreProcessing")
sys.path.append(cleanerPath)

import pytest
import pandas as pd 
import numpy as np

# Custom class
from DataCleaner import DataCleaner
import DataInformation as di 

def assert_items_in_list(l1, l2):
    assert set(l1) == set(l2)

def test_DataCleaner_should_remove_unclean_data():
    # Initialize
    dfOrig,  dfMonthly = get_test_data()
    sut = DataCleaner()
    
    expected_loans = ["F113Q1000314"]
        
    # Act
    resultOrig, resultMonthly = sut.clean_data(dfOrig, dfMonthly)
    
    # Assert
    resultOrig_loans = resultOrig.id_loan.unique().tolist()
    resultMonthly_loans = resultMonthly.id_loan.unique().tolist()
    
    assert_items_in_list(resultMonthly_loans, expected_loans)
    assert_items_in_list(resultOrig_loans, expected_loans)
    
def get_test_data():
    curDir = os.path.dirname(__file__)
    origFilePath = os.path.join(curDir, "..", "..", "TestData", "OrigTestFile.xlsx")
    monthlyFilePath = os.path.join(curDir, "..", "..", "TestData", "MonthlyTestFile.xlsx")

    headersOrig = di.get_origination_data_headers()
    dtypesOrig = di.get_orig_dtypes()
    typeDictOrig = {k : v for k, v in zip(headersOrig, dtypesOrig)}
        
    headersMonthly = di.get_monthly_performance_headers()
    dtypesMonthly = di.get_monthly_dtypes()
    typeDictMonthly = {k : v for k,v in zip(headersMonthly, dtypesMonthly)}

    dfOrig = pd.read_excel(origFilePath, sheet_name="test", dtype=typeDictOrig)
    dfMonthly = pd.read_excel(monthlyFilePath, sheet_name="test", dtype=typeDictMonthly)
    
    return dfOrig, dfMonthly