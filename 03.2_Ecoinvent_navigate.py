#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
B4B2018
Massimo Pizzol
"""

import pandas as pd
import numpy as np
from brightway2 import *

#Find a project where there are both biosphere and ecoinvent
projects
projects.set_current('C3BO') # Replace name with your project...

projects.set_current('bw2_import_ecoinvent_3.4') # Replace name with your project...
databases

# Search stuff in biosphere
CO2 = Database("biosphere3").get("349b29d1-3e58-4c66-98b9-9d1a076efd2e") # This code works acorss bw2 installations, 
                                                                    ### i.e. is univocal for biosphere3 everywhere
CO2['name'] # there is more than one activity with this name. Only code is univocal.
CO2['code']

Database("biosphere3").search('Carbon dioxide')
 
# Search stuff in ecoinvent

#'diesel production, low-sulfur' (kilogram, RoW, None)
#b5010d1257630217c6d7e89a872d0611

# Search by keyword
databases
mydb = Database('ecoinvent 3.4 conseq')
mydb.search("*") # to search everything
mydb.search("transport")

activity_name = 'diesel'

# Same but different:
mylist = []
for activity in Database("ecoinvent 3.4 conseq").search(activity_name, limit = 150):  
    print(activity)
    print(activity['code'])
    mylist.append(activity['code'])
len(mylist)        


# Try this        
for activity in Database("biosphere3").search(activity_name, limit = 1000):  
    print(activity)
    print(activity['code'])

for activity in Database("biosphere3").search('methane', limit = 1000):  
    print(activity)
    print(activity['code']) # now it works :)

for activity in Database("ecoinvent 3.4 conseq").search(activity_name, filter={"location" : 'DK'}):
    print(activity)
    print(activity['code'])
    

# How to select activities? 

# If you know the code (e.g. found with method above) it's simple.        
mycode = 'a0b8a22a4a9d4d73bf6007a3ab976a00'
myact = Database("ecoinvent 3.4 conseq").get(mycode)
#myact = Database("biosphere3").get(mycode)  # Not working of course...

myact['name']
myact._data
for i in list(myact.exchanges()):  # Explore the activity
    print(i['type'])
    print(i)
    print(i['amount'])
    print(i['input'])

# If you know the name and want to select it:
# Assume I wasnt diesel prod from RoW
activity_name = 'diesel production, low-sulfur'

mydb.search(activity_name)
    
for activity in Database("ecoinvent 3.4 conseq"):  
    if activity['name'] == activity_name:
        myact_code = Database("ecoinvent 3.4 conseq").get(activity['code'])

myact_code # Careful! Will return the Swiss one. Not what I wanted! 

for activity in Database("ecoinvent 3.4 conseq"):  
    if activity['name'] == activity_name:
        if activity['location'] == 'RoW':
            myact_code = Database("ecoinvent 3.4 conseq").get(activity['code'])

myact_code # The one I wanted

# another way with LIST COMPREHENSION
mylc = [a for a in Database("ecoinvent 3.4 conseq") if (a['name'] == activity_name and a['location'] == 'RoW')]
myactivity = mylc[0]
myactivity


# See the uncertainties
[print(exc.uncertainty) for exc in list(myact.exchanges())]  # check uncertainties...


# This to find who uses a specific activity
for act in Database("ecoinvent 3.4 conseq"):
    for exc in list(act.exchanges()):
        if exc['input'][1] == mycode:
         print(exc['input'])
         print('***')
         print(exc)
         print(exc.uncertainty)
         print(exc['uncertainty type'])
         if 'scale' in exc.uncertainty: 
             print(exc['scale'])