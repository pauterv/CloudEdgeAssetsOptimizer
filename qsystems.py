#
#   Main functions of queueing_systems package
#
#   Author: Paulius Tervydis
#   Date: 2023-07-09
#
# ==============================================================
import numpy as np 
# ==============================================================
# ssqs function 
# ==============================================================
def ssqs(**parameters):
    """This function calculates the parameters of various single-server queueing systems.

    A queueing system is considered stable when the arrival rate is lower than the service rate. 
    If the parameters are incorrect or missing, exceptions will be raised to alert the user. 
    Additionally, certain input parameters are optional and can be automatically calculated based 
    on the selected system type.
   
    Parameters
    ----------
    **parameters : (keyword arguments)
    qs : str
        Type of queueing system according Kendall's notations:
        "MM1", "MD1", "MG1", "DM1","DG1","DD1","GM1","GD1". Defaults "MM1".
        Examples of accepted formats: "mm1", "MM1", "m/m/1", "M/M/1" 
    ar : float
        Arrival rate. Optional if mean inter-arrival time is given.   
    sr : float
        Service rate. Optional if mean service time is given.
    a : float
        Mean inter-arrival time. Optional if arrival rate is given.
    s : float
        Mean service time. Optional if service rate is given.
    va : float
        Variance of inter-arrival time. Must be provided only for "GM1","GD1","GG1" type systems.
    vs : float
        Variance of service time. Must be provided only for "MG1","DG1","GG1" type systems.

    Returns
    -------
    result : dictionary with such keys
    'qs' - queueing system notation
    'ar' - arrival rate
    'sr' - service rate
    'a'  - mean inter-arrival time
    'va' - variance of inter-arrival time 
    's'  - mean service time 
    'vs' - variance of service time 
    'u'  - the utilization of the system 
    'l'  - mean number of entities in the system
    'lq' - mean number of entities in the queue    
    'w'  - the mean waiting (total time) in system
    'wq' - the mean waiting time in queue

    Example
    -------
    >>> result = ssqs(qs='md1',ar=10,s=0.05)
    >>> print(result)
    >>> {'qs': 'md1', 'ar': 10.0, 'sr': 20.0, 'a': 0.1, 'va': 0.01, 
        's': 0.05, 'vs': 0, 'u': 0.5, 'l': 0.75, 'lq': 0.25, 'wq': 0.025, 'w': 0.075} 
    """

    # -------------------------------------------------------------------
    qs = None
    a = None
    s = None
    va = None
    vs = None
    ar = None

    if "qs" in parameters:
        qs = parameters.get("qs")

    if qs is None:
        qs = "mm1"    

    qs_f = qs.replace("/", "")
    qs_f = qs_f.upper()

    # Arrival parameters -----------------------------------------------
    # arrival rate
    if "ar" in parameters:
        ar = parameters.get("ar")
    # mean inter-arrival time
    if "a" in parameters:
        a = parameters.get("a")
    # variance of inter-arrival times
    if "va" in parameters:
        va = parameters.get("va")

    # Service parameters ---------------------------------------------
    # service rate
    if "sr" in parameters:
        sr = parameters.get("sr")
    # mean service time
    if "s" in parameters:
        s = parameters.get("s")
        if s is not None:
            sr = 1/s
    # variance of service times
    if "vs" in parameters:
        vs = parameters.get("vs")

    # Verification ---------------------------------------------------
    if ar == 0:
        a = float('inf')
    else:
        a = 1 / ar
    if sr == 0:
        s = float('inf')
    else:
        s = 1 / sr    
    if qs_f[0] == "G" and va is None:
        raise Exception("Missing parameters. 'va' value is not provided")
    if qs_f[1] == "G" and vs is None:
        raise Exception("Missing parameters. 'vs' value is not provided")
    if qs_f[0] == "M":
        va = a ** 2
    if qs_f[1] == "M":
        vs = s ** 2
    if qs_f[0] == "D":
        va = 0
    if qs_f[1] == "D":
        vs = 0
    if qs_f[2] != "1":
        raise Exception("Incompatible system notation")    
    if a is None and ar is not None:
        a = 1 / ar
    if a is None and ar is None:
        raise Exception("Missing parameters. 'ar' or 'a' values are not provided")
    if s is None and sr is not None:
        s = 1 / sr
    if s is None and sr is None:
        raise Exception("Missing parameters. 'sr' or 's' values are not provided")

    if s < 0 or a < 0:
        raise Exception("Negative parameters. Ensure that 'a' and 's' > 0")
    if qs_f[0] == "G" or qs_f[1] == "G":
        if vs < 0 or va < 0:
            raise Exception("Negative parameters. Ensure that 'va' and 'vs' > 0")
    if s >= a:
        raise Exception("Unstable system. Ensure that: 's' < 'a' or 'ar' < 'sr'")

    # Parameter calculation -----------------------------------------
    # The arrival rate
    ar = 1 / a
    # The service rate
    sr = 1 / s
    # The utilization of the system
    u = ar / sr
    # The mean waiting time in queue:
    if qs_f == "MM1":
        wq = (u * s)/(1 - u)
    elif qs_f == "MD1":
        wq = (u * s)/(2*(1 - u))
    else:
        # The actual mean waiting time in queue is obtained by Marchall’s approximation
        wq = (u * s) / (2 * (1 - u)) * ((va + vs) /
                                        (s ** 2)) * ((s ** 2 + vs) / (a ** 2 + vs))
    # The mean total time in system
    w = wq + s
    # The mean number of entities in the system
    l = ar * w
    # The mean number of entities in the queue
    lq = ar * wq
    result = {"qs": qs, 
              "ar": round(ar,14), 
              "sr": round(sr,14),
              "a" : round(a,14), 
              "va": round(va,14), 
              "s" : round(s,14), 
              "vs": round(vs,14),
              "u" : round(u,14),
              "l" : round(l,14),
              "lq": round(lq,14),
              "wq": round(wq,14),
              "w" : round(w,14)}
    return result
