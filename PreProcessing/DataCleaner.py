import pandas as pd

# Custom modules
import DataCleaning as cleaning

class DataCleaner():
    
    def get_ids_to_remove(self, dfOrig, dfMonthly):
        ids_fico = self._get_ids(dfOrig, dfOrig["fico"] == 9999)
        ids_cltv = self._get_ids(dfOrig, dfOrig["cltv"] == 999)
        ids_dti = self._get_ids(dfOrig, dfOrig["dti"] == 999)
        ids_ltv = self._get_ids(dfOrig, dfOrig["ltv"] == 999)
        ids_prod_type = self._get_ids(dfOrig, dfOrig["prod_type"] == "_")
        
        dfOrig["ppmt_pnlty"] = dfOrig["ppmt_pnlty"].astype(str)
        ids_ppmt_pnlty = self._get_ids(dfOrig, (dfOrig["ppmt_pnlty"].str == "") | (dfOrig["ppmt_pnlty"].str.lower() == "nan"))
        
        ids_foreclosure_remove = self._get_ids(dfMonthly, dfMonthly["cd_zero_bal"] > 1)
                
        ids = list(set(ids_fico + ids_cltv + ids_dti + ids_ltv + ids_ppmt_pnlty + ids_prod_type + ids_foreclosure_remove))
        
        return ids
        
    def clean_data(self, dfOrig, dfMonthly):
        ids = self.get_ids_to_remove(dfOrig, dfMonthly)
        
        dfOrigClean = dfOrig[~dfOrig["id_loan"].isin(ids)].copy().reset_index()
        dfMonthlyClean = dfMonthly[~dfMonthly["id_loan"].isin(ids)].copy().reset_index()
        
        cleaning.clean_columns(dfOrigClean, dfMonthlyClean)
        
        return dfOrigClean, dfMonthlyClean
        
    def _get_ids(self, df, condition):
        return df[condition].id_loan.unique().tolist()