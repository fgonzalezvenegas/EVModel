# EVModel
The EVModel is an agent based EV charging simulation model. It allows to generate charging, availability,
and flexibility profiles for large numbers of EVs for several weeks, and considering different charging strategies.

It includes a non-systematic plug-in behavior model. If you use it, please reference the associated paper: Gonzalez Venegas, F., Petit, M., Perez, Y., "Plug-in behavior of electric vehicles users: insights from alarge-scale trial and impacts for grid integration studies" 2021, eTransportation.

A script to generate EV charging profiles is provided.

# CHARGING STRATEGIES:

# Uncontrolled:
The charging process starts as soon as possible

# Modulated:
The charging process is done at constant power during the whole charging session.

# Cost minimization:
Optimized charging based on variable costs using cvxopt library

# Reversed:
Similar to Uncontrolled, but charging starts at the end of charging session, ensuring a full charge.

# RandStart:
Charging process starts at a random moment between the start and end of charging session, ensuring a full charge.

# PFC: 
Primary frequency regulation based on the algorithm in Codani, Integration des véhicules électriques dans les réseaux électriques : Modèles d’affaire et contraintes techniques pour constructeurs automobiles, PhD Thesis, Université Paris-Saclay, 2016.


# PARAMETERS:
When creating a set of vehicles to simulate, you can specify the following parameters:

EV PARAMETERS

batt_size: Battery size [kWh]

dr_eff : Driving efficiency/consumption [kWh/km], default 0.14 + 0.0009*batt_size

CHARGING PARAMETERS

ch_power : Charging power [kW], default 3.6

ch_eff : Charger efficiency [pu], default 0.95 

pmin_charger: Minimum charging power [pu] (modulated charging only). Default: 0

target_soc: Objective State-of-Charge at the end of the session. Default: 1

PLUG-IN DECISION PARAMETERS

charging_type: plug-in behavior of the user. Types: if_needed (non-systematic), all_days, and others

alpha: plug-in preference of user. Default value given by calibration with Electric Nation data.

range_anxiety: The margin with respect to next-trip distance under which the user always plugs in. Default 1.5

ARRIVAL, DEPARTURE AND DISTANCES PARAMETERS:

dist_wd: Dictionnary of probability parameters for week-day distances. (see example.py)

dist_we: Dictionnary of probability parameters for week-end distances. 

arrival_departure_data: Dictionnary of probability parameters for week-day arrival and departure times.

TIME-OF-USE CHARGING:

tou_ini: hour at which the off-peak period starts (weekdays)
tou_end: hour at which the off-peak period ends
tou_we: Whether there is an off-peak peariod during the weekend. If false, the whole weekend is considered as off-peak
tou_ini_we: hour at which the off-peak period starts during weekends
tou_end_we: hour at which the off-peak period starts durign weekends

OTHER:
boss: Aggregator (object) that will set prices/limits to the charging process.