# ==============================================================


# ==============================================================
# msqs function 
# ==============================================================
def msqs(ar, sn, qs=None, sr1=None, s1=None, vs=None):
    """This function calculates parameters of multi-server queueing systems. 

    A multi-server queueing system is considered, where the arrival rate is evenly 
    distributed among the servers upon arrival to the system. The function returns 
    the parameters specific to a single server within the multi-server system. 
    It assumes that all servers in the system are identical.

    Parameters
    ----------
    ar : float
        Arrival rate.
    sn : int
        Number of servers
    sr1 : float, optional
        Single server service rate. Optional if s1 is given.
    qs : str, optional
        Type of queueing system according Kendall's notations. By default "MM1" or None
        With this function only such systems can be analyzed: 
        "MM1", "MD1", "MG1","DM1","DD1","DG1". Defaults "MM1".
        Examples of accepted formats: "mm1", "MM1", "m/m/1", "M/M/1" 
    s1 : float, optional    
        Mean service time in single server. Optional if sr1 is given.
    vs : float, optional
        Variance of service time. Must be provided only for "MG1" type system.    

    Returns
    -------
    result : list of dictionaries for each server with such keys:
    'qs' - queueing system notation
    'ar' - arrival rate
    'sr' - service rate
    'a'  - mean inter-arrival time
    'va' - variance of inter-arrival time 
    's'  - mean service time 
    'vs' - variance of service time 
    'u'  - the utilization of the system 
    'l'  - mean number of entities in the system
    'lq' - mean number of entities in the queue    
    'w'  - the mean waiting (total time) in system
    'wq' - the mean waiting time in queue
    
    Example
    -------
    >>> result = msqs(ar=10, sn=5, sr1=4)
    >>> print(result)
    >>> {'qs': 'mm1', 'w': 0.5, 'wq': 0.25, 'u': 0.5, 'ar': 2.0, 'sr': 4.0, 
        'l': 1.0, 'lq': 0.5, 'a': 0.5, 's': 0.25, 'va': 0.25, 'vs': 0.0625}
    """

    if qs is None:
        qs = "mm1"    

    qs_f = qs.replace("/", "")
    qs_f = qs_f.upper()
    if (sr1 is None) and (s1 is None):
        raise Exception("Missing parameters: sr1 or s1 must be given.")
    
    if (sr1 is None) and (s1 is not None):
        sr1 = 1/s1

    if type(sn) != int or sn < 1:
        raise Exception("Wrong parameter: sn must be integer >= 1")

    if ar > sn*sr1:
        raise Exception("Unstable system: ar must be < sn*sr1")
    
    if qs_f[0] == "G" or qs_f[2]!="1":
        raise Exception('Wrong system type: only "MM1", "MD1", "MG1","DM1","DD1","DG1" are valid')

    result = ssqs(qs=qs_f, ar=ar/sn, sr=sr1, s=s1, vs=vs)
    result["ar"] = ar
    result['sn'] = sn
    return result
# ==============================================================


