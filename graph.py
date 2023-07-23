import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import numpy as np

def plotgraph(parameters):
    # Parameters
    Lambda = parameters['lambda']
    P_E = parameters['P_E']
    P_C = 1 - P_E
    NN_E = parameters['NN_E']
    NN_C = parameters['NN_C']
    PP_S = parameters['PP_S']
    RR_S = parameters['RR_S']
    CC_S = parameters['CC_S']
    W_cr = parameters['W_cr']
    C_C_pricing = parameters['C_C_pricing']
    T_bat_cr = parameters['T_bat_cr']
  
    PP_S_max = parameters['PP_S_max']
    N_E_opt = parameters['N_E_opt']
    N_C_opt = parameters['N_C_opt']
    Lambda_E = Lambda * P_E
    Lambda_C = Lambda * P_C
    N_E_opt_ind = parameters['N_E_opt_ind']
    N_C_opt_ind = parameters['N_C_opt_ind']
   
    # Plot
    if P_E != 0 and P_C != 0:
        fig = plt.figure(figsize=(10, 5))

        fig.subplots_adjust(wspace=0.4)
        ax = fig.add_subplot(121, projection='3d')
        ax.plot_surface(NN_E, NN_C, PP_S,cmap='viridis')
        ax.view_init(elev=20, azim=-145)
        ax.set_xlabel('$N_E$')
        ax.set_ylabel('$N_C$')
        ax.set_zlabel('Profit, Eur/h.')
        plt.title('Max Profit = %.2f Eur/h.'% PP_S_max)
        
        ax2 = fig.add_subplot(122)
        contour_plot=plt.contourf(NN_E, NN_C, PP_S,cmap='viridis',levels=50)
        plt.axvline(N_E_opt,color='black',linestyle=':',linewidth=2)
        plt.axhline(N_C_opt,color='black',linestyle=':',linewidth=2)
        plt.grid()
        plt.suptitle("$\lambda = %.2f$ req./h, $P_E = %.2f, N_{Eopt}$ = %d, $N_{Copt}$ = %d, Capacity pricing = % s"% (Lambda,P_E,N_E_opt,N_C_opt,C_C_pricing));
        colorbar = plt.colorbar(contour_plot)
        plt.xlabel('$N_E$')
        plt.ylabel('$N_C$')
        # plt.savefig('Rez_P.png', format="png", bbox_inches="tight") 
        plt.draw()

# ---------------------------------------
    if P_C != 0:
        plt.figure()
        plt.plot(NN_C[:,0],CC_S[:,np.max(N_E_opt_ind)],label="Cost")
        plt.plot(NN_C[:,0],RR_S[:,np.max(N_E_opt_ind)],label="Revenue")
        plt.plot(NN_C[:,0],PP_S[:,np.max(N_E_opt_ind)],label="Profit")
        plt.axvline(N_C_opt,color='black',linestyle=':',linewidth=2)
        plt.text(N_C_opt,np.max(PP_S),"$N_{Copt}$ = %d "%(N_C_opt));
        plt.xlabel("$N_C$")
        plt.ylabel("Profit, Eur/h")
        plt.grid()
        plt.legend()
        plt.title("$\lambda_C$ = %d req./h, $W_{cr}$ = %d s, Capacity pricing = % s"%(Lambda_C,W_cr*3600,C_C_pricing))
        plt.draw()
# -----------
    if P_E != 0:
        plt.figure()
        plt.plot(NN_E[0],CC_S[N_C_opt_ind][0],label="Cost")
        plt.plot(NN_E[0],RR_S[N_C_opt_ind][0],label="Revenue")
        plt.plot(NN_E[0],PP_S[N_C_opt_ind][0],label="Profit")
        plt.axvline(N_E_opt,color='black',linestyle=':',linewidth=2)
        plt.text(N_E_opt,np.max(PP_S),"$N_{Eopt}$ = %d"%(N_E_opt));
        plt.xlabel("$N_E$")
        plt.ylabel("Profit, Eur/h")
        plt.grid()
        plt.legend()
        plt.title("$\lambda_E$ = %d req./h, $W_{cr}$ = %d s, $T_{bat \: cr} = %d$ h"%(Lambda_E,W_cr*3600,T_bat_cr))
        plt.draw()

    plt.show()
    