import os 

def make_directory_if_not_exists(dirpath):
    if(not os.path.exists(dirpath)):
        os.makedirs(dirpath)
        
def check_extension(filePath, ext):
    if(filePath.endswith(f".{ext}")):
        return filePath
    else:
        return f"{filePath}.{ext}"