# -*- coding: utf-8 -*-
"""
@author: msardar2

PFAS_SAT
"""
try:
    from .GUI.PFAS_SAT_run import MyQtApp
    from PySide2 import QtWidgets
except ImportError:
    print("GUI is not imported")
import sys

# Import Main
from PFAS_SAT.Inventory import Inventory
from PFAS_SAT.IncomFlow import IncomFlow
from PFAS_SAT.Project import Project

# Import Input Data
from PFAS_SAT.MC import MC
from PFAS_SAT.InputData import InputData
from PFAS_SAT.CommonData import CommonData

# Import process models
from PFAS_SAT.ProcessModelsMetaData import ProcessModelsMetaData
from PFAS_SAT.ProcessModel import ProcessModel
from PFAS_SAT.Flow import Flow
from PFAS_SAT.Comp import Comp
from PFAS_SAT.LandApp import LandApp
from PFAS_SAT.Landfill import Landfill
from PFAS_SAT.WWT import WWT
from PFAS_SAT.Stab import Stab
from PFAS_SAT.AdvWWT import AdvWWT
from PFAS_SAT.ThermalTreatment import ThermalTreatment
from PFAS_SAT.AD import AD
from PFAS_SAT.SCWO import SCWO
from PFAS_SAT.SurfaceWaterRelease import SurfaceWaterRelease

__all__ = [
    'MyQtApp',
    'PFAS_SAT',
    'Flow',
    'Inventory',
    'IncomFlow',
    'Project',
    'ProcessModel',
    'Comp',
    'LandApp',
    'Landfill',
    'WWT',
    'Stab',
    'AdvWWT',
    'ThermalTreatment',
    'AD',
    'SCWO',
    'SurfaceWaterRelease',
    'ProcessModelsMetaData',
    'MC',
    'InputData',
    'CommonData'
    ]

__version__ = '0.1.9'


class PFAS_SAT():
    def __init__(self):
        self.app = QtWidgets.QApplication(sys.argv)
        self.qt_app = MyQtApp()
        self.qt_app.show()
        self.app.exec_()