# ==============================================================
# mssqsa function 
# ==============================================================
def msqsa(ar, pl, sl):
    """This function provides advanced estimation for parameters of multi-server queueing systems. 
    
    The arrival rate is distributed based on a provided list of probabilities. 
    Each server in the system can have distinct characteristics.
    
    Parameters
    ----------
    ar : float
        Arrival rate to the multi-server system.
    pl : float, array like
        The input is an array or list that represents the probability distribution of the 
        arrival rate between servers in the system.
    sl : dict
        The input is a list of dictionaries where each dictionary represents the parameters 
        of a server in the queueing system. The main server parameters align with those used 
        in the 'ssqs' function. Additionally, it is possible to assign additional and custom 
        parameters to each server.
        Additional and optional parameters:
        'i' - str
            Info text to describe the server.
        'c' - float
            Server cost.
        'r' - float
            The limit or maximum capacity of expendable resources when a server is being utilized.
   
    Returns
    -------
    result : list of dictionaries for each server with such keys:
    'qs' - queueing system notation
    'w'  - the mean total time in system
    'wq' - the mean waiting time in queue
    'u'  - the utilization of the system
    'ar' - arrival rate to the server
    'sr' - service rate
    'l'  - mean number of entities in the system
    'lq' - mean number of entities in the queue
    'a'  - mean inter-arrival time
    's'  - mean service time
    'va' - variance of inter-arrival time
    'vs' - variance of service time
    'p'  - probability of arrival rate distribution to the server
    'c'  - cost (if provided in 'sl')
    'cu' - cost if it depends on utilization (if 'c' provided in 'sl')
    'r'  - amount of expendable resources of the server ('if 'r' provided in 'sl')
    'rt' - time interval between refills of expendable resources ('if 'r' provided in 'sl')
    'i'  - info (if provided in 'sl')

    Example
    -------
    >>> pl = [0.4,0.6]
    >>> sl = [{'qs':'md1','sr':1},{'qs':'mg1','sr':1,'vs':0.1}]
    >>> result = msqsa(ar=1,pl=pl,sl=sl)
    >>> print(result) 
    >>> [{'qs': 'md1', 'w': 1.5, 'wq': 0.5, 'u': 0.5, 'ar': 0.5, 'sr': 1.0, 'l': 0.75, 
        'lq': 0.25, 'a': 2.0, 's': 1.0, 'va': 4.0, 'vs': 0, 'p': 0.5}, 
        {'qs': 'mg1', 'w': 1.5615, 'wq': 0.5615, 'u': 0.5, 'ar': 0.5, 'sr': 1.0, 
        'l': 0.78075, 'lq': 0.28075, 'a': 2.0, 's': 1.0, 'va': 4.0, 'vs': 0.123, 'p': 0.5}]  
    """
    if len(pl) != len(sl):
        raise Exception("Lengths of 'prob_list' and 'server_list' must be equal.")
    result = []
    for i in range(len(pl)):
        if pl[i]*ar < sl[i]["sr"]:
            params = sl[i]
            params['ar']=pl[i]*ar
            res = ssqs(**params)
                
            res["p"] = pl[i]

            if sl[i].get("c") is not None:
                res["c"] = sl[i]["c"] 
                res["cu"] = sl[i]["c"]*res["u"] 
            if sl[i].get("r") is not None:
                res["r"] = sl[i]["r"] 
                res["rt"] = sl[i]["r"]*res["s"]/res["u"]
            if sl[i].get("i") is not None:
                res["i"] = sl[i]["i"]
            result.append(res)
        else:
            print("System unstable: arrival rate > service rate")
    return result
# ==============================================================

def msqs_ar_cr(sn,sr,w,qs='mm1'):
    # if w < 1/sr:
    #     return -1
    if qs == 'mm1':
        ar_cr = sn*(w*sr-1)/w
        return ar_cr
    if qs == 'md1':
        ar_cr = sn*2*sr*(w*sr-1)/(2*w*sr-1)
        return ar_cr

def msqs_ar_cr2(sn,sr,w,qs='mm1'):
    if qs == 'mm1':
        ar_cr = (sn+1)*(w*sr-1)/w
        return ar_cr
    if qs == 'md1':
        ar_cr = (sn+1)*2*sr*(w*sr-1)/(2*w*sr-1)
        return ar_cr

def msqs_sn_cr(ar,sr,w,qs='mm1'):
    # if w < 1/sr:
    #     return -1
    if qs == 'mm1':
        sn_cr = np.ceil(ar*w/(sr*w-1))
        return sn_cr
    if qs == 'md1':
        sn_cr = np.ceil(ar*(2*w*sr-1)/(2*sr*(w*sr-1)))
        return sn_cr
