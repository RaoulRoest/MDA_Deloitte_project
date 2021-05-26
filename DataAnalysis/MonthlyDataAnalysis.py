import os
import sys

curDir = os.path.dirname(__file__)
sys.path.append(os.path.join(curDir, "..", "PreProcessing"))
sys.path.append(os.path.join(curDir, "..", "General"))

import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt

import DataSetBuilder as dataBuilder
from DataLoader import DataLoader
import PrepaymentInfoProvider as ppm

import GraphHelper as gh
import PathUtilities as pu
import Helpers
import ConsoleWriter as logger

"""
Just run the script for output
"""


class InputVariables():
    def get_prepayment_cols():
        return [
            'id_loan',
            "svcg_cycle",
            'time',
            'zeroPaymentFlag',
            'prepayment_flag',
            'prepayment_type',
            'orig_loan_term',
        ]
    
    def get_monthly_cols():
        return [
            'repch_flag',
            'mths_remng',
            'step_mod_flag',
            'defered_payment_plan', 
            'eltv',
            'dt_zero_bal',
            'dt_lst_pi',
            'current_upb',
        ]
        
    def get_cols_to_skip_in_analysis():
        return [
            "id_loan", 
            "svcg_cycle", 
            "mths_remng", 
            "t",
            "orig_loan_term",
            "prepayment_flag",
            "dt_lst_pi",
            "dt_zero_bal",
        ]
        
    DefaultDirectoryName = "MonthlyDataAnalysis"
    def get_dir(years):
        return os.path.join(InputVariables.DefaultDirectoryName, pu.get_years_addition(years=years))
        

def count_flag_condtion(flagName, condition, dfCombine, dfOrig):
    dfCombine[flagName] = 0
    dfCombine.loc[condition, flagName] = 1 
    
    dfSum = dfCombine[["id_loan", flagName]].groupby('id_loan', observed=True).sum()
    
    dfOrig = dfOrig.merge(dfSum, how ="left", on="id_loan")

    return dfOrig

def boxplot_flag_results(dfOrig, flagName, include=True):
    fppm = dfOrig[(dfOrig["prepayment_type"] == 2) & (dfOrig[flagName] > 0)].index.to_list()

    if include:
        withPpm = dfOrig[dfOrig.index.isin(fppm) & dfOrig[flagName] > 0]
        whitoutPpm = dfOrig[~dfOrig.index.isin(fppm) & dfOrig[flagName] > 0]

        title_ppm = f"With full prepayment and flag {flagName} count > 0"
        title_no_ppm = f"With no full prepayment and flag {flagName} count > 0"
    
    else:
        withPpm = dfOrig[dfOrig.index.isin(fppm)]
        whitoutPpm = dfOrig[~dfOrig.index.isin(fppm)]

        title_ppm = f"With full prepayment"
        title_no_ppm = f"With no full prepayment"

    ncols = 2
    nrows = 1
    fig, axs = plt.subplots(ncols=ncols, nrows=nrows, figsize=(ncols*5, nrows*5))

    withPpm.boxplot(flagName, ax=axs[0])
    whitoutPpm.boxplot(flagName, ax=axs[1])

    axs[0].set_title(title_ppm)
    axs[1].set_title(title_no_ppm)
    
    return fig

def get_features(dfCombine):
    features = [x for x in dfCombine.columns if x not in InputVariables.get_cols_to_skip_in_analysis()]
    num, noNum = Helpers.check_dtypes(dfCombine, features) 
    
    noNum_featureDict = []
    num_featureDict = []

    for k in noNum:
        for v in dfCombine[k].unique():
            noNum_featureDict.append((k, v))

    for k in num:
        values = dfCombine[k][~dfCombine[k].isnull()].unique()
        if(len(values)>2):
            num_featureDict.append((k, np.mean(values)))
        else:
            for v in values:
                noNum_featureDict.append((k, v))
                
    return noNum_featureDict, num_featureDict

def get_data(years):
    dfOrig = dataBuilder.build_data_set(years=years)
    
    dl = DataLoader()
    dfOrigOld, dfMonthly = dl.get_data_set(years=years)
    dfPPM = ppm.calculate_prepayment_info(dfOrig=dfOrigOld, dfMonthly=dfMonthly)
    
    
    dfCombine = dfMonthly[InputVariables.get_monthly_cols()].merge(dfPPM[InputVariables.get_prepayment_cols()], 
                                                                   how="inner", 
                                                                   on=["id_loan", "svcg_cycle"])
    
    dfCombine["t"] = dfCombine.groupby("id_loan").cumcount()
    dfCombine.loc[dfCombine["prepayment_flag"] == True, "time"] = dfCombine.loc[dfCombine["prepayment_flag"] == True, "t"]
    ppm_map = {"No Prepayment" : 0, "PartialPrepayment" : 1, "FullPrepayment" : 2}
    dfCombine["prepayment_type"] = dfCombine["prepayment_type"].map(ppm_map)
    
    # Clean orig
    dfOrig.drop("Unnamed: 0", axis=1, inplace=True)
    dfOrig.set_index("id_loan", inplace=True, drop=True)
    
    return dfOrig, dfCombine

def plot_boxplot(dfOrig, flagName, include, directory="MonthlyDataAnalysis"):
    fig = boxplot_flag_results(dfOrig, flagName, include=include)
    plt.tight_layout()
    gh.save_plot(fig, f"{flagName}_WholePop_{not include}", directory)
    plt.close(fig)
    

def process_monthly_data(dfCombine, dfOrig, noNum_featureDict, num_featureDict, directroy):
    for k,v in noNum_featureDict:
        feature = k
        value = v
        condition = dfCombine[feature] == value
        flagName = f"{feature}_{value}_flag"

        dfOrig = count_flag_condtion(flagName, condition, dfCombine, dfOrig)
        plot_boxplot(dfOrig=dfOrig, flagName=flagName, include=True, directory=directroy)
        plot_boxplot(dfOrig=dfOrig, flagName=flagName, include=False, directory=directroy)        

    for k,v in num_featureDict:
        feature = k
        value = v
        condition = dfCombine[feature] > value
        flagName = f"{feature}_{value}_flag"

        dfOrig = count_flag_condtion(flagName, condition, dfCombine, dfOrig)
        plot_boxplot(dfOrig=dfOrig, flagName=flagName, include=True, directory=directroy)
        plot_boxplot(dfOrig=dfOrig, flagName=flagName, include=False, directory=directroy)

def perform_analysis(years):
    dfOrig, dfCombine = get_data(years=years)
    noNum_featureDict, num_featureDict = get_features(dfCombine=dfCombine)
    process_monthly_data(dfCombine=dfCombine, 
                         dfOrig=dfOrig, 
                         noNum_featureDict=noNum_featureDict, 
                         num_featureDict=num_featureDict,
                         directroy=InputVariables.get_dir(years=years))

if __name__ == "__main__":
    ys = range(2013, 2021)
    for y in ys:
        logger.info(f"Run analysis for year: {y}")
        perform_analysis([y])
        
    logger.info(f"Run analysis for all years")
    perform_analysis(ys)
    
    logger.info("DONE...")
    