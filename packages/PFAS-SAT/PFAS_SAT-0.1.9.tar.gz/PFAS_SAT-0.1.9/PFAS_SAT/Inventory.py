# -*- coding: utf-8 -*-
"""
Created on Mon Jul 27 22:09:10 2020

@author: msmsa
"""
import pandas as pd
from .CommonData import CommonData
import numpy as np


class Inventory:
    def __init__(self):
        self._PFAS_Index = CommonData.PFAS_Index
        self._index = ['Flow_name', 'Source', 'Target', 'Unit'] + self._PFAS_Index
        self.Inv = pd.DataFrame(index=self._index)
        self.Col_index = 0

    def add(self, Flow_name, Source, Target, flow):
        data = [Flow_name, Source, Target, 'μg/year'] + list(np.round(flow.PFAS.values, 1))
        self.Inv[self.Col_index] = data
        self.Col_index += 1

    def report_Water(self):
        water_inv = self.Inv[self.Inv.columns[self.Inv.loc['Target'] == 'Water']]
        return(water_inv)

    def report_Soil(self):
        soil_inv = self.Inv[self.Inv.columns[self.Inv.loc['Target'] == 'Soil']]
        return(soil_inv)

    def report_Air(self):
        air_inv = self.Inv[self.Inv.columns[self.Inv.loc['Target'] == 'Air']]
        return(air_inv)

    def report_Destroyed(self):
        Destroyed_inv = self.Inv[self.Inv.columns[self.Inv.loc['Target'] == 'Destroyed']]
        return(Destroyed_inv)

    def report_Stored(self):
        Stored_inv = self.Inv[self.Inv.columns[self.Inv.loc['Target'] == 'Stored']]
        return(Stored_inv)

    def clear(self):
        self.Inv = pd.DataFrame(index=self._index)
        self.Col_index = 0

    def report(self, TypeOfPFAS='All'):
        if TypeOfPFAS == 'All':
            Index = self._PFAS_Index
        else:
            Index = [TypeOfPFAS]
        fp = 1
        report = dict()
        report['Water (10e-6g/year)'] = round(self.report_Water().loc[Index].sum(axis=1).sum(), fp)
        report['Soil (10e-6g/year)'] = round(self.report_Soil().loc[Index].sum(axis=1).sum(), fp)
        report['Air (10e-6g/year)'] = round(self.report_Air().loc[Index].sum(axis=1).sum(), fp)
        report['Destroyed (10e-6g/year)'] = round(self.report_Destroyed().loc[Index].sum(axis=1).sum(), fp)
        report['Stored (10e-6g/year)'] = round(self.report_Stored().loc[Index].sum(axis=1).sum(), fp)
        return(report)
