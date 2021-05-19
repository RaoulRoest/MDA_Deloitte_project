import os

import pandas as pd
import numpy as np

import PathUtilities as pu

import PathUtilities as pu
import ConsoleWriter as logger

def get_specific_filepath(specific, filename):
    if specific is not None:
        path = pu.get_specific_path(specific)
        filePath = os.path.join(path, filename)
    
        return filePath
    
    else:
        return filename

def write_to_csv(df, filename, specific=None, sep=','):
    filePath = get_specific_filepath(specific=specific, filename=filename)
    filePath = pu.check_extension(filePath=filePath, ext="csv")
    
    logger.info(f"Write file to {filePath}.", level=1)
    df.to_csv(filePath, sep=sep)

def write_numpy_to_csv(arr, filePath, specific=None, sep=','):
    filePath = get_specific_filepath(specific=specific, filename=filePath)
    pu.check_extension(filePath=filePath, ext="csv")
    
    logger.info(f"Write file to {filePath}.", level=1)
    np.savetxt(filePath, arr, delimiter=sep, fmt='%s')