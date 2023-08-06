# -*- coding: utf-8 -*-
"""
Created on Tue Jul 21 11:51:33 2020

@author: msmsa
"""
import pandas as pd
from .Flow import Flow
from .SubProcesses import mix, soil_sorption
from .LandAppInput import LandAppInput
from .ProcessModel import ProcessModel


class LandApp(ProcessModel):
    """
    Assumptions:
        1. No volatilization or degradation of PFAS.
        2. Steady state.
        3. Soil and amendments are well mixed.
        4. Annual time horizon.
    """
    ProductsType = []

    def __init__(self, input_data_path=None, CommonDataObjct=None, InventoryObject=None, Name=None):
        super().__init__(CommonDataObjct, InventoryObject)
        self.InputData = LandAppInput(input_data_path)
        self.Name = Name if Name else 'Land Application'

    def calc(self, Inc_flow):
        # Initialize the Incoming flow
        self.Inc_flow = Inc_flow

        # Calculating the mass of soil mixed with the Incoming flow
        soil_mass_mix = self.InputData.LandApp['depth_mix']['amount'] * self.Inc_flow.ts \
            / self.InputData.LandApp['appl_dens']['amount'] * self.InputData.SoilProp['bulk_dens']['amount']

        # Initializing the Soil flow
        self.Soil_flow = Flow()
        kwargs = {}
        for key, data in self.InputData.SoilProp.items():
            kwargs[key] = data['amount']
        kwargs['mass_flow'] = soil_mass_mix
        self.Soil_flow.set_flow(**kwargs)

        # Mixing the Incoming flow with soil
        self.Mixed_flow = mix(self.Inc_flow, self.Soil_flow)

        # Calculating the volume of percipitation (includes RunOff and Leachate)
        Percip_Vol = self.Inc_flow.ts / self.InputData.LandApp['appl_dens']['amount'] * self.InputData.Percip['ann_precip']['amount'] * 1000  # L/yr
        Leachate_Vol = Percip_Vol * self.InputData.Percip['frac_leach']['amount']  # L/yr
        RunOff_Vol = Percip_Vol * self.InputData.Percip['frac_runoff']['amount']  # L/yr

        # Calculating the PFAS in water and soil partitions
        self.Remaining, self.Leachate, self.RunOff = soil_sorption(self.Mixed_flow, self.InputData.LogPartCoef, Leachate_Vol, RunOff_Vol)

        # add to Inventory
        self.Inventory.add('Leachate', self.Name, 'Water', self.Leachate)
        self.Inventory.add('RunOff', self.Name, 'Water', self.RunOff)
        self.Inventory.add('Remaining', self.Name, 'Soil', self.Remaining)

    def products(self):
        Products = {}
        return(Products)

    def setup_MC(self, seed=None):
        self.InputData.setup_MC(seed)

    def MC_Next(self):
        input_list = self.InputData.gen_MC()
        return(input_list)

    def report(self, normalized=False):
        report = pd.DataFrame(index=self.Inc_flow._PFAS_Index)
        if not normalized:
            report['Remaining'] = self.Remaining.PFAS
            report['Leachate'] = self.Leachate.PFAS
            report['RunOff'] = self.RunOff.PFAS
        else:
            report['Remaining'] = self.Remaining.PFAS / self.Inc_flow.PFAS
            report['Leachate'] = self.Leachate.PFAS / self.Inc_flow.PFAS
            report['RunOff'] = self.RunOff.PFAS / self.Inc_flow.PFAS
        return(report)
