# -*- coding: utf-8 -*-
"""
Created on Tue Aug 18 10:44:45 2020

@author: msmsa
"""
import pandas as pd
from .Flow import Flow
from .ADInput import ADInput
from .ProcessModel import ProcessModel
from .SubProcesses import split, curing


class AD(ProcessModel):
    """
    Assumptions:
    1. No volatilization or degradation of PFAS.
    2. Steady state.
    3. Waste is well-mixed.
    4. Annual time horizon.
    5. C content of solids does not change.
    6. No water loss during AD.
    """
    ProductsType = ['Digestate', 'Compost']

    def __init__(self, input_data_path=None, CommonDataObjct=None, InventoryObject=None, Name=None):
        super().__init__(CommonDataObjct, InventoryObject)
        self.InputData = ADInput(input_data_path)
        self.Name = Name if Name else 'AD'

    def calc(self, Inc_flow):
        # Initialize the Incoming flow
        self.Inc_flow = Inc_flow

        # PFAS Balance
        self.Volatilization = Flow()
        self.Digestate_product = Flow()
        self.Volatilization.PFAS = self.Inc_flow.PFAS * self.InputData.AD['frac_PFAS_to_Vol']['amount']
        self.Digestate_product.PFAS = self.Inc_flow.PFAS - self.Volatilization.PFAS

        # Mass balance
        vs_loss = self.Inc_flow.VS * self.InputData.AD['frac_VS_loss']['amount']
        self.Digestate_product.ts = self.Inc_flow.ts - vs_loss
        self.Digestate_product.moist = self.Inc_flow.moist
        self.Digestate_product.mass = self.Digestate_product.moist + self.Digestate_product.ts
        self.Digestate_product.C = self.Inc_flow.get_Ccont() * self.Digestate_product.ts  # Assume C content of solids does not change.

        # Allocate digestate to Curing
        frac_curing = self.InputData.AD['frac_cured']['amount']
        self.Digestate = split(self.Digestate_product, **{'Digestate': 1-frac_curing, 'to_curing': frac_curing})

        # Curing
        self.Finished_Comp, self.Leachate_cu, self.RunOff_cu = curing(self.Digestate['to_curing'],
                                                                      self.InputData.Curing,
                                                                      self.InputData.LogPartCoef,
                                                                      self.InputData.Percip)

        # add to Inventory
        self.Inventory.add('Volatilization', self.Name, 'Air', self.Volatilization)
        self.Inventory.add('Leachate', self.Name, 'Water', self.Leachate_cu)
        self.Inventory.add('RunOff', self.Name, 'Water', self.RunOff_cu)

    def products(self):
        Products = {}
        Products['Digestate'] = self.Digestate['Digestate']
        Products['Compost'] = self.Finished_Comp
        return(Products)

    def setup_MC(self, seed=None):
        self.InputData.setup_MC(seed)

    def MC_Next(self):
        input_list = self.InputData.gen_MC()
        return(input_list)

    def report(self, normalized=False):
        report = pd.DataFrame(index=self.Inc_flow._PFAS_Index)
        if not normalized:
            report['Volatilization'] = self.Volatilization.PFAS
            report['Digestate'] = self.Digestate['Digestate'].PFAS
            report['Finished Compost'] = self.Finished_Comp.PFAS
            report['Leachate'] = self.Leachate_cu.PFAS
            report['RunOff'] = self.RunOff_cu.PFAS
        else:
            report['Volatilization'] = self.Volatilization.PFAS / self.Inc_flow.PFAS
            report['Digestate'] = self.Digestate['Digestate'].PFAS / self.Inc_flow.PFAS
            report['Finished Compost'] = self.Finished_Comp.PFAS / self.Inc_flow.PFAS
            report['Leachate'] = self.Leachate_cu.PFAS / self.Inc_flow.PFAS
            report['RunOff'] = self.RunOff_cu.PFAS / self.Inc_flow.PFAS
        return(report)
