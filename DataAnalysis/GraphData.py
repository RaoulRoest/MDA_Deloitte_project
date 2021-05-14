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

import GraphHelper as gh
import ConsoleWriter as logger
import InputGraphData.InputReader as inputReader

def hist_feature(df, feature, bins=100, max_ticks=20):
    dfGraph = df[feature].copy()
    
    fig, ax = plt.subplots()
    dfGraph.hist(ax=ax, grid=False, xrot=90, bins=bins)
    xloc = plt.MaxNLocator(max_ticks)
    ax.xaxis.set_major_locator(xloc)
    
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
        try:
            dfMonthly.loc[l, feature].plot(ax=ax, rot=90, label=l)
        except:
            logger.warning(f"THE FEATURE {feature} WAS NOT PLOTTED", level=1)
    
    name_addition = get_loan_info(loan_id)
    gh.set_plot_params(ax, 
                       title=f"Plot over time for loans: {name_addition}", 
                       xlabel="YearMonth", 
                       ylabel=f"{feature}",
                       legend=True)
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
    toPlot, notToPlot = check_dtypes(df, featureList)
    
    if toPlot:
        df.boxplot(column=toPlot, ax=ax)
    else:
        logger.warning("THERE WERE NO FEATURES TO PLOT.", level=1)
        
    if notToPlot:
        featuresNotPlotted = "----".join(notToPlot)
        message = f"THE FOLLOWING FEATURES WERE NOT PLOTTED :: {featuresNotPlotted} BECAUSE THEY ARE NOT NUMERIC."
        logger.warning(message=message, level=1)
    
    gh.set_plot_params(ax,
                       title="Boxplot of several features",
                       xlabel="feature name")
    return fig

def check_dtypes(df, featureList):
    numerics = []
    nonNumerics = []

    for f in featureList:
        if(pd.api.types.is_numeric_dtype(df[f])):
            numerics.append(f)
        else:
            nonNumerics.append(f)
    
    return numerics, nonNumerics

def main(years, plotOrigFeatures, plotMonthlyFeatures, scatterOrigFeatures, boxplotOrigFeatures):
    """
    ===============================
    Definition of the main function
    ===============================
    Plot features of the monthly and the orig file. 
    """

    logger.info("Start computations")
    logger.info("Get data")
    loader = DataLoader()
    dfOrig, dfMonthly = loader.get_data_set(years=years)
    
    if(plotOrigFeatures["plot"]):
        logger.info("Plot histograms of originate data")
        for column in plotOrigFeatures["features"]:
            logger.info(f"Plot feature: {column}", level=1)
            fig = hist_feature(dfOrig, column)
            
            fig.tight_layout()
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
            
            fig.tight_layout()
            gh.save_plot(fig, filename, "PlotMonthlyFeaturesOverTime")
            plt.close()

    if(scatterOrigFeatures["plot"]):
        logger.info("Scatter features of originate data")
        for f1, f2 in scatterOrigFeatures["features"]:
            logger.info(f"Scatter {f1} against {f2}")
            fig = scatter_features(dfOrig, f1, f2)
            
            fig.tight_layout()
            filename = f"{f1}_{f2}_scatter_plot"
            gh.save_plot(fig, filename, "ScatterOrigData")
            plt.close()
            
    if(boxplotOrigFeatures["plot"]):
        logger.info("Make boxplot of features in originate data")
        fig = boxplot_features(dfOrig, boxplotOrigFeatures["features"])
        
        fig.tight_layout()
        filename = f"Boxplot_of_several_features"
        gh.save_plot(fig, filename, "BoxplotOrigData")
        plt.close()
            
            
"""
=============================
Parameters:
Parameters are read from the csv files 
in the directory: 
\\InputGraphData

see --> InputReader.py 
for more info.
=============================
"""
years = range(2013, 2021)
plotOrigFeatures = {
    "plot" : False, 
    "features" : inputReader.read_orig_features(),
}

plotMonthlyFeatures = {
    "plot" : False,
    "features" : inputReader.read_monthly_features(),
    "loan" : inputReader.read_loans()
}

scatterOrigFeatures = {
    "plot" : False,
    "features" : inputReader.read_orig_scatter_features()
}

boxplotOrigFeatures = {
    "plot" : False, 
    "features" : inputReader.read_orig_features(),
}



"""
=============================
Run main function/script
=============================
"""
main(years, plotOrigFeatures, plotMonthlyFeatures, scatterOrigFeatures, boxplotOrigFeatures)
logger.info("Finished calculations")

"""
New Part
"""
def Complement(list1, list2):
    return [i for i in list1 if i not in list2]

