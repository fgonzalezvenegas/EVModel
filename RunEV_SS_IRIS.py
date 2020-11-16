# -*- coding: utf-8 -*-
"""
Created on Mon Nov  9 19:06:48 2020

@author: U546416
"""
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import EVmodel
import time

times = [time.time()]
# DATA DATA
print('Loading data')
# Load data
# DAILY DISTANCE 
# Histograms of Distance per commune
print('Loading Histograms of distance')
folder_hdata = r'c:\user\U546416\Documents\PhD\Data\Mobilité'
hhome = pd.read_csv(folder_hdata + r'\HistHomeModal.csv', 
                    engine='python', index_col=0)
hwork = pd.read_csv(folder_hdata + r'\HistWorkModal.csv', 
                    engine='python', index_col=0)
if 'ZE' in hwork.columns:
    hwork = hwork.drop(['ZE', 'Status', 'UU', 'Dep'], axis=1)
    hhome = hhome.drop(['ZE', 'Status', 'UU', 'Dep'], axis=1)
times.append(time.time())
print('Finished loading, elapsed time: {} s'.format(np.round(times[-1]-times[-2],1)))

# DEMOGRAPHIC DATA, NUMBER OF RESIDENTS & WORKERS PER IRIS
# IRIS & Commune info
print('Loading IRIS')
folder_consodata = r'c:\user\U546416\Documents\PhD\Data\Mobilité\Data_Traitee\Conso'
iris = pd.read_csv(folder_consodata + r'\IRIS_enedis_2017.csv', 
                    engine='python', index_col=0)
times.append(time.time())
print('Finished loading, elapsed time: {} s'.format(np.round(times[-1]-times[-2],1)))

# DISTRIBUTION OF ARRIVAL AND DEPARTURES
# Histograms of arrival/departures
print('Arrival departures')
# Bi variate distributions for arrival/departures
folder_arrdep = r'c:\user\U546416\Documents\PhD\Data\Mobilité\Data_Traitee\Mobilité'
res_arr_dep_wd = pd.read_csv(folder_arrdep + r'\EN_arrdep_wd_modifFR.csv', 
                             engine='python', index_col=0)
res_arr_dep_we = pd.read_csv(folder_arrdep + r'\EN_arrdep_we_modifFR.csv', 
                             engine='python', index_col=0)
# Bi-variate distribution
work_arr_dep_wd = pd.read_csv(folder_arrdep + r'\Arr_Dep_pdf.csv', 
                          engine='python', index_col=0)
times.append(time.time())
print('Finished loading, elapsed time: {} s'.format(np.round(times[-1]-times[-2],1)))



# PARAMETERS OF SIMULATION

#############################
# IRIS TO SIMULATE
# iris_ss should be a list/pandas Series with IRIS codes
data_ss = pd.read_csv(r'c:\user\U546416\Documents\PhD\Data\MVGrids\Boriette\ProcessedData\MVLV.csv',
                       index_col=0, engine='python')
iris_ss = data_ss.Geo.unique()    
############################

###########################
# SIMULATION PARAMETERS
# Days, steps
nweeks = 3
ndays = 7 + 7*nweeks + 1 # Recommended to have at least 1 extra day at the end and one week before.
step = 15 # time step (minutes)

###########################################
# GENERAL EV DATA

# EV penetration (0 to 1)
ev_penetration = 1
# EV home/work charging (0 to 1). 0.3 means 30% of EVs will charge 'at work'
ev_work_ratio = 0.3
# EV charging parameters (charging power, battery size, etc)
charging_power_home=7.2
charging_power_work=10
batt_size = 50

# Tou is used if Off-peak hours are enforced for home charging
tou = False
#tou_ini = 23
#tou_end = 8
#h_tous = 10
#start_tous = 21
#end_tous = 3
#delta_tous = (end_tous - start_tous) % 24


#####################################################
# ARRIVAL AND DEPARTURE SCHEDULES
#####################################################

# Arrival and departure hourly CDFs
n = res_arr_dep_wd.shape[0]
bins = np.arange(0,24.5,0.5)
arr_dep_data_h_wd = dict(pdf_a_d=res_arr_dep_wd.values,
                         bins=bins)
arr_dep_data_h_we = dict(pdf_a_d=res_arr_dep_we.values,
                         bins=bins)
