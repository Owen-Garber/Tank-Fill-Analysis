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
V_ext=0.013399702 #an ESTIMATION for the 20lbs external tank, [m^3], volume of external tank, also don't use this so far.
T_ext_prefill=[272.039, 274.817, 277.594, 280.372,283.15, 285.928, 288.706, 291.483, 294.261] #removed these values: 297.039, 299.817, 302.594, 305.372, 308.15] #[K]
c_v_vent=0.0028 #a flow coefficient for our vent valve, O'keefe B-11-SS, we can use to estimate m_dot. Would be 0.0067 for B-17-ss, or 0.00035 for B-4-SS
T_int = T_ext_prefill #an assumption to simplify model. Not extremely accurate
c_v_fill_solenoid=.02
diam = 0.0127 #[m], diameter of flex hose
length = 5.4864 #[m], length of flex hoses we have
final_list = [] #create list to house information from for loop in a list of lists. Each list within
total_nitrous = 9.07185 #kg of nitrous we have (abt 20 lbs)
m_dot_list = []
#################for loop to get info#######################################################################################################
for i in T_ext_prefill:
    P_ext = PropsSI('P', 'T', i, 'Q', 1, Fluid)/1000 #[kPa]hopefully a matrix of vapor pressures for external tank before filling
    delta_p_for_vent = PropsSI('P', 'T', i, 'Q', 1, Fluid)  # [Pa] must be [Pa] for now to input into int_liquid_density. Q here is the vapor quality, Q=0 since saturated liquid in the tank. This line gives the vapor pressure of the nitrous. assume same as tank pressure
    int_liquid_density = PropsSI ('D','P', delta_p_for_vent ,'Q' ,0 , Fluid ) # [should be kg/m^3] this is reasonable according to internet
    int_vapor_density=PropsSI ('D','P', delta_p_for_vent ,'Q' ,1 , Fluid )
    #Add ullage fluid density
    delta_p_for_vent = PropsSI('P', 'T', i, 'Q', 1, Fluid)/1000  # [kPa] We are redefining it in psi. Q here is the vapor quality, Q=0 since saturated liquid in the tank. This line gives the vapor pressure of the nitrous. assume same as tank pressure
    SG_n2o_int=int_vapor_density/1000  #[unitless]pretty sure that the units match, [should be kg/m^3 for both]
    ##################REALLY UNSURE IF WE SHOULD BE DOING SG OF N2O IN GASEOUS FORM. NOT SURE IF EQN HOLDS FOR GASSES##########################
    ######### TRYING TO SOLVE BASED ON THIS: https://www.idealvalve.com/pdf/Flow-Calculation-for-Gases.pdf but cant find in metric yet
    #########"When the upstream pressure equals or exceeds two times the downstream pressure DEFINITELY IN OUR CASE, it is known as a ???choked flow??? situation.
    ######### This calls for use of a Critical flow formula, can't find in metric at the moment
    #########################################################################################################################################
    delta_p_for_fill = (P_ext-1034.21)/2 #[kPa] assuming that the delta p will be linear and the average will be half of difference of initial pressure in external tank, and the ~150psi left in tank when it empties fully
    m_dot_orif = ((c_v_vent*int_vapor_density)/(11.6*math.sqrt(SG_n2o_int/delta_p_for_vent)*3600)) #[kg/s] taken from eqn for volume flowrate from here: https://www.engineeringtoolbox.com/flow-coefficients-d_277.html
    m_dot_list.append(m_dot_orif)
    fill_rate = ((c_v_fill_solenoid*int_liquid_density)/(11.6*math.sqrt(SG_n2o_int/delta_p_for_fill)*3600)) - m_dot_orif #[kg/s]
    fill_time = mass_n2o / fill_rate  # [sec] time to fill while venting at the m_dot_orif
    nitrous_vented=m_dot_orif*fill_time #[kg]
    mass_fluid_in_flex_line = int_liquid_density*(diam/2)**2*math.pi*length #[kg], want to ensure not too much that it detracts from how much we can fill.
    excess_nitrous = total_nitrous - (mass_n2o+nitrous_vented+mass_fluid_in_flex_line)
    max_stoppage_time = excess_nitrous/m_dot_orif
    row_list = [i,nitrous_vented,fill_rate/m_dot_orif,fill_time,mass_fluid_in_flex_line,excess_nitrous,max_stoppage_time,delta_p_for_fill*0.145038]
    final_list.append(row_list)

    ##########TEST PRINT STATEMENTS####################################################################
    #print("Fill rate is",fill_rate)
    #print("m_dot_orif is", m_dot_orif)
    #print("int_liquid_density is",int_liquid_density)
    #print(
