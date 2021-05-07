import numpy as np
import pandas as pd

from pydoc import locate

def get_header_info_type_dict():
    return {
        "Header" : str,
        "FullName" : str,
        "dType" : type, 
        "ColumnPosition" : int
    }    

def get_data_dict(filePath):
    # Read dict from xlsx file
    headerDict = get_header_info_type_dict()
    df = pd.read_excel(filePath, dtype=headerDict)
    
    # Strip whitespaces from strings
    df["Header"] = df["Header"].str.strip()
    df["FullName"] = df["FullName"].str.strip()
    df["dType"] = df["dType"].str.strip()
    
    # Set index for mapping
    df.set_index("Header", inplace=True)
    
    # Get correct class corresponding to type (with locate function)
    dtypeDict = df["dType"].to_dict()
    dtypeDict = {k : locate(v) for k, v in dtypeDict.items()} 
    
    return dtypeDict
    