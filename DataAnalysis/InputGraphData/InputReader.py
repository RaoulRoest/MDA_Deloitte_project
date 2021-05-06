import os 
import sys
general = os.path.join(os.path.dirname(__file__), "..", "..", "General")
sys.path.append(general)

import csv 

# Custom modules
import PathUtilities as pu 

# Parameters
delimiter = ','

# General file names
yearsFile = "InputGraph_Years"
origFile = "InputGraph_OrigFeatures"
monthlyFile = "InputGraph_MonthlyFeatures"
origScatterFile = "InputGraph_OrigScatter"
loansFile = "InputGraph_Loans"

def get_filepath(filename):
    return os.path.join(os.path.dirname(__file__), filename)

# Functions
def read_csv_file_one_column_to_list(filename):
    filename = pu.check_extension(filename, "csv")
    with open(filename, newline="") as f:
        reader = csv.reader(f, delimiter=delimiter)
        data = [row[0] for row in reader]
    
    return data
        
def read_csv_file_multiple_column_to_list_of_tuples(filename):
    filename = pu.check_extension(filename, "csv")
    with open(filename, newline="") as f:
        reader = csv.reader(f, delimiter=delimiter)
        data = [tuple(row) for row in reader]
    
    return data

def read_years():
    return read_csv_file_one_column_to_list(get_filepath(yearsFile))

def read_orig_features():
    return read_csv_file_one_column_to_list(get_filepath(origFile))

def read_monthly_features():
    return read_csv_file_one_column_to_list(get_filepath(monthlyFile))

def read_orig_scatter_features():
    return read_csv_file_multiple_column_to_list_of_tuples(get_filepath(origScatterFile))

def read_loans():
    return read_csv_file_one_column_to_list(get_filepath(loansFile))