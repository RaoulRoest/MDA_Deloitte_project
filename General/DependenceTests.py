from scipy.stats import ks_2samp
from scipy.stats import chi2_contingency
import ConsoleWriter as logger

def ks_test_two_df(df1,df2,features=1):
    """Returns two dictionaries, first one containing KS_statistics and second one containing P-values
    Use to determine depencies between columns of two dataframes correspondign to same variable"""
    logger.info("Performing KS-test on two dataframes")
    pvals={}
    KS_statistic={}
    if features==1:
        features=df1.columns
    for i in features:
        KSs,P=ks_2samp(df1[i],df2[i])
        pvals[i]=P
        KS_statistic[i]=KSs    
    logger.info("KS-test completed on two dataframes")
    return KS_statistic,pvals

def ks_test_one_df(df,features=1):
    """Returns two dictionaries, first one containing KS_statistics and second one containing P-values
    Use to determine depencies in one dataframe"""
    logger.info("Performing KS-test on one dataframe")
    pvals={}
    KS_statistic={}
    if features==1:
        features=df.columns
    for i in features:
        for j in features[list(features).index(i)+1:]:
            KSs,P=ks_2samp(df[i],df[j])
            pvals[i,j]=P
            KS_statistic[i,j]=KSs    
    logger.info("KS-test completed on one dataframe")
    return KS_statistic,pvals