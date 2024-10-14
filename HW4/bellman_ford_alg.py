# Bellman-Ford Algorithm with Negative Cycle and Arbitrage Detection
# 
# Code Authors: Madie Munro, Redempta Manzi, Brittany Boles
#
import requests
import pandas as pd
import numpy as np

# Graph Class
class Graph:

    # Initialize Graph object
    def __init__(self,verts):
        self.V = verts
        self.G = []

    # Add edge to graph. Edges have two vertices as edge endpoints and a weight value    
    def addEdge(self,u,v,w):
        self.G.append([u,v,w])

    # Print utility function to format path distance nicely
    def printPath(self,d):
        print("Distance from start to end vertex of the given graph:")
        for i in range(self.V):
            print("{0}\t\t{1}".format(i, d[i]))

    # Print utility function to output negative cycles detected
    def printNegCycles(self,s,pred):

        # Initialize the start of the cycle
        cycle_start = s
        for _ in range(self.V):
            cycle_start = pred[cycle_start]

        # Detect cycle and its vertices
        cycle = []
        v = cycle_start
        while True:
            cycle.append(v)
            v = pred[v]
            if v == cycle_start and len(cycle) > 1:
                cycle.append(cycle_start)
                break

        # Print cycle
        cycle.reverse()
        print("Negative cycle found: ", cycle)

    # Print utility function to output arbitrage detected
    def printArbitrage(self,s,pred,currency):

        # Initialize the start of the cycle
        cycle_start = s
        for _ in range(self.V):
            cycle_start = pred[cycle_start]

        # Detect arbitrage and its vertices
        cycle = []
        v = cycle_start
        while True:
            cycle.append(v)
            v = pred[v]
            if v == cycle_start and len(cycle) > 1:
                cycle.append(cycle_start)
                break

        # Print arbitrage detected
        cycle.reverse()
        print("Arbitrage found: ", [currency[i] for i in cycle])

    # Bellman-Ford Algorithm (for Negative Cycle Detection)
    def BellmanFordAlg(self,start):
        distance = [float("Inf")] * self.V # Create distance array
        distance[start] = 0 # Set distance from starting vertex to 0
        predecessor = [-1] * self.V # Set up predecessor vertex array

        # Iterate over vertices to find shortest path from source to another vertex. 
        # Update the distance if a shorter path is found
        for _ in range(self.V - 1):
            for u, v, w in self.G:
                if distance[u] != float("Inf") and distance[u] + w < distance[v]:
                    distance[v] = distance[u] + w
                    predecessor[v] = u

        # Print all distances
        self.printPath(distance)

        # Check for negative cycles
        for u, v, w in self.G:
            if distance[u] != float("Inf") and distance[u] + w < distance[v]:
                print("A negative cycle was found")
                self.printNegCycles(v, predecessor) 
                return

    # Bellman-Ford Algorithm (for Arbitrage Detection)
    def BellmanFordArbitrage(self,start,currency):
        distance = [float("Inf")] * self.V # Create distance array
        distance[start] = 0 # Set distance from starting vertex to 0
        predecessor = [-1] * self.V # Set up predecessor vertex array

        # Iterate over vertices to find shortest path from source to another vertex. 
        # Update the distance if a shorter path is found
        for _ in range(self.V - 1):
            for u, v, w in self.G:
                if distance[u] != float("Inf") and distance[u] + w < distance[v]:
                    distance[v] = distance[u] + w
                    predecessor[v] = u

        # Print all distances
        self.printPath(distance)

        # Check for arbitrage opportunity
        for u, v, w in self.G:
            if distance[u] != float("Inf") and distance[u] + w < distance[v]:
                print("An arbitrage opportunity was found")
                self.printArbitrage(v, predecessor, currency) 
                return

def create_exchange_rate_graph(df):
    graph = Graph(len(df.index))  
    currency_names = {currency: index for index, currency in enumerate(df.index)}  # Index currencies
    currency_index = {index: currency for index, currency in enumerate(df.index)}  # Reverse lookup

    # Add edges with weights (negative log of exchange rate)
    for currency in df.index:
        for target_currency, rate in df.loc[currency].items():
                if rate > 0 and target_currency in currency_names:
                    graph.addEdge(currency_names[currency], currency_names[target_currency], -np.log(rate)) #reverse log negative cycles to detect arbitrage

    return graph, currency_names, currency_index  # Return the graph and the currency names and index

def main():

    # Basic Example
    graph = Graph(5)

    graph.addEdge(0,1,2)
    graph.addEdge(0,3,6)
    graph.addEdge(1,2,4)
    graph.addEdge(2,3,1)
    graph.addEdge(3,4,2)

    graph.BellmanFordAlg(0)

    print("\n\n")

    # Example with a negative cycle
    graph_neg_cycle = Graph(10)
    
    graph_neg_cycle.addEdge(0, 2, -3)
    graph_neg_cycle.addEdge(0, 1, 4)
    graph_neg_cycle.addEdge(1, 2, 5)
    graph_neg_cycle.addEdge(1, 3, 4)
    
    # negative cycle edges
    graph_neg_cycle.addEdge(2, 3, 1)
    graph_neg_cycle.addEdge(3, 4, -2)
    graph_neg_cycle.addEdge(4, 2, -2)

    graph_neg_cycle.addEdge(3, 8, 12)
    graph_neg_cycle.addEdge(4, 5, 4)
    graph_neg_cycle.addEdge(5, 7, 3)
    graph_neg_cycle.addEdge(5, 6, 1)
    graph_neg_cycle.addEdge(6, 7, -1)
    graph_neg_cycle.addEdge(6, 8, 5)
    graph_neg_cycle.addEdge(7, 9, 5)
    graph_neg_cycle.addEdge(7, 8, 7)
    graph_neg_cycle.addEdge(8, 9, 2)

    graph_neg_cycle.BellmanFordAlg(0)

    print("\n\n")

    #------------------------------------------------------------------------------------------------------------

    # Check currency arbitrage
    exchange_rates = {}  

    # Make API calls (TODO: remove API key when submitting)
    for currency in ["AUD", "HKD", "INR", "KRW", "CAD", "CNY", "MXN", "RUB", "ZAR", "AED", "EUR", "GBP", "RWF", "JPY", "USD", "BRL"]: # Select currencies to graph
        url = f'https://v6.exchangerate-api.com/v6/[API KEY HERE]/latest/{currency}' 
        response = requests.get(url)
        data = response.json()

        # Store rates in dictionary
        if "conversion_rates" in data:
            exchange_rates[currency] = data["conversion_rates"]

    # Convert rate dictionary to Dataframe
    currency_exchange_rates = pd.DataFrame(exchange_rates).T 

    # Create graph from exchange data
    curr_ex_graph, currency_names, currency_index = create_exchange_rate_graph(currency_exchange_rates)

    # Run Bellman-Ford Alg
    curr_ex_graph.BellmanFordArbitrage(currency_names["USD"], currency_index)

if __name__ == "__main__":
    main()