from qsystems import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import numpy as np
from calculation import *
# from gui import *

def find_optimal_configuration(parameters):
    Lambda = parameters['lambda']     
    r_p = parameters['r_p']        
    P_E = parameters['P_E']         
    N_E = parameters['N_E']         
    T_E = parameters['T_E']        
    T_E_distr = parameters['T_E_distr']   
    B_p = parameters['B_p']         
    C_E = parameters['C_E']        
    N_C = parameters['N_C']         
    T_C = parameters['T_C']         
    T_C_distr = parameters['T_C_distr']  
    C_C = parameters['C_C']         
    C_C_pricing = parameters['C_C_pricing'] 
    W_cr = parameters['W_cr']        
    T_bat_cr = parameters['T_bat_cr']  

    if T_E_distr ==  'Determined':
        qs_E = 'md1'
    if T_E_distr ==  'Exponential':
        qs_E = 'mm1'
    if T_C_distr ==  'Determined':
        qs_C = 'md1'
    if T_C_distr ==  'Exponential':
        qs_C = 'mm1'

    mu_C = 1/T_C
    mu_E = 1/T_E
    P_C = 1 - P_E

    def model(N_E, N_C):
        lambda_Ecr = msqs_ar_cr(sn=N_E-1,sr=mu_E,w=W_cr,qs=qs_E)
        lambda_Ccr = msqs_ar_cr(sn=N_C-1,sr=mu_C,w=W_cr,qs=qs_C)
                # ok
        if Lambda_E > 0:
            P_Ea=np.where(Lambda_E > lambda_Ecr,1-((Lambda_E-lambda_Ecr)/Lambda_E),1)
        else:
            P_Ea = 0
        if Lambda_C > 0:    
            P_Ca=np.where(Lambda_C > lambda_Ccr,1-((Lambda_C-lambda_Ccr)/Lambda_C),1)
        else:
            P_Ca = 0

        rho_E = Lambda_E/(N_E*mu_E)
        rho_C = Lambda_C/(N_C*mu_C)
        if C_C_pricing == "Dedicated":
            C_S = N_E*C_E + N_C*C_C
        if C_C_pricing == "On-demand":
            C_S = N_E*C_E + N_C*C_C*rho_C
       
        R_S = (Lambda_E*P_Ea + Lambda_C*P_Ca)*r_p
        P_S = R_S - C_S
        return P_S,R_S,C_S

    Lambda_E = P_E * Lambda
    Lambda_C = (1-P_E) * Lambda

    if Lambda_E != 0:
        N_Emax = msqs_sn_cr(ar=Lambda_E,sr=mu_E,w=W_cr,qs=qs_E)
    else:
        N_Emax = 100
    if Lambda_C != 0:
        N_Cmax = msqs_sn_cr(ar=Lambda_C,sr=mu_C,w=W_cr,qs=qs_C)
    else:
        N_Cmax = 100
    
    # This line ensures that battery-powered Edge device working time > T_B_min
    N_E_bat_cr = np.ceil((Lambda_E*T_bat_cr)/B_p) 

    N_E = np.arange(N_E_bat_cr,N_Emax*2+1,1)
    N_C = np.arange(2,N_Cmax*2+1,1)
    NN_E, NN_C = np.meshgrid(N_E, N_C)
    PP_S,RR_S,CC_S = model(NN_E, NN_C)

    # Find the global maximum revenue value
    PP_S_max = np.max(PP_S) # global max profit

    # Find the indices where the global maximum profit occurs
    max_indices = np.where(PP_S == PP_S_max)

    # Find the indices of the maximum revenue
    # print("max_indices",max_indices)

    # Extract the corresponding values of N_Eopt and N_Copt
    N_E_opt = N_E[max_indices[1][0]]
    N_C_opt = N_C[max_indices[0][0]]

    N_E_opt_ind = max_indices[1]
    N_C_opt_ind = max_indices[0]
   
    parameters['NN_E'] = NN_E
    parameters['NN_C'] = NN_C
    parameters['PP_S'] = PP_S
    parameters['RR_S'] = RR_S
    parameters['CC_S'] = CC_S
    parameters['PP_S_max'] = PP_S_max
    parameters['N_E_opt'] = N_E_opt
    parameters['N_C_opt'] = N_C_opt
    parameters['N_E_opt_ind'] = N_E_opt_ind
    parameters['N_C_opt_ind'] = N_C_opt_ind

    return parameters
