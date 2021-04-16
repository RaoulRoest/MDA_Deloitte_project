import sys 
import os 
preProcessing_dir = os.path.join(os.path.dirname(__file__), "..", "..", "PreProcessing")
sys.path.append(preProcessing_dir)

import pytest

# Custom class 
from DataLoader import DataLoader

def test_alternative_dir():
    # Init
    altDir = "someDir" 
    sut = DataLoader(altDir)
    
    # Assert
    assert sut._dataDir == altDir 

def test_get_data_directory_should_return_data_directory():
    # Init
    sut = DataLoader()     
    
    # Act
    data_dir = sut.get_data_directory()
    
    # Assert
    file_number = len(os.listdir(data_dir))
    assert file_number > 0

def test_load_origination_data_file_should_return_df_for_correct_year():
    # Init
    year = 2013
    sut = DataLoader()
    
    # Act
    df = sut.load_origination_data_file(year) 
    
    # assert
    assert len(df.columns) > 0

def test_load_origination_data_file_should_raise_for_wrong_year():
    # Init
    year = 10
    sut = DataLoader()
    
    # Act
    with pytest.raises(Exception):
        sut.load_origination_data_file(year) 

def test_load_monthly_performance_data_file_should_return_df_for_correct_year():
    # Init
    year = 2020
    sut = DataLoader()
    
    # Act
    df = sut.load_monthly_performance_data_file(year) 
    
    # assert
    assert len(df.columns) > 0

def test_get_all_originate_years_should_return_for_multiple_years():
    # Init
    years = [2013, 2014]
    sut = DataLoader()
    
    # Act
    df = sut.get_all_originate_years(years) 
    
    # assert
    assert len(df.columns) > 0