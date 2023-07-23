import tkinter as tk
from tkinter import ttk

from PIL import Image, ImageTk
import numpy as np
import os
from calculation import *
from graph import *
from optimizer import *
import pandas as pd
# from calculation

info_text = """
CloudEdgeAssetsOptimizer can find the optimal numbers of Edge devices N_E and Cloud servers N_C required for data processing. This estimation is based on factors such as arrival rate lambda of data processing requests, load balancing or distribution between Edge an Cloud (estimated by P_E and P_C=1-P_E) probabilities), processing capabilities (mean time of data processing in Edge devices T_E and Cloud servers T_C), and user demand for the waiting time W_E and W_C. By analyzing these parameters, the software can determine the optimum number of devices needed to handle the workload efficiently, without causing excessive waiting times or delays. 

On the other hand, CloudEdgeAssetsOptimizer can estimate the critical arrival rate lambda_cr of requests or tasks within the network. By considering factors such as data processing performance requirements (W_E, W_C)  and data processing network capacity N_E, N_C, T_E, T_C and utilization of processing devices rho_E, rho_C, the software can estimate what is the critical threshold of request arrival rate lambda_cr. This information allows network administrators to ensure that the mean waiting time for data processing remains below a critical threshold, thus optimizing user experience and satisfaction.

Another important capability of CloudEdgeAssetsOptimizer is its ability to assess the performance of battery-powered Edge devices. By considering the power consumption characteristics of these devices, the software can estimate utilization of such device rho_E and if it will operate for a specific duration without requiring a battery recharge. This estimation is crucial for planning the deployment of Edge devices and ensuring uninterrupted operation within the network.

Furthermore, CloudEdgeAssetsOptimizer takes into account economical criteria when determining the optimal number of assets within the network. It considers factors such as the cost of devices C_E, C_C, retinue and profit of service provider. By analyzing these factors, the software can recommend the optimal number of assets that not only meet the technical requirements but also provide the most cost-effective solution. The CloudEdgeAssetsOptimizer goes beyond traditional analysis by considering different pricing strategies. Users can evaluate the cost of the system under fixed pricing (reserved resources) or pricing that depends on utilization rho_C. This capability provides valuable insights for making informed decisions about pricing strategies and resource allocation.
"""

def get_parameters():
    parameters = {}
    parameters['lambda'] = float(arrival_rate_value.get())
    parameters['r_p'] = float(r_p_value.get())
    parameters['P_E'] = float(P_E_value.get())
    parameters['N_E'] = int(N_E_value.get())
    parameters['T_E'] = float(T_E_value.get())/3600
    parameters['T_E_distr'] = str(T_E_distr_value.get())
    parameters['B_p'] = float(B_p_value.get())
    parameters['C_E'] = float(C_E_value.get())
    parameters['N_C'] = int(N_C_value.get())
    parameters['T_C'] = float(T_C_value.get())/3600
    parameters['T_C_distr'] = str(T_C_distr_value.get())
    parameters['C_C'] = float(C_C_value.get())
    parameters['C_C_pricing'] = str(C_C_pricing_value.get())
    parameters['W_cr'] = float(W_cr_value.get())/3600
    parameters['T_bat_cr'] = float(T_bat_cr_value.get())
    return parameters

def calculate_button_click():
    input_parameters = get_parameters()
    calculated_params = calc_system_performance(input_parameters)
    try:  # if no error
        df = pd.DataFrame(calculated_params)
        df_str = df.to_string(index=True)
        results_text.configure(state="normal")
        results_text.delete("1.0", tk.END)
        results_text.insert(tk.END,
                "System performance evaluation for the given parameters:\n"
                + df_str)
        results_text.configure(state="disabled")
    except:
        results_text.configure(state="normal")
        results_text.delete("1.0", tk.END)
        results_text.insert(tk.END, calculated_params)
        results_text.configure(state="disabled")

