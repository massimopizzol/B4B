#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  8 11:30:17 2017

@author: massimo
"""

import brightway2 as bw


# If you want to make a new project OR import the database into a specific project 
# Use these commands below
# Otherwsie skip them
list(bw.projects)
bw.projects.current
bw.projects.set_current("<your project  name here>") 


# Import the biosphere3 database

bw.bw2setup()  # This will take some time


# Import ecoinvent

# You need to chenge the line below with the directory wher eyou have saved ecoinvent
fpei34 = "/Users/massimo/Documents/AAU/Research/Databases/ecoinvent v3.4/datasets"

bw.databases
if 'ecoinvent 3.4 conseq' in bw.databases:
    print("Database has already been imported")
else:
    ei34 = bw.SingleOutputEcospold2Importer(fpei34, 'ecoinvent 3.4 conseq')
    ei34.apply_strategies()
    ei34.statistics()


ei34.write_database() # This will take some time.
