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
import DependenceTests as DT

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
#main(years, plotOrigFeatures, plotMonthlyFeatures, scatterOrigFeatures, boxplotOrigFeatures)
#logger.info("Finished calculations")

"""
New Part
"""
def Complement(list1, list2):
    return [i for i in list1 if i not in list2]

def hist_feature2(name1, name2,df1,df2, feature, bins=100, max_ticks=20,colour="blue", month=False):
    # dfGraph1 = df1[feature].copy()
    # dfGraph2 = df2[feature].copy()
    fig, ax = plt.subplots()
    plt.hist(df1[feature], bins=bins,alpha=0.3,color="blue",density=True,stacked=True)
    plt.hist(df2[feature], bins=bins,alpha=0.3,color="red",density=True,stacked=True)
    # dfGraph1.hist(ax=ax, grid=False, xrot=90, bins=bins,alpha=0.3,color="blue",density=True)
    # dfGraph2.hist(ax=ax, grid=False, xrot=90, bins=bins,alpha=0.3,color="red",density=True)
    plt.legend([name1,name2])
    xloc = plt.MaxNLocator(max_ticks)
    ax.xaxis.set_major_locator(xloc)
    if month==False:
        gh.set_plot_params(ax, f"Histogram of {feature} of the orig data", feature)
    else:
        gh.set_plot_params(ax, f"Histogram of {feature} of the monthly data", feature)
    return fig

def boxplot_features2(df1,df2, featureList,column,name1,name2):
    fig, ax = plt.subplots(1,1)
    toPlot, notToPlot = check_dtypes(df1, featureList)
    if toPlot:
        plt.boxplot([df1[column],df2[column]])
        plt.xticks([1, 2],[name1, name2])
        plt.ylabel(column)
    else:
        logger.warning("THERE WERE NO FEATURES TO PLOT.", level=1)

    if notToPlot:
        featuresNotPlotted = "----".join(notToPlot)
        logger.warning(f"THE FOLLOWING FEATURES WERE NOT PLOTTED :: {featuresNotPlotted}", level=1)
    
    gh.set_plot_params(ax,title="Boxplot of feature",xlabel="")
    return fig
    

from PrepaymentInfoProvider import calculate_prepayment_info

years = [2013,2014,2015,2016,2017,2018,2019,2020]
loader = DataLoader()
dfOrig, dfMonthly = loader.get_data_set(years)
dfPP=calculate_prepayment_info(dfOrig,dfMonthly)
lengthloan={}
loanids=dfOrig.index
for i in loanids:
    lengthloan[i]=len(dfMonthly.loc[i])

def dfprepayment_to_dfstandard(dfPP2):
    dfPP2["prepayment_type"].replace({'FullPrepayment': 5000, 'PartialPrepayment': 1, 'No Prepayment':0 }, inplace=True)
    fullpp=np.array([0]*len(loanids))
    partpp=np.array([0]*len(loanids))
    fullandpartpp=np.array([0]*len(loanids))
    nopp=np.array([0]*len(loanids))
    s=0
    sums={}
    for i in loanids:
        sums[i]=sum(dfPP2["prepayment_type"].iloc[s:s+lengthloan[i]])
        s+=lengthloan[i]
    logger.info("Get type of prepayment")
    vals=np.array(list(sums.values()))
    fullpp=(vals==5000)
    logger.info("Full Prepayment done")
    partpp=(vals>0)&(vals<5000)
    logger.info("Partial Prepayment done")
    fullandpartpp=(vals>5000)
    logger.info("Full and Partial Prepayment combined done")
    nopp=(vals==0)
    logger.info("No Prepayment done")
    df=pd.DataFrame({"No Prepayment":nopp,"Partial Prepayment":partpp, "Full Prepayment":fullpp, "Partial and Full Prepayment":fullandpartpp},index=loanids)
    #df=pd.DataFrame(np.array([nopp, partpp, fullpp,fullandpartpp]),index=loanids,columns=["No Prepayment","Partial Prepayment","Full Prepayment", "Partial and Full Prepayment"])
    return df

