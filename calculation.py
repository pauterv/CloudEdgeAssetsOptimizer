from qsystems import *
import numpy as np

def calc_system_performance(parameters):
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

    # print(parameters) 

    if T_E_distr ==  'Determined':
        qs_E = 'md1'
    if T_E_distr ==  'Exponential':
        qs_E = 'mm1'
    if T_C_distr ==  'Determined':
        qs_C = 'md1'
    if T_C_distr ==  'Exponential':
        qs_C = 'mm1'

    P_C = 1 - P_E
    Lambda_E = Lambda*P_E
    Lambda_C = Lambda*P_C

    if Lambda*P_E > 0 and N_E <= 0 or Lambda == 0:
        return "Wrong Lambda, P_E or N_E parameters!\n\n"\
                f"Possible solutions:\n"\
                "   N_E must be > 0 if Lambda*P_E > 0\n"
    else:
        lambda_E = Lambda*P_E/N_E
    if Lambda*P_C > 0 and N_C <= 0:
        return "Wrong Lambda, P_E or N_C parameters!\n\n"\
                f"Possible solutions:\n"\
                "   N_C must be > 0 if Lambda*(1-P_E) > 0\n"
    else:
        lambda_C = Lambda*P_C/N_C
    
    if T_E <= 0 and lambda_E > 0:
        return "Wrong T_E parameter!\n\n"\
                f"Possible solutions:\n"\
                "   T_E must be > 0 if Lambda*P_E > 0\n"
    else:
        mu_E = 1/T_E

    if T_C <= 0 and lambda_C > 0:
        return "Wrong T_C parameter!\n\n"\
                f"Possible solutions:\n"\
                "   T_C must be > 0 if Lambda*(1-P_C) > 0\n"
    else:
        mu_C = 1/T_C
  
    if mu_E < lambda_E:
        T_E_cr = T_E/(lambda_E/mu_E)
        N_E_cr = msqs_sn_cr(ar=Lambda*P_E,sr=mu_E,w=W_cr,qs=qs_E)
        return "Edge part of the data processing system is unstable!\n\n"\
                f"Possible solutions:\n"\
                "   for given Lambda, P_E and W_cr values\n"\
                f"  1) T_E < {T_E_cr*3600} s\n"\
                "   or\n"\
                f"  2) N_E >= {N_E_cr}\n"
    
    rho_E = lambda_E/mu_E

    if rho_E > 0:
        T_E_bat = B_p*T_E/rho_E
        # print("T_E_bat",T_E_bat)
        if T_E_bat < T_bat_cr:
            # N_E_bat_cr = ceil(T_bat_cr*lambda_E*B_p/(T_bat_cr*mu_E))
            # P_E_cr = (N_E*T_bat_cr*mu_E/(Lambda*B_p*T_E))
            N_E_bat_cr = np.ceil((lambda_E*T_bat_cr)/B_p) 
            return f"Warning: Working time of battery powered devices T_E_bat = {T_E_bat} h < T_bat_cr!\n\n"\
                    f"Possible solutions to ensure T_E_bat > T_bat_cr:\n"\
                    "   for given Lambda, P_E, T_bat_cr:\n"\
                    "   1) increase number of Edge devices N_E:\n"\
                    f"      minimum N_E = {N_E_bat_cr}\n"\
                    "   2) increase B_p of Edge devices\n"\
                    # f"      maximum P_E = {P_E_cr}"
                    
    if mu_C < lambda_C:
        T_C_cr = T_C/(lambda_C/mu_C)
        N_C_cr = msqs_sn_cr(ar=Lambda*P_C,sr=mu_C,w=W_cr,qs=qs_C)
        return "Cloud part of the data processing system is unstable!\n\n"\
                f"Possible solutions for given Lambda, P_E and Wcr values:\n"\
                f"  1) decrease processing time T_C < {T_C_cr*3600} s\n"\
                    "   or\n"\
                f"  2) increase number of Cloud servers N_C >= {N_C_cr}\n"
                
    rho_C = lambda_C/mu_C
    
    E_params = msqs(ar = Lambda*P_E, sn = N_E, s1 = T_E, qs=qs_E)    
    C_params = msqs(ar = Lambda*P_C, sn = N_C, s1 = T_C, qs=qs_C)    
        
    lambda_Ecr = msqs_ar_cr(sn=N_E-1,sr=mu_E,w=W_cr,qs=qs_E)
    lambda_Ccr = msqs_ar_cr(sn=N_C-1,sr=mu_C,w=W_cr,qs=qs_C)
    

    if Lambda_E > 0:
        P_Ea=np.where(Lambda_E > lambda_Ecr,1-((Lambda_E-lambda_Ecr)/Lambda_E),1)
    else:
        P_Ea = 0
    if Lambda_C > 0:    
        P_Ca=np.where(Lambda_C > lambda_Ccr,1-((Lambda_C-lambda_Ccr)/Lambda_C),1)
    else:
        P_Ca = 0

    if C_C_pricing == "Dedicated":
        C_S = N_E*C_E + N_C*C_C
        C_S_C = N_C*C_C
    if C_C_pricing == "On-demand":
        C_S = N_E*C_E + N_C*C_C*rho_C
        C_S_C = N_C*C_C*rho_C
    
    C_S_E = N_E*C_E
    
    R_S = (Lambda_E*P_Ea + lambda_C*P_Ca)*r_p
    P_S = R_S - C_S
 
    R_S_E = Lambda_E*P_Ea*r_p
    R_S_C = Lambda_C*P_Ca*r_p

    P_S_E = R_S_E - C_S_E
    P_S_C = R_S_C - C_S_C

    E_system_params = {}
    E_system_params['Arrival rate [req./h]'] = E_params['ar']
    E_system_params['Service rate [req./h]'] = E_params['sr']
    E_system_params['Mean inter-arrival time [s]'] = E_params['a']*3600
    E_system_params['St.dev of inter-arrival time [s]'] = np.sqrt(E_params['va'])*3600
    E_system_params['Mean service time [s]'] = E_params['s']*3600
    E_system_params['St.dev of service time [s]'] = np.sqrt(E_params['vs'])*3600
    E_system_params['Utilization (or load)'] = (E_params['u'])
    E_system_params['Mean number of requests in system'] = E_params['ar']*E_params['w']
    E_system_params['Mean number of requests in queue'] = E_params['ar']*E_params['wq']
    E_system_params['Mean waiting time in queue [s]'] = E_params['wq']*3600
    E_system_params['Mean waiting time in system [s]'] = E_params['w']*3600

    C_system_params = {}
    C_system_params['Arrival rate [req./h]'] = C_params['ar']
    C_system_params['Service rate [req./h]'] = C_params['sr']
    C_system_params['Mean inter-arrival time [s]'] = C_params['a']*3600
    C_system_params['St.dev of inter-arrival time [s]'] = np.sqrt(C_params['va'])*3600
    C_system_params['Mean service time [s]'] = C_params['s']*3600
    C_system_params['St.dev of service time [s]'] = np.sqrt(C_params['vs'])*3600
    C_system_params['Utilization (or load)'] = (C_params['u'])
    C_system_params['Mean number of requests in system'] = C_params['ar']*C_params['w']
    C_system_params['Mean number of requests in queue'] = C_params['ar']*C_params['wq']
    C_system_params['Mean waiting time in queue [s]'] = C_params['wq']*3600
    C_system_params['Mean waiting time in system [s]'] = C_params['w']*3600

    E_system_params['Number of processing units'] = N_E
    C_system_params['Number of processing units'] = N_C
    E_system_params['Crit. arrival rate (for W<Wcr) [req/h]'] = lambda_Ecr
    C_system_params['Crit. arrival rate (for W<Wcr) [req/h]'] = lambda_Ccr
    try:
        E_system_params['Working time on battery [h]'] = T_E_bat
    except:
        E_system_params['Working time on battery [h]'] = None
    E_system_params['System Cost [Eur/h]'] = C_S_E
    C_system_params['System Cost [Eur/h]'] = C_S_C
    E_system_params['System revenue [Eur/h]'] = R_S_E
    C_system_params['System revenue [Eur/h]'] = R_S_C
    E_system_params['System Profit [Eur/h]'] = P_S_E
    C_system_params['System Profit [Eur/h]'] = P_S_C

    return {"Edge_System_params":E_system_params, "Cloud_System_params":C_system_params}

