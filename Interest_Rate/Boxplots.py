# -*- coding: utf-8 -*-
"""
Created on Wed May 26 12:29:28 2021

@author: tom_h
"""
from scipy.stats import ks_2samp
import pandas as pd
import numpy as np
from scipy.stats import ttest_ind
import matplotlib.pyplot as plt
from numpy import inf
#x[x == -inf] = 0

#loadin csv
columns=["id_loan", "svcg_cycle", "current_upb", "int_rt", "payments", "prepayment_type"]
interestrate_date=pd.read_excel("Interestrate_per_month.xlsx")


interestrate_big=pd.read_csv("Interestrate_file_2013.csv", usecols=columns)

#merge market interestrate
interestrate_all = interestrate_big.merge(interestrate_date[["svcg_cycle","interestrate"]], 
                                                          how="left", 
                                                          on="svcg_cycle")
#interestrate_flag
#new_column = interestrate_all["int_rt"]> interestrate_all["interestrate"]
#interestrate_all["interest_flag"]=new_column*1

#nopre_flag
#new_column3=interestrate_all["prepayment_type"]!="FullPrepayment"
#interestrate_all["nofullpre_flag"]=new_column3*1

#make new columns
interestrate_all["interest_incentive"]=interestrate_all["int_rt"]- interestrate_all["interestrate"]
new_column2=interestrate_all["prepayment_type"]=="FullPrepayment"
interestrate_all["fullpre_flag"]=new_column2*1
interestrate_all["fullpre_amount"]=interestrate_all["fullpre_flag"]*interestrate_all["payments"]

#make column ratio
dfgroup = interestrate_all.groupby(["svcg_cycle",])[["current_upb","fullpre_amount"]]
dfgroupsum=dfgroup.sum()
dfgroupsum["ratio"]=dfgroupsum["fullpre_amount"]/dfgroupsum["current_upb"]*100
#dfgroupsum["ratio"].plot()
interestrate_final = interestrate_all.merge(dfgroupsum["ratio"], 
                                                          how="left", 
                                                         on="svcg_cycle")



#percentage interest_flag only noprepayment
nopre=interestrate_all.loc[interestrate_all["prepayment_type"]=="No Prepayment"]
#print(nopre["interest_flag"].sum()/len(nopre))

#percentage interest_flag only partialprepayments
partialpre = interestrate_all.loc[interestrate_all["prepayment_type"]=="PartialPrepayment"]
#print(partialpre["interest_flag"].sum()/len(partialpre))

#percentage interest_flag only fullprepayments
fullpre = interestrate_all.loc[interestrate_all["prepayment_type"]=="FullPrepayment"]
#print(fullpre["interest_flag"].sum()/len(fullpre))

fullpartialpre = interestrate_all.loc[(interestrate_all["prepayment_type"]=="FullPrepayment")|(interestrate_all["prepayment_type"] == "PartialPrepayment")]

#percentage interest_flag over alles
#print(interestrate_all["interest_flag"].sum()/len(interestrate_all))

column="interest_incentive"
fig = plt.figure()
fig.suptitle("Boxplot of feature")
ax = plt.subplots(1,1)

plt.boxplot([nopre[column], fullpre[column],partialpre[column],fullpartialpre[column]])
plt.xticks([1, 2, 3, 4],["No Prepayments","Full Prepayments","Partial Prepayments", "Full or Partial Prepayment"])
plt.ylabel(column)


ks_2samp(nopre["interest_incentive"],fullpartialpre["interest_incentive"])