# network flow for Money Reconciliation
# 
# Code Authors: Madie Munro, Redempta Manzi, Brittany Boles
#
from collections import defaultdict, deque
import numpy as np
import networkx as nx

# detects the minimum weight and cost cycle within an undirected graph, then deletes the min cost edge from the cycle
def min_cycle(graph, cycle):

    #find minimum weight in cycle
    min_edge = min(
        cycle,
        key=lambda edge: (
            graph[edge[0]][edge[1]]['weight']
            if graph.has_edge(edge[0], edge[1])
            else graph[edge[1]][edge[0]]['weight']
        )
    )
    #determine minimum cost
    min_cost = (
        graph[min_edge[0]][min_edge[1]]['weight']
        if graph.has_edge(min_edge[0], min_edge[1])
        else graph[min_edge[1]][min_edge[0]]['weight']
    )
    
    #adjust weights in cycle by removing the minimum cost edge (zero)
    for u, v in cycle:
        if (u, v) == min_edge:
            graph[u][v]['weight'] -= min_cost
            if graph[u][v]['weight'] == 0:
                graph.remove_edge(u, v)
        elif graph.has_edge(u, v):
            graph[u][v]['weight'] -= min_cost
            if graph[u][v]['weight'] == 0:
                graph.remove_edge(u, v)
        elif graph.has_edge(v, u):
            graph[v][u]['weight'] += min_cost

def find_min_transactions(A,n):

    #create graph G (directed) with n nodes (n being the number of friends/roommates)
    G = nx.DiGraph()
    for i in range(n):
        G.add_node(i)

    #add edges between roommates based on what amounts are owed (i owe j x, j owes i y, etc...)
    for i in range(n):
        for j in range(n):
            if A[i,j] > 0:
                if A[j,i] > 0:
                    if A[i,j] > A[j,i]:
                        G.add_edge(i, j, weight = (A[i,j] - A[j,i])) #weights are the imbalaces between roomates, or just the amount owed
                    elif A[i,j] < A[j,i]:
                        G.add_edge(j, i, weight = (A[j,i] - A[i,j]))
                else:
                    G.add_edge(i, j, weight = A[i,j])
    
    #C=convert DiGraph to Undirected Graph
    G_undir = G.to_undirected()

    #detect undirected cycles, then find minimum cycle in original graph
    while True:
        G_undir = G.to_undirected() #refresh instance of an undirected graph (a key error pops up otherwise)
        try:
            cycle = nx.find_cycle(G_undir)
            min_cycle(G, cycle)
        except nx.NetworkXNoCycle: #if no cycle is found, stop
            break

    #aggregate transactions between roommates
    transactions = []
    for i, j, data in G.edges(data=True):
            if data["weight"] > 0:
                transactions.append((i, j, data["weight"]))
    
    return transactions

def main():
    friends = 7  #number of friends in the apartment
    A = np.zeros((friends, friends))  #initialize matrix keeping track of money owed between friends
    friend_names = {0: "Madie", 1: "Brittany", 2: "Yvette", 3: "Emma", 4: "Mark", 5: "Redempta", 6: "Aidan"}  #friends

    #read in imbalance data
    roommate_IOU = open("C:/Users/madie/OneDrive/Desktop/CSCI 532/Algorithms/HW5/roommate_check_reconciliation_imbalanced.txt", "r")

    #split entities in file, then calculate amounts each friend owes each other
    for line in roommate_IOU.readlines():
        line = line.strip("\n")
        entities = line.split(' ')
        payer, payee, amount = entities[0], entities[1], float(entities[2])

        #assign index for friends
        payer_index = next((k for k, v in friend_names.items() if v == payer), None)
        payee_index = next((k for k, v in friend_names.items() if v == payee), None)

        if payer_index is None or payee_index is None:
            print(f"Error: {payer} or {payee} not found in friend names.")
            continue
        
        #calculate amount owed between friends
        A[payer_index, payee_index] += amount

    #close file
    roommate_IOU.close()

    #determine number of checks to distribute (using undirected cycle detection)
    checks = find_min_transactions(A, friends)

    #print checks needed between friends
    if checks:
        print("Checks to dole out:")
        for c in checks:
            print(f"{friend_names[c[0]]} needs to pay {friend_names[c[1]]} ${c[2]:.2f}")
    else:
        print("Perfectly balanced, as all things should be")


if __name__ == "__main__":
    main()
