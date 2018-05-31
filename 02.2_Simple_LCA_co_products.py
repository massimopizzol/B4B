# -*- coding: utf-8 -*-
"""
Created on Wed Jan  4 21:03:55 2017

@author: massimo
"""

from brightway2 import *

t_db1 = Database("testdb")

t_db1.write({
    ("testdb", "Electricity production"):{
        'name':'Electricity production',
        'unit': 'kWh', 
        'exchanges': [{
                'input': ('testdb', 'Fuel production'),
                'amount': 2,
                'unit': 'kg',
                'type': 'technosphere'
            },{
                'input': ('testdb', 'Carbon dioxide'),
                'amount': 1,
                'unit': 'kg',
                'type': 'biosphere'
            },{
                'input': ('testdb', 'Sulphur dioxide'),
                'amount': 0.1,
                'unit': 'kg',
                'type': 'biosphere'
            },{
                'input': ('testdb', 'Electricity production'), #important to write the same process name in output
                'amount': 10,
                'unit': 'kWh',
                'type': 'production'
            },{
                'input': ('testdb', 'Heat production'),
                'amount': -3,
                'unit': 'MJ',
                'type': 'technosphere'
            }]
        },
    ('testdb', 'Fuel production'):{
        'name': 'Fuel production',
        'unit': 'kg',
        'exchanges':[{
                'input': ('testdb', 'Carbon dioxide'),
                'amount': 10,
                'unit': 'kg',
                'type': 'biosphere'
            },{
                'input': ('testdb', 'Sulphur dioxide'),
                'amount': 2,
                'unit': 'kg',
                'type': 'biosphere'
            },{
                'input': ('testdb', 'Crude oil'),
                'amount': -50,
                'unit': 'kg',
                'type': 'biosphere'
            },{
                'input': ('testdb', 'Fuel production'),
                'amount': 100,
                'unit': 'kg',
                'type': 'production'
            }]
        },
    ('testdb', 'Heat production'):{
        'name': 'Heat production',
        'unit': 'MJ',
        'exchanges':[{
                'input': ('testdb', 'Carbon dioxide'),
                'amount': 10000, # some exaggerated nr...
                'unit': 'kg',
                'type': 'biosphere'
            },{
                'input': ('testdb', 'Heat production'),
                'amount': 3,
                'unit': 'MJ',
                'type': 'production'
            }]
        },
    ('testdb', 'Carbon dioxide'):{'name': 'Carbon dioxide', 'unit':'kg', 'type': 'biosphere'},
    ('testdb', 'Sulphur dioxide'):{'name': 'Sulphur dioxide', 'unit':'kg', 'type': 'biosphere'},
    ('testdb', 'Crude oil'):{'name': 'Crude oil', 'unit':'kg', 'type': 'biosphere'}

    })


# Or just do like this:


t_db2 = Database("testdb")

t_db2.write({
    ("testdb", "Electricity production"):{
        'name':'Electricity production',
        'unit': 'kWh', 
        'exchanges': [{
                'input': ('testdb', 'Fuel production'),
                'amount': 2,
                'unit': 'kg',
                'type': 'technosphere'
            },{
                'input': ('testdb', 'Carbon dioxide'),
                'amount': 1,
                'unit': 'kg',
                'type': 'biosphere'
            },{
                'input': ('testdb', 'Sulphur dioxide'),
                'amount': 0.1,
                'unit': 'kg',
                'type': 'biosphere'
            },{
                'input': ('testdb', 'Electricity production'), #important to write the same process name in output
                'amount': 10,
                'unit': 'kWh',
                'type': 'production'
            },{
                'input': ('testdb', 'Heat production'),
                'amount': 3,
                'unit': 'MJ',
                'type': 'substitution'
            }]
        },
    ('testdb', 'Fuel production'):{
        'name': 'Fuel production',
        'unit': 'kg',
        'exchanges':[{
                'input': ('testdb', 'Carbon dioxide'),
                'amount': 10,
                'unit': 'kg',
                'type': 'biosphere'
            },{
                'input': ('testdb', 'Sulphur dioxide'),
                'amount': 2,
                'unit': 'kg',
                'type': 'biosphere'
            },{
                'input': ('testdb', 'Crude oil'),
                'amount': -50,
                'unit': 'kg',
                'type': 'biosphere'
            },{
                'input': ('testdb', 'Fuel production'),
                'amount': 100,
                'unit': 'kg',
                'type': 'production'
            }]
        },
    ('testdb', 'Heat production'):{
        'name': 'Heat production',
        'unit': 'MJ',
        'exchanges':[{
                'input': ('testdb', 'Carbon dioxide'),
                'amount': 10000, # some exaggerated nr...
                'unit': 'kg',
                'type': 'biosphere'
            },{
                'input': ('testdb', 'Heat production'),
                'amount': 3,
                'unit': 'MJ',
                'type': 'production'
            }]
        },
    ('testdb', 'Carbon dioxide'):{'name': 'Carbon dioxide', 'unit':'kg', 'type': 'biosphere'},
    ('testdb', 'Sulphur dioxide'):{'name': 'Sulphur dioxide', 'unit':'kg', 'type': 'biosphere'},
    ('testdb', 'Crude oil'):{'name': 'Crude oil', 'unit':'kg', 'type': 'biosphere'}

    })



# Create a LCIA method. 

myLCIAdata = [[('testdb', 'Carbon dioxide'), 2.0], 
              [('testdb', 'Sulphur dioxide'), 2.0],
              [('testdb', 'Crude oil'), 2.0]]

method_key = ('simplemethod', 'imaginaryendpoint', 'imaginarymidpoint')
my_method = Method(method_key)
my_method.validate(myLCIAdata)
my_method.register() 
my_method.write(myLCIAdata)
my_method.load()


# Compare the two

functional_unit1 = {t_db1.get("Electricity production") : 1000}
lca1 = LCA(functional_unit1, method_key) 
lca1.lci()
lca1.lcia()
print(lca1.inventory)
print(lca1.score)

functional_unit2 = {t_db2.get("Electricity production") : 1000}
lca2 = LCA(functional_unit2, method_key) 
lca2.lci()
lca2.lcia()
print(lca2.inventory)
print(lca2.score)

lca1.score == lca2.score
