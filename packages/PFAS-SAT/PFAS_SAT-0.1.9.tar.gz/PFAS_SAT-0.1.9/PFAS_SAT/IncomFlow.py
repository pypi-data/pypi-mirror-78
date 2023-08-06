# -*- coding: utf-8 -*-
"""
Created on Fri Jul 24 11:48:31 2020

@author: msmsa
"""
from .Flow import Flow
from .IncomFlowInput import IncomFlowInput


class IncomFlow():
    def __init__(self, input_data_path=None):
        self.InputData = IncomFlowInput(input_data_path)
        wasteMaterils = self.InputData.Data['Dictonary_Name'].unique()
        wasteMaterilsFullName = self.InputData.Data['Category'].unique()
        self.WasteMaterials = []
        self.WasteMaterialsFullName = []
        self.WasteMaterialsNameHelper = {}

        for i in range(len(wasteMaterils)):
            if 'PFAS' not in wasteMaterils[i]:
                self.WasteMaterials.append(wasteMaterils[i])
            if 'PFAS' not in wasteMaterilsFullName[i]:
                self.WasteMaterialsFullName.append(wasteMaterilsFullName[i])
                self.WasteMaterialsNameHelper[wasteMaterilsFullName[i]] = wasteMaterils[i]

    def set_flow(self, flow_name, mass_flow):
        if flow_name in self.WasteMaterialsNameHelper:
            flow_name = self.WasteMaterialsNameHelper[flow_name]
        self._flow_name = flow_name
        self._mass_flow = mass_flow
        self.calc()

    def calc(self):
        # Initialize the Incoming flow
        self.Inc_flow = Flow()
        kwargs = {}
        Data = getattr(self.InputData, self._flow_name)
        for key, data in Data.items():
            kwargs[key] = data['amount']
        kwargs['mass_flow'] = self._mass_flow

        kwargs['PFAS_cont'] = {}
        PFAS_Data = getattr(self.InputData, self._flow_name+'_PFAS')
        for key, data in PFAS_Data.items():
            kwargs['PFAS_cont'][key] = data['amount']

        self.Inc_flow.set_flow(**kwargs)
        self.Inc_flow.set_FlowType(self._flow_name)

    def setup_MC(self, seed=None):
        self.InputData.setup_MC(seed)

    def MC_Next(self):
        input_list = self.InputData.gen_MC()
        return(input_list)

    def report(self):
        pass
