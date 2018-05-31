# -*- coding: utf-8 -*-
"""
Created on Thu Jan  5 13:44:13 2017

@author: massimo
"""

'''
Same as in the previous version (Simple_LCA.py) 
but this time I create two databases, 
one for product flows and one for environmental flows.
Note how the two are linked and that you can't creatt the first without 
creating the second first.
'''

from brightway2 import *


t_db = Database("testdb")

t_db.write({
    ("testdb", "Electricity production"):{
        'name':'Electricity production',
        'unit': 'kWh', 
        'exchanges': [{
                'input': ('testdb', 'Fuel production'),
                'amount': 2,
                'unit': 'kg',
                'type': 'technosphere'
            },{
                'input': ('biosphere', 'Carbon dioxide'), #this is the KEY line, put biosphere to show that the flow is from the other database.
                'amount': 1,
                'unit': 'kg',
                'type': 'biosphere'
            },{
                'input': ('biosphere', 'Sulphur dioxide'),
                'amount': 0.1,
                'unit': 'kg',
                'type': 'biosphere'
            },{
                'input': ('testdb', 'Electricity production'), #important to write the same process name in output
                'amount': 10,
                'unit': 'kWh',
                'type': 'production'
            }]
        },
    ('testdb', 'Fuel production'):{
        'name': 'Fuel production',
        'unit': 'kg',
        'exchanges':[{
                'input': ('biosphere', 'Carbon dioxide'),
                'amount': 10,
                'unit': 'kg',
                'type': 'biosphere'
            },{
                'input': ('biosphere', 'Sulphur dioxide'),
                'amount': 2,
                'unit': 'kg',
                'type': 'biosphere'
            },{
                'input': ('biosphere', 'Crude oil'),
                'amount': -50,
                'unit': 'kg',
                'type': 'biosphere'
            },{
                'input': ('testdb', 'Fuel production'),
                'amount': 100,
                'unit': 'kg',
                'type': 'production'
            }]
    }})


bs_db = Database("biosphere")

bs_db.write({
    ('biosphere', 'Carbon dioxide'):{'name': 'Carbon dioxide', 'unit':'kg', 'type': 'biosphere'},
    ('biosphere', 'Sulphur dioxide'):{'name': 'Sulphur dioxide', 'unit':'kg', 'type': 'biosphere'},
    ('biosphere', 'Crude oil'):{'name': 'Crude oil', 'unit':'kg', 'type': 'biosphere'}
    })



functional_unit = {t_db.get("Electricity production") : 1000}
lca = LCA(functional_unit) 
lca.lci()
print(lca.inventory)


myLCIAdata = [[('biosphere', 'Carbon dioxide'), 2.0], 
              [('biosphere', 'Sulphur dioxide'), 2.0],
              [('biosphere', 'Crude oil'), 2.0]]

method_key = ('simplemethod', 'imaginaryendpoint', 'imaginarymidpoint')
my_method = Method(method_key)
my_method.validate(myLCIAdata)
my_method.register() 
my_method.write(myLCIAdata)
my_method.load()

lca = LCA(functional_unit, method_key) #run LCA calculations again with method
lca.lci()
lca.lcia()
print(lca.inventory)
print(lca.characterized_inventory)