def optimize_button_click():

    input_parameters = get_parameters()
    optimized_parameters = find_optimal_configuration(input_parameters)
    optimized_parameters.pop('NN_E')
    optimized_parameters.pop('NN_C')
    optimized_parameters.pop('PP_S')
    optimized_parameters.pop('RR_S')
    optimized_parameters.pop('CC_S')
    optimized_parameters.pop('N_E_opt_ind')
    optimized_parameters.pop('N_C_opt_ind')
    optimized_parameters['N_E'] = int(optimized_parameters['N_E_opt'])
    optimized_parameters['N_C'] = int(optimized_parameters['N_C_opt'])
    optimized_parameters = calc_system_performance(optimized_parameters)
    df = pd.DataFrame(optimized_parameters)
    df_str = df.to_string(index=True)

    results_text.configure(state="normal")
    results_text.delete("1.0", tk.END)
    results_text.insert(
        tk.END, "System performance for estimated optimal number of processing units (N_E and N_C):\n"+df_str)
    results_text.configure(state="disabled")


def graph_button_click():
    input_parameters = get_parameters()
    graph_parameters = find_optimal_configuration(input_parameters)
    plotgraph(graph_parameters)


# Create the main application window
root = tk.Tk()
root.title("CloudEdgeAssetOptimizer")

params_frame = ttk.Frame(root, padding="10", borderwidth=1)
params_frame.pack(side="left", fill="both", expand=True)

edge_params_frame = ttk.LabelFrame(params_frame, text="Edge parameters:")
cloud_params_frame = ttk.LabelFrame(params_frame, text="Cloud parameters:")

edge_params_frame.pack(side="top", fill="x")
cloud_params_frame.pack(side="top", fill="x")

arrival_params_frame = ttk.LabelFrame(
    params_frame, text="Data processing requests:")
arrival_params_frame.pack(side="top", pady=2, fill="x")
arrival_rate_var = tk.StringVar(value="1000")
ttk.Label(arrival_params_frame,
          text=u"Arrival rate (\u03bb) [req./h]", width=28
          ).grid(column=0, row=1, sticky="w", padx=5)
arrival_rate_value = ttk.Spinbox(arrival_params_frame,
                                 textvariable=arrival_rate_var, format="%.8f",
                                 from_=0.0, to=10000.0, increment=0.1, width=10)
arrival_rate_value.grid(column=1, row=1, padx=5, pady=2)

r_p_var = tk.StringVar(value="0.05")
ttk.Label(arrival_params_frame,
          text=u"Retinue per processed req. (r_p) [Eur]", width=28
          ).grid(column=0, row=2, sticky="w", padx=5)
r_p_value = ttk.Spinbox(arrival_params_frame,
                        textvariable=r_p_var, format="%.8f",
                        from_=0.0, to=10000.0, increment=0.1, width=10)
r_p_value.grid(column=1, row=2, padx=5, pady=2)

balancing_params_frame = ttk.LabelFrame(params_frame, text="Load balancing:")
balancing_params_frame.pack(side="top", pady=2, fill="x")
P_E_value_var = tk.StringVar(value="0.3")
ttk.Label(balancing_params_frame,
          text=u"Distribution probability (P_E)", width=28
          ).grid(column=0, row=1, sticky="w", padx=5)
P_E_value = ttk.Spinbox(balancing_params_frame,
                        textvariable=P_E_value_var, format="%.8f",
                        from_=0.0, to=1.0, increment=0.1, width=10)
P_E_value.grid(column=1, row=1, padx=5, pady=2)

edge_params_frame = ttk.LabelFrame(params_frame, text="Edge parameters:")
edge_params_frame.pack(side="top", pady=2, fill="x")
N_E_value_var = tk.StringVar(value="20")
ttk.Label(edge_params_frame,
          text=u"Number of Edge devices (N_E)", width=28
          ).grid(column=0, row=1, sticky="w", padx=5)