def hist_feature2(df1,df2, feature, bins=100, max_ticks=20,colour="blue",month=False):
    dfGraph1 = df1[feature].copy()
    dfGraph2 = df2[feature].copy()
    
    fig, ax = plt.subplots()
    dfGraph1.hist(ax=ax, grid=False, xrot=90, bins=bins,alpha=0.3,color="blue")
    dfGraph2.hist(ax=ax, grid=False, xrot=90, bins=bins,alpha=0.3,color="red")
    plt.legend(["No PrePayment","PrePayment"])
    xloc = plt.MaxNLocator(max_ticks)
    ax.xaxis.set_major_locator(xloc)
    if month==False:
        gh.set_plot_params(ax, f"Histogram of {feature} of the orig data", feature)
    else:
        gh.set_plot_params(ax, f"Histogram of {feature} of the monthly data", feature)
    return fig

def boxplot_features2(df1,df2, featureList):
    fig, (ax1,ax2) = plt.subplots(1,2)
    toPlot, notToPlot = check_dtypes(df1, featureList)
    
    if toPlot:
        df1.boxplot(column=toPlot, ax=ax1)
        df2.boxplot(column=toPlot, ax=ax2)
    else:
        logger.warning("THERE WERE NO FEATURES TO PLOT.", level=1)
        
    if notToPlot:
        featuresNotPlotted = "----".join(notToPlot)
        logger.warning(f"THE FOLLOWING FEATURES WERE NOT PLOTTED :: {featuresNotPlotted}", level=1)
    
    gh.set_plot_params(ax1,
                       title="Boxplot of several features",
                       xlabel="feature name")
    return fig

from PrepaymentInfoProvider import calculate_prepayment_info

years = [2013,2014,2015,2016,2017,2018,2019,2020]
loader = DataLoader()
dfOrig, dfMonthly = loader.get_data_set(years)
dfPP=calculate_prepayment_info(dfOrig,dfMonthly)

def plot_full_prepayment(dfPP):  
    dfFullPrepayment=dfPP.loc[dfPP["prepayment_type"] == "FullPrepayment"]
    loanids=dfOrig.index
    #NFPPdfFPP=dfFPP.loc[dfFPP["FlagFullPrepayment"] == True]
    loanidsFullPrepayment=dfFullPrepayment.index
    loanidsNoFullPrepayment=Complement(loanids,loanidsFullPrepayment)
    loanidsFullPrepayment=list(set(loanidsFullPrepayment))
    loanidsNoFullPrepayment=list(set(loanidsNoFullPrepayment))
    dfOrigFullPrepayment=dfOrig.loc[loanidsFullPrepayment]
    dfOrigFullNoPrepayment=dfOrig.loc[loanidsNoFullPrepayment]
    
    for column in plotOrigFeatures["features"]:
        fig = hist_feature2(dfOrigFullNoPrepayment,dfOrigFullPrepayment, column)
        fig.tight_layout()
        plt.show()
        gh.save_plot(fig, f"{column}_histogram_{years}", "FullPrePayment/Histograms")
        plt.close()
    
    for column in boxplotOrigFeatures["features"]:
        fig = boxplot_features2(dfOrigFullNoPrepayment,dfOrigFullPrepayment,[column])
        fig.tight_layout()
        plt.show()
        gh.save_plot(fig, f"Boxplot_of_{column}_{years}", "FullPrePayment/Boxplots")
        plt.close()
        
 
def plot_partial_prepayment(dfPP): 
    dfPartialPrepayment=dfPP.loc[dfPP["prepayment_type"] == "PartialPrepayment"]
    loanids=dfOrig.index
    #NFPPdfFPP=dfFPP.loc[dfFPP["FlagFullPrepayment"] == True]
    loanidsPartialPrepayment=dfPartialPrepayment.index
    loanidsNoPartialPrepayment=Complement(loanids,loanidsPartialPrepayment)
    loanidsPartialPrepayment=list(set(loanidsPartialPrepayment))
    loanidsNoPartialPrepayment=list(set(loanidsNoPartialPrepayment))
    dfOrigPartialPrepayment=dfOrig.loc[loanidsPartialPrepayment]
    dfOrigNoPartialPrepayment=dfOrig.loc[loanidsNoPartialPrepayment]
    
    for column in plotOrigFeatures["features"]:
        fig = hist_feature2( dfOrigNoPartialPrepayment,dfOrigPartialPrepayment, column)
        fig.tight_layout()
        plt.show()
        gh.save_plot(fig, f"{column}_histogram_{years}", "PartialPrePayment/Histograms")
        plt.close()
        
        
    for column in boxplotOrigFeatures["features"]:
        fig = boxplot_features2( dfOrigNoPartialPrepayment,dfOrigPartialPrepayment,[column])
        fig.tight_layout()
        plt.show()
        gh.save_plot(fig, f"Boxplot_of_{column}_{years}", "PartialPrePayment/Boxplots")
        plt.close()
    
    
