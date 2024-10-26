# network flow for Money Reconciliation
# 
# Code Authors: Madie Munro, Redempta Manzi, Brittany Boles
#
import numpy as np
import networkx as nx


#build flow network, then calculate the number of checks to be written and how much should be on them
def reconciliation_checks(imbalance, amounts, n):
    #construct graph using networkx package
    G = nx.DiGraph()
    src, sink = "s", "t" #source and sink

    #add edges between src and sink based on imbalances calculated between friends
    for i in range(n):
        if imbalance[i] > 0:
            G.add_edge(src, i, capacity=imbalance[i])
        elif imbalance[i] < 0:
            G.add_edge(i, sink, capacity=-imbalance[i])

    #add edges between friends based on amounts owed
    for i in range(n):
        for j in range(n):
            if amounts[i, j] > 0:
                G.add_edge(i, j, capacity=amounts[i, j])

    return successive_shortest_path(G,src,sink)  #calculate number of checks needed and their amounts


#run successive shortest path on reconciliation graph
def successive_shortest_path(graph,s,t):
    flow = nx.max_flow_min_cost(graph,s,t)  #calculate the max flows of min cost within graph
    checks = []  #checks to dole out

    #add to check list the graph edges not containing the src or sink and that have positive flow.
    for i in flow:
        for j in flow[i]:
            if i != 's' and j != 't' and flow[i][j] > 0:  # Ensure flow is positive
                checks.append((i, j, flow[i][j]))
    return checks


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

    #calculate the imbalance
    I = [0] * friends
    for i in range(friends):
        for j in range(friends):
            I[i] += A[j, i] - A[i, j]

    #determine number of checks to distribute (using flow network)
    checks = reconciliation_checks(I, A, friends)

    #print checks needed between friends
    if checks:
        print("Checks to dole out:")
        for c in checks:
            print(f"{friend_names[c[0]]} needs to pay {friend_names[c[1]]} ${c[2]:.2f}")
    else:
        print("Perfectly balanced, as all things should be")


if __name__ == "__main__":
    main()
