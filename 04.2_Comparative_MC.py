#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 30 07:05:07 2018

@author: massimo
"""

from brightway2 import *
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from scipy import stats

projects
projects.set_current('bw2_import_ecoinvent_3.4')
databases

db = Database("ecoinvent 3.4 conseq")

ipcc = ('IPCC 2013', 'climate change', 'GTP 100a')


# Simple montecarlo on ecoinvent process as we know it.
mydemand = {db.random(): 1}  # select a random process
lca = LCA(mydemand, ipcc)
lca.lci()
lca.lcia()
lca.score

mc = MonteCarloLCA(mydemand, ipcc)
mc_results = [next(mc) for x in range(500)]

plt.hist(mc_results, density=True)
plt.ylabel("Probability")
plt.xlabel(methods[ipcc]["unit"])

pd.DataFrame(mc_results).describe() 

lca.score
np.exp(np.mean(np.log(mc_results))) # geometric mean



# Now comparative analysis
db.search('lorry transport euro5') # look at the names

activity_name = 'transport, freight, lorry >32 metric ton, EURO5'    
for activity in Database("ecoinvent 3.4 conseq"):
    if activity['name'] == activity_name:
        truckE5 = Database("ecoinvent 3.4 conseq").get(activity['code'])

activity_name = 'transport, freight, lorry >32 metric ton, EURO6'    
for activity in Database("ecoinvent 3.4 conseq"):
    if activity['name'] == activity_name:
        truckE6 = Database("ecoinvent 3.4 conseq").get(activity['code'])


truckE5.as_dict()
truckE6.as_dict()

# make a list with the alternatives
demands = [{truckE5: 1}, {truckE6: 1}]

mc = MonteCarloLCA(demands[0], ipcc)
next(mc)

# look at this first
mc.redo_lcia(demands[0])
mc.score
mc.redo_lcia(demands[1])
mc.score
mc.redo_lcia(demands[0])
mc.score

# Now for several iterations
iterations = 100
simulations = []

for _ in range(iterations):
    print(_)
    next(mc)
    mcresults = []    
    for i in demands:
        mc.redo_lcia(i)
        mcresults.append(mc.score)
    simulations.append(mcresults)
    
    
simulations
df = pd.DataFrame(simulations, columns = ['truckE5','truckE6'])
df.to_csv('ComparativeMCsimulation.csv') # to save it

#plot stuff (using the matplotlib package)

df.plot(kind = 'box')
#df.T.melt()

plt.plot(df.truckE5, df.truckE6, 'o')
plt.xlabel('truckE5 - kg CO2-eq')
plt.ylabel('truckE6 - kg CO2-eq')

# You can see how many times the difference is positive. This is what Simapro does

df.diffe = df.truckE5 - df.truckE6
plt.hist(df.diffe.values)
len(df.diffe[df.diffe < 0])
len(df.diffe[df.diffe > 0])
len(df.diffe[df.diffe == 0])

# Statistical testing (using the stats package)
# I can use a paired t-test

t_value, p_value = stats.ttest_rel(df.truckE5,df.truckE6)
t_value
p_value

# But wait! did we check for normality?
plt.hist(df.truckE5.values)
plt.xlabel('truckE5 - kg CO2-eq')

SW_value, SW_p_value = stats.shapiro(df.truckE5)
SW_p_value # Not normally distributed...

plt.hist(df.truckE6.values)
SW_value, SW_p_value = stats.shapiro(df.truckE6)
SW_p_value # Normally distributed if alpha = 0.05...Not strong though if we hasd say 1000 samples

# Alright need a non-parametric test. Wilcox sign rank test
s_value, p_value = stats.wilcoxon(df.truckE5, df.truckE6)
s_value
p_value # Not bad, significant difference!



# What if we had done the MC on the processes independently.
mc1 = MonteCarloLCA({truckE5: 1}, ipcc)
mc1_results = [next(mc1) for x in range(100)]

mc2 = MonteCarloLCA({truckE5: 1}, ipcc)  # it's still truckE5!
mc2_results = [next(mc2) for x in range(100)]

df_ind = pd.DataFrame({'mc1': mc1_results, 'mc2' : mc2_results})

# compare to this
demands = [{truckE5: 1}, {truckE5: 1}]  # I am using the smae process two times.
mc = MonteCarloLCA(demands[0], ipcc)
iterations = 100
simulations = []

for _ in range(iterations):
    print(_)
    next(mc)
    mcresults = []    
    for i in demands:
        mc.redo_lcia(i)
        mcresults.append(mc.score)
    simulations.append(mcresults)
    
    
simulations
df_dep = pd.DataFrame(simulations, columns = ['mc1','mc2'])

# Plot stuff
df_dep.plot(kind = 'box')
df_ind.plot(kind = 'box')

plt.plot(df_dep.mc1, df_dep.mc2, 'o')
plt.plot(df_ind.mc1, df_ind.mc2, 'o') # see?

# and of course:
t_value, p_value = stats.ttest_rel(df_dep.mc1, df_dep.mc2)
t_value
p_value  # no difference AT ALL (as expected)

t_value, p_value = stats.ttest_rel(df_ind.mc1, df_ind.mc2)
t_value
p_value  # no difference (as expected! But still some variance!)

s_value, p_value = stats.wilcoxon(df_ind.mc1, df_ind.mc2)
s_value
p_value





