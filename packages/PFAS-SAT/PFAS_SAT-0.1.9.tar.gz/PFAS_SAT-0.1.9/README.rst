.. General

================================================================
Perfluoroalkyl Substances(PFAS) Systems Analysis Tool(SAT) 
================================================================

.. image:: https://img.shields.io/pypi/v/PFAS_SAT.svg
        :target: https://pypi.python.org/pypi/PFAS_SAT
        
.. image:: https://img.shields.io/pypi/pyversions/PFAS_SAT.svg
    :target: https://pypi.org/project/PFAS_SAT/
    :alt: Supported Python Versions

.. image:: https://img.shields.io/pypi/l/PFAS_SAT.svg
    :target: https://pypi.org/project/PFAS_SAT/
    :alt: License

.. image:: https://img.shields.io/pypi/format/PFAS_SAT.svg
    :target: https://pypi.org/project/PFAS_SAT/
    :alt: Format

.. image:: https://readthedocs.org/projects/pfas_sat/badge/?version=latest
        :target: https://pfas_sat.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status


* Free software: GNU GENERAL PUBLIC LICENSE V2
* Documentation: https://PFAS_SAT.readthedocs.io.
* Repository: https://bitbucket.org/msm_sardar/PFAS_SAT



Objective
---------

* The objective of this project is to develop a comprehensive systems analysis tool (SAT) to estimate PFAS release associated with management alternatives for a wide range of PFAS-containing wastes.


.. Installation

Installation
------------
1- Download and install miniconda from:  https://docs.conda.io/en/latest/miniconda.html

2- Update conda in a terminal window or anaconda prompt::

        conda update conda

3- Create a new environment for PFAS_SAT::

        conda create --name PFAS_SAT python=3.7 graphviz

4- Activate the environment (Windows users)::

        conda activate PFAS_SAT

Note: If you are using Linux or macOS::

        source activate PFAS_SAT
        
5- Install PFAS_SAT in the environment::

        pip install PFAS_SAT

6- Only for Windows user (If you are using Linux or macOS, go to the next step). Make sure that ``bin/`` subdirectory of graphviz which contains
the layout commands for rendering graph descriptions (dot) is on your system path: On the command-line, ``dot -V`` should print the version
of your Graphiz.


7- Open python to run PFAS_SAT::

        python

8- Run PFAS_SAT in python::

        from PFAS_SAT import *
        PFAS_SAT()


.. endInstallation
