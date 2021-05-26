import os
import pandas as pd

import PathUtilities as pu
import ConsoleWriter as logger

def get_dir():
    path = os.path.join(os.path.dirname(__file__), "..", "Data")
    pu.make_directory_if_not_exists(path)
    return path

def get_specific_path(pathName):
    path = os.path.join(get_dir(), pathName)
    pu.make_directory_if_not_exists(path)
    return path

def write_to_csv(df, filename, specific, sep=','):
    path = get_specific_path(specific)
    filePath = os.path.join(path, filename)
    filePath = pu.check_extension(filePath=filePath, ext="csv")
    
    logger.info(f"Write file to {filePath}.", level=1)
    df.to_csv(filePath, sep=sep)
    