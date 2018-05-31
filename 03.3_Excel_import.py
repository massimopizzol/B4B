#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sept 1 12:00:00 2017

@author: massimo
"""


import pandas as pd
import numpy as np
from lci_to_bw2 import *
from brightway2 import *


projects.set_current('bw2_import_ecoinvent_3.4') # Find a project where there is ecoinvent
databases

# Import csv file
mydb = pd.read_csv('test_db_excel_w_ecoinvent.csv', header = 0, sep = ";") # if using csv file

# clean up a bit
mydb = mydb.drop('Notes', 1)  # remove the columns not needed
mydb['Exchange uncertainty type'] = mydb['Exchange uncertainty type'].fillna(0).astype(int) # uncertainty as integer 
                    ### Note: (can't have the full column if there are mixed nan and values, so use zero as default)
mydb    
   

# Create a dict that can be written as database
bw2_db = lci_to_bw2(mydb) # Perfect.
bw2_db

if 'testdb' in databases: del databases['testdb']
t_db = Database("testdb")
t_db.write(bw2_db)



[print(act) for act in t_db]  # check more stuff 
[[print(act, exc) for exc in list(act.exchanges())]for act in t_db]  # check more stuff 
[[print(exc.uncertainty) for exc in list(act.exchanges())]for act in t_db]  # check more stuff

myact = Database("testdb").get('Fuel production')
list(myact.exchanges())


# check if calculations work
t_db.search('electricity')

el = t_db.get("Electricity production") # this is an activity (a DICT)
list(el.exchanges())  # yeps, this one
functional_unit = {el: 1000}
lca = LCA(functional_unit) 
lca.lci()
print(lca.inventory)


mymethod = ('IPCC 2013', 'climate change', 'GWP 100a')

lca = LCA(functional_unit, mymethod) #run LCA calculations again with method
lca.lci()
lca.lcia()
print(lca.inventory)
print(lca.characterized_inventory)
print(lca.score) # some results
