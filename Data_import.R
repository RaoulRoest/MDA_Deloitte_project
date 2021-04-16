# *** Import Freddie Mac mortgage data ('sample_orig_yyyy.txt' and 'sample_svcg_yyyy.txt') and market mortgage rates ('MORTGAGE15US.xlsx') ***
rm(list=ls())
#setwd("")

# Import origination and monthly performance data files (http://www.freddiemac.com/research/datasets/sf_loanlevel_dataset.page)
# Please note that the user guide of the data ('user_guide.pdf') specifies the Loan Sequence Number incorrectly, the unique identifier (F1YYQnXXXXXX) that is assigned to each loan is structured as follows:
#    - F1: Fixed rate mortgage;
#    - YYQn: Origination year and quarter;
#    - XXXXXX: Randomly assigned digits.
origclass <- c('integer','integer','character', 'integer', 'character', 'real', 'integer', 'character','real','integer','integer','integer','real','character','character','character','character', 'character','character','character','character', 'integer', 'integer','character','character' ,'character', 'character', 'character', 'character', 'integer')
svcgclass <- c('character', 'integer', 'real', 'character', 'integer', 'integer', 'character', 'character', 'integer', 'integer', 'real', 'real', 'numeric', 'real', 'character', 'real', 'real', 'real', 'real', 'real', 'real', 'real', 'real', 'character', 'character', 'real', 'real', 'character', 'character')

# 2013
origfile_2013 <- read.table("sample_orig_2013.txt", sep="|", header=FALSE, colClasses=origclass )
names(origfile_2013)=c('fico','dt_first_pi','flag_fthb','dt_matr','cd_msa',"mi_pct",'cnt_units','occpy_sts','cltv','dti','orig_upb','ltv','int_rt','channel','ppmt_pnlty','prod_type','st', 'prop_type','zipcode','id_loan','loan_purpose', 'orig_loan_term','cnt_borr','seller_name','servicer_name', 'flag_sc')
svcgfile_2013 <- read.table("sample_svcg_2013.txt", sep="|", header=FALSE, colClasses=svcgclass)
names(svcgfile_2013)=c('id_loan','svcg_cycle','current_upb','delq_sts','loan_age','mths_remng', 'repch_flag','flag_mod', 'cd_zero_bal', 'dt_zero_bal','current_int_rt','non_int_brng_upb','dt_lst_pi','mi_recoveries', 'net_sale_proceeds','non_mi_recoveries','expenses', 'legal_costs', 'maint_pres_costs','taxes_ins_costs','misc_costs','actual_loss', 'modcost')

# 2014
origfile_2014 <- read.table("sample_orig_2014.txt", sep="|", header=FALSE, colClasses=origclass )
names(origfile_2014)=c('fico','dt_first_pi','flag_fthb','dt_matr','cd_msa',"mi_pct",'cnt_units','occpy_sts','cltv','dti','orig_upb','ltv','int_rt','channel','ppmt_pnlty','prod_type','st', 'prop_type','zipcode','id_loan','loan_purpose', 'orig_loan_term','cnt_borr','seller_name','servicer_name', 'flag_sc')
svcgfile_2014 <- read.table("sample_svcg_2014.txt", sep="|", header=FALSE, colClasses=svcgclass)
names(svcgfile_2014)=c('id_loan','svcg_cycle','current_upb','delq_sts','loan_age','mths_remng', 'repch_flag','flag_mod', 'cd_zero_bal', 'dt_zero_bal','current_int_rt','non_int_brng_upb','dt_lst_pi','mi_recoveries', 'net_sale_proceeds','non_mi_recoveries','expenses', 'legal_costs', 'maint_pres_costs','taxes_ins_costs','misc_costs','actual_loss', 'modcost')