############Formating into a table and printing########################################################################################################
HEADER = ['Temp (K)','Nitrous Vented (kg)','M_Dot Ratio (Fill/Vent)','Fill Time (s)','Mass of Fluid in Flex Line (kg)','Excess Nitrous (kg)', 'Max Stoppage Time (s)', 'approximate avg \u0394P for Fill (psi)']
for item in HEADER:
    print('{:<35s}'.format(item),end='')

print()

for item in final_list:
    for i in item:
        print('{:<35f}'.format(i),end='')
    print()
######find time to reduce pressure a certain amount through the bleed valve with the fill line shut off, starting at pressure P1 and ending at P2 for a delta of P2-P1, over a time t##################################################################################################################################################

fill_percent_list = []
initial_fill_percent = .4
while initial_fill_percent < .85: #used to be .85
    initial_fill_percent += .025
    fill_percent_list.append(initial_fill_percent)

R = 8.3144598 #[J/(K*mol)] gas constant
delta_p = 0.0 #[Pa] initializing as zero
delta_p_target = 1000000 #[Pa]

####lists to output#############

print()
print()
print("##########################################################################################################################")
print()
print()
NEW_HEADER = [ 'ullage percentage','Temp (K)','Time to vent target pressure (s)', 'm_lost [kg]']
for item in NEW_HEADER:
    print('{:<35s}'.format(item), end='')

print()

new_row_list=[]
for i in fill_percent_list:
    V_gas_n2o=V_ext*(1-i)
    n_i = (P_ext*V_gas_n2o)/(R*T_ext_prefill[-1]) #[mols]
    for u in T_ext_prefill:
        P_i = PropsSI('P', 'T', u, 'Q', 1,Fluid)  # [Pa]hopefully a matrix of vapor pressures for external tank before filling
        n_i = (P_i * V_gas_n2o) / (R * u) #[mols]
        delta_p = 0.0
        t = 0.0  # [s] initialize as zero
        dt= .001 #[s] increments to iterate over
        P_f=P_i
        m_lost=0
        while delta_p < delta_p_target: #[Pa]
            int_vapor_density=PropsSI ('D','P', P_f ,'Q' ,1 , Fluid ) # [should be kg/m^3] density of vapor only
            m_dot_orif = ((c_v_vent * int_vapor_density) / (11.6 * math.sqrt((int_vapor_density/1000) / P_f) * 3600))  # [kg/s]
            n_dot_orif=m_dot_orif/.044013 #converts m_dot_orif from kg/s to [mol/s]
            n_f = n_i - (n_dot_orif * dt) #[mols] creating new number of moles
            n_i = n_f #redefining n_i as the new number of moles, n_f
            P_f = (n_f * R * u) / ( V_gas_n2o)
            t += dt
            delta_p = P_i-P_f
            m_lost+=m_dot_orif*dt
            if delta_p > delta_p_target:
                new_row_list.append([1-i,u,t,m_lost])
        print('{:<35f}{:<35f}{:<35f}{:<35f}'.format(1 - i, u, t, m_lost))

#print()
#print()
#print("##########################################################################################################################")
#print()
#print()
#NEW_HEADER = [ 'ullage percentage','Temp (K)','Time to vent target pressure (s)', 'm_lost [kg]']
#for item in NEW_HEADER:
    #print('{:<35s}'.format(item), end='')

#print()

#for item in new_row_list:

    #for i in item:
            #print('{:<35f}'.format(i), end='')
    #print()
