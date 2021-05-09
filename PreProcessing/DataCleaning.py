"""
Functions for cleaning the data:

For the originate data.
    Columns to drop: 
    	pre-HARP --> Drop (no values)
    	Harp_indicator --> Drop (no values)
    	Interest_only_indicator --> Drop (no values)
    
    Columns to enrich:
        flag_sc : Nan --> "N"
        
    Not enriched:
        cd_msa : numeric (Nan is fine)
    
For the monthly data:
    Columns to drop:
        mi_recoveries --> Drop (no values at all)
        net_sale_proceeds --> Drop (no values at all)
        non_mi_recoveries --> Drop (no values at all)
        expenses --> Drop (no values at all)
        legal_costs --> Drop (no values at all)
        maint_pres_costs --> Drop (no values at all)
        taxes_ins_costs --> Drop (no values at all)
        misc_costs --> Drop (no values at all)
        actual_loss --> Drop (no values at all)
        deliquent_accrued_interest --> Drop (no values at all)
    
    Columns to enrich:
        dt_lst_pi : Nan --> "Not available"
        dt_zero_bal : Nan --> "Not applicable"
        flag_mod : Nan --> "N"
        repch_flag : Nan --> "Y"
        defered_payment_plan : Nan --> "N"
        step_mod_flag : Nan --> " "
        delinquency_due_to_disaster : Nan --> "N"
        borrower_assistance_code : Nan --> "Not available"
        
    Not enriched: 
        cd_zero_bal -- No default value
        modcost -- numeric (Nan is fine)
        eltv -- numeric (Nan is fine)
        zero_balance_removal -- numeric (Nan is fine)
        
"""
import pandas as pd 

def get_orig_columns_to_drop():
    return [
        "pre-HARP",
        "Harp_indicator",
        "Interest_only_indicator",
    ]

def get_monthly_columns_to_drop():
    return [
        "mi_recoveries",
        "net_sale_proceeds",
        "non_mi_recoveries",
        "expenses",
        "legal_costs",
        "maint_pres_costs",
        "taxes_ins_costs",
        "misc_costs",
        "actual_loss",
        "deliquent_accrued_interest",
    ]

def drop_columns(df, dataType="Orig"):
    if(dataType == "Orig"):
        columns_to_drop = get_orig_columns_to_drop()
    else:
        columns_to_drop = get_monthly_columns_to_drop()
        
    df.drop(columns_to_drop, axis=1, inplace=True)

def get_orig_replace_dict():
    """
    Mapping of column to value to fill nan with.
    """
    return {
        "flag_sc" : "N",
    }

def get_monthly_replace_dict():
    """
    Mapping of column to value to fill nan with.
    """
    return {
        "dt_lst_pi" : "Not available",
        "dt_zero_bal" : "Not applicable",
        "flag_mod" : "N",
        "repch_flag" : "Y",
        "defered_payment_plan" : "N",
        "step_mod_flag" : " ",
        "delinquency_due_to_disaster" : "N",
        "borrower_assistance_code" : "Not available",        
    }

def clean_columns(dfOrig, dfMonthly):
    drop_columns(dfOrig, dataType="Orig")
    drop_columns(dfMonthly, dataType="Monthly")
    
    for k, v in get_orig_replace_dict().items():
        dfOrig[k].fillna(value=v, inplace=True)

    for k,v in get_monthly_replace_dict().items():
        dfMonthly[k].fillna(value=v, inplace=True)