N_E_value = ttk.Spinbox(edge_params_frame,
                        textvariable=N_E_value_var,
                        from_=0, to=10000, increment=1, width=10)
N_E_value.grid(column=1, row=1, padx=5, pady=2)

T_E_var = tk.StringVar(value="200.0")
ttk.Label(edge_params_frame,
          text=u"Processing time in Edge device (T_E) [s]", width=28
          ).grid(column=0, row=2, sticky="w", padx=5)
T_E_value = ttk.Spinbox(edge_params_frame,
                        textvariable=T_E_var,
                        from_=0, to=10000, increment=1, width=10)
T_E_value .grid(column=1, row=2, padx=5, pady=2)

ttk.Label(edge_params_frame,
          text=u"T_E distribution", width=20
          ).grid(column=0, row=3, sticky="w", padx=5)
T_E_distr_value = tk.StringVar()
T_E_distr_combo = ttk.Combobox(edge_params_frame,
                               state="readonly", width=10,
                               values=["Determined", "Exponential"],
                               textvariable=T_E_distr_value
                               ).grid(column=1, row=3)
T_E_distr_value.set("Determined")

B_p_var = tk.StringVar(value="400")  # Battery-Related Performance Index
ttk.Label(edge_params_frame,
          text=u"Battery performance index (B_p)", width=28
          ).grid(column=0, row=4, sticky="w", padx=5)
B_p_value = ttk.Spinbox(edge_params_frame,
                        textvariable=B_p_var,
                        from_=0, to=10000, increment=1, width=10)
B_p_value.grid(column=1, row=4, padx=5, pady=2)

C_E_var = tk.StringVar(value="0.1")  # Battery-Related Performance Index
ttk.Label(edge_params_frame,
          text=u"Cost of Edge device (C_E) [Eur/h]", width=28
          ).grid(column=0, row=5, sticky="w", padx=5)
C_E_value = ttk.Spinbox(edge_params_frame,
                        textvariable=C_E_var,
                        from_=0, to=10000, increment=1, width=10)
C_E_value .grid(column=1, row=5, padx=5, pady=2)

cloud_params_frame = ttk.LabelFrame(params_frame, text="Cloud parameters:")
cloud_params_frame.pack(side="top", pady=2, fill="x")
N_C_value_var = tk.StringVar(value="20")
ttk.Label(cloud_params_frame,
          text=u"Number of Cloud VM servers (N_C)", width=28
          ).grid(column=0, row=1, sticky="w", padx=5)
N_C_value = ttk.Spinbox(cloud_params_frame,
                        textvariable=N_C_value_var,
                        from_=0, to=10000, increment=1, width=10)
N_C_value.grid(column=1, row=1, padx=5, pady=2)

T_C_var = tk.StringVar(value="100.0")
ttk.Label(cloud_params_frame,
          text=u"Proc. time in Cloud VM server (T_C) [s]", width=28
          ).grid(column=0, row=2, sticky="w", padx=5)
T_C_value = ttk.Spinbox(cloud_params_frame,
                        textvariable=T_C_var,
                        from_=0, to=10000, increment=1, width=10)
T_C_value .grid(column=1, row=2, padx=5, pady=2)

ttk.Label(cloud_params_frame,
          text=u"T_C distribution", width=20
          ).grid(column=0, row=3, sticky="w", padx=5)
T_C_distr_value = tk.StringVar()
T_C_distr_combo = ttk.Combobox(cloud_params_frame,
                               state="readonly", width=10,
                               values=["Determined", "Exponential"],
                               textvariable=T_C_distr_value
                               ).grid(column=1, row=3)
T_C_distr_value.set("Determined")

C_C_var = tk.StringVar(value="0.10")  # Battery-Related Performance Index
ttk.Label(cloud_params_frame,
          text=u"Cost of Cloud VM server (C_C) [Eur/h]", width=28
          ).grid(column=0, row=4, sticky="w", padx=5)
