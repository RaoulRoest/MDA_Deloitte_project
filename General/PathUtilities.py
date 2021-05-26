import os 

def make_directory_if_not_exists(dirpath):
    if(not os.path.exists(dirpath)):
        os.makedirs(dirpath)
        
def check_extension(filePath, ext):
    if(filePath.endswith(f".{ext}")):
        return filePath
    else:
        return f"{filePath}.{ext}"
    
def get_data_dir():
    curDir = os.path.dirname(__file__) 
    return os.path.join(curDir, "..", "Data")

def get_specific_path(pathName):
    """
    Returns specific path based on the data folder
    """
    path = os.path.join(get_data_dir(), pathName)
    make_directory_if_not_exists(path)
    
    return path

def get_years_addition(years):
    if(len(years) > 1):
        return f"{years[0]}-{years[-1]}"
    else:
        return f"{years[0]}"