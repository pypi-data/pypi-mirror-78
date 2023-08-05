import networkx as nx
from networkx.algorithms.flow.maxflow import maximum_flow
import matplotlib.pyplot as plt


def average(val_1, val_2):
    return ( float(val_1) + float(val_2) ) / 2

class NodalMarket():
    def __init__(self):
        self.G = nx.DiGraph()
        self.transmission = {}
        self.surplus_gen_capacity = {}

    def add_node(self, node_label):
        """
        Adds a trading node (ie location in a locational marginal pricing market).
        """
        self.G.add_node(node_label)
    
    def set_transmission(self, from_node, to_node, capacity, label):
        """
            Adds unidirectional transmission between two nodes, at a certain capacity (MW)
            Label must be unique. 
        """
        key = from_node+'-'+to_node
        self.transmission[key] = {} if key not in self.transmission else self.transmission[key]
        self.transmission[key][label] = {'from_node':from_node, 'to_node': to_node, 'label':label, 'capacity':int(capacity)}
        total = sum([self.transmission[key][label]['capacity'] for label in self.transmission[key] ])
        self.G.add_edge(from_node,to_node,capacity=int(total))
    
    def set_surplus_capacity(self, node, gen_capacity):
        """
            Set surplus generation capacity on a given node. 
        """
        self.surplus_gen_capacity[node] = gen_capacity
    
    def clear_surplus_capacity(self):
        """
            Clears/resets all surplus generation capacity at all nodes. 
        """
        self.surplus_gen_capacity = {}

    def get_transmission(self):
        return self.transmission

    def calculate_max_flow(self, to_node):
        # Add a consolidated source node to all nodes with spare capacities. 
        self.G.add_node('Consolidated Source')
        for node in self.surplus_gen_capacity:
            self.G.add_edge('Consolidated Source', node, capacity=int(self.surplus_gen_capacity[node]))
        
        flow_value, flow_dict = maximum_flow(self.G, 'Consolidated Source', to_node)

        # Cleaning Up - Remove the consolidated source node.
        self.G.remove_node('Consolidated Source')
        return flow_value

    def calculate_nersi(self, region, region_demand, region_available_capacity, generator_capacity):
        """
            Given a market model with transmission constraints and surplus capacities set, 
            calculates the Network-Extended Residual Supply Index for a market participant (with capacity <generator_capacity>) 
            in a given region, with a set demand (in the same units as gen capacity) and available capacity from all generators (including the generator under investigation)
        """
        max_flow = self.calculate_max_flow(region)
        total_available = max_flow + region_available_capacity - generator_capacity
        nersi = max(total_available,0) / region_demand
        return nersi

    def calculate_max_generator_capacity(self, region, region_demand, region_available_capacity):
        """
            Calculates the maximum generator capacity in a region, for all generators in that region to have a NERSI greater than 1. 
        """
        STEP_SIZE = 20
        NERSI_THRESHOLD = 1
        if region_demand <= STEP_SIZE:
            return region_available_capacity
        
        

        low_bound = 0
        high_bound = region_demand * 3
        generator_capacity = average(high_bound, low_bound)

        while(high_bound - low_bound > STEP_SIZE):
            nersi = self.calculate_nersi( region, region_demand,region_available_capacity, generator_capacity)
            # If greater than the NERSI threshold, generator_cap is too small (ie there is sufficient competition.)
            # So set lower bound to the gen_cap
            if nersi > NERSI_THRESHOLD:
                low_bound = generator_capacity
            else:
                high_bound = generator_capacity

            generator_capacity = average(high_bound, low_bound)

        return generator_capacity

    def print(self):
        print("Edges:")
        for e in self.G.edges:
            print(e, self.G.edges[e])
        

    def draw(self):
        
        nx.draw(self.G)
        plt.show()

if __name__ == "__main__":
    # Interconnector capacities below taken as maximums in 'INTERCONNECTOR CAPABILITIES FOR THE NATIONAL ELECTRICITY MARKET' (2017) https://www.aemo.com.au/-/media/Files/Electricity/NEM/Security_and_Reliability/Congestion-Information/2017/Interconnector-Capabilities.pdf
    market = LMPFactory().get_australian_nem()
    
    # I think these need to be netted internally - seems to only support one edge between two nodes. 
    market.set_surplus_capacity('VIC', 100)
    market.set_surplus_capacity('NSW', 50)
    market.set_surplus_capacity('QLD', 600)

    flow = market.calculate_max_flow('SA')
    # print(flow)

    # market.draw()
    market.print()


# Breadth first search. Start with the closest nodes. Calc maximum flow at their max avail. Constrain closest lines as per flow. Repeat. 

# This is NEARLY the maximum flow algorithm with multiple sources and one sink. 
# To do this you add a consolidated source connected to each node, with constraints at the required node residual capacities. 
# YES. Solved. 