# 2015
origfile_2015 <- read.table("sample_orig_2015.txt", sep="|", header=FALSE, colClasses=origclass )
names(origfile_2015)=c('fico','dt_first_pi','flag_fthb','dt_matr','cd_msa',"mi_pct",'cnt_units','occpy_sts','cltv','dti','orig_upb','ltv','int_rt','channel','ppmt_pnlty','prod_type','st', 'prop_type','zipcode','id_loan','loan_purpose', 'orig_loan_term','cnt_borr','seller_name','servicer_name', 'flag_sc')
svcgfile_2015 <- read.table("sample_svcg_2015.txt", sep="|", header=FALSE, colClasses=svcgclass)
names(svcgfile_2015)=c('id_loan','svcg_cycle','current_upb','delq_sts','loan_age','mths_remng', 'repch_flag','flag_mod', 'cd_zero_bal', 'dt_zero_bal','current_int_rt','non_int_brng_upb','dt_lst_pi','mi_recoveries', 'net_sale_proceeds','non_mi_recoveries','expenses', 'legal_costs', 'maint_pres_costs','taxes_ins_costs','misc_costs','actual_loss', 'modcost')

# 2016
origfile_2016 <- read.table("sample_orig_2016.txt", sep="|", header=FALSE, colClasses=origclass )
names(origfile_2016)=c('fico','dt_first_pi','flag_fthb','dt_matr','cd_msa',"mi_pct",'cnt_units','occpy_sts','cltv','dti','orig_upb','ltv','int_rt','channel','ppmt_pnlty','prod_type','st', 'prop_type','zipcode','id_loan','loan_purpose', 'orig_loan_term','cnt_borr','seller_name','servicer_name', 'flag_sc')
svcgfile_2016 <- read.table("sample_svcg_2016.txt", sep="|", header=FALSE, colClasses=svcgclass)
names(svcgfile_2016)=c('id_loan','svcg_cycle','current_upb','delq_sts','loan_age','mths_remng', 'repch_flag','flag_mod', 'cd_zero_bal', 'dt_zero_bal','current_int_rt','non_int_brng_upb','dt_lst_pi','mi_recoveries', 'net_sale_proceeds','non_mi_recoveries','expenses', 'legal_costs', 'maint_pres_costs','taxes_ins_costs','misc_costs','actual_loss', 'modcost')

# 2017
origfile_2017 <- read.table("sample_orig_2017.txt", sep="|", header=FALSE, colClasses=origclass )
names(origfile_2017)=c('fico','dt_first_pi','flag_fthb','dt_matr','cd_msa',"mi_pct",'cnt_units','occpy_sts','cltv','dti','orig_upb','ltv','int_rt','channel','ppmt_pnlty','prod_type','st', 'prop_type','zipcode','id_loan','loan_purpose', 'orig_loan_term','cnt_borr','seller_name','servicer_name', 'flag_sc')
svcgfile_2017 <- read.table("sample_svcg_2017.txt", sep="|", header=FALSE, colClasses=svcgclass)
names(svcgfile_2017)=c('id_loan','svcg_cycle','current_upb','delq_sts','loan_age','mths_remng', 'repch_flag','flag_mod', 'cd_zero_bal', 'dt_zero_bal','current_int_rt','non_int_brng_upb','dt_lst_pi','mi_recoveries', 'net_sale_proceeds','non_mi_recoveries','expenses', 'legal_costs', 'maint_pres_costs','taxes_ins_costs','misc_costs','actual_loss', 'modcost')

# 2018
origfile_2018 <- read.table("sample_orig_2018.txt", sep="|", header=FALSE, colClasses=origclass )
names(origfile_2018)=c('fico','dt_first_pi','flag_fthb','dt_matr','cd_msa',"mi_pct",'cnt_units','occpy_sts','cltv','dti','orig_upb','ltv','int_rt','channel','ppmt_pnlty','prod_type','st', 'prop_type','zipcode','id_loan','loan_purpose', 'orig_loan_term','cnt_borr','seller_name','servicer_name', 'flag_sc')
svcgfile_2018 <- read.table("sample_svcg_2018.txt", sep="|", header=FALSE, colClasses=svcgclass)
names(svcgfile_2018)=c('id_loan','svcg_cycle','current_upb','delq_sts','loan_age','mths_remng', 'repch_flag','flag_mod', 'cd_zero_bal', 'dt_zero_bal','current_int_rt','non_int_brng_upb','dt_lst_pi','mi_recoveries', 'net_sale_proceeds','non_mi_recoveries','expenses', 'legal_costs', 'maint_pres_costs','taxes_ins_costs','misc_costs','actual_loss', 'modcost')

