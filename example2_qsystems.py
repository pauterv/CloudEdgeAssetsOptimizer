#
#   Example 2: Single server queueing system parameters vs arrival rate
#
#   Author: Paulius Tervydis
#   Date: 2023-07-09
# 
# ==============================================================
#             Single Server Queueing System (ssqs)
#               +-----------------------------+
#    Arrival    |                  Server     |    Output 
#               |    Queue    +--------------+|     
#  arrival_rate | ----------+ |              ||      
#  ------------>|   | | | | | | service_rate || ------------>
#               | ----------+ |              ||
#               |             +--------------+|   
#               +-----------------------------+
#
# System notation (A/B/1):
# A - distribution of inter-arrival time 
# B - distribution of service time is determined
# 1 - single server
# 
# Distribution types: 
# M - exponential, 
# D - determined (fixed), 
# G - general (time variance must be provided))
# ==============================================================

from qsystems import ssqs
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# --------------------------------------------------------------
# System initial parameters:
# --------------------------------------------------------------
# List of queueing systems to be evaluated
system_notation = ["M/M/1","M/D/1","D/M/1","D/D/1"] 
# Arrival parameters:
arrival_rate_start = 0 # [entities/t.u.], for example [users/hour]
arrival_rate_stop = 80
arrival_rate_step = 0.5
# Server parameters
service_rate = 100 # [entities/t.u.]
# Note: For stable system arrival_rate must be < service_rate
# --------------------------------------------------------------

# --------------------------------------------------------------
# Example how to estimate dependence of system parameters on arrival time.
# 
arrival_rate_array = np.arange(arrival_rate_start,
                               arrival_rate_stop+arrival_rate_step,
                               arrival_rate_step)

# Results are stored in pandas dataframe 
param_df = pd.DataFrame()
for q_system in system_notation:
    for arrival_rate in arrival_rate_array:
        sys_params = ssqs(qs=q_system, ar=arrival_rate, sr=service_rate)
        df = pd.DataFrame(sys_params,index=[0])
        param_df  = pd.concat([param_df ,df], axis=0)
param_df.reset_index(drop=True, inplace=True)

print(param_df)

# --------------------------------------------------------------
# Plot parameters
#
def plot_system_param_versus(q_system,param_df,param,versus):
    param_text =  {'w' :"Mean waiting time",
                   'wq':"Mean waiting time in queue",
                   'l' :"Mean number of entities in system",
                   'lq':"Mean number of entities in queue",
                   'ar':"Arrival rate",
                   'u' :"System utilization"}
    fig_title = param_text[param]+" vs "+param_text[versus]
    plt.figure(fig_title)
    plot_data_x = param_df[(param_df["qs"]==q_system)][versus]
    plot_data_y = param_df[(param_df["qs"]==q_system)][param]
    plt.plot(plot_data_x,plot_data_y,label=q_system)
    plt.xlabel(param_text[versus])
    plt.ylabel(param_text[param])
    plt.legend()
    plt.grid(True)
    plt.draw()

for q_system in system_notation:
    plot_system_param_versus(q_system,param_df,'w','ar')
    plot_system_param_versus(q_system,param_df,'wq','ar')
    plot_system_param_versus(q_system,param_df,'lq','ar')
    plot_system_param_versus(q_system,param_df,'l','ar')
    plot_system_param_versus(q_system,param_df,'w','u')
    plot_system_param_versus(q_system,param_df,'wq','u')
    plot_system_param_versus(q_system,param_df,'lq','u')
    plot_system_param_versus(q_system,param_df,'l','u')
plt.show()   