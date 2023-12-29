from qsystems import ssqs, msqs

class Node:
    """All the network node classes are inherited from the Node class.

    Parameters
    ----------
    id : str
        Text string to describe a network node. 
    input_rate : float
        Arrival rate.   
    service_rate : float
        Service rate. 
    output_rate : float
        Output rate.
    input : list
        List of nodes that are connected to this node. Data flow is arriving from the nodes to this node's input.
    output : list
        List of nodes that this node is connected to. Data flow from this node's output goes to the inputs of the nodes in the list.
    time_in_system : float
        Sum of time spent in the node's queue and service (processing) time.
    total_time : float
        Cumulative time in the network (from the node that starts data flow to this node inclusive). 
    profit : float
        Cumulative profit of the network link (from the node that starts data flow to this node inclusive). 
    """
     
    def __init__(self,id,rate):
        """Constructor"""
        self.id = id
        self.input_rate = 0
        self.service_rate = None 
        self.output_rate = None
        self.input = []
        self.output = []
        self.time_in_system = 0
        self.utilization = 0
        self.total_time = 0
        self.profit = 0
        
    def connect_to(self, node, ratio=1):
        """Function used to connect this node to another. If this node is connected to several 
        another nodes, then the output flow ratio can be defined."""
        node.set_input(self, ratio)
        self.output.append(node)

    def set_input(self, node, ratio=1):
        """Function sets the input and the data flow ratio to a node."""
        self.input.append(node)
        self.input_rate += node.output_rate*ratio
        parameters = ssqs(qs="md1",ar=self.input_rate,sr=self.service_rate)
        self.time_in_system = parameters['w']
        self.utilization = parameters['u']

        dt = 1/self.input_rate+self.time_in_system
        self.output_rate = 1/dt

    def __str__(self):
        """This function creates a string output with node parameters if print(node) is used"""
        attrs = vars(self)
        vars_str = ""
        for item in attrs:
            if item == "output":
                for o in self.output:
                    vars_str += "%s: %s, " % (item, o.id)
            elif item == "input":
                for i in self.input:
                    vars_str += "%s: %s, " % (item, i.id)
            else:
                vars_str += "%s: %s, " % (item,attrs[item])
        return vars_str
    
    def get_info(self, total_time=0, total_profit=0, links=""):
        """This function is used recursively to form the output prompt with a network link 
        details starting from the node that originates data flow to the terminal node."""
        total_time += self.time_in_system
        total_profit += self.profit
        for i,output in enumerate(self.output):
            if i==0:
                links += self.id+" --> "
            output.get_info(total_time,total_profit,links)
        if len(self.output) == 0:
            if total_profit!=0:
                print(links + self.id+", Total time: %f"%(total_time*3600) + ", Total profit: %f"%total_profit)
            else:
                print(links + self.id+", Total time: %f"%(total_time*3600))
   
class Sensor(Node):
    """Class that defines data flow originating network node"""
    def __init__(self,id,input_rate):
        Node.__init__(self,id,input_rate)
        self.input_rate = input_rate
        self.output_rate = input_rate
        self.service_rate = input_rate
        self.total_time = 0
        self.profit = 0

class DataChannel(Node):
    """Class to define a data network channel."""
    def __init__(self,id,service_rate):
        Node.__init__(self,id,service_rate)
        self.service_rate = service_rate

class Balancer(Node):
    """Class to define load balancer. It is used to define data flow ratios."""
    def __init__(self,id,rate=0):
        Node.__init__(self,id,rate)
        self.service_rate = rate
    def set_input(self, node,ratio=1):
        self.input.append(node)
        self.input_rate += node.output_rate*ratio
        self.time_in_system = 0
        dt = 1/self.input_rate+self.time_in_system
        self.output_rate = 1/dt

class Database(Node):
    """Class to define a database. In the given example it is used as data flow termination node."""
    def __init__(self,id,service_rate):
        Node.__init__(self,id,service_rate)
        self.service_rate = service_rate

class EdgeDevice(Node):
    """Class to define an Edge device. 
    Additional parameters to estimate Edge devices working battery time, cost and retinue are added."""
    def __init__(self,id,service_rate,battery_perf_index=0,cost=0,retinue_index=0):
        Node.__init__(self,id,service_rate)
        self.service_rate = service_rate
        self.battery_perf_index = battery_perf_index 
        self.battery_time = None
        self.cost = cost
        self.retinue = 0
        self.retinue_index = retinue_index
        self.profit = 0
    def set_input(self, node, ratio=1):
        self.input.append(node)
        self.input_rate += node.output_rate*ratio
        parameters = ssqs(qs="md1",ar=self.input_rate,sr=self.service_rate)
        self.time_in_system = parameters['w']
        self.utilization = parameters['u']
        self.battery_time = self.battery_perf_index/(self.utilization*self.service_rate)
        dt = 1/self.input_rate+self.time_in_system
        self.output_rate = 1/dt
        self.retinue = self.input_rate*self.retinue_index
        self.profit = self.retinue - self.cost

class CloudServer(Node):
    """Class to define a Cloud server. 
    Additional parameters to estimate cost and retinue are added."""
    def __init__(self,id,service_rate,cost=0,retinue_index=0):
        Node.__init__(self,id,service_rate)
        self.service_rate = service_rate
        self.cost = cost
        self.retinue = 0
        self.retinue_index = retinue_index
        self.profit = 0
    def set_input(self, node, ratio=1):
        self.input.append(node)
        self.input_rate += node.output_rate*ratio
        parameters = ssqs(qs="md1",ar=self.input_rate,sr=self.service_rate)
        self.time_in_system = parameters['w']
        self.utilization = parameters['u']
        dt = 1/self.input_rate+self.time_in_system
        self.output_rate = 1/dt
        self.retinue = self.input_rate*self.retinue_index
        self.profit = self.retinue - self.cost