# 2019
origfile_2019 <- read.table("sample_orig_2019.txt", sep="|", header=FALSE, colClasses=origclass )
names(origfile_2019)=c('fico','dt_first_pi','flag_fthb','dt_matr','cd_msa',"mi_pct",'cnt_units','occpy_sts','cltv','dti','orig_upb','ltv','int_rt','channel','ppmt_pnlty','prod_type','st', 'prop_type','zipcode','id_loan','loan_purpose', 'orig_loan_term','cnt_borr','seller_name','servicer_name', 'flag_sc')
svcgfile_2019 <- read.table("sample_svcg_2019.txt", sep="|", header=FALSE, colClasses=svcgclass)
names(svcgfile_2019)=c('id_loan','svcg_cycle','current_upb','delq_sts','loan_age','mths_remng', 'repch_flag','flag_mod', 'cd_zero_bal', 'dt_zero_bal','current_int_rt','non_int_brng_upb','dt_lst_pi','mi_recoveries', 'net_sale_proceeds','non_mi_recoveries','expenses', 'legal_costs', 'maint_pres_costs','taxes_ins_costs','misc_costs','actual_loss', 'modcost')

# 2020
origfile_2020 <- read.table("sample_orig_2020.txt", sep="|", header=FALSE, colClasses=origclass )
names(origfile_2020)=c('fico','dt_first_pi','flag_fthb','dt_matr','cd_msa',"mi_pct",'cnt_units','occpy_sts','cltv','dti','orig_upb','ltv','int_rt','channel','ppmt_pnlty','prod_type','st', 'prop_type','zipcode','id_loan','loan_purpose', 'orig_loan_term','cnt_borr','seller_name','servicer_name', 'flag_sc')
svcgfile_2020 <- read.table("sample_svcg_2020.txt", sep="|", header=FALSE, colClasses=svcgclass)
names(svcgfile_2020)=c('id_loan','svcg_cycle','current_upb','delq_sts','loan_age','mths_remng', 'repch_flag','flag_mod', 'cd_zero_bal', 'dt_zero_bal','current_int_rt','non_int_brng_upb','dt_lst_pi','mi_recoveries', 'net_sale_proceeds','non_mi_recoveries','expenses', 'legal_costs', 'maint_pres_costs','taxes_ins_costs','misc_costs','actual_loss', 'modcost')

# 2013-2020
origfile_all = rbind(origfile_2013,origfile_2014,origfile_2015,origfile_2016,origfile_2017,origfile_2018,origfile_2019,origfile_2020)
svcgfile_all = rbind(svcgfile_2013,svcgfile_2014,svcgfile_2015,svcgfile_2016,svcgfile_2017,svcgfile_2018,svcgfile_2019,svcgfile_2020)

# Clean data:
# i) Identify loans with missing data
fico_remove = origfile_all$id_loan[origfile_all$fico==9999]
cltv_remove = origfile_all$id_loan[origfile_all$cltv==999]
dti_remove = origfile_all$id_loan[origfile_all$dti==999]
ltv_remove = origfile_all$id_loan[origfile_all$ltv==999]
ppmt_pnlty_remove = origfile_all$id_loan[origfile_all$ppmt_pnlty==""]
prod_type_remove = origfile_all$id_loan[origfile_all$prod_type=="_"]

# ii) Identify loans with foreclosed property
foreclosure_remove = svcgfile_all$id_loan[svcgfile_all$cd_zero_bal>1]
foreclosure_remove = foreclosure_remove[!is.na(foreclosure_remove)]

# Remove loans identified in i) and ii)
origfile_all = origfile_all[!(origfile_all$id_loan %in% c(fico_remove,cltv_remove,dti_remove,ltv_remove,ppmt_pnlty_remove,prod_type_remove,foreclosure_remove)), ]
svcgfile_all = svcgfile_all[!(svcgfile_all$id_loan %in% c(fico_remove,cltv_remove,dti_remove,ltv_remove,ppmt_pnlty_remove,prod_type_remove,foreclosure_remove)), ]

# Import 15Y weekly market mortgage rates (https://fred.stlouisfed.org/series/MORTGAGE15US)
library(openxlsx)
market_mortgage_rt = read.xlsx("MORTGAGE15US.xlsx", rows = c(11:429), colNames = TRUE)