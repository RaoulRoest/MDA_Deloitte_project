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
    return read_csv_file_one_column_to_list(yearsFile)