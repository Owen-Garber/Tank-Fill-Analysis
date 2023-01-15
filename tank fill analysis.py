#Note: Goes with tank fill analysis document in hybrid propulsion 2022-2023 google drive
#Outputs: Fill Time, Nitrous Waste, and temperature drop
#ALGORITHM: use cool prop, temp, volumes, and the lowest c_v flow coefficient in lines to find fill time and nitrous leakage
import math
from CoolProp.CoolProp import PropsSI
#ALGORITHM 1: Find m_dot_orif, as a function of T_int, where T_int is a function of T_ext_prefill

#inputs#################################################################################################################
Fluid = 'N2O'
mass_n2o=5.2707431 #[kg]
V_int=0.008068420320081144 #[m^3] volume of internal tank
v_ext=0.013399702 #an estimation from another 20lbs tank, [m^3], volume of external tank
T_ext_prefill=[272.039, 274.817, 277.594, 280.372, 283.15, 285.928, 288.706, 291.483, 294.261, 297.039, 299.817, 302.594, 305.372, 308.15]
#treating as matrix of temps from 30F to 95F (in kelvin above), temp of external tank before filling
P_ext = PropsSI('P', 'T', T_ext_prefill, 'Q', 0, Fluid) #hopefully a matrix of vapor pressures for external tank before filling
c_v_vent=0.0028 #a flow coefficient for our vent valve, O'keefe B-11-SS, we can use to estimate m_dot. Would be 0.0067 for B-17-ss, or 0.00035 for B-4-SS

############derive values and solve for flow rate out of the vent orifice#######################################################################################################################

T_int = [272.039, 274.817, 277.594, 280.372, 283.15, 285.928, 288.706, 291.483, 294.261, 297.039, 299.817, 302.594, 305.372, 308.15]
#treating as matrix of temps from 30F to 95F (in kelvin above), temp of external tank before filling
delta_p_for_vent= PropsSI('P', 'T', T_int, 'Q', 0, Fluid)  # [Pa] Q here is the vapor quality, Q=0 since saturated liquid in the tank. This line gives the vapor pressure of the nitrous. assume same as tank pressure
int_liquid_density = PropsSI ('D','P', delta_p_for_vent ,'Q' ,0 , Fluid ) # [should be kg/m^3] this is reasonable according to internet
SG_n2o_int=int_liquid_density/1000  #pretty sure that the units match, [should be kg/m^3 for both]
delta_p_for_fill=P_ext - PropsSI('P', 'T', T_int, 'Q', 0, Fluid)
m_dot_orif=(c_v_vent/math.sqrt(SG_n2o_int/delta_p_for_vent))*int_liquid_density #taken from eqn for volume flowrate from here: https://www.electricsolenoidvalves.com/blog/valve-flow-coefficient-how-calculate/#:~:text=The%20equation%20for%20calculating%20the,%E2%88%9A%20(SQ%2FP).

############derive values and solve for total flow rate including into and out of internal tank#######################################################################################################################

c_v_fill_solenoid=.02 #from our specs here: https://www.mcmaster.com/1190N23/    pretty sure this will be the lowest in the fill lines and what bottlenecks flow
fill_rate= (c_v_fill_solenoid/math.sqrt(SG_n2o_int/delta_p_for_fill))*int_liquid_density-m_dot_orif
fill_time= mass_n2o/fill_rate#time to fill while venting at the m_dot_orif
nitrous_waste=m_dot_orif*fill_time #[kg]
