import sys 
import os
preProcessing_dir = os.path.join(os.path.dirname(__file__), "..", "PreProcessing")
general = os.path.join(os.path.dirname(__file__), "..", "General")
sys.path.append(preProcessing_dir)
sys.path.append(general)

import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 

# Custom modules
from DataLoader import DataLoader
from DataCleaner import DataCleaner

import GraphHelper as gh
import ConsoleWriter as logger

def get_data(years):
    # years = range(2013, 2021) #Python uses 0-indexing, hence this will be [2013, 2020, steps=1]
    
    dl = DataLoader()
    dc = DataCleaner()
    
    dfOrig = dl.get_all_originate_years(years)
    dfMonthly = dl.get_all_monthly_performance_years(years)
    
    dfOrigClean, dfMonthlyClean = dc.clean_data(dfOrig, dfMonthly)
    
    dfMonthlyClean.dropna(axis='columns', inplace=True) #Drop the columns with na values. 
    
    # Set indexes for faster searches
    dfMonthlyClean.set_index(["id_loan", "svcg_cycle"], inplace=True) #Index on loan index, and timestep. 
    dfOrigClean.set_index("id_loan", inplace=True) #Index on loan index
        
    return dfOrigClean, dfMonthlyClean

def hist_feature(df, feature, bins=10):
    dfGraph = df[feature].copy()
    
    fig, ax = plt.subplots()
    dfGraph.hist(ax=ax, grid=False, xrot=90, bins=bins)
    
    gh.set_plot_params(ax, f"Histogram of {feature} of the orig data", feature)
    return fig

def plot_monthly_feature_over_time(dfMonthly, feature, loan_id=None):
    if(loan_id is None):
        loans = list(set([l for l, t in dfMonthly.index.values]))
    else:
        if(isinstance(loan_id, str)):
            loans = [loan_id]
        elif(isinstance(loan_id, list)):
            loans = loan_id
        else:
            raise Exception("This function can only manage None, list or string")
    
    fig, ax = plt.subplots()
    for l in loans:
        dfMonthly.loc[l, feature].plot(ax=ax, rot=90)
    
    name_addition = get_loan_info(loan_id)
    gh.set_plot_params(ax, 
                       title=f"Plot over time for loans: {name_addition}", 
                       xlabel="YearMonth", 
                       ylabel=f"{feature}")
    return fig

def get_loan_info(loans):
    if(loans is None):
        name_addition = "all"
    elif(isinstance(loans, list)):
        name_addition = "selected"
    elif(isinstance(loans, str)):
        name_addition = loans
    else:
        raise Exception() # just in case.
    
    return name_addition
    
def scatter_features(df, feature1, feature2):
    fig, ax = plt.subplots()
    df.plot.scatter(feature1, feature2, ax=ax)
    
    gh.set_plot_params(ax, 
                       title=f"Scatter plot of {feature1} against {feature2}",
                       xlabel=f"{feature1}",
                       ylabel=f"{feature2}")

    return fig    

def boxplot_features(df, featureList):
    fig, ax = plt.subplots()
    df.boxplot(column=featureList, ax=ax)
    
    gh.set_plot_params(ax,
                       title="Boxplot of several features",
                       xlabel="feature name")
    return fig

def main(years, plotOrigFeatures, plotMonthlyFeatures, scatterOrigFeatures, boxplotOrigFeatures):
    """
    ===============================
    Definition of the main function
    ===============================
    Plot features of the monthly and the orig file. 
    """

    logger.info("Start computations")
    logger.info("Get data")
    dfOrig, dfMonthly = get_data(years)
    
    if(plotOrigFeatures["plot"]):
        logger.info("Plot histograms of originate data")
        for column in plotOrigFeatures["features"]:
            logger.info(f"Plot feature: {column}", level=1)
            fig = hist_feature(dfOrig, column)
            gh.save_plot(fig, f"{column}_histogram", "HistogramsOriginateFeatures")
            plt.close()
    
    if(plotMonthlyFeatures["plot"]):
        logger.info("Plot features over time")
        loans = plotMonthlyFeatures["loan"]
        for column in plotMonthlyFeatures["features"]:
            logger.info(f"Plot feature: {column}", level=1)
            fig = plot_monthly_feature_over_time(dfMonthly, column, loan_id=loans)
            
            name_addition = get_loan_info(loans)
            filename = f"{column}_monthly_plot_loan_{name_addition}"
            gh.save_plot(fig, filename, "PlotMonthlyFeaturesOverTime")
            plt.close()

    if(scatterOrigFeatures["plot"]):
        logger.info("Scatter features of originate data")
        for f1, f2 in scatterOrigFeatures["features"]:
            logger.info(f"Scatter {f1} against {f2}")
            fig = scatter_features(dfOrig, f1, f2)
            
            filename = f"{f1}_{f2}_scatter_plot"
            gh.save_plot(fig, filename, "ScatterOrigData")
            plt.close()
            
    if(boxplotOrigFeatures["plot"]):
        logger.info("Make boxplot of features in originate data")
        fig = boxplot_features(dfOrig, boxplotOrigFeatures["features"])
        
        filename = f"Boxplot_of_several_features"
        gh.save_plot(fig, filename, "BoxplotOrigData")
        plt.close()
            
            
"""
=============================
Parameters
=============================
"""
years = [2013]
plotOrigFeatures = {
    "plot" : False, 
    "features" : [
        "fico",
    ],
}

plotMonthlyFeatures = {
    "plot" : False,
    "features" : [
        "current_upb",
    ],
    "loan" : [
        "F113Q3265933",
        "F113Q1100382",
    ],
}

scatterOrigFeatures = {
    "plot" : False,
    "features" : [
        ("fico", "flag_fthb"),
    ],
}

boxplotOrigFeatures = {
    "plot" : True, 
    "features" :[
        "fico",
        "int_rt",
    ],
}
"""
=============================
Run main function/script
=============================
"""
main(years, plotOrigFeatures, plotMonthlyFeatures, scatterOrigFeatures, boxplotOrigFeatures)
logger.info("Finished calculations")