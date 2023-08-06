# -*- coding: utf-8 -*-
"""
Created on Thu Jul 23 18:27:22 2020

@author: Mojtaba Sardarmehni
"""
from .InputData import InputData
from pathlib import Path


class CommonData(InputData):
    # waste Materials
    WasteMaterials = ['FoodWaste', 'Compost', 'Digestate',
                      'MSW', 'CombustionResiduals', 'CompostResiduals',
                      'ContaminatedSoil',
                      'LFLeachate', 'ContaminatedWater', 'ContactWater', 'WWTEffluent',
                      'RawWWTSolids', 'DewateredWWTSolids', 'DriedWWTSolids', 'WWTSolids',
                      'SCWOSteam', 'SCWOSlurry',
                      'SpentGAC', 'ROConcentrate']

    # PFAS Index
    PFAS_Index = ['Summed PFAS', 'PFOA', 'PFOS', 'PFAS#4', 'PFAS#5', 'PFAS#6',
                  'PFAS#7', 'PFAS#8', 'PFAS#9', 'PFAS#10']

    def __init__(self, input_data_path=None):
        if input_data_path:
            self.input_data_path = input_data_path
        else:
            self.input_data_path = Path(__file__).parent/'Data/CommonData.csv'

        # Initialize the superclass
        super().__init__(self.input_data_path)