C_C_value = ttk.Spinbox(cloud_params_frame,
                        textvariable=C_C_var,
                        from_=0, to=10000, increment=1, width=10)
C_C_value .grid(column=1, row=4, padx=5, pady=2)

ttk.Label(cloud_params_frame,
          text=u"Capacity pricing", width=20
          ).grid(column=0, row=5, sticky="w", padx=5)
C_C_pricing_value = tk.StringVar()
C_C_pricing_combo = ttk.Combobox(cloud_params_frame,
                                 state="readonly", width=10,
                                 values=["Dedicated", "On-demand"],
                                 textvariable=C_C_pricing_value
                                 ).grid(column=1, row=5)
C_C_pricing_value.set("Dedicated")

performance_params_frame = ttk.LabelFrame(
    params_frame, text="Critical parameters:")
performance_params_frame.pack(side="top", pady=2, fill="x")
W_cr_value_var = tk.StringVar(value="240.0")
ttk.Label(performance_params_frame,
          text=u"Critical Waiting time (W_cr) [s]", width=28
          ).grid(column=0, row=1, sticky="w", padx=5)
W_cr_value = ttk.Spinbox(performance_params_frame,
                         textvariable=W_cr_value_var,
                         from_=0, to=10000, increment=1, width=10)
W_cr_value.grid(column=1, row=1, padx=5, pady=2)

T_bat_cr_value_var = tk.StringVar(value="8")
ttk.Label(performance_params_frame,
          text=u"Working time on Battery (T_bat_cr) [h]", width=28
          ).grid(column=0, row=2, sticky="w", padx=5)
T_bat_cr_value = ttk.Spinbox(performance_params_frame,
                             textvariable=T_bat_cr_value_var,
                             from_=0, to=10000, increment=1, width=10)
T_bat_cr_value.grid(column=1, row=2, padx=5, pady=2)

buttons_frame = ttk.Frame(params_frame, padding="10")
calculate_button = ttk.Button(
    buttons_frame, text="Calculate", command=calculate_button_click)
calculate_button.pack(side="left", pady=20, fill="x")

optimize_button = ttk.Button(
    buttons_frame, text="Optimize", command=optimize_button_click)
optimize_button.pack(side="left", pady=20, fill="x")

graph_button = ttk.Button(buttons_frame, text="Graph",
                          command=graph_button_click)
graph_button.pack(side="right", pady=20, fill="x")
buttons_frame.pack(side="top")
params_frame.pack(side="left", fill="both", expand=True)

# -------------------------------------------------

results_frame = ttk.Frame(root)
results_frame.pack(side="right", fill="both", expand=True)

results_tab_control = ttk.Notebook(results_frame)
# Results tab
results_tab = ttk.Frame(results_tab_control)
results_tab_control.add(results_tab, text="Results")

results_text = tk.Text(results_tab, state="disabled",
                       wrap="word", width=60, height=15)
results_text.pack(side="bottom", fill="both", expand=True)


info_tab = ttk.Frame(results_tab_control)
results_tab_control.add(info_tab, text="Info")

# Load and display the image
picture_folder = os.path.join(os.path.dirname(__file__), 'pics')
# Get the path to the picture file using the relative path
picture_path = os.path.join(picture_folder, 'Fig_Cloud_Edge.png')

image = Image.open(picture_path)
photo = ImageTk.PhotoImage(image)
image_label = ttk.Label(results_frame, image=photo, pad=20)
image_label.pack(side="top")

info_text_box = tk.Text(info_tab, state="disabled",
                        wrap="word", width=60, height=15)
info_text_box.pack(side="bottom", fill="both", expand=True)
info_text_box.configure(state="normal")
info_text_box.insert(tk.END, info_text)
info_text_box.configure(state="disabled")

results_tab_control.pack(fill=tk.BOTH, expand=True)

root.mainloop()

