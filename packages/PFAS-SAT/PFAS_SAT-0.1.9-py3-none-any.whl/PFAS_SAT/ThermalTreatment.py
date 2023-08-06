# -*- coding: utf-8 -*-
"""
Created on Tue Aug 18 10:44:45 2020

@author: msmsa
"""
import pandas as pd
from .Flow import Flow
from .ThermalTreatmentInput import ThermalTreatmentInput
from .ProcessModel import ProcessModel


class ThermalTreatment(ProcessModel):
    """
    Assumptions:
        1. Steady state.
        2. Waste is well-mixed.
        3. Annual time horizon.
        4. No PFAS in wastewater streams
    """
    ProductsType = ['CombustionResiduals']

    def __init__(self, input_data_path=None, CommonDataObjct=None, InventoryObject=None, Name=None):
        super().__init__(CommonDataObjct, InventoryObject)
        self.InputData = ThermalTreatmentInput(input_data_path)
        self.Name = Name if Name else 'Thermal Treatment'

    def calc(self, Inc_flow):
        # Initialize the Incoming flow
        self.Inc_flow = Inc_flow

        # PFAS Balance
        self.CombRes = Flow()
        self.Exhaust = Flow()
        self.Destructed = Flow()
        for i in self.Inc_flow._PFAS_Index:
            self.Exhaust.PFAS[i] = self.Inc_flow.PFAS[i] * (1 - self.InputData.DRE[i]['amount'])
            self.CombRes.PFAS[i] = self.Inc_flow.PFAS[i] * self.InputData.DRE[i]['amount'] * self.InputData.Frac_to_res[i]['amount']
            self.Destructed.PFAS[i] = self.Inc_flow.PFAS[i] * self.InputData.DRE[i]['amount'] * (1 - self.InputData.Frac_to_res[i]['amount'])

        # Combustion Residual
        self.CombRes.ts = self.Inc_flow.ts * self.InputData.Comb_param['frac_sol_to_res']['amount']
        self.CombRes.mass = self.CombRes.ts / self.InputData.Comb_param['res_ts_cont']['amount']
        self.CombRes.moist = self.CombRes.mass - self.CombRes.ts

        # add to Inventory
        self.Inventory.add('Exhaust', self.Name, 'Air', self.Exhaust)
        self.Inventory.add('Destructed', self.Name, 'Destroyed', self.Destructed)

    def products(self):
        Products = {}
        Products['CombustionResiduals'] = self.CombRes
        return(Products)

    def setup_MC(self, seed=None):
        self.InputData.setup_MC(seed)

    def MC_Next(self):
        input_list = self.InputData.gen_MC()
        return(input_list)

    def report(self, normalized=False):
        report = pd.DataFrame(index=self.Inc_flow._PFAS_Index)
        if not normalized:
            report['Exhaust'] = self.Exhaust.PFAS
            report['CombustionResiduals'] = self.CombRes.PFAS
            report['Destructed'] = self.Destructed.PFAS
        else:
            report['Exhaust'] = self.Exhaust.PFAS / self.Inc_flow.PFAS
            report['CombustionResiduals'] = self.CombRes.PFAS / self.Inc_flow.PFAS
            report['Destructed'] = self.Destructed.PFAS / self.Inc_flow.PFAS
        return(report)
