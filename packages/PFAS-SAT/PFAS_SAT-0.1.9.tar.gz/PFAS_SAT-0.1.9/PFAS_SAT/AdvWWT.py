# -*- coding: utf-8 -*-
"""
Created on Tue Aug 18 10:44:45 2020

@author: msmsa
"""
import pandas as pd
from .Flow import Flow
from .SubProcesses import split
from .AdvWWTInput import AdvWWTInput
from .ProcessModel import ProcessModel
import warnings


class AdvWWT(ProcessModel):
    """
    Assumptions:
        1. No volatilization or degradation of PFAS.
        2. Steady state.
        3. Concentration in water remains constant.
        4. Annual time horizon.
    """
    ProductsType = ['SpentGAC', 'ROConcentrate']

    def __init__(self, input_data_path=None, CommonDataObjct=None, InventoryObject=None, Name=None):
        super().__init__(CommonDataObjct, InventoryObject)
        self.InputData = AdvWWTInput(input_data_path)
        self.Name = Name if Name else 'Advanced WWT'

    def calc(self, Inc_flow):
        # Initialize the Incoming flow
        self.Inc_flow = Inc_flow

        # Allocation to RO and GAC
        if abs(self.InputData.Trtmnt_optn['frac_to_RO']['amount'] + self.InputData.Trtmnt_optn['frac_to_GAC']['amount'] - 1) > 0.01:
            warnings.warn("Sum of allocation factors to RO and GAC is not 1 \n Factors are normalized.")
            Total = self.InputData.Trtmnt_optn['frac_to_RO']['amount'] + self.InputData.Trtmnt_optn['frac_to_GAC']['amount']
            self.InputData.Trtmnt_optn['frac_to_RO']['amount'] = self.InputData.Trtmnt_optn['frac_to_RO']['amount'] / Total
            self.InputData.Trtmnt_optn['frac_to_GAC']['amount'] = self.InputData.Trtmnt_optn['frac_to_GAC']['amount'] / Total

        self.Allocted_vol = split(self.Inc_flow, **{'RO': self.InputData.Trtmnt_optn['frac_to_RO']['amount'],
                                                    'GAC': self.InputData.Trtmnt_optn['frac_to_GAC']['amount']})

        # RO
        # RO PFAS balance
        self.RO_effluent = Flow()
        self.RO_concentrate = Flow()
        self.RO_concentrate.PFAS = self.Allocted_vol['RO'].PFAS * self.InputData.RO['frac_PFAS_rem_eff']['amount']
        self.RO_effluent.PFAS = self.Allocted_vol['RO'].PFAS * (1 - self.InputData.RO['frac_PFAS_rem_eff']['amount'])

        # RO volume balance
        self.RO_concentrate.vol = max(sum(self.RO_concentrate.PFAS) / self.InputData.RO['rem_med_conc_pfas']['amount'],
                                      self.Allocted_vol['RO'].vol * self.InputData.RO['frac_effl_rem_med']['amount'])
        self.RO_effluent.vol = self.Allocted_vol['RO'].vol - self.RO_concentrate.vol

        # GAC
        # GAC PFAS balance
        self.GAC_effluent = Flow()
        self.SpentGAC = Flow()
        self.SpentGAC.PFAS = self.Allocted_vol['GAC'].PFAS * self.InputData.GAC['frac_PFAS_rem_eff']['amount']
        self.GAC_effluent.PFAS = self.Allocted_vol['GAC'].PFAS * (1 - self.InputData.GAC['frac_PFAS_rem_eff']['amount'])

        # Spent GAC
        self.SpentGAC.ts = self.Allocted_vol['GAC'].vol / self.InputData.GAC['Bed_vol_ratio']['amount'] * self.InputData.GAC['GAC_dens']['amount']
        self.SpentGAC.moist = self.Allocted_vol['GAC'].vol * self.InputData.GAC['frac_effl_rem_med']['amount'] / 1 * 1  # Water liter to kg
        self.SpentGAC.mass = self.SpentGAC.ts + self.SpentGAC.moist

        # GAC Volume balance
        self.GAC_effluent.vol = self.Allocted_vol['GAC'].vol - self.Allocted_vol['GAC'].vol * self.InputData.GAC['frac_effl_rem_med']['amount']

        # add to Inventory
        self.Inventory.add('Leachate', self.Name, 'Water', self.RO_effluent)
        self.Inventory.add('Storage', self.Name, 'Water', self.GAC_effluent)

    def products(self):
        Products = {}
        Products['ROConcentrate'] = self.RO_concentrate
        Products['SpentGAC'] = self.SpentGAC
        return(Products)

    def setup_MC(self, seed=None):
        self.InputData.setup_MC(seed)

    def MC_Next(self):
        input_list = self.InputData.gen_MC()
        return(input_list)

    def report(self, normalized=False):
        report = pd.DataFrame(index=self.Inc_flow._PFAS_Index)
        if not normalized:
            report['effluent_RO'] = self.RO_effluent.PFAS
            report['ROConcentrate'] = self.RO_concentrate.PFAS
            report['effluent_GAC'] = self.GAC_effluent.PFAS
            report['SpentGAC'] = self.SpentGAC.PFAS
        else:
            report['effluent_RO'] = self.RO_effluent.PFAS / self.Inc_flow.PFAS
            report['ROConcentrate'] = self.RO_concentrate.PFAS / self.Inc_flow.PFAS
            report['effluent_GAC'] = self.GAC_effluent.PFAS / self.Inc_flow.PFAS
            report['SpentGAC'] = self.SpentGAC.PFAS / self.Inc_flow.PFAS
        return(report)
