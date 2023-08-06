# -*- coding: utf-8 -*-
"""
Created on Fri Jul 24 11:48:31 2020

@author: msmsa
"""
import pandas as pd
from .Flow import Flow
from .SubProcesses import mix, aerobic_composting, curing
from .CompInput import CompInput
from .ProcessModel import ProcessModel


class Comp(ProcessModel):
    """
    Assumptions:
        1. No volatilization or degradation of PFAS.
        2. Steady state.
        3. Feedstocks, active piles, and curing piles are well mixed.
        4. Annual time horizon.
    """
    ProductsType = ['Compost', 'ContactWater']

    def __init__(self, input_data_path=None, CommonDataObjct=None, InventoryObject=None, Name=None):
        super().__init__(CommonDataObjct, InventoryObject)
        self.InputData = CompInput(input_data_path)
        self.Name = Name if Name else 'Composting'

    def calc(self, Inc_flow):
        # Initialize the Incoming flow
        self.Inc_flow = Inc_flow

        # Calculating the mass of Amendments
        Amnd_mass = self.InputData.AmndProp['mass_ratio']['amount'] * self.Inc_flow.mass

        # Initializing the Soil flow
        self.Amnd_flow = Flow()
        kwargs = {}
        kwargs['mass_flow'] = Amnd_mass
        kwargs['ts_cont'] = self.InputData.AmndProp['ts_cont']['amount']
        kwargs['C_cont'] = self.InputData.AmndProp['C_cont']['amount']
        self.Amnd_flow.set_flow(**kwargs)

        # Mixing the Incoming flow with soil
        self.Mix_to_ac = mix(self.Inc_flow, self.Amnd_flow)

        # Active Composting
        self.Mix_to_cu, self.Leachate_ac, self.RunOff_ac, self.Contact_water_ac = aerobic_composting(self.Mix_to_ac,
                                                                                                     self.InputData.AComp,
                                                                                                     self.InputData.LogPartCoef,
                                                                                                     self.InputData.Percip)

        # Curing
        self.Finished_Comp, self.Leachate_cu, self.RunOff_cu = curing(self.Mix_to_cu,
                                                                      self.InputData.Curing,
                                                                      self.InputData.LogPartCoef,
                                                                      self.InputData.Percip)

        self.Leachate = mix(self.Leachate_ac, self.Leachate_cu)
        self.RunOff = mix(self.RunOff_ac, self.RunOff_cu)
        self.Contact_water = self.Contact_water_ac

        # add to Inventory
        self.Inventory.add('Leachate', self.Name, 'Water', self.Leachate)
        self.Inventory.add('RunOff', self.Name, 'Water', self.RunOff)

    def products(self):
        Products = {}
        Products['Compost'] = self.Finished_Comp
        Products['ContactWater'] = self.Contact_water
        return(Products)

    def setup_MC(self, seed=None):
        self.InputData.setup_MC(seed)

    def MC_Next(self):
        input_list = self.InputData.gen_MC()
        return(input_list)

    def report(self, normalized=False):
        report = pd.DataFrame(index=self.Inc_flow._PFAS_Index)
        if not normalized:
            report['Finished Compost'] = self.Finished_Comp.PFAS
            report['Leachate'] = self.Leachate.PFAS
            report['RunOff'] = self.RunOff.PFAS
            report['Contact water'] = self.Contact_water.PFAS
        else:
            report['Finished Compost'] = self.Finished_Comp.PFAS / self.Inc_flow.PFAS
            report['Leachate'] = self.Leachate.PFAS / self.Inc_flow.PFAS
            report['RunOff'] = self.RunOff.PFAS / self.Inc_flow.PFAS
            report['Contact water'] = self.Contact_water.PFAS / self.Inc_flow.PFAS
        return(report)
