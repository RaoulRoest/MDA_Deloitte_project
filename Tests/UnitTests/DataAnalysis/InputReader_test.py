import os
import sys
curDir = os.path.dirname(__file__)
inputReaderPath = os.path.join(curDir, "..", "..", "..", "DataAnalysis", "InputGraphData")
sys.path.append(inputReaderPath)
utilsPath = os.path.join(curDir, "..", "..", "Common")
sys.path.append(utilsPath)

# Custom module
import TestUtilities as utils
from Assertions import assert_items_in_list
import InputReader as sut

def test_read_csv_file_one_column_to_list():
    # Init
    testDir = utils.get_test_input_dir()
    filename = "OneColumnInput.csv"
    filepath = os.path.join(testDir, filename)
    expected = [f"{i}" for i in range(1, 6)]
    
    # Act
    result = sut.read_csv_file_one_column_to_list(filepath)

    # Assert
    assert_items_in_list(result, expected)

def test_read_csv_file_multiple_column_to_list_of_tuples():
    # Init
    testDir = utils.get_test_input_dir()
    filename = "TwoColumnInput.csv"
    filepath = os.path.join(testDir, filename)
    expected = [("a", "1"), ("b", "2"), ("c", "3"), ("d", "4")]
    
    # Act
    result = sut.read_csv_file_multiple_column_to_list_of_tuples(filepath)

    # Assert
    assert_items_in_list(result, expected)
