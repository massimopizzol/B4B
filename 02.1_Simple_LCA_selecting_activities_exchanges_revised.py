# -*- coding: utf-8 -*-
'''
Created on Tue Jan 10 15:09:02 2017

@author: massimo
'''

from brightway2 import *

t_db = Database('testdb')

t_db.write({
    ('testdb', 'Electricity production'): {
        'name': 'Electricity production',
        'unit': 'kWh',
        'exchanges': [{
                'input': ('testdb', 'Fuel production'),
                'amount': 2,
                'unit': 'kg',
                'type': 'technosphere'
            }, {
                'input': ('testdb', 'Carbon dioxide'),
                'amount': 1,
                'unit': 'kg',
                'type': 'biosphere'
            }, {
                'input': ('testdb', 'Sulphur dioxide'),
                'amount': 0.1,
                'unit': 'kg',
                'type': 'biosphere'
            }, {
                'input': ('testdb', 'Electricity production'),  # important to write the same process name in output
                'amount': 10,
                'unit': 'kWh',
                'type': 'production'
            }]
        },
    ('testdb', 'Fuel production'): {
        'name': 'Fuel production',
        'unit': 'kg',
        'exchanges': [{
                'input': ('testdb', 'Carbon dioxide'),
                'amount': 10,
                'unit': 'kg',
                'type': 'biosphere'
            }, {
                'input': ('testdb', 'Sulphur dioxide'),
                'amount': 2,
                'unit': 'kg',
                'type': 'biosphere'
            }, {
                'input': ('testdb', 'Crude oil'),
                'amount': -50,
                'unit': 'kg',
                'type': 'biosphere'
            }, {
                'input': ('testdb', 'Fuel production'),
                'amount': 100,
                'unit': 'kg',
                'type': 'production'
            }]
    },
    ('testdb', 'Carbon dioxide'): {'name': 'Carbon dioxide', 'unit': 'kg', 'type': 'biosphere'},
    ('testdb', 'Sulphur dioxide'): {'name': 'Sulphur dioxide', 'unit': 'kg', 'type': 'biosphere'},
    ('testdb', 'Crude oil'):{'name': 'Crude oil', 'unit':'kg', 'type': 'biosphere'}

    })

functional_unit = {t_db.get('Electricity production'): 1000}
lca = LCA(functional_unit)
lca.lci()
print(lca.inventory)


myLCIAdata = [[('testdb', 'Carbon dioxide'), 2.0],
              [('testdb', 'Sulphur dioxide'), 2.0],
              [('testdb', 'Crude oil'), 2.0]]

method_key = ('simplemethod', 'imaginaryendpoint', 'imaginarymidpoint')
my_method = Method(method_key)
my_method.validate(myLCIAdata)
my_method.register()
my_method.write(myLCIAdata)
my_method.load()

lca = LCA(functional_unit, method_key)  # LCA calculations with method
lca.lci()
lca.lcia()
print(lca.inventory)
print(lca.characterized_inventory)


# How to navigate activities and exchanges.

# I'll first get one activity
el = t_db.get('Electricity production')  # this is an activity (a DICT)
print(el)

for i in el:  # these the possible keys of an activity dictionary
    print(i)


el.as_dict()  # or just this (press '.' and then 'tab')
print(el['name'], el['code'], 
      el['unit'], el['database'])
el.get('unit')  # another way

#el['exchanges']  # this does not work.
#el.exchanges()  # neither this
list(el.exchanges())  # yeps, this one

for exc in el.exchanges():  # or this, visualize all exchanges of an activity
    print(exc)
    print(exc['type'])
    print(exc['input'][1])
    print(exc.input)


# get the first exchange of this activity
el_exc = list(el.exchanges())[0]   # the first exchange (this is also a DICT)

print(type(el))  # compare the three
print(type(el.exchanges()))
print(type(el_exc))

for i in el_exc:  # the possible keys of an exchange (DICT iteration)
    print(i, ':', el_exc[i])

el_exc.as_dict()  # or just this, as above
el_exc.items()  # another nice one
el_exc.unit == el_exc['unit']  # equivalent ways, different from activities
print(el_exc['amount'], el_exc['unit'], el_exc['input'], 'to',
      el_exc['output'], 'within', el_exc['type'])

el_exc_fp.input  # I guess the intended meaning of 'input' is "from'
el_exc_fp.output  # I guess the indended meaning of 'output' is 'to'


# What if I want to get a specific exchange of a specific activity
# Without using numeric indexing, but by using its name!
# Let's see if we can find the value of the CO2 emissions from el prod

for exc in list(el.exchanges()):
    if exc['input'] == ('testdb', 'Carbon dioxide'):
        print(exc)
    else:
        print('Not this one')
        
# Good. Now we store the value in a variable
for exc in list(el.exchanges()):
    if exc['input'] == ('testdb', 'Carbon dioxide'):
        elCO2_amount = exc['amount']

print(elCO2_amount)

