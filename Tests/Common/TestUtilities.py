import os 

def get_test_input_dir():
    curDir = os.path.dirname(__file__)
    return os.path.join(curDir, "..", "TestData")
    