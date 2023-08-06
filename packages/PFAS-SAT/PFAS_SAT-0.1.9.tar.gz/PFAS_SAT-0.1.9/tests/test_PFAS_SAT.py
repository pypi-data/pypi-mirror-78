# -*- coding: utf-8 -*-
"""
Created on Fri May  8 00:12:49 2020

@author: msmsa
"""
import PFAS_SAT as ps


def check_processmodel(process_model_cls, feed):
    Input = ps.IncomFlow()
    Input.set_flow(feed, 1000)
    Input.calc()
    model = process_model_cls()
    model.calc(Input.Inc_flow)
    model.report()
    model.report(normalized=True)
    model.setup_MC()
    model.MC_Next()
    model.calc(Input.Inc_flow)
    model.report()


def test_LandApp():
    check_processmodel(ps.LandApp, 'Compost')


def test_Comp():
    check_processmodel(ps.Comp, 'FoodWaste')


def test_Landfill():
    check_processmodel(ps.Landfill, 'MSW')


def test_WWT():
    check_processmodel(ps.WWT, 'LFLeachate')


def test_Stab():
    check_processmodel(ps.Stab, 'Compost')


def test_AdvWWT():
    check_processmodel(ps.AdvWWT, 'LFLeachate')


def test_SCWO():
    check_processmodel(ps.SCWO, 'LFLeachate')


def test_ThermalTreatment():
    check_processmodel(ps.ThermalTreatment, 'MSW')


def test_AD():
    check_processmodel(ps.AD, 'FoodWaste')


def test_SurfaceWaterRelease():
    check_processmodel(ps.SurfaceWaterRelease, 'ContaminatedWater')