def plot_partial_and_full_prepayment(dfPP):  
    dfFullPrepayment=dfPP.loc[dfPP["prepayment_type"] == "FullPrepayment"]
    dfPartialPrepayment=dfPP.loc[dfPP["prepayment_type"] == "PartialPrepayment"]
    dfPartialFullPrepayment=dfFullPrepayment.append(dfPartialPrepayment)
    loanids=dfOrig.index
    #NFPPdfFPP=dfFPP.loc[dfFPP["FlagFullPrepayment"] == True]
    loanidsPartialFullPrepayment=dfPartialFullPrepayment.index
    loanidsNoPartialFullPrepayment=Complement(loanids,loanidsPartialFullPrepayment)
    loanidsPartialFullPrepayment=list(set(loanidsPartialFullPrepayment))
    loanidsNoPartialFullPrepayment=list(set(loanidsNoPartialFullPrepayment))
    dfOrigPartialFullPrepayment=dfOrig.loc[loanidsPartialFullPrepayment]
    dfOrigNoPartialFullPrepayment=dfOrig.loc[loanidsNoPartialFullPrepayment]
    
    for column in plotOrigFeatures["features"]:
        fig = hist_feature2(dfOrigNoPartialFullPrepayment,dfOrigPartialFullPrepayment, column)
        fig.tight_layout()
        plt.show()
        gh.save_plot(fig, f"{column}_histogram_{years}", "CombinedPrePayment/Histograms")
        plt.close()
        
    for column in boxplotOrigFeatures["features"]:
        fig = boxplot_features2(dfOrigNoPartialFullPrepayment,dfOrigPartialFullPrepayment,[column])
        fig.tight_layout()
        plt.show()
        gh.save_plot(fig, f"Boxplot_of_{column}_{years}", "CombinedPrePayment/Boxplots")
        plt.close()
        
def get_months_prepayment(df):
    """Df as returned by prepayment_info(dfOrig,dfMonthly)"""
    dfNoPrepayment=df.loc[df["prepayment_type"] == "No Prepayment"]
    dfFullPrepayment=df.loc[df["prepayment_type"] == "FullPrepayment"]
    dfPartialPrepayment=df.loc[df["prepayment_type"] == "PartialPrepayment"]
    dfMonthNoPrepayment=dfNoPrepayment["orig_loan_term"]-dfNoPrepayment["mths_remng"]
    dfMonthFullPrepayment=dfFullPrepayment["orig_loan_term"]-dfFullPrepayment["mths_remng"]
    dfMonthPartialPrepayment=dfPartialPrepayment["orig_loan_term"]-dfPartialPrepayment["mths_remng"]
    return dfMonthNoPrepayment,dfMonthFullPrepayment,dfMonthPartialPrepayment

def split_data_prepayment(df):
    """df as returned by prepayment_info(dfOrig,dfMonthly)"""
    dfNoPrepayment=df.loc[df["prepayment_type"] == "No Prepayment"]
    dfFullPrepayment=df.loc[df["prepayment_type"] == "FullPrepayment"]
    dfPartialPrepayment=df.loc[df["prepayment_type"] == "PartialPrepayment"]
    return dfNoPrepayment,dfFullPrepayment,dfPartialPrepayment

def boxplot_features4(df1,df2,df3,df4, featureList):
    fig, (ax1,ax2,ax3,ax4) = plt.subplots(1,4)
    toPlot, notToPlot = check_dtypes(df1, featureList)
    
    if toPlot:
        df1.boxplot(column=toPlot, ax=ax1)
        df2.boxplot(column=toPlot, ax=ax2)
        df3.boxplot(column=toPlot, ax=ax3)
        df4.boxplot(column=toPlot, ax=ax4)
    else:
        logger.warning("THERE WERE NO FEATURES TO PLOT.", level=1)
        
    if notToPlot:
        featuresNotPlotted = "----".join(notToPlot)
        logger.warning(f"THE FOLLOWING FEATURES WERE NOT PLOTTED :: {featuresNotPlotted}", level=1)
    
    gh.set_plot_params(ax1,
                       title="Boxplot of several features",
                       xlabel="feature name")
    return fig

def plot_prepayment_comparison(df):
    df["timescale"]=df["mths_remng"]/df["orig_loan_term"]
    df["payscale"]=df["current_upb"]/df["orig_upb"]
    dfNoPrepayment,dfFullPrepayment,dfPartialPrepayment=split_data_prepayment(df)
    # for column in plotMonthlyFeatures["features"]:
    #     fig = boxplot_features4(NPPnewdfOrig,PPnewdfOrig,[column])
    #     fig.tight_layout()
    #     plt.show()
    fig=boxplot_features4(dfNoPrepayment,dfFullPrepayment,dfPartialPrepayment,df,["timescale","payscale"])
    fig.tight_layout()
    plt.show()
    gh.save_plot(fig,"PrePayment Monthly File", "MonthlyFile/PrePayment")
    plt.close()
    
plot_full_prepayment(dfPP)
plot_partial_prepayment(dfPP)
plot_partial_and_full_prepayment(dfPP)
plot_prepayment_comparison(dfPP)



        
        
        
    
    
        
        
    

