# -*- coding: utf-8 -*-
"""
Created on Tue Aug 18 10:44:45 2020

@author: msmsa
"""
import pandas as pd
from .Flow import Flow
from .SCWOInput import SCWOInput
from .ProcessModel import ProcessModel


class SCWO(ProcessModel):
    """
    Assumptions:
    1. Steady state.
    2. Annual time horizon.
    3. Assume all remaining PFAS in effluent.
    """
    ProductsType = ['SCWOSteam', 'SCWOSlurry']

    def __init__(self, input_data_path=None, CommonDataObjct=None, InventoryObject=None, Name=None):
        super().__init__(CommonDataObjct, InventoryObject)
        self.InputData = SCWOInput(input_data_path)
        self.Name = Name if Name else 'SCWO'

    def calc(self, Inc_flow):
        # Initialize the Incoming flow
        self.Inc_flow = Inc_flow

        # PFAS Balance
        self.Steam = Flow()
        self.Slurry = Flow()
        self.Effluent = Flow()

        for i in self.Inc_flow._PFAS_Index:
            self.Effluent.PFAS[i] = self.Inc_flow.PFAS[i] * (1 - self.InputData.DRE[i]['amount'])
            self.Slurry.PFAS[i] = self.Inc_flow.PFAS[i] * self.InputData.DRE[i]['amount'] * self.InputData.SCWO['frac_PFAS_to_slurry']['amount']
            self.Steam.PFAS[i] = self.Inc_flow.PFAS[i] * self.InputData.DRE[i]['amount'] * self.InputData.SCWO['frac_PFAS_to_steam']['amount']

        # Volume balance
        self.Slurry.vol = self.Inc_flow.vol * self.InputData.SCWO['frac_water_to_slurry']['amount']
        self.Steam.vol = self.Inc_flow.vol * self.InputData.SCWO['frac_water_to_steam']['amount']
        self.Effluent.vol = self.Inc_flow.vol - self.Slurry.vol - self.Steam.vol

        # add to Inventory
        self.Inventory.add('Effluent', self.Name, 'Water', self.Effluent)

    def products(self):
        Products = {}
        Products['SCWOSteam'] = self.Steam
        Products['SCWOSlurry'] = self.Slurry
        return(Products)

    def setup_MC(self, seed=None):
        self.InputData.setup_MC(seed)

    def MC_Next(self):
        input_list = self.InputData.gen_MC()
        return(input_list)

    def report(self, normalized=False):
        report = pd.DataFrame(index=self.Inc_flow._PFAS_Index)
        if not normalized:
            report['Effluent'] = self.Effluent.PFAS
            report['Slurry'] = self.Slurry.PFAS
            report['Steam'] = self.Steam.PFAS
        else:
            report['Effluent'] = self.Effluent.PFAS / self.Inc_flow.PFAS
            report['Slurry'] = self.Slurry.PFAS / self.Inc_flow.PFAS
            report['Steam'] = self.Steam.PFAS / self.Inc_flow.PFAS
        return(report)
