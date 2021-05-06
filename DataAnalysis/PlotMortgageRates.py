import os
import sys 
curDir = os.path.dirname(__file__)
preProcessing = os.path.join(curDir, "..", "PreProcessing")
sys.path.append(preProcessing)
general = os.path.join(curDir, "..", "General")
sys.path.append(general)

import matplotlib.pyplot as plt
import pandas as pd

# Custom packages
from DataLoader import DataLoader 
import GraphHelper as gh
import ConsoleWriter as logger

def main():
    logger.info("Get data")
    dl = DataLoader()
    dfUsRate = dl.get_fifteen_years_mortgage_rate()
    
    logger.info("Plot the data")
    fig, ax = plt.subplots()
    dfUsRate.plot(ax=ax, rot=90, label="US 15-year mortgage rates")
    fig.tight_layout()
    
    logger.info("Save the plot")
    gh.save_plot(fig, "US_Mortgage_Rates", "MortgageRates")
    
    plt.close()
main()