#
#   Example 1: Evaluation of single server queueing system parameters   
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

# --------------------------------------------------------------
# System initial parameters:
# --------------------------------------------------------------
system_notation = "M/D/1" 
# Arrival parameters
arrival_rate = 80 # [entities/t.u.], for example [users/hour]
# Server parameters
service_rate = 100 # [entities/t.u.]
# Note: For stable system arrival_rate must be < service_rate
# --------------------------------------------------------------

# --------------------------------------------------------------
sys_params = ssqs(qs=system_notation, ar=arrival_rate, sr=service_rate)

print("System %s parameters:"%sys_params['qs'])
print(" - Arrival rate:",round(sys_params['ar'],10))
print(" - Service rate:",sys_params['sr'])
print(" - Mean inter-arrival time:",sys_params['a'])
print(" - Variance of inter-arrival time:",round(sys_params['va'],10))
print(" - Mean service time:",sys_params['s'])
print(" - Variance of service time:",sys_params['vs'])
print(" - Server utilization (load):",sys_params['u'])
print(" - Mean number of entities in queue:",sys_params['lq'])
print(" - Mean number of entities in system:",sys_params['l'])
print(" - Mean waiting time in queue:",sys_params['wq'])
print(" - Mean waiting time (total time) in system:",sys_params['w'])

