# -*- coding: utf-8 -*-
'''
Created on Tue Jan 10 15:09:02 2017

@author: massimo
'''

from brightway2 import *
import pandas as pd
from matplotlib.pylab import *


t_db = Database('testdb')

t_db.write({  # A simplified version, only CO2 as emission
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
                'input': ('testdb', 'Fuel production'),
                'amount': 100,
                'unit': 'kg',
                'type': 'production'
            }]
    },
    ('testdb', 'Carbon dioxide'): {'name': 'Carbon dioxide', 'unit': 'kg', 'type': 'biosphere'}
    })

functional_unit = {t_db.get('Electricity production'): 1000}
lca = LCA(functional_unit)
lca.lci()
print(lca.inventory)


myLCIAdata = [[('testdb', 'Carbon dioxide'), 1.0]]

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
print(lca.score)


# Now add uncertainty 
# Tutorial here:
# http://nbviewer.jupyter.org/urls/bitbucket.org/cmutel/brightway2/raw/default/notebooks/Activities%20and%20exchanges.ipynb


# NOTE: uncertainties are always added to EXCHANGES (not to ativities...)
# So I'll get one  exchange from one activity
el = t_db.get('Electricity production')  
co2_exc = list(el.exchanges())[1]   # the second exchange

# Lognormal distr first
from stats_arrays import LognormalUncertainty
import numpy as np
co2_exc['uncertainty type'] = LognormalUncertainty.id
print(co2_exc['uncertainty type'])

co2_exc['loc'], co2_exc['scale'] = np.log(co2_exc['amount']), np.log(1.01)
#co2_exc['loc'], co2_exc['scale']  = np.log(-co2_exc['amount']), np.log(1.01)
co2_exc.save()
co2_exc.uncertainty  # check that
co2_exc.as_dict()  # Now uncertainty included
co2_exc.random_sample(n=10)  # perfect

# this in case you want to try with normal dist
from stats_arrays import NormalUncertainty

co2_exc['uncertainty type'] = NormalUncertainty.id
co2_exc['loc'], co2_exc['scale'] = 1, 0.01
co2_exc.save()
co2_exc.uncertainty  # check that
co2_exc.as_dict()  # OK
co2_exc.random_sample(n=10)  # perfect


#  Now MC simulation
#  Sources here:
'''
1) example: http://stackoverflow.com/questions/38532146/obtaining-distribution-of-results-from-lcia
2) example: https://brightwaylca.org/examples/getting-started.html
3) source code: https://bitbucket.org/cmutel/brightway2-calc/src/662740694a8c70074105b5dca45b58651adb5eb5/bw2calc/monte_carlo.py?at=default&fileviewer=file-view-default
'''

# Check uncertainty info is stored
makeatest = list(el.exchanges())[1]
makeatest.uncertainty  # ok works

# This is the montecarlo simulation
mc = MonteCarloLCA({el: 1000}, method_key)  # Monte Carlo class
mc_results = [next(mc) for x in range(500)]

# Look at the MC results
hist(mc_results, density=True)  # From matplotlib package
ylabel("Probability")
mean(mc_results)
median(mc_results)
np.exp(mean(np.log(mc_results))) # geometric mean VERY close to 120
pd.DataFrame(mc_results).describe()  # Using the pandas package
lca.score


# Do this again and compare results
mc2 = MonteCarloLCA({el: 1000}, method_key)  # Monte Carlo class
mc2_results = [next(mc2) for x in range(500)]
hist(mc2_results, density=True)
ylabel("Probability")

scatter(mc_results, mc2_results) # Correct. Do you understand why?


# Another way to do it
iterations = 1000
scores = np.zeros([1, iterations])  # 1-dimensional array filled with zeros
for iteration in range(iterations):
    next(mc)
    scores[0, iteration] = mc.score
for i in range(1, 10):
    print(scores[0][i])  # need the zero because one-dimensional array


# Another way, get a list instead of an array
iterations = 1000
scores = []
for iteration in range(iterations):
    next(mc)
    scores.append(mc.score)
for i in range(1, 10):
    print(scores[i])
type(scores) == type(mc_results)  # same type of results as in the first case