dfPP2=dfPP.copy()
dfPP_otherformat=dfprepayment_to_dfstandard(dfPP2)
loanidsFullPrepayment=dfPP_otherformat.loc[dfPP_otherformat["Full Prepayment"] == 1].index
loanidsPartialPrepayment=dfPP_otherformat.loc[dfPP_otherformat["Partial Prepayment"] == 1].index
loanidsFullandPartialPrepayment=dfPP_otherformat.loc[dfPP_otherformat["Partial and Full Prepayment"] == 1].index
loanidsNoPrepayment=dfPP_otherformat.loc[dfPP_otherformat["No Prepayment"] == 1].index
dfOrigFullPrepayment=dfOrig.loc[loanidsFullPrepayment]
dfOrigPartialPrepayment=dfOrig.loc[loanidsPartialPrepayment]
dfOrigFullandPartialPrepayment=dfOrig.loc[loanidsFullandPartialPrepayment]
dfOrigNoPrepayment=dfOrig.loc[loanidsNoPrepayment]
dfOrigNoFullPrepayment=dfOrigNoPrepayment.append(dfOrigPartialPrepayment)
dfOrigNoPartialPrepayment=dfOrigNoPrepayment.append(dfOrigFullPrepayment)
dfOrigPartialOrFullPrepayment=dfOrigFullPrepayment.append(dfOrigPartialPrepayment.append(dfOrigFullandPartialPrepayment))
dfOrigFullPrepaymentoverPartialPrepayment=dfOrigFullPrepayment.append(dfOrigFullandPartialPrepayment)
dfPrePayment=dfOrigFullPrepaymentoverPartialPrepayment.append(dfOrigPartialPrepayment)

def plot_full_against_no_prepayment():   
    """Plot Full Prepayment against No Prepayment, hence no partial and no combination"""
    for column in plotOrigFeatures["features"]:
        fig = hist_feature2("No Prepayment","Full Prepayment",dfOrigNoPrepayment,dfOrigFullPrepayment, column)
        fig.tight_layout()
        plt.show()
        gh.save_plot(fig, f"{column}_histogram_{years}", "NoPrepayment_VS_FullPrePayment/Histograms")
        plt.close()
    
    for column in boxplotOrigFeatures["features"]:
        fig = boxplot_features2(dfOrigNoPrepayment,dfOrigFullPrepayment,[column],column,"No Prepayment","Full Prepayment")
        fig.tight_layout()
        plt.show()
        gh.save_plot(fig, f"Boxplot_of_{column}_{years}", "NoPrePayment_VS_FullPrePayment/Boxplots")
        plt.close()
        
def plot_full_against_no_full_prepayment():
    """Plot Full Prepayment against No Full prepayment. If both Partial and Full Prepayment happens, it is counted as Full Prepayment"""
    for column in plotOrigFeatures["features"]:
        fig = hist_feature2("No Full Prepayment","Full Prepayment",dfOrigNoFullPrepayment,dfOrigFullPrepayment, column)
        fig.tight_layout()
        plt.show()
        gh.save_plot(fig, f"{column}_histogram_{years}", "NoFullPrepayment_VS_FullPrePayment/Histograms")
        plt.close()
    
    for column in boxplotOrigFeatures["features"]:
        fig = boxplot_features2(dfOrigNoPrepayment,dfOrigFullPrepayment,[column],column,"No Full Prepayment","Full Prepayment")
        fig.tight_layout()
        plt.show()
        gh.save_plot(fig, f"Boxplot_of_{column}_{years}", "NoFullPrePayment_VS_FullPrePayment/Boxplots")
        plt.close()

def plot_partial_against_no_prepayment():
    for column in plotOrigFeatures["features"]:
        fig = hist_feature2("No Prepayment","Partial Prepayment",dfOrigNoPrepayment,dfOrigPartialPrepayment, column)
        fig.tight_layout()
        plt.show()
        gh.save_plot(fig, f"{column}_histogram_{years}", "NoPrepayment_VS_PartialPrePayment/Histograms")
        plt.close()
    
    for column in boxplotOrigFeatures["features"]:
        fig = boxplot_features2(dfOrigNoPrepayment,dfOrigPartialPrepayment,[column],column,"No Full Prepayment","Partial Prepayment")
        fig.tight_layout()
        plt.show()
        gh.save_plot(fig, f"Boxplot_of_{column}_{years}", "NoPrePayment_VS_PartialPrePayment/Boxplots")
        plt.close()
        
def plot_partial_and_full_against_no_prepayment():
    for column in plotOrigFeatures["features"]:
        fig = hist_feature2("No Prepayment","Partial and Full Prepayment",dfOrigNoPrepayment,dfOrigFullandPartialPrepayment, column)
        fig.tight_layout()
        plt.show()
        gh.save_plot(fig, f"{column}_histogram_{years}", "NoPrepayment_VS_PartialAndFullPrePayment/Histograms")
        plt.close()
    
    for column in boxplotOrigFeatures["features"]:
        fig = boxplot_features2(dfOrigNoPrepayment,dfOrigFullandPartialPrepayment,[column],column,"No Prepayment","Partial and Full Prepayment")
        fig.tight_layout()
        plt.show()
        gh.save_plot(fig, f"Boxplot_of_{column}_{years}", "NoPrePayment_VS_PartialAndFullPrePayment/Boxplots")
        plt.close()
        
