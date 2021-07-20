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
Primary frequency regulation based on the algorithm in Codani, 2016.


# PARAMETERS:
When creating a set of vehicles to simulate, you can specify the following parameters:
CHARGING PARAMETERS

ch_power : Charging power [kW], default 3.6

ch_eff : Charger efficiency [pu], default 0.95 

dr_eff : Driving efficiency/consumption [kWh/km], default 0.2

PLUG-IN DECISION PARAMETERS

charging_type: plug-in behavior of the user. Types: if_needed (non-systematic), all_days, and others

alpha: plug-in preference of user. Default value given by calibration with Electric Nation data.

range_anxiety: 
