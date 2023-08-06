# -*- coding: utf-8 -*-
"""
Created on Fri Jul 31 20:48:42 2020

@author: msmsa
"""
ProcessModelsMetaData = {}

ProcessModelsMetaData['LandApp'] = {}
ProcessModelsMetaData['LandApp']['Name'] = 'Land Application'
ProcessModelsMetaData['LandApp']['File'] = 'LandApp.py'
ProcessModelsMetaData['LandApp']['InputType'] = ['Compost', 'Digestate', 'DriedWWTSolids']

ProcessModelsMetaData['Comp'] = {}
ProcessModelsMetaData['Comp']['Name'] = 'Composting'
ProcessModelsMetaData['Comp']['File'] = 'Comp.py'
ProcessModelsMetaData['Comp']['InputType'] = ['FoodWaste', 'DewateredWWTSolids']

ProcessModelsMetaData['AD'] = {}
ProcessModelsMetaData['AD']['Name'] = 'AD'
ProcessModelsMetaData['AD']['File'] = 'AD.py'
ProcessModelsMetaData['AD']['InputType'] = ['FoodWaste', 'DewateredWWTSolids']

ProcessModelsMetaData['Landfill'] = {}
ProcessModelsMetaData['Landfill']['Name'] = 'Landfill'
ProcessModelsMetaData['Landfill']['File'] = 'Landfill.py'
ProcessModelsMetaData['Landfill']['InputType'] = ['MSW', 'FoodWaste', 'Compost', 'SpentGAC', 'CompostResiduals',
                                                  'CombustionResiduals', 'DewateredWWTSolids', 'WWTSolids']

ProcessModelsMetaData['ThermalTreatment'] = {}
ProcessModelsMetaData['ThermalTreatment']['Name'] = 'Thermal Treatment'
ProcessModelsMetaData['ThermalTreatment']['File'] = 'ThermalTreatment.py'
ProcessModelsMetaData['ThermalTreatment']['InputType'] = ['MSW', 'FoodWaste', 'SpentGAC',
                                                          'DriedWWTSolids']

ProcessModelsMetaData['WWT'] = {}
ProcessModelsMetaData['WWT']['Name'] = 'WWT'
ProcessModelsMetaData['WWT']['File'] = 'WWT.py'
ProcessModelsMetaData['WWT']['InputType'] = ['ContactWater', 'LFLeachate', 'ContaminatedWater']

ProcessModelsMetaData['SCWO'] = {}
ProcessModelsMetaData['SCWO']['Name'] = 'SCWO'
ProcessModelsMetaData['SCWO']['File'] = 'SCWO.py'
ProcessModelsMetaData['SCWO']['InputType'] = []

ProcessModelsMetaData['AdvWWT'] = {}
ProcessModelsMetaData['AdvWWT']['Name'] = 'Advanced WWT'
ProcessModelsMetaData['AdvWWT']['File'] = 'AdvWWT.py'
ProcessModelsMetaData['AdvWWT']['InputType'] = ['WWTEffluent', 'ContaminatedWater']

ProcessModelsMetaData['Stab'] = {}
ProcessModelsMetaData['Stab']['Name'] = 'Stabilization'
ProcessModelsMetaData['Stab']['File'] = 'Stab.py'
ProcessModelsMetaData['Stab']['InputType'] = ['DewateredWWTSolids', 'ContaminatedSoil', 'RawWWTSolids']

ProcessModelsMetaData['SurfaceWaterRelease'] = {}
ProcessModelsMetaData['SurfaceWaterRelease']['Name'] = 'Surface Water Release'
ProcessModelsMetaData['SurfaceWaterRelease']['File'] = 'SurfaceWaterRelease.py'
ProcessModelsMetaData['SurfaceWaterRelease']['InputType'] = ['WWTEffluent']