def plot_partial_or_full_against_no_prepayment():
    for column in plotOrigFeatures["features"]:
        fig = hist_feature2("No Prepayment","Partial or Full Prepayment",dfOrigNoPrepayment,dfOrigPartialOrFullPrepayment, column)
        fig.tight_layout()
        plt.show()
        gh.save_plot(fig, f"{column}_histogram_{years}", "NoPrepayment_VS_PartialOrFullPrePayment/Histograms")
        plt.close()
    
    for column in boxplotOrigFeatures["features"]:
        fig = boxplot_features2(dfOrigNoPrepayment,dfOrigPartialOrFullPrepayment,[column],column,"No Prepayment","Partial or Full Prepayment")
        fig.tight_layout()
        plt.show()
        gh.save_plot(fig, f"Boxplot_of_{column}_{years}", "NoPrePayment_VS_PartialOrFullPrePayment/Boxplots")
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

def boxplot_features4b(df1,df2,df3,df4, featureList,column,name1,name2,name3,name4):
    fig, ax = plt.subplots(1,1)
    toPlot, notToPlot = check_dtypes(df1, featureList)
    if toPlot:
        plt.boxplot([df1[column],df2[column],df3[column],df4[column]])
        plt.xticks([1, 2, 3, 4],[name1, name2, name3, name4])
        plt.ylabel(column)
    else:
        logger.warning("THERE WERE NO FEATURES TO PLOT.", level=1)

    if notToPlot:
        featuresNotPlotted = "----".join(notToPlot)
        logger.warning(f"THE FOLLOWING FEATURES WERE NOT PLOTTED :: {featuresNotPlotted}", level=1)
    
    gh.set_plot_params(ax,title="Boxplot of feature",xlabel="")
    return fig

def plot_prepayment_comparison(df):
    df["timescale"]=df["mths_remng"]/df["orig_loan_term"]
    df["payscale"]=df["current_upb"]/df["orig_upb"]
    dfNoPrepayment,dfFullPrepayment,dfPartialPrepayment=split_data_prepayment(df)
    fig=boxplot_features4(dfNoPrepayment,dfFullPrepayment,dfPartialPrepayment,df,["timescale","payscale"])
    fig.tight_layout()
    plt.show()
    gh.save_plot(fig,"PrePayment Monthly File", "MonthlyFile/PrePayment")
    plt.close()
    
# plot_full_against_no_prepayment()
# plot_full_against_no_full_prepayment()
# plot_partial_against_no_prepayment()
# plot_partial_and_full_against_no_prepayment()
# plot_partial_or_full_against_no_prepayment()

from DependenceTests import ks_test_two_df
ks_test_two_df(dfOrigNoPrepayment,dfOrigFullPrepaymentoverPartialPrepayment,["orig_upb"])
ks_test_two_df(dfOrigNoPrepayment,dfOrigPartialPrepayment,["orig_upb"])
ks_test_two_df(dfOrigNoPrepayment,dfPrePayment,["orig_upb"])
ks_test_two_df(dfOrigFullPrepaymentoverPartialPrepayment,dfOrigPartialPrepayment,["orig_upb"])

fig=boxplot_features4b(dfOrigNoPrepayment,dfOrigFullPrepaymentoverPartialPrepayment, dfOrigPartialPrepayment, dfPrePayment,["ltv"],"ltv","No Prepayment", "Full Prepayment", "Partial Prepayment", "Full or Partial Prepayment")
#fig.tight_layout()
plt.show()
#gh.save_plot(fig, f"Boxplot_of_lltv_{years}_", "Preliminairy/Boxplots")
#plt.close()  

fig=boxplot_features4b(dfOrigNoPrepayment,dfOrigFullPrepaymentoverPartialPrepayment, dfOrigPartialPrepayment, dfPrePayment,["cltv"],"cltv","No Prepayment", "Full Prepayment", "Partial Prepayment", "Full or Partial Prepayment")
fig.tight_layout()
plt.show()
#gh.save_plot(fig, f"Boxplot_of_cltv_{years}_", "Preliminairy/Boxplots")
#plt.close() 

fig=boxplot_features4b(dfOrigNoPrepayment,dfOrigFullPrepaymentoverPartialPrepayment, dfOrigPartialPrepayment, dfPrePayment,["orig_upb"],"orig_upb","No Prepayment", "Full Prepayment", "Partial Prepayment", "Full or Partial Prepayment")
fig.tight_layout()
plt.show()
#gh.save_plot(fig, f"Boxplot_of_upb_{years}_", "Preliminairy/Boxplots")
#plt.close() 
        
    
    
        
        
    

