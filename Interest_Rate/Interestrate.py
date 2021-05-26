# -*- coding: utf-8 -*-
"""
Created on Wed May 19 14:08:20 2021

@author: tom_h
"""

import pandas as pd
import numpy as np
from scipy.stats import ttest_ind
import matplotlib.pyplot as plt
from numpy import inf
#x[x == -inf] = 0

#loadin csv
columns=["id_loan", "svcg_cycle", "current_upb", "int_rt", "payments", "prepayment_type"]
interestrate_date=pd.read_excel("Interestrate_per_month.xlsx")


interestrate_big=pd.read_csv("Interestrate_file_allyears.csv", usecols=columns)

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
interestrate_final = interestrate_all.merge(dfgroupsum["ratio"], 
                                                          how="left", 
                                                         on="svcg_cycle")


#make scatter with al points
#df=interestrate_final.groupby(['interest_incentive','ratio'])["svcg_cycle"]
#dataplot=df.count()
#dataplotframe=dataplot.to_frame()
#dataplotframe.reset_index(inplace=True)
#interest_incentive=dataplotframe['interest_incentive'].values
#ratio=dataplotframe['ratio'].values
#S= dataplotframe['svcg_cycle'].values/dataplotframe['svcg_cycle'].sum()

#plt.scatter(interest_incentive, ratio, 
 #            s=S*10000,
  #           alpha=0.5)
#plt.xlabel("Interest Incentive")
#plt.ylabel("Ratio")
#plt.title("interest rate incentive against the observed prepayment rate")

#make plot with mean
df2=interestrate_final.groupby(['ratio'])['interest_incentive']

datacount2=df2.count()
datacountframe2=datacount2.to_frame()
datacountframe2.reset_index(inplace=True)

dataplot2=df2.mean()
dataplotframe2=dataplot2.to_frame()
dataplotframe2.reset_index(inplace=True)

S2= datacountframe2['interest_incentive'].values/datacountframe2['interest_incentive'].sum()
interest_incentive2=dataplotframe2['interest_incentive'].values
ratio2=dataplotframe2['ratio'].values

plt.figure(1)
sc=plt.scatter(interest_incentive2, ratio2, 
             s=S2*10000,
             alpha=0.5,
             color='red')
plt.legend(sc.legend_elements("sizes", num=6, color='red')[0],[50000,100000,150000,200000,250000], title='Observations')
plt.xlabel("Interest Incentive (%)")
plt.ylabel("Observed Prepayment Ratio (%)")
plt.title("Mortgages over all years")
plt.show()
