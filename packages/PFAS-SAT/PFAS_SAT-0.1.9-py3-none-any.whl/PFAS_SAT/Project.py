# -*- coding: utf-8 -*-
"""
Created on Wed Jul 29 17:03:27 2020

@author: msmsa
"""
import pandas as pd
import numpy as np
from .SubProcesses import split
import graphviz
import plotly.graph_objects as go
from plotly.offline import plot
import json
import warnings
import time
from .utils import NpEncoder
import importlib  # to import moduls with string name
from .ProcessModelsMetaData import ProcessModelsMetaData


class Project():
    def __init__(self, Inventory, CommonData, ProcessModels=None):
        self.Inventory = Inventory

        self.CommonData = CommonData
        self.WasteMaterials = self.CommonData.WasteMaterials

        if ProcessModels:
            self.ProcessModels = ProcessModels
        else:
            self.ProcessModels = {}
            for P in ProcessModelsMetaData:
                self.ProcessModels[P] = {}
                self.ProcessModels[P]['Name'] = ProcessModelsMetaData[P]['Name']
                self.ProcessModels[P]['InputType'] = []
                for flow in ProcessModelsMetaData[P]['InputType']:
                    self.ProcessModels[P]['InputType'].append(flow)
                clas_file = ProcessModelsMetaData[P]['File'].split('.')[0]
                module = importlib.import_module('PFAS_SAT.'+clas_file)
                model = module.__getattribute__(P)
                self.ProcessModels[P]['Model'] = model(input_data_path=None,
                                                       CommonDataObjct=self.CommonData,
                                                       InventoryObject=self.Inventory,
                                                       Name=self.ProcessModels[P]['Name'])

        self.Processes = list(self.ProcessModels.keys())
        self._ProcessNameRef = {}
        for key, val in self.ProcessModels.items():
                self._ProcessNameRef[val['Name']] = key

        self.WasteTreatment = {}
        for i in self.WasteMaterials:
            self.WasteTreatment[i] = self._find_destination(i)
        print('\n Treatment options for each waste material: {} \n\n'.format(self.WasteTreatment))

        # Print warnings
        warnings.simplefilter('always', UserWarning)

    def _find_destination(self, product):
        destination = []
        for P in self.Processes:
            if product in self.ProcessModels[P]['InputType']:
                destination.append(P)
        return(destination)

    def get_process_set(self, InputFlow):
        self.Inventory.clear()
        self.InputFlow = InputFlow

        ProcessSet = set()
        # Input flow
        for P in self.WasteTreatment[self.InputFlow.FlowType]:
            ProcessSet.add(P)
            # Intermediate products (Level 1)
            for Product1 in self.ProcessModels[P]['Model'].ProductsType:
                # Add the processes for treatment of level 1 products
                for PP in self.WasteTreatment[Product1]:
                    ProcessSet.add(PP)
                    # Intermediate products (Level 2)
                    for Product2 in self.ProcessModels[PP]['Model'].ProductsType:
                        # Add the processes for treatment of level 2 products
                        for PPP in self.WasteTreatment[Product2]:
                            ProcessSet.add(PPP)
        return(ProcessSet)

    def set_process_set(self, ProcessSet):
        self.ProcessSet = ProcessSet
        self.FlowSet = []
        self.FlowSet.append(self.InputFlow.FlowType)

        self._NtwkrNode = set()
        self._NtwkrNodeShape = {}
        self._NtwkrNodeColor = {}
        self._Ntwkedge = set()

        self._NtwkrNode.add(self.InputFlow.FlowType)
        self._NtwkrNodeShape[self.InputFlow.FlowType] = 'oval'
        self._NtwkrNodeColor[self.InputFlow.FlowType] = 'azure'

        for P in self.ProcessSet:
            self._NtwkrNode.add(self.ProcessModels[P]['Name'])
            self._NtwkrNodeShape[self.ProcessModels[P]['Name']] = 'rectangle'
            self._NtwkrNodeColor[self.ProcessModels[P]['Name']] = 'cyan3'
            for product in self.ProcessModels[P]['Model'].ProductsType:
                self._NtwkrNode.add(product)
                self._NtwkrNodeShape[product] = 'oval'
                self._NtwkrNodeColor[product] = 'azure'
                self._Ntwkedge.add((self.ProcessModels[P]['Name'], product))
                if product not in self.FlowSet:
                    self.FlowSet.append(product)

    def get_flow_params(self, normalize=True):
        self.FlowParams = dict()
        for F in self.FlowSet:
            self.FlowParams[F] = {}
            for P in self.ProcessSet:
                if F in self.ProcessModels[P]['InputType']:
                    self.FlowParams[F][self.ProcessModels[P]['Name']] = 0
                    self._Ntwkedge.add((F, self.ProcessModels[P]['Name']))
        if normalize:
            for key, val in self.FlowParams.items():
                if len(val) > 0:
                    for key2 in val:
                        val[key2] = np.round(1/len(val), 4)
        return(self.FlowParams)

    def set_flow_params(self, FlowParams):
        for key, value in FlowParams.items():
            if len(value) > 0:
                if abs(1-sum(value.values())) > 0.01:
                    raise ValueError('Sum of the fractions for {} is not 1'.format(key))
        self.FlowParams = FlowParams

    def setup_network(self):
        self.Inventory.clear()
        self.CuttOff = sum(self.InputFlow.PFAS.values) * 0.01
        product = {self.InputFlow.FlowType: self.InputFlow}
        Project.calc(product, self.InputFlow.FlowType, self.ProcessModels, self.FlowParams, self.Inventory, self.CuttOff, self._ProcessNameRef)

    @staticmethod
    def calc(product, source, processmodel, FlowParams, Inventory, CuttOff, ProcessNameRef):
        for prdct in product:
            if FlowParams[prdct]:
                flows = split(InputFlow=product[prdct], **FlowParams[prdct])
                for prcs, flw in flows.items():
                    if sum(flw.PFAS.values) > CuttOff:
                        if source not in ProcessNameRef:
                            Inventory.add(prdct, source, prcs, flw)
                        else:
                            Inventory.add(prdct, source, prcs, flw)
                        processmodel[ProcessNameRef[prcs]]['Model'].calc(flw)
                        product_2 = processmodel[ProcessNameRef[prcs]]['Model'].products()
                        Project.calc(product_2, prcs, processmodel, FlowParams, Inventory, CuttOff, ProcessNameRef)
            else:
                # Change the warning to exception when all the process models are done
                warnings.warn("No process is defined for {} treatment".format(prdct))

    def setup_MC(self, InputFlow_object, seed=None):
        self.InputFlow_object = InputFlow_object
        self.InputFlow_object.setup_MC(seed=None)
        for p in self.ProcessSet:
            self.ProcessModels[p]['Model'].setup_MC(seed=None)

    def MC_Next(self):
        NewInputData = []
        NewInputData += self.InputFlow_object.MC_Next()
        for p in self.ProcessSet:
            Raw_newdata = []
            for x in self.ProcessModels[p]['Model'].MC_Next():
                Raw_newdata.append(((p, x[0]), x[1]))
            NewInputData += Raw_newdata

        self.Inventory.clear()
        self.InputFlow_object.calc()
        product = {self.InputFlow_object.Inc_flow.FlowType: self.InputFlow_object.Inc_flow}
        Project.calc(product, 'Start', self.ProcessModels, self.FlowParams, self.Inventory, self.CuttOff, self._ProcessNameRef)
        return(NewInputData)

    def MC_Run(self, n, signal=None):
        # Print warning only first time
        warnings.simplefilter('once', UserWarning)

        progress = 0
        progress_steps = [int(x) for x in np.linspace(1, n, 19)]
        MC_results = []
        for i in range(n):
            NewInputData = self.MC_Next()
            MC_results.append((i, NewInputData, self.Inventory.report()))
            if signal:
                if i in progress_steps:
                    progress += 5
                    signal.emit(progress)
                    print('Iteration {} \n ... '.format(i))
                    time.sleep(0.1)

        self.Reset_static_Data()
        return(MC_results)

    def Reset_static_Data(self):
        self.InputFlow_object.InputData.reset_static_vals()
        for p in self.Processes:
            self.ProcessModels[p]['Model'].InputData.reset_static_vals()

    def Result_to_DF(self, results):
        DF = pd.DataFrame()
        DF['Iteration'] = [results[j][0] for j in range(len(results))]
        for i in results[0][2].keys():
            DF[i] = [results[j][2][i] for j in range(len(results))]
        for i in range(len(results[0][1])):
            DF[results[0][1][i][0]] = [results[j][1][i][1] for j in range(len(results))]
        return(DF)

    def setup_SA(self, InputFlow_object):
        self.InputFlow_object = InputFlow_object

    def SensitivityAnalysis(self, Model, Category, Paramter, Start, Stop, Nstep, TypeOfPFAS='All'):
        try:
            SA_results = []
            param_vals = np.linspace(Start, Stop, Nstep)
            default_value = 'Not Set'
            for i, val in enumerate(param_vals):
                # Update the Input data
                if Model == 'IncomFlow':
                    if default_value == 'Not Set':
                        default_value = self.InputFlow_object.InputData.Input_dict[Category][Paramter]['amount']
                    self.InputFlow_object.InputData.Input_dict[Category][Paramter]['amount'] = val
                else:
                    if default_value == 'Not Set':
                        default_value = self.ProcessModels[Model]['Model'].InputData.Input_dict[Category][Paramter]['amount']
                    self.ProcessModels[Model]['Model'].InputData.Input_dict[Category][Paramter]['amount'] = val

                # Calculating results
                self.Inventory.clear()
                self.InputFlow_object.calc()
                product = {self.InputFlow_object.Inc_flow.FlowType: self.InputFlow_object.Inc_flow}
                Project.calc(product, 'Start', self.ProcessModels, self.FlowParams, self.Inventory, self.CuttOff, self._ProcessNameRef)

                # Store Results
                SA_results.append((i, [(Paramter, val)], self.Inventory.report(TypeOfPFAS)))

        except Exception as e:
            print('Error while running the SA: \n')
            print(e)

        finally:
            # Reset Values
            self.Reset_static_Data()
            self.Inventory.clear()
            return(SA_results)

    def plot_network(self, view=True, show_vals=True, all_flow=True):
            """
            To render the generated DOT source code, you also need to install `Graphviz <https://www.graphviz.org/download>`_.

            ..note:: Make sure that the directory containing the dot executable is on your systems path.

            """
            # Initialize PFAS treatment network
            self.network = graphviz.Digraph(name='Network', filename='Network.gv', format='png', engine='dot')
            self.network.graph_attr['rankdir'] = 'LR'
            self.network.attr(dpi='300')
            self.network.attr(size='4,8')
            for x in self._NtwkrNode:
                self.network.node(x, shape=self._NtwkrNodeShape[x], fillcolor=self._NtwkrNodeColor[x], style='filled', width='1.2')

            for e in self._Ntwkedge:
                self.network.edge(e[0], e[1], label=None, color='black')
            try:
                self.network.render('Network', view=view)
            except Exception:
                print("""
                      To render the generated DOT source code, you also need to install Graphviz (`Graphviz <https://www.graphviz.org/download>`_).\n
                      Make sure that the directory containing the dot executable is on your systems’ path.
                      """)

    def plot_sankey(self, view=True, filename=None):

        Data = self.Inventory.Inv

        label = []
        label_dict = {}
        source = []
        target = []
        value = []
        label_link = []
        color_link = []

        # List of colors: https://flaviocopes.com/rgb-color-codes/
        edge_color_dict = {'CompFeed': (202, 255, 112),  # darkolivegreen1  #CAFF70
                           'CompFin': (110, 139, 61),  # darkolivegreen4	#6E8B3D
                           'CompRes': (118, 238, 0),  # chartreuse2	#76EE00
                           'Digestate': (124, 252, 0),  # lawn green	#7CFC00
                           'MSW': (139, 101, 8),  # darkgoldenrod4	#8B6508
                           'C&DWaste': (238, 232, 205),  # cornsilk2	#EEE8CD
                           'MedWaste': (220, 20, 60),  # crimson	#DC143C
                           'MRFRes': (189, 183, 107),  # darkkhaki	#BDB76B
                           'ContaminatedSoil': (128, 138, 135),  # coldgrey	#808A87
                           'CombRes': (169, 169, 169),  # darkgray	#A9A9A9
                           'ContactWater': (142, 229, 238),  # cadetblue2	#8EE5EE
                           'ContaminatedWater': (0, 0, 139),  # dark blue	#00008B
                           'LFLeachate': (0, 0, 255),  # blue	#0000FF
                           'DewWWTSol': (128, 128, 128),  # gray / grey	#808080
                           'DryWWTSol': (192, 192, 192),  # silver	#C0C0C0
                           'WWTSol': (112, 128, 144),  # slate gray	#708090
                           'SCWO_Steam': (123, 104, 238),  # medium slate blue	#7B68EE
                           'SCWO_Slurry': (72, 61, 139),  # dark slate blue	#483D8B
                           'SpentGAC': (138, 43, 226),  # blue violet	#8A2BE2
                           'ROConc': (70, 130, 180),  # steel blue	#4682B4
                           'RunOff': (0, 255, 255)}  # aqua	#00FFFF

        index = 0
        for i in Data.loc['Source']:
            if i not in label_dict:
                label_dict[i] = index
                label.append(i)
                index += 1
            source.append(label_dict[i])

        for i in Data.loc['Target']:
            if i not in label_dict:
                label_dict[i] = index
                label.append(i)
                index += 1
            target.append(label_dict[i])

        for i in Data.loc[self.CommonData.PFAS_Index].sum():
            value.append(i)

        for i in Data.loc['Flow_name']:
            label_link.append(i)
            if i in edge_color_dict:
                color_link.append('rgba({},{},{}, 0.8)'.format(*edge_color_dict[i]))
            else:
                color_link.append('rgba(255,127, 0, 0.8)')

        print("""
              # Sankey Mass flows
              label = {}
              source = {}
              target = {}
              label_link = {}
              value = {}""".format(label, source, target, label_link, value))

        node = dict(pad=20,
                    thickness=20,
                    line=dict(color="black", width=0.5),
                    label=label,
                    color='rgba({}, {}, {}, 0.8)'.format(*(176, 196, 222)))  # light steel blue	#B0C4DE

        link = dict(source=source,
                    target=target,
                    value=value,
                    label=label_link,
                    color=color_link)

        # The other good option for the valueformat is ".3f".
        layout = go.Layout(title_text=None,
                           font_size=16,
                           hoverlabel=dict(font_size=14))
        data = go.Sankey(valueformat=".3s",
                         valuesuffix="μg/year",
                         node=node,
                         link=link)
        fig = go.Figure(data=[data], layout=layout)
        plot(fig, filename=filename if filename else 'sankey.html', auto_open=view)

        # Store data for ploting the sankey
        store_data = {}
        store_data['title_text'] = None
        store_data['font_size'] = 16
        store_data['hoverlabel'] = dict(font_size=14)
        store_data['valueformat'] = ".3s"
        store_data['valuesuffix'] = "μg/year"
        store_data['node'] = node
        store_data['link'] = link

        print(store_data)
        with open('Sankey_Data.JSON', 'w') as outfile:
            json.dump(store_data, outfile, indent=4, cls=NpEncoder)
