# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 21:31:49 2020

@author: msmsa
"""
from abc import ABC, abstractmethod
from .CommonData import CommonData
from .Inventory import Inventory


class ProcessModel(ABC):
    def __init__(self, CommonDataObjct, InventoryObject):
        if CommonDataObjct:
            self.CommonData = CommonDataObjct
        else:
            self.CommonData = CommonData()

        if InventoryObject:
            self.Inventory = InventoryObject
        else:
            self.Inventory = Inventory()

    @property
    @abstractmethod
    def ProductsType(self):
        pass

    @abstractmethod
    def calc(self):
        pass

    @abstractmethod
    def setup_MC(self, seed=None):
        pass

    @abstractmethod
    def MC_Next(self):
        pass

    @abstractmethod
    def report(self):
        pass
