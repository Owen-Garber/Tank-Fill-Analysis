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
T_ext_prefill=[ 272.039, 274.817, 277.594, 280.372,283.15, 285.928, 288.706, 291.483, 294.261, 297.039, 299.817, 302.594, 305.372, 308.15]
c_v_vent=0.0028 #a flow coefficient for our vent valve, O'keefe B-11-SS, we can use to estimate m_dot. Would be 0.0067 for B-17-ss, or 0.00035 for B-4-SS
T_int = T_ext_prefill
c_v_fill_solenoid=.02
diam = 1 #arbitrary, diameter of flex hose
length = 1 #arbitrary, length of flex hose
final_list = []
for i in T_ext_prefill:
    P_ext = PropsSI('P', 'T', i, 'Q', 0, Fluid)*0.000145038 #hopefully a matrix of vapor pressures for external tank before filling
    delta_p_for_vent = PropsSI('P', 'T', i, 'Q', 0, Fluid)  # [Pa] Q here is the vapor quality, Q=0 since saturated liquid in the tank. This line gives the vapor pressure of the nitrous. assume same as tank pressure
    int_liquid_density = PropsSI ('D','P', delta_p_for_vent ,'Q' ,0 , Fluid ) # [should be kg/m^3] this is reasonable according to internet
    delta_p_for_vent = PropsSI('P', 'T', i, 'Q', 0, Fluid)*0.000145038  # [Pa] Q here is the vapor quality, Q=0 since saturated liquid in the tank. This line gives the vapor pressure of the nitrous. assume same as tank pressure
    #print(int_liquid_density)
    SG_n2o_int=int_liquid_density/1000  #pretty sure that the units match, [should be kg/m^3 for both]
    delta_p_for_fill = (P_ext-150)/2
    m_dot_orif = (c_v_vent*math.sqrt(delta_p_for_vent/SG_n2o_int))*int_liquid_density*60*0.00378541 #taken from eqn for volume flowrate from here: https://www.electricsolenoidvalves.com/blog/valve-flow-coefficient-how-calculate/#:~:text=The%20equation%20for%20calculating%20the,%E2%88%9A%20(SQ%2FP).
    print(m_dot_orif)
    fill_rate = (c_v_fill_solenoid*math.sqrt(delta_p_for_fill / SG_n2o_int)) * int_liquid_density*60*0.00378541 - m_dot_orif
    #print(fill_rate)
    fill_time = mass_n2o / fill_rate  # time to fill while venting at the m_dot_orif
    nitrous_waste=m_dot_orif*fill_time #[kg]
    mass_fluid = int_liquid_density*diam*length
    row_list = [i,nitrous_waste,fill_rate/m_dot_orif,fill_time,mass_fluid]
    final_list.append(row_list)

HEADER = ['Temp (K)','Nitrous Waste (kg)','M_Dot Ratio (Fill/Vent)','Fill Time (s)','Mass of Fluid in Flex Line (kg)']
for item in HEADER:
    print('{:<25s}'.format(item),end='')

print()

for item in final_list:
    for i in item:
        print('{:<25f}'.format(i),end='')
    print()

#treating as matrix of temps from 30F to 95F (in kelvin above), temp of external tank before filling
############derive values and solve for flow rate out of the vent orifice#######################################################################################################################
#treating as matrix of temps from 30F to 95F (in kelvin above), temp of external tank before filling

############derive values and solve for total flow rate including into and out of internal tank#######################################################################################################################
