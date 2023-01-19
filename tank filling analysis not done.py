#NOTE: goes with tank fill analysis document in hybrid propulsion 2022-2023 google drive
#Outputs: Fill Time, Nitrous Waste, and ratio of flow in to flow out
##################ALGORITHM####################################################################################################: 

#use cool prop, temp, volumes, and the lowest c_v flow coefficient in lines to find flow rates, fill time, and nitrous leakage.
#set up inputs, then create a for loop to calculate things we want at different temperatures. Append list of the info to a list of lists.
#after the for loop, format to put into a table
##################IMPORT STATEMENTS#####################################################################################################
import math
from CoolProp.CoolProp import PropsSI
#ALGORITHM 1: Find m_dot_orif, as a function of T_int
#ASSUMPTIONS OF MODEL: T_int=T_ext, our solenoid valve C_V is our bottleneck to our filling

##################INPUTS#################################################################################################################
Fluid = 'N2O'
mass_n2o=5.2707431 #[kg]
V_int=0.008068420320081144 #[m^3] volume of internal tank, currenty don't use this. Will need if incorporate temperature prediction
v_ext=0.013399702 #an ESTIMATION for the 20lbs external tank, [m^3], volume of external tank, also don't use this so far.
T_ext_prefill=[272.039, 274.817, 277.594, 280.372,283.15, 285.928, 288.706, 291.483, 294.261, 297.039, 299.817, 302.594, 305.372, 308.15] #[K]
c_v_vent=0.0028 #a flow coefficient for our vent valve, O'keefe B-11-SS, we can use to estimate m_dot. Would be 0.0067 for B-17-ss, or 0.00035 for B-4-SS
T_int = T_ext_prefill #an assumption to simplify model. Not extremely accurate
c_v_fill_solenoid=.02
diam = 1 #arbitrary, diameter of flex hose
length = 1 #arbitrary, length of flex hose
final_list = [] #create list to house information from for loop in a list of lists. Each list within
#################for loop to get info#######################################################################################################
for i in T_ext_prefill:
    P_ext = PropsSI('P', 'T', i, 'Q', 0, Fluid)*0.000145038 #[psi]hopefully a matrix of vapor pressures for external tank before filling
    delta_p_for_vent = PropsSI('P', 'T', i, 'Q', 0, Fluid)  # [Pa] must be [Pa] for now to input into int_liquid_density. Q here is the vapor quality, Q=0 since saturated liquid in the tank. This line gives the vapor pressure of the nitrous. assume same as tank pressure
    int_liquid_density = PropsSI ('D','P', delta_p_for_vent ,'Q' ,0 , Fluid ) # [should be kg/m^3] this is reasonable according to internet
    delta_p_for_vent = PropsSI('P', 'T', i, 'Q', 0, Fluid)*0.000145038  # [psi] We are redefining it in psi. Q here is the vapor quality, Q=0 since saturated liquid in the tank. This line gives the vapor pressure of the nitrous. assume same as tank pressure
    #print(int_liquid_density)
    SG_n2o_int=int_liquid_density/1000  #[unitless]pretty sure that the units match, [should be kg/m^3 for both]
    delta_p_for_fill = (P_ext-150)/2 #[psi]
    m_dot_orif = (c_v_vent*math.sqrt(delta_p_for_vent/SG_n2o_int))*int_liquid_density*60*0.00378541 #[NOT SURE] taken from eqn for volume flowrate from here: https://www.electricsolenoidvalves.com/blog/valve-flow-coefficient-how-calculate/#:~:text=The%20equation%20for%20calculating%20the,%E2%88%9A%20(SQ%2FP).
    print(m_dot_orif)
    fill_rate = (c_v_fill_solenoid*math.sqrt(delta_p_for_fill / SG_n2o_int)) * int_liquid_density*60*0.00378541 - m_dot_orif #[NOT SURE]
    #print(fill_rate)
    fill_time = mass_n2o / fill_rate  # [sec] time to fill while venting at the m_dot_orif
    nitrous_waste=m_dot_orif*fill_time #[kg]
    mass_fluid_in_flex_line = int_liquid_density*diam*length #[kg], want to ensure not too much that it detracts from how much we can fill. 
    row_list = [i,nitrous_waste,fill_rate/m_dot_orif,fill_time,mass_fluid_in_flex_line]
    final_list.append(row_list)
############Formating into a table and printing########################################################################################################
HEADER = ['Temp (K)','Nitrous Waste (kg)','M_Dot Ratio (Fill/Vent)','Fill Time (s)','Mass of Fluid in Flex Line (kg)']
for item in HEADER:
    print('{:<25s}'.format(item),end='')

print()

for item in final_list:
    for i in item:
        print('{:<25f}'.format(i),end='')
    print()
