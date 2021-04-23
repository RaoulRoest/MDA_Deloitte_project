import os 
import sys
generalPath = os.path.join(os.path.dirname(__file__), "..", "..", "..", "General")
sys.path.append(generalPath)

import pytest

# Custom module
import PathUtilities as pu 

def get_test_results_directory():
    return os.path.join(os.path.dirname(__file__), "..", "..", "TestResults", "PathUtitlitiesTests")

def clean_env(dirPath):
    os.rmdir(dirPath)

def test_make_dir_should_make_dir():
    env = get_test_results_directory()
    dirname = os.path.join(env, "testDir")
    
    pu.make_directory_if_not_exists(dirname)
    
    assert os.path.exists(dirname) == True
    
    clean_env(dirname) # remove dir for sake of test.
    
def test_check_extension_should_add_extension():
    filePath = "someFilePath"
    ext = "someExt"
    expected = f"{filePath}.{ext}"
    
    result = pu.check_extension(filePath, ext)
    
    assert result == expected
    
def test_check_extension_should_not_add_extension_if_already_there():
    filePath = "someFilePath.someExt"
    ext = "someExt"
    expected = f"{filePath}"
    
    result = pu.check_extension(filePath, ext)
    
    assert result == expected