arr_dep_data_w = dict(pdf_a_d=work_arr_dep_wd.values)

###############################################
# CREATING SET OF PARAMETERS TO CREATE EV TYPES
##############################################
# these are common for all types of evs
general_params = dict(batt_size = batt_size)

# these are for each kind of EV type
# Home charging params
home_params = dict(charging_power = charging_power_home,
                   arrival_departure_data_wd = arr_dep_data_h_wd,
                   arrival_departure_data_we = arr_dep_data_h_we,
                   charging_type = 'if_needed',
                   n_if_needed = 0.15,   # This gives a mean of 2.5 plugs per week, similar to seen in demo projects
                   tou_we=False) 
# Day charging params
day_params = dict(charging_power = charging_power_work,
                  arrival_departure_data_wd = arr_dep_data_w,
                  charging_type = 'weekdays',
                  tou_we = False,
                  dist_we= 0, # To have 0 distance during weekends
                  pmin_charger=0.8)


#%% Create Grid
times.append(time.time())
grid = EVmodel.Grid(ndays=ndays, step=step)
# Add EVs for each IRIS
#for i in iris_ss.index:
for i in iris_ss:
    # Compute # of EVs 
    # Number of Evs
#    comm = iris_ss.COMM_CODE[i]
    comm  = int(i)//10000
    nevs_h = int(iris.N_VOIT[i] * ev_penetration * (1-ev_work_ratio))
    nevs_w = int(hwork.loc[comm].sum() * iris.Work_pu[i] * # First term is total work EVs in the commune, second is the ratio of Workers in the iris
                 ev_penetration * ev_work_ratio * 1.78) # 1.78 is the ratio between nation-wide Work EVs and Total EVs  
    print('EVs Overnight', nevs_h)
    print('EVs Work', nevs_w)
    
    
    # Add EVs
    grid.add_evs('Home_' + str(i) , nevs_h, ev_type='dumb',
                 #pmin_charger=0.1,
                 dist_wd=dict(cdf = hhome.loc[comm].cumsum()/hhome.loc[comm].sum()),
                 **general_params,
                 **home_params)  
    grid.add_evs('Work_' + str(i), nevs_w, ev_type='mod',
                 dist_wd= dict(cdf = hwork.loc[comm].cumsum()/hwork.loc[comm].sum()),
                 **general_params,
                 **day_params)

times.append(time.time())
print('Finished preprocessing, elapsed time: {} s'.format(np.round(times[-1]-times[-2],1)))


#%% Do simulations
times.append(time.time())
grid.do_days()
times.append(time.time())
print('Finished running, elapsed time: {} s'.format(np.round(times[-1]-times[-2],1)))
global_data = grid.get_global_data()
ev_data = grid.get_ev_data()
grid.plot_total_load(day_ini=7, days=7)
grid.plot_ev_load(day_ini=7, days=7)

print('EV mean dist')
for t in grid.ev_sets:
    if 'Home' in t:
        print(t, 'Wd: ', np.round(np.mean([ev.dist_wd for ev in grid.evs_sets[t]]),1),
              ';  Weekend: ', np.round(np.mean([ev.dist_we for ev in grid.evs_sets[t]]),1))
for t in grid.ev_sets:
    if 'Home' in t:
        print(t, 'Wd: ', np.round(np.mean([ev.dist_wd for ev in grid.evs_sets[t]]),1), 
              ';  Weekend: ', np.round(np.mean([ev.dist_we for ev in grid.evs_sets[t]]),1))

print('EV plug in')
for t in grid.ev_sets:
    if 'Home' in t:
        print(t, 'Wd: ', np.round(np.mean([ev.ch_status.sum() for ev in grid.evs_sets[t]])/grid.ndays,3))
for t in grid.ev_sets:
    if 'Work' in t:
        print(t, 'Wd: ', np.round(np.mean([ev.ch_status.sum() for ev in grid.evs_sets[t]])/grid.ndays,3))


#%% Get EV data and save
output_folder = ''
init_idx = int(7 * 24 *60 / step)
end_idx =  int(1 * 24 *60 / step)
evdata = {}
for t in grid.evs:
    evdata[t] = grid.ev_load[t][init_idx:-end_idx]
evdata = pd.DataFrame(evdata)

evdata.to_csv(output_folder + 'EV_data.csv')