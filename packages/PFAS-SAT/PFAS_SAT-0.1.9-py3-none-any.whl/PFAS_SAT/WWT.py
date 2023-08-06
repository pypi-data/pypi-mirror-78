# -*- coding: utf-8 -*-
"""
Created on Tue Aug 18 10:44:45 2020

@author: msmsa
"""
import pandas as pd
from .Flow import Flow
from .SubProcesses import split, mix, dewatering, drying
from .WWTInput import WWTInput
from .ProcessModel import ProcessModel


class WWT(ProcessModel):
    """
    Assumptions:
        1. No volatilization or degradation of PFAS.
        2. Steady state.
        3. Concentration in water remains constant.
        4. Annual time horizon.
    """
    ProductsType = ['WWTEffluent', 'DewateredWWTSolids', 'DriedWWTSolids', 'WWTSolids']

    def __init__(self, input_data_path=None, CommonDataObjct=None, InventoryObject=None, Name=None):
        super().__init__(CommonDataObjct, InventoryObject)
        self.InputData = WWTInput(input_data_path)
        self.Name = Name if Name else 'WWT'

    def calc(self, Inc_flow):
        # Initialize the Incoming flow
        self.Inc_flow = Inc_flow

        # Screen and Grit Removal
        rmvd_frac = self.InputData.Screen['frac_sr-grit']['amount']
        self.screen = split(self.Inc_flow, **{'effluent': 1-rmvd_frac, 'rmvd': rmvd_frac})

        # set properties for screen rejects
        self.screen['rmvd'].mass = self.screen['rmvd'].vol * 1 / (1 - self.InputData.Screen['sol_cont_sr_grit']['amount'])
        self.screen['rmvd'].ts = self.screen['rmvd'].mass * self.InputData.Screen['sol_cont_sr_grit']['amount']
        self.screen['rmvd'].C = 0 if self.Inc_flow.ts == 0 else self.screen['rmvd'].ts / self.Inc_flow.ts * self.Inc_flow.C
        self.screen['rmvd'].moist = self.screen['rmvd'].mass - self.screen['rmvd'].ts

        # Primary Settling
        rmvd_frac = self.InputData.PrimSet['is_prim_set']['amount'] * self.InputData.PrimSet['frac_prim_solids']['amount']
        self.prim_set = split(self.screen['effluent'], **{'effluent': 1-rmvd_frac, 'rmvd': rmvd_frac})

        # Set the mass flow for rmvd solids in Primary Settling
        self.prim_set['rmvd'].mass = self.prim_set['rmvd'].vol * 1 / (1 - self.InputData.PrimSet['sol_cont_prim_solids']['amount'])
        self.prim_set['rmvd'].ts = self.prim_set['rmvd'].mass * self.InputData.PrimSet['sol_cont_prim_solids']['amount']
        self.prim_set['rmvd'].C = 0 if self.Inc_flow.ts == 0 else self.prim_set['rmvd'].ts / self.Inc_flow.ts * self.Inc_flow.C
        self.prim_set['rmvd'].moist = self.prim_set['rmvd'].mass - self.prim_set['rmvd'].ts

        # Secondary Settling
        rmvd_frac = self.InputData.SecSet['is_sec_set']['amount'] * self.InputData.SecSet['frac_sec_solids']['amount']
        self.sec_set = split(self.prim_set['effluent'], **{'effluent': 1-rmvd_frac, 'rmvd': rmvd_frac})

        # Set the mass flow for rmvd solids in Secondary Settling
        self.sec_set['rmvd'].mass = self.sec_set['rmvd'].vol * 1 / (1 - self.InputData.SecSet['sol_cont_sec_solids']['amount'])
        self.sec_set['rmvd'].ts = self.sec_set['rmvd'].mass * self.InputData.SecSet['sol_cont_sec_solids']['amount']
        self.sec_set['rmvd'].C = 0 if self.Inc_flow.ts == 0 else self.sec_set['rmvd'].ts / self.Inc_flow.ts * self.Inc_flow.C
        self.sec_set['rmvd'].moist = self.sec_set['rmvd'].mass - self.sec_set['rmvd'].ts

        # Calc mass to Thickening
        if self.InputData.Thick['is_prim_thick']['amount'] and self.InputData.Thick['is_sec_thick']['amount']:
            self.flow_to_thick = mix(self.prim_set['rmvd'], self.sec_set['rmvd'])
        elif self.InputData.Thick['is_prim_thick']['amount']:
            self.flow_to_thick = self.prim_set['rmvd']
        elif self.InputData.Thick['is_sec_thick']['amount']:
            self.flow_to_thick = self.sec_set['rmvd']
        else:
            self.flow_to_thick = Flow()

        # Thickening: assumed that the removed water has the same PFAS concentration as input flow
        self.thick = {}
        self.thick['solids'], self.thick['rmvd_water'] = dewatering(mixture=self.flow_to_thick,
                                                                    final_sol_cont=self.InputData.Thick['sol_cont_thick']['amount'],
                                                                    cont_PFAS_water=self.Inc_flow.get_PFAScont(),
                                                                    is_active=True)

        # Dewatering: assumed that the removed water has the same PFAS concentration as input flow
        self.Dew = {}
        self.Dew['solids'], self.Dew['rmvd_water'] = dewatering(mixture=self.thick['solids'],
                                                                final_sol_cont=self.InputData.Dew['sol_cont_dewat']['amount'],
                                                                cont_PFAS_water=self.Inc_flow.get_PFAScont(),
                                                                is_active=self.InputData.Dew['is_sol_dew']['amount'])

        # Drying: assumed that the removed water has the same PFAS concentration as input flow
        self.Dry = {}
        if self.InputData.Dry['is_sol_dry']['amount']:
            self.Dry['solids'], self.Dry['DryerExhaust'] = drying(mixture=self.Dew['solids'],
                                                                  dryer_param=self.InputData.Dry,
                                                                  cont_PFAS_water=self.Inc_flow.get_PFAScont())
        else:
            self.Dry['solids'] = Flow()
            self.Dry['DryerExhaust'] = Flow()

        # Efflunet
        self.Efflunet = mix(self.sec_set['effluent'], self.thick['rmvd_water'], self.Dew['rmvd_water'])

        # add to Inventory
        self.Inventory.add('DryerExhaust', self.Name, 'Air', self.Dry['DryerExhaust'])

    def products(self):
        Products = {}
        Products['WWTSolids'] = self.screen['rmvd']
        Products['WWTEffluent'] = self.Efflunet
        if self.InputData.Dry['is_sol_dry']['amount']:
            Products['DewateredWWTSolids'] = Flow()
            Products['DriedWWTSolids'] = self.Dry['solids']
        else:
            Products['DewateredWWTSolids'] = self.Dew['solids']
            Products['DriedWWTSolids'] = Flow()
        return(Products)

    def setup_MC(self, seed=None):
        self.InputData.setup_MC(seed)

    def MC_Next(self):
        input_list = self.InputData.gen_MC()
        return(input_list)

    def report(self, normalized=False):
        report = pd.DataFrame(index=self.Inc_flow._PFAS_Index)
        if not normalized:
            report['Effluent'] = self.Efflunet.PFAS
            if self.InputData.Dry['is_sol_dry']['amount']:
                report['solids'] = self.Dry['solids'].PFAS
            else:
                report['solids'] = self.Dew['solids'].PFAS
            report['res'] = self.screen['rmvd'].PFAS
        else:
            report['Effluent'] = self.Efflunet.PFAS / self.Inc_flow.PFAS
            if self.InputData.Dry['is_sol_dry']['amount']:
                report['solids'] = self.Dry['solids'].PFAS / self.Inc_flow.PFAS
            else:
                report['solids'] = self.Dew['solids'].PFAS / self.Inc_flow.PFAS
            report['res'] = self.screen['rmvd'].PFAS / self.Inc_flow.PFAS
        return(report)
