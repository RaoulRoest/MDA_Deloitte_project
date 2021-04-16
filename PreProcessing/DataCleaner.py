import pandas as pd

class DataCleaner():
    
    def get_ids_to_remove(self, dfOrig):
        ids_fico = self._get_ids(dfOrig, dfOrig["fico"] != 9999)
        ids_cltv = self._get_ids(dfOrig, dfOrig["cltv"] != 999)
        ids_dti = self._get_ids(dfOrig, dfOrig["dti"] != 999)
        ids_ltv = self._get_ids(dfOrig, dfOrig["ltv"] != 999)
        ids_ppmt_pnlty = self._get_ids(dfOrig, dfOrig["ppmt_pnlty"] != "")
        ids_prod_type = self._get_ids(dfOrig, dfOrig["prod_type"] != "_")
        
        ids = list(set(ids_fico + ids_cltv + ids_dti + ids_ltv + ids_ppmt_pnlty + ids_prod_type))
        
        return ids
        
    def clean_dfOriginate(self, dfOrig):
        ids = self.get_ids_to_remove(dfOrig)
        
    def _get_ids(self, df, condition):
        return df[condition].id_loan.unique().tolist()