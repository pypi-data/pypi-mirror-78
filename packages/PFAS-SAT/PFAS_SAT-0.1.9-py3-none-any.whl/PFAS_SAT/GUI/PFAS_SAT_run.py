# -*- coding: utf-8 -*-
"""
Created on Thu Jul  9 11:39:58 2020

@author: msmsa
"""
# Import UI
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtWebEngineWidgets import QWebEngineView, QWebEngineDownloadItem, QWebEngineProfile
from .Table_from_pandas import *
from . import PFAS_SAT_ui
from . import MC_ui
from . import SA_ui
from . import HelpGuide_ui
from .Workers import Worker_MC, Worker_Plot

# Import Top level
import os
import io
import csv
import sys
import ast
import pickle
import importlib  #to import moduls with string name

# Import General
import pandas as pd
import numpy as np
from time import time
from copy import deepcopy
from pathlib import Path


# Import PFAS_SAT
from .. IncomFlow import IncomFlow
from .. CommonData import CommonData
from .. Inventory import Inventory
from .. Project import Project
from .. ProcessModelsMetaData import ProcessModelsMetaData

# Import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.pyplot as plt


class MyQtApp(PFAS_SAT_ui.Ui_PFAS_SAT, QtWidgets.QMainWindow):
    def __init__(self):
        super(MyQtApp,self).__init__()
        self.setupUi(self)
        self.init_app()

        self.WM_tab.setDisabled(True)
        self.PM_tab.setDisabled(True)
        self.SYS_tab.setDisabled(True)
        self.FA_tab.setDisabled(True)
        self.MC_tab.setDisabled(True)
        self.SA_tab.setDisabled(True)
                
        self.WM_tab_init_status = False
        self.PM_tab_init_status = False
        self.SYS_tab_init_status = False
        self.FA_tab_init_status = False
        self.MC_tab_init_status = False
        self.SA_tab_init_status = False
        
        ### Menu
        self.actionHelp_Gui.triggered.connect(self.Help_Gui_func)

        # Icon
        self.icon = QtGui.QIcon()
        self.icon.addPixmap(QtGui.QPixmap(":/icons/ICONS/PFAS_SAT_1.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

    def init_app(self):
        self.PFAS_SAT_1.setCurrentWidget(self.Start_tab)
        
        #Radio bottoms
        self.Start_def_process.setChecked(True)
        
        #bottoms connection
        self.Start_new_project.clicked.connect(self.Start_new_project_func)
        
    
    @QtCore.Slot()
    def Start_new_project_func(self):
        if self.Start_user_process.isChecked():
            self.init_WM_tab()
            self.PFAS_SAT_1.setCurrentWidget(self.WM_tab)
        else:
            self.IncomFlow = IncomFlow()
            
            self.ListOfProcessModels = list(ProcessModelsMetaData.keys())
            self.AllProcessModels = {}
            for P in self.ListOfProcessModels:
                self.AllProcessModels[P]={}
                self.AllProcessModels[P]['Default']=True
                self.AllProcessModels[P]['InputDataPath']=None
                self.AllProcessModels[P]['Name']= ProcessModelsMetaData[P]['Name']
                self.AllProcessModels[P]['InputType']=[]
                for flow in ProcessModelsMetaData[P]['InputType']:
                    self.AllProcessModels[P]['InputType'].append(flow)
            
            self.import_PM_init_SYS()

    
#%% WM tab          
# =============================================================================
# =============================================================================
    ### Waste Materials tab
# =============================================================================
# =============================================================================   
    def init_WM_tab(self):
        if not self.WM_tab_init_status:
            self.WM_tab.setEnabled(True)
            self.IncomFlow = IncomFlow()
            self.WM_Combo.clear()
            self.WM_Combo.currentTextChanged.connect(self.Load_Waste_Prop_func)
            self.WM_Combo.addItems(self.IncomFlow.WasteMaterialsFullName)
            
            self.Clear_WM_uncert.clicked.connect(self.Clear_WM_Uncert_func)
            self.Update_WM_prop.clicked.connect(self.Update_WM_prop_func)
            self.Def_Proc_models.clicked.connect(self.init_PM_tab_func)
            
            self.WM_tab_init_status = True
        
    
    @QtCore.Slot(str)
    def Load_Waste_Prop_func(self,waste):
        data = self.IncomFlow.InputData.Data[:][(self.IncomFlow.InputData.Data['Category']== waste) | (self.IncomFlow.InputData.Data['Category']==waste+' PFAS Concentration')]
        Waste_Prop_model = Table_from_pandas_editable(data)
        self.WM_table_prop.setModel(Waste_Prop_model)
        self.WM_table_prop.resizeColumnsToContents()
    
    @QtCore.Slot()
    def Clear_WM_Uncert_func(self):
        self.WM_table_prop.model()._data['uncertainty_type'] = 0
        self.WM_table_prop.model()._data[['loc','scale','shape','minimum','maximum']] = np.nan
        self.WM_table_prop.model().layoutChanged.emit()
        self.WM_table_prop.resizeColumnsToContents()

    @QtCore.Slot()
    def Update_WM_prop_func(self):
        self.IncomFlow.InputData.Update_input(self.WM_table_prop.model()._data)
        self.msg_popup('Updata Input Data','The data is updated successfully.','Information')

#%% PM tab          
# =============================================================================
# =============================================================================
    ### Process Models tab
# =============================================================================
# =============================================================================           
    @QtCore.Slot()
    def init_PM_tab_func(self):
        if not self.PM_tab_init_status:
            self.PM_tab.setEnabled(True)
            
            # Disable flows that are not modeled.
            self.Med_Waste.setDisabled(True)
            self.MOSP.setDisabled(True)
            self.AutoShredRes.setDisabled(True)

            self._InputKey = {'MSW': self.MSW,
                            'C&DWaste': self.C_D_Waste,
                            'Med_Waste': self.Med_Waste,
                            'MOSP': self.MOSP,
                            'FoodWaste': self.FW,
                            'Compost': self.Compost,
                            'Digestate': self.Digestate,
                            'CompostResiduals': self.CompRes,
                            'MRFRes': self.MRFRes,
                            'CombustionResiduals': self.CombRes,
                            'AutoShredRes': self.AutoShredRes,
                            'ContaminatedWater': self.ContWater,
                            'ContaminatedSoil': self.ContSoil,
                            'WWTEffluent': self.WWTEffluent,
                            'DewateredWWTSolids': self.DewWWTSol,
                            'DriedWWTSolids': self.DryWWTSol,
                            'RawWWTSolids': self.RawWWTSol,
                            'WWTSolids': self.WWTSol,
                            'ROConcentrate': self.ROC,
                            'LFLeachate': self.LFLeach,
                            'ContactWater': self.ContactWater,
                            'Solidi_Waste': self.Solidi_Waste,
                            'SpentGAC': self.SGAC,
                            'SIER': self.SIER,
                            'AFFF': self.AFFF}
            for CheckBox in self._InputKey.values():
                CheckBox.setChecked(False)
    
            self.ListOfProcessModels = list(ProcessModelsMetaData.keys())
            self.AllProcessModels = {}
            for P in self.ListOfProcessModels:
                self.AllProcessModels[P]={}
                self.AllProcessModels[P]['Default']=True
                self.AllProcessModels[P]['InputDataPath']=None
                self.AllProcessModels[P]['Name']= ProcessModelsMetaData[P]['Name']
                self.AllProcessModels[P]['InputType']=[]
                for flow in ProcessModelsMetaData[P]['InputType']:
                    self.AllProcessModels[P]['InputType'].append(flow)
            
            self.ProcessNamehelper={}
            for key,val in ProcessModelsMetaData.items():
                self.ProcessNamehelper[val['Name']] = key

            self.ProcModel_Combo.clear()
            self.ProcModel_Combo.currentTextChanged.connect(self.load_PM_metadata)
            self.ProcModel_Combo.addItems(list(self.ProcessNamehelper.keys()))
            
            self.ProcModel_Brow_Input.clicked.connect(self.select_file(self.ProcModel_Input_path,"CSV (*.csv)"))
            self.ProcModel_update.clicked.connect(self.update_PM_metadata)
            self.ProcModel_clear.clicked.connect(self.clear_PM_metadata)
            self.Def_System.clicked.connect(self.import_PM_init_SYS)
            
            self.PM_tab_init_status = True
        
        self.PFAS_SAT_1.setCurrentWidget(self.PM_tab)
                
    @QtCore.Slot(str)
    def load_PM_metadata(self,process):
        process = self.ProcessNamehelper[process]
        self.ProcModel_def_input.setChecked(self.AllProcessModels[process]['Default'])
        
        if self.AllProcessModels[process]['InputDataPath']:
            self.ProcModel_Input_path.setText(self.AllProcessModels[process]['InputDataPath'])
        else:
            self.ProcModel_Input_path.setText(None)

        for CheckBox in self._InputKey.values():
            CheckBox.setChecked(False)
        
        for flow in self.AllProcessModels[process]['InputType']:
            self._InputKey[flow].setChecked(True)
    
    @QtCore.Slot()
    def update_PM_metadata(self):
        Process = self.ProcessNamehelper[self.ProcModel_Combo.currentText()]
        self.AllProcessModels[Process]['Default']=self.ProcModel_def_input.isChecked()
        if self.ProcModel_user_input.isChecked():
            self.AllProcessModels[Process]['InputDataPath']= self.ProcModel_Input_path.text()
        else:
            self.AllProcessModels[Process]['InputDataPath']= None
        
        self.AllProcessModels[Process]['InputType']=[]
        for flow,CheckBox in self._InputKey.items():
            if CheckBox.isChecked():
                self.AllProcessModels[Process]['InputType'].append(flow)
        self.msg_popup('Updata Process Model','The input data for the process model ({}) is updated successfully.'.format(self.ProcModel_Combo.currentText()),'Information')

    @QtCore.Slot()
    def clear_PM_metadata(self):
        self.ProcModel_def_input.setChecked(True)
        self.ProcModel_Input_path.setText(None)
        for flow,CheckBox in self._InputKey.items():
            CheckBox.setChecked(False)
            
    @QtCore.Slot()
    def import_PM_init_SYS(self):
        self.CommonData = CommonData()
        self.Inventory = Inventory()
        for proc in self.AllProcessModels:
            clas_name= proc
            clas_file=  ProcessModelsMetaData[proc]['File'].split('.')[0]
            module = importlib.import_module('PFAS_SAT.'+clas_file)
            model = module.__getattribute__(clas_name)
            self.AllProcessModels[proc]['Model'] = model(input_data_path=self.AllProcessModels[proc]['InputDataPath'],
                                                         CommonDataObjct=self.CommonData,
                                                         InventoryObject=self.Inventory,
                                                         Name=self.AllProcessModels[proc]['Name'])
        
        print('\n \n All the process models: \n {} \n\n'.format(self.AllProcessModels))
        self.init_SYS_tab_func()
        
    
#%% SYS tab          
# =============================================================================
# =============================================================================
    ### Define System tab
# =============================================================================
# =============================================================================            
    @QtCore.Slot()
    def init_SYS_tab_func(self):
        if not self.SYS_tab_init_status:
            self.SYS_tab.setEnabled(True)
            self.FU.clear()
            self.FU.addItems(self.IncomFlow.WasteMaterialsFullName)
            self.FU_unit.setText('Kg/Year')
            self.FU_amount.setText('1000')
            self.reset.clicked.connect(self.clear_project_setup)
            self.InitProject_Buttom.clicked.connect(self.init_project)
            self.Set_ProcessSet.clicked.connect(self.set_process_set_func)
            self.Update_Flowparams.clicked.connect(self.set_flow_params_func)
            self.FA_Btm.clicked.connect(self.init_FA_tab_func)
            self.MC_Btm.clicked.connect(self.init_MC_tab_func)
            self.SA_Btm.clicked.connect(self.init_SA_tab_func)
            
            self.init_project_status = True
            
            self.SYS_tab_init_status = True
        
        self.PFAS_SAT_1.setCurrentWidget(self.SYS_tab)
        
    def init_project(self):
        if self.SYS_tab_init_status:
            self.IncomFlow.set_flow(self.FU.currentText(),float(self.FU_amount.text()))
            self.Project = Project(Inventory=self.Inventory,CommonData=self.CommonData,ProcessModels=self.AllProcessModels)
            Process_set=self.Project.get_process_set(self.IncomFlow.Inc_flow)
            self.Process_set_dict={}
            self.Layout = QtWidgets.QGridLayout(self.ProcessSetFrame)
            row=0
            col=0
            for P in Process_set:
                self.Process_set_dict[P] = QtWidgets.QCheckBox(self.ProcessSetFrame)
                self.Process_set_dict[P].setObjectName(P)
                self.Process_set_dict[P].setText(self.AllProcessModels[P]['Name'])
                self.Process_set_dict[P].setChecked(True)
                self.Layout.addWidget(self.Process_set_dict[P],row,col)
                col+=1
                if col==2:
                    col=0
                    row+=1
            self.SYS_tab_init_status=False
            return(None)
        if not self.SYS_tab_init_status:
            self.msg_popup('Error: Create new scenario', 'Reset the scenario to start a new one','Warning')
            
            
        
    @QtCore.Slot()
    def clear_project_setup(self):
        self.Process_set_dict = {}
        self.Layout = None
        for Layout in self.ProcessSetFrame.findChildren(QtWidgets.QGridLayout):
            for Checkbox in Layout.findChildren(QtWidgets.QCheckBox):
                Checkbox.deleteLater()
            Layout.deleteLater()
        for Checkbox in self.ProcessSetFrame.findChildren(QtWidgets.QCheckBox):
            Checkbox.deleteLater()
        self.Network_ImageLable.clear()
        self.FlowParams_TreeView.setModel(None)
        self.SYS_tab_init_status=True
        QtWidgets.QApplication.processEvents()
        self.MC_tab.setEnabled(False)
        self.FA_tab.setEnabled(False)
            
    @QtCore.Slot()
    def set_process_set_func(self):
        process_set = []
        for key,val in self.Process_set_dict.items():
            if val.isChecked():
                process_set.append(key)
        
        self.Project.set_process_set(process_set)
        print('\n Process set: {} \n'.format(process_set))
        
        self.FlowParams = self.Project.get_flow_params()
        print(self.FlowParams)
        
        model = TreeView(self.FlowParams)
        self.FlowParams_TreeView.setModel(model)
        self.FlowParams_TreeView.expandAll()
        self.FlowParams_TreeView.resizeColumnToContents(0)


    @QtCore.Slot()
    def set_flow_params_func(self):
        flowparams = self.FlowParams_TreeView.model().model_to_dict()
        print('\n flow paramters: {}\n \n '.format(flowparams))
        try:
            self.Project.set_flow_params(flowparams)
        except ValueError as msg:
            self.msg_popup('Error', str(msg),'Warning')
            
        self.Project.setup_network()
        
        ### Plot Network
        self.Project.plot_network(view=False)
        image = QtGui.QImage('Network.png')
        pixmap = QtGui.QPixmap(image)
        self.Network_ImageLable.setPixmap(pixmap)
                
#%% FA tab          
# =============================================================================
# =============================================================================
    ### Define Flow analysis tab
# =============================================================================
# =============================================================================            
    @QtCore.Slot()
    def init_FA_tab_func(self):
        if not self.FA_tab_init_status:
            self.FA_tab.setEnabled(True)
        
            # connect the signal for download file
            QWebEngineProfile.defaultProfile().downloadRequested.connect(self.on_downloadRequested)
            
            # set the htm webEngine
            self.html_figur = QWebEngineView(parent=self.Sankey_groupBox)
            self.Sankey_layout.addWidget(self.html_figur)
            
            self.FA_tab_init_status = True
        
        self.FA_tab.setEnabled(True)
        self.PFAS_SAT_1.setCurrentWidget(self.FA_tab)
        
        self.Project.setup_network()
        
        ### Inventory Table
        model = Table_from_pandas(self.Project.Inventory.Inv)
        self.Inventory_table.setModel(model)
        self.Inventory_table.resizeColumnsToContents()
                    
        ### Plot Sankey
        plot_worker = Worker_Plot(parent=self.FA_Btm, project = self.Project)
        plot_worker.Plot.connect(self.setup_sankey)
        plot_worker.start()
        
    @QtCore.Slot()
    def setup_sankey(self):
        self.html_figur.setUrl(QtCore.QUrl.fromLocalFile(os.getcwd()+'\\sankey.html'))
        


#%% MC tab          
# =============================================================================
# =============================================================================
    ### Define MC tab
# =============================================================================
# =============================================================================  
    @QtCore.Slot()
    def init_MC_tab_func(self):
        if not self.MC_tab_init_status:
            self.MC_tab.setEnabled(True)
            self.MC_N_runs.setMinimum(1)
            self.MC_N_runs.setMaximum(1000000)
            self.MC_PBr.setMaximum(100)
            self.MC_PBr.setMinimum(0)
            self.MC_PBr.setValue(0)
            self.MC_Model.currentTextChanged.connect(self.show_inputdata)
            self.MC_unceratin_clear.clicked.connect(self.Clear_MC_Uncert_func)
            self.MC_uncertain_update.clicked.connect(self.Update_MC_Uncert_func)
            self.MC_run.clicked.connect(self.MC_Run_func)
            self.MC_show.clicked.connect(self.show_res_func)
            self.MC_save.clicked.connect(self.MC_save_file())
            self.MC_uncertain_filter.clicked.connect(self.MC_uncertain_filter_func)
            self.MC_tab_init_status = True            
        
        self.MC_tab.setEnabled(True)
        self.PFAS_SAT_1.setCurrentWidget(self.MC_tab)    
        self.MC_Model.clear()
        self.MC_Model.addItems(['IncomFlow']+[self.Project.ProcessModels[p]['Name'] for p in self.Project.ProcessSet])
    
    @QtCore.Slot(str)
    def show_inputdata(self,process):
        if process == '':
            pass
        elif process == 'IncomFlow':
            self._uncertain_data = self.IncomFlow.InputData.Data
        else:
            self._uncertain_data = self.Project.ProcessModels[self.Project._ProcessNameRef[process]]['Model'].InputData.Data
            
        model = Table_from_pandas_editable(self._uncertain_data)
        self.MC_Uncertain_table.setModel(model)
        self.MC_Uncertain_table.resizeColumnsToContents()
    
    @QtCore.Slot()
    def Clear_MC_Uncert_func(self):
        self.MC_Uncertain_table.model()._data['uncertainty_type'] = 0
        self.MC_Uncertain_table.model()._data[['loc','scale','shape','minimum','maximum']] = np.nan
        self.MC_Uncertain_table.model().layoutChanged.emit()
        self.MC_Uncertain_table.resizeColumnsToContents()

    @QtCore.Slot()
    def Update_MC_Uncert_func(self):
        process = self.MC_Model.currentText()
        if process == 'IncomFlow':
            self.IncomFlow.InputData.Update_input(self.MC_Uncertain_table.model()._data)
        else:
            self.Project.ProcessModels[self.Project._ProcessNameRef[process]]['Model'].InputData.Update_input(self.MC_Uncertain_table.model()._data)
        
        self.msg_popup('Updata Input Data','The data is updated successfully.','Information')

    @QtCore.Slot()
    def MC_uncertain_filter_func(self):            
        if self.MC_uncertain_filter.isChecked():
            model = Table_from_pandas_editable(self._uncertain_data[:][self._uncertain_data['uncertainty_type']>1])
        else:
            model = Table_from_pandas_editable(self._uncertain_data)
        self.MC_Uncertain_table.setModel(model)
        self.MC_Uncertain_table.resizeColumnsToContents()

        
    @QtCore.Slot()
    def MC_Run_func(self):
        self.MC_is_runnning = True
        #start = time()
        print(" \n Monte Carlo simulation is started. \n Number of iterations: {} \n".format(int(self.MC_N_runs.text())))
        #self.Project.setup_MC(self.IncomFlow)
        #MC_results_raw=self.Project.MC_Run(int(self.MC_N_runs.text()))
        #self.MC_results  =self.Project.MC_Result_DF(MC_results_raw)
        #total_time = round(time()-start)
        #self.msg_popup('Monte Carlo Simulation','The monte carlo simulation is done successfully in {} seconds.'.format(total_time),'Information')
        #print('The monte carlo simulation is done successfully in {} seconds. \n'.format(total_time))
        
        MC_worker = Worker_MC(parent=self.MC_run,project=self.Project, InputFlow_object=self.IncomFlow, n=int(self.MC_N_runs.text()), seed=None)
        MC_worker.UpdatePBr_Opt.connect(self.setPBr_MC)
        MC_worker.Report.connect(self.report_time_WP)
        MC_worker.start()

    @QtCore.Slot()
    def report_time_WP(self, report):
        #Notift the user that the project has created successfully
        self.MC_results = report['results']
        self.msg_popup('Monte Carlo Simulation','The monte carlo simulation is done successfully in {} seconds.'.format(report['time']),'Information')
        print('The monte carlo simulation is done successfully in {} seconds. \n'.format(report['time']))
        
    @QtCore.Slot(int)
    def setPBr_MC(self, val):
        self.MC_PBr.setValue(val)

    @QtCore.Slot()  # select file and read the name of it. Import the name to the LineEdit.
    def MC_save_file(self):
        fileDialog = QtWidgets.QFileDialog()
        def helper():
            file_name = str(fileDialog.getSaveFileName(filter="CSV (*.csv)")[0])
            if file_name:
                self.MC_results.to_csv(file_name)
        return(helper)        
        

#%% MC results window          
# =============================================================================
# =============================================================================
    ### Define MC results window
# =============================================================================
# =============================================================================
    @QtCore.Slot()
    def show_res_func(self):
        Dialog = QtWidgets.QDialog()
        self.MC_Widget = MC_ui.Ui_MC_Results()
        self.MC_Widget.setupUi(Dialog)
        self.MC_Widget.tabWidget.setCurrentWidget(self.MC_Widget.MC_Data)
        
        ### Data Tab
        MC_res_table_model = Table_from_pandas(self.MC_results)
        self.MC_Widget.MC_Res_Table.setModel(MC_res_table_model)
        self.MC_Widget.MC_Res_Table.resizeColumnsToContents()
        self.MC_Widget.MC_Res_Table.installEventFilter(self)
        self.MC_Widget.MC_Res_Table.setSortingEnabled(True)
        
        ### Plot tab
        #Figure initialization _ plot
        self.fig_plot_mc = Figure(figsize=(4, 5), dpi=65, facecolor=(1, 1, 1), edgecolor=(0, 0, 0))
        self.canvas_plot_mc = FigureCanvas(self.fig_plot_mc)
        toolbar = NavigationToolbar(self.canvas_plot_mc, self)
        lay = QtWidgets.QVBoxLayout(self.MC_Widget.plot)
        lay.addWidget(toolbar)
        lay.addWidget(self.canvas_plot_mc)
        #self.ax_plot_mc = self.fig_plot_mc.add_subplot(111)
        
        #Figure initialization _ plot dist
        self.fig_plot_dist_mc = Figure(figsize=(4, 5), dpi=65, facecolor=(1, 1, 1), edgecolor=(0, 0, 0))
        self.canvas_plot_dist_mc = FigureCanvas(self.fig_plot_dist_mc)
        toolbar2 = NavigationToolbar(self.canvas_plot_dist_mc, self)
        lay2 = QtWidgets.QVBoxLayout(self.MC_Widget.plot_dist)
        lay2.addWidget(toolbar2)
        lay2.addWidget(self.canvas_plot_dist_mc)
        #self.ax_plot_dist_mc = self.fig_plot_dist_mc.add_subplot(111)
        
        self.MC_Widget.y_axis.addItems([str(x) for x in self.MC_results.columns])
        self.MC_Widget.x_axis.addItems([str(x) for x in self.MC_results.columns])
        self.MC_Widget.scatter.setChecked(True)
        self.MC_Widget.param.addItems([str(x) for x in self.MC_results.columns])
        self.MC_Widget.box.setChecked(True)
        
        
        ### Connect the push bottoms
        self.MC_Widget.Update_plot.clicked.connect(self.mc_plot_func)
        self.MC_Widget.Update_dist_fig.clicked.connect(self.mc_plot_dist_func)
        
        ### Correlation tab
        self.corr_data = self.MC_results[self.MC_results.columns[1:]].corr(method='pearson')
        
        self._MC_results_index = ['Water (10e-6g/year)','Soil (10e-6g/year)','Air (10e-6g/year)','Destroyed (10e-6g/year)','Stored (10e-6g/year)']

        # Correlation plot
        self.MC_Widget.Corr_param.addItems(self._MC_results_index)
        self.MC_Widget.Corr_btm.clicked.connect(self.corr_plot_func)
        
        #Figure initialization _ correlation plot
        self.fig_corr = Figure(figsize=(4, 5), dpi=65, facecolor=(1, 1, 1), edgecolor=(0, 0, 0))
        self.canvas_corr = FigureCanvas(self.fig_corr)
        toolbar = NavigationToolbar(self.canvas_corr, self)
        lay = QtWidgets.QVBoxLayout(self.MC_Widget.Corr_plot)
        lay.addWidget(toolbar)
        lay.addWidget(self.canvas_corr)        
        
        Dialog.show()
        Dialog.exec_()

    @QtCore.Slot()
    def corr_plot_func(self):
        self.fig_corr.clear()
        self.ax_plot_corr = self.fig_corr.add_subplot(111)
    
        #ploting the DataFrame
        param=list(self.corr_data.columns)
        for x in self._MC_results_index:
            param.remove(x)

        corr_data_plot = self.corr_data[self.MC_Widget.Corr_param.currentText()][param]
        sorted_corr=corr_data_plot.abs().sort_values()

        if len(sorted_corr.index) <= 10:
            index = sorted_corr.index
        else:
            index = sorted_corr.index[0:10]
        
        self.ax_plot_corr=corr_data_plot[index].plot(kind='barh',
                                                     ax=self.ax_plot_corr)
        #set lables
        self.ax_plot_corr.set_xlabel('Correlation with {}'.format(self.MC_Widget.Corr_param.currentText()), fontsize=18)
        self.ax_plot_corr.set_xlim(-1,1)
        self.ax_plot_corr.tick_params(axis='both', which='major', labelsize=18,rotation='auto')
        self.ax_plot_corr.tick_params(axis='both', which='minor', labelsize=16,rotation='auto')

        #set margins
        self.canvas_corr.draw()
        self.fig_corr.set_tight_layout(True)
        
    @QtCore.Slot()
    def mc_plot_func(self):
        self.fig_plot_mc.clear()
        self.ax_plot_mc = self.fig_plot_mc.add_subplot(111)
    
        #ploting the DataFrame        
        self.ax_plot_mc=self.MC_results.plot(kind='scatter' if self.MC_Widget.scatter.isChecked() else 'hexbin',
                                        x=self.MC_results.columns[self.MC_Widget.x_axis.currentIndex()],
                                        y=self.MC_results.columns[self.MC_Widget.y_axis.currentIndex()],
                                        ax=self.ax_plot_mc)
        #set lables
        self.ax_plot_mc.set_title(str(self.IncomFlow.Inc_flow.FlowType), fontsize=18)
        self.ax_plot_mc.set_ylabel(self.MC_Widget.y_axis.currentText(), fontsize=18)
        self.ax_plot_mc.set_xlabel(self.MC_Widget.x_axis.currentText(), fontsize=18)
        self.ax_plot_mc.tick_params(axis='both', which='major', labelsize=18,rotation='auto')
        self.ax_plot_mc.tick_params(axis='both', which='minor', labelsize=16,rotation='auto')

        #set margins
        self.canvas_plot_mc.draw()
        self.fig_plot_mc.set_tight_layout(True)
            
    @QtCore.Slot()    
    def mc_plot_dist_func(self):
        self.fig_plot_dist_mc.clear()
        self.ax_plot_dist_mc = self.fig_plot_dist_mc.add_subplot(111)
        
        if self.MC_Widget.hist.isChecked():
            kind = 'hist'
        elif self.MC_Widget.box.isChecked():
            kind = 'box'
        else:
            kind = 'density'

        #ploting the DataFrame  
        if kind == 'hist':
            self.ax_plot_dist_mc=self.MC_results[self.MC_results.columns[self.MC_Widget.param.currentIndex()]].plot(kind=kind,
                                        ax=self.ax_plot_dist_mc, bins=max(30,len(self.MC_results)/100))
        else:
            self.ax_plot_dist_mc=self.MC_results[self.MC_results.columns[self.MC_Widget.param.currentIndex()]].plot(kind=kind,
                                        ax=self.ax_plot_dist_mc)
            
        

        
        #set lables
        self.ax_plot_dist_mc.set_title(str(self.IncomFlow.Inc_flow.FlowType), fontsize=18)
        plt.rcParams["font.size"] = "18"
        self.ax_plot_dist_mc.tick_params(axis='both', which='major', labelsize=18,rotation='auto')
        self.ax_plot_dist_mc.tick_params(axis='both', which='minor', labelsize=16,rotation='auto')

        #set margins
        self.canvas_plot_dist_mc.draw()
        self.fig_plot_dist_mc.set_tight_layout(True)

#%%  SA tab          
# =============================================================================
# =============================================================================
    ### Sensitivity analysis
# =============================================================================
# =============================================================================
    @QtCore.Slot()
    def init_SA_tab_func(self):
        if not self.SA_tab_init_status:
            self.SA_tab.setEnabled(True)
            self.SA_PFAS.clear()
            self.SA_PFAS.addItems(['All']+[i for i in self.CommonData.PFAS_Index])
            self.SA_Model.currentTextChanged.connect(self.load_categories_func)
            self.SA_Category.currentTextChanged.connect(self.load_parameters_func)
            self.SA_Parameter.currentTextChanged.connect(self.load_paramInfo_func)
            self.SA_Run.clicked.connect(self.SA_Run_func)
            self.SA_Save.clicked.connect(self.SA_save_file())
            self.SA_Clear.clicked.connect(self.SA_Clear_func)
            self.SA_Plot.clicked.connect(self.show_sa_res_func)

        self.PFAS_SAT_1.setCurrentWidget(self.SA_tab)
        self.SA_Model.clear()
        self.SA_Model.addItems(['...', 'IncomFlow']+[self.Project.ProcessModels[p]['Name'] for p in self.Project.ProcessSet])
        self.SA_PFAS.setCurrentIndex(0)

    @QtCore.Slot(str)
    def load_categories_func(self,process):
        if process == '...' or process == '':
            categories = ['...']
        elif process == 'IncomFlow':
            categories = ['...']+list(self.IncomFlow.InputData.Input_dict.keys())
        else:
            categories = ['...']+list(self.Project.ProcessModels[self.Project._ProcessNameRef[process]]['Model'].InputData.Input_dict.keys())
        
        self.SA_Category.clear()
        self.SA_Category.addItems(categories)

    @QtCore.Slot(str)
    def load_parameters_func(self,category):
        if category == '...' or category == '':
            parameters = ['...']
        elif self.SA_Model.currentText() == 'IncomFlow':
            parameters = ['...']+['{}: {}'.format(key, val['Name']) for key,val  in self.IncomFlow.InputData.Input_dict[category].items()]
        else:
            parameters = ['...']+['{}: {}'.format(key, val['Name']) for key,val in self.Project.ProcessModels[self.Project._ProcessNameRef[self.SA_Model.currentText()]]['Model'].InputData.Input_dict[category].items()]
        
        self.SA_Parameter.clear()
        self.SA_Parameter.addItems(parameters)       

    @QtCore.Slot(str)
    def load_paramInfo_func(self,parameter):
        if parameter == '...' or parameter == '':
            info= ''
        elif self.SA_Model.currentText() == 'IncomFlow':
            param = parameter.split(':')[0]
            param_dict = self.IncomFlow.InputData.Input_dict[self.SA_Category.currentText()][param]
            info = str()
            for key in ['amount', 'uncertainty_type', 'loc', 'scale', 'minimum', 'maximum', 'Comment', 'Reference']:
                val = param_dict[key]
                if isinstance(val, str):
                    info += key + ': ' + str(val) + '\n'
                elif not np.isnan(val):
                    info += key + ': ' + str(val) + '\n'                    
        else:
            param = parameter.split(':')[0]
            param_dict = self.Project.ProcessModels[self.Project._ProcessNameRef[self.SA_Model.currentText()]]['Model'].InputData.Input_dict[self.SA_Category.currentText()][param]
            info = str()
            for key in ['amount', 'uncertainty_type', 'loc', 'scale', 'minimum', 'maximum', 'Comment', 'Reference']:
                val = param_dict[key]
                if isinstance(val, str):
                    info += key + ': ' + str(val) + '\n'
                elif not np.isnan(val):
                    info += key + ': ' + str(val) + '\n'
        self.SA_ParamInfo.setText(info)        

    @QtCore.Slot(str)
    def SA_Run_func(self):
        self.Project.setup_MC(self.IncomFlow)
        if self.SA_Model.currentText() == 'IncomFlow':
            model = 'IncomFlow'
        else:
            model = self.Project._ProcessNameRef[self.SA_Model.currentText()]

        SA_Res_raw = self.Project.SensitivityAnalysis(Model=model,
                                                      Category=self.SA_Category.currentText(),
                                                      Paramter=str.split(self.SA_Parameter.currentText(),':')[0],
                                                      Start=float(self.SA_Start.text()),
                                                      Stop=float(self.SA_Stop.text()),
                                                      Nstep=int(self.SA_NStep.text()),
                                                      TypeOfPFAS=self.SA_PFAS.currentText())
        self.SA_Res = self.Project.Result_to_DF(SA_Res_raw)
    
        ### Data Tab
        SA_Res_table_model = Table_from_pandas(self.SA_Res)
        self.SA_Results.setModel(SA_Res_table_model)
        self.SA_Results.resizeColumnsToContents()
        self.SA_Results.installEventFilter(self)
        self.SA_Results.setSortingEnabled(True)

    @QtCore.Slot()  # select file and read the name of it. Import the name to the LineEdit.
    def SA_save_file(self):
        fileDialog = QtWidgets.QFileDialog()
        def helper():
            file_name = str(fileDialog.getSaveFileName(filter="CSV (*.csv)")[0])
            if file_name:
                self.SA_Res.to_csv(file_name)
        return(helper) 

    @QtCore.Slot(str)
    def SA_Clear_func(self):
        self.SA_Model.setCurrentIndex(0)
        self.SA_Start.clear()
        self.SA_Stop.clear()
        self.SA_NStep.clear()
        self.SA_ParamInfo.clear()
        self.SA_Results.setModel(Table_from_pandas(pd.DataFrame()))
        self.SA_PFAS.setCurrentIndex(0)

#%% SA results window          
# =============================================================================
# =============================================================================
    ### Define SA results window
# =============================================================================
# =============================================================================
    @QtCore.Slot()
    def show_sa_res_func(self):
        Dialog = QtWidgets.QDialog()
        self.SA_Widget = SA_ui.Ui_SA_Plot()
        self.SA_Widget.setupUi(Dialog)
        
        ### Plot tab
        #Figure initialization _ plot
        self.fig_plot_sa = Figure(figsize=(4, 5), dpi=65, facecolor=(1, 1, 1), edgecolor=(0, 0, 0))
        self.canvas_plot_sa = FigureCanvas(self.fig_plot_sa)
        toolbar = NavigationToolbar(self.canvas_plot_sa, self)
        lay = QtWidgets.QVBoxLayout(self.SA_Widget.plot)
        lay.addWidget(toolbar)
        lay.addWidget(self.canvas_plot_sa)
        
        self.SA_Widget.y_axis.addItems([str(x) for x in self.SA_Res.columns])
        self.SA_Widget.x_axis.addItems([str(x) for x in self.SA_Res.columns])
    
        ### Connect the push bottoms
        self.SA_Widget.Update_plot.clicked.connect(self.sa_plot_func)
        
        Dialog.show()
        Dialog.exec_()
        
    @QtCore.Slot()
    def sa_plot_func(self):
        self.fig_plot_sa.clear()
        self.ax_plot_sa = self.fig_plot_sa.add_subplot(111)
    
        #ploting the DataFrame        
        self.ax_plot_sa=self.SA_Res.plot(kind='scatter',
                                        x=self.SA_Res.columns[self.SA_Widget.x_axis.currentIndex()],
                                        y=self.SA_Res.columns[self.SA_Widget.y_axis.currentIndex()],
                                        ax=self.ax_plot_sa)
        #set lables
        self.ax_plot_sa.set_title(str(self.IncomFlow.Inc_flow.FlowType), fontsize=18)
        self.ax_plot_sa.set_ylabel(self.SA_Widget.y_axis.currentText(), fontsize=18)
        self.ax_plot_sa.set_xlabel(self.SA_Widget.x_axis.currentText(), fontsize=18)
        self.ax_plot_sa.tick_params(axis='both', which='major', labelsize=18,rotation='auto')
        self.ax_plot_sa.tick_params(axis='both', which='minor', labelsize=16,rotation='auto')

        #set margins
        self.canvas_plot_sa.draw()
        self.fig_plot_sa.set_tight_layout(True)

#%% General Functions          
# =============================================================================
# =============================================================================
    ### General Functions
# =============================================================================
# =============================================================================   
    def msg_popup(self,Subject,Information,Type):
        msg = QtWidgets.QMessageBox()
        if Type =='Warning':
            msg.setIcon(msg.Icon.Warning)
        elif Type == 'Information':
            msg.setIcon(msg.Icon.Information)
        msg.setWindowTitle('PFAS SAT')
        msg.setWindowIcon(self.icon)
        msg.setText(Subject)
        msg.setInformativeText(Information)
        Ok=msg.addButton(msg.Ok)
        msg.exec()    

    @QtCore.Slot()  # select file and read the name of it. Import the name to the LineEdit.
    def select_file(self, LineEdit,Filter):
        fileDialog = QtWidgets.QFileDialog()
        def edit_line():
            file_name = str(fileDialog.getOpenFileName(filter=Filter)[0])
            LineEdit.setText(file_name)
        return(edit_line)
    
    
    @QtCore.Slot()
    def on_downloadRequested(self, download):
        """
        https://stackoverflow.com/questions/55963931/how-to-download-csv-file-with-qwebengineview-and-qurl
        """
        old_path = download.url().path()
        path, _ = QtWidgets.QFileDialog.getSaveFileName(
            self, "Save File", old_path, "*.png")
        if path:
            download.setPath(path)
            download.accept()

    @QtCore.Slot()
    def Help_Gui_func(self):
        Dialog = QtWidgets.QDialog()
        Help_Gui_Widget = HelpGuide_ui.Ui_HelpGuide()
        Help_Gui_Widget.setupUi(Dialog)
    
        urlLink="<a href=\"https://pfas-sat.readthedocs.io/en/latest/Getting_started.html\">(Learn How)</a>" 
        Help_Gui_Widget.link_Create_project.setText(urlLink)
        Help_Gui_Widget.link_Create_project.setOpenExternalLinks(True)

        urlLink="<a href=\"https://pfas-sat.readthedocs.io/en/latest/Getting_started.html\">(Learn How)</a>" 
        Help_Gui_Widget.link_MC.setText(urlLink)
        Help_Gui_Widget.link_MC.setOpenExternalLinks(True)

        urlLink="<a href=\"https://pfas-sat.readthedocs.io/en/latest/Getting_started.html\">(Learn How)</a>" 
        Help_Gui_Widget.link_UserDef.setText(urlLink)
        Help_Gui_Widget.link_UserDef.setOpenExternalLinks(True)

        urlLink="<a href=\"https://pfas-sat.readthedocs.io/en/latest/doc_PFAS_SAT.html\">(Learn How)</a>" 
        Help_Gui_Widget.link_CodeDoc.setText(urlLink)
        Help_Gui_Widget.link_CodeDoc.setOpenExternalLinks(True)

        urlLink="<a href=\"https://pfas-sat.readthedocs.io/en/latest/contributing.html\">(Learn How)</a>" 
        Help_Gui_Widget.link_Contr.setText(urlLink)
        Help_Gui_Widget.link_Contr.setOpenExternalLinks(True)        
        
        Dialog.show()
        Dialog.exec_()
        