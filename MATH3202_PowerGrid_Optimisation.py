"""
Authors: Matthew Smith (45326242) and Joshua Sloman (44828196)
Date: 21/03/2021
Title: MATH3202 Assignment 1
"""

from gurobipy import *
from numpy import sqrt, absolute
from math import ceil

"""
Sets and Data
"""
# Data used is from Matthew Smith (45326242)
# Insert node data (you may have to change file name back to 'nodes2.csv')
nodesfile = open('nodes2_Matt.csv', 'r')
nodeslist = [list(map(int,w.strip().split(','))) 
                 for w in nodesfile if 'Node' not in w]
nodes = [ {'x': w[1], 'y': w[2], 'D0': w[3], 'D1': w[4], 'D2': w[5], 
           'D3': w[6], 'D4': w[7], 'D5': w[8]} for w in nodeslist]

N = range(len(nodes))
T = range(6)    # Number of time periods described in Communication 4

# Insert arc data (you may have to change file name back to 'grid.csv')
arcfile = open('grid_Matt.csv', 'r')
arclist = [list(map(int,w.strip().split(','))) 
               for w in arcfile if 'Arc' not in w]
arcs = [ {'Node1': w[1], 'Node2': w[2]} for w in arclist]

A = range(len(arcs))

# Generator data: (Node, Capacity (MW), Cost ($/MWh))
G = {'Node18': (18, 362, 67),
     'Node19': (19, 569, 71),
     'Node28': (28, 786, 76),
     'Node33': (33, 821, 84)
        }

# Define quantities outlined by company:
    # Communication 2
loss = 0.001

    # Communication 3
arclimit = 129.0  

    # Communication 5
delta_P = 216.0

# Communication 3 - list of arcs with unlimited capacity:
L = [2, 3, 4, 5, 6, 7, 12, 13, 16, 17, 18, 19, 44, 45, 88, 89, 114, 115]

m = Model("Electrigrid")

"""
Add Variables
"""
P = {(g,t): m.addVar() for g in G for t in T}
F = {(i,j,t): m.addVar() for i in N for j in N for t in T}

"""
Objective Function
"""
m.setObjective(quicksum(4*P[g,period]*G[g][2] for g in G for period in T))

"""
Constraints
"""

# Define a function that calculates the distance of an arc with starting node i
# and an end node n
def distance(i,j):
    return sqrt((nodes[i]['x'] - nodes[j]['x'])**2 + (nodes[i]['y'] 
                - nodes[j]['y'])**2)

for period in T:
    for n in N:
        starts = []
        ends = []
        # Find nodes immediately connected to node n
        for a in A:
            # If the node is in the 'Node 2' list, record the 'Node 1'
            if n == arcs[a]['Node2']:
                starts.append(arcs[a]['Node1'])
            # If the node is in the 'Node 1' list, record the 'Node 2'
            if n == arcs[a]['Node1']:
                ends.append(arcs[a]['Node2'])    
        # Constraints related to power in and out of nodes
            # Generators: P_out - P_in*(1-Loss*Distance) = Generation
        if nodes[n]['D{}'.format(period)] == 0:
            m.addConstr(quicksum(F[n,j,period] for j in ends) 
                        -quicksum(F[i,n,period]*(1-loss*distance(i,n)) 
                        for i in starts) == P['Node{}'.format(n),period])
            # Non-generators: P_in*(1-Loss*Distance) - P_out = Demand
        else:                                         
            m.addConstr(quicksum(F[i,n,period]*(1-loss*distance(i,n))
                        for i in starts)-quicksum(F[n,j,period] for j in ends) 
                            == nodes[n]['D{}'.format(period)])
    
    # Set constraints to ensure power going through each arc does not exceed
    # the limits in the lines                     
    for a in A:
        # There are no limits for the lines in the list L
        if L.count(a):
            continue
        else:
            start = arcs[a]['Node1']
            end = arcs[a]['Node2']
            m.addConstr(F[start,end,period] <= arclimit)
           
    # Constraints ensuring generators do not exceed capacity and that the 
    # change in power output from a generator from one period to another does
    # not exceed the limit given 
    for g in G:
        # Generator capacity constraint
        m.addConstr(P[g,period] <= G[g][1])
        if period == 5:
            # First period is constrained by the last period from the previous 
            # day
            Pchange = P[g,0] - P[g,period]
        else:
            Pchange = P[g,period+1] - P[g,period]
        m.addConstr(Pchange <= delta_P)
        m.addConstr(Pchange >= -delta_P)
      
m.optimize()

for period in T:
    for g in G:
        print('{} power for period {} ='.format(g,period),
              round(P[g,period].x,2),'MW',', with a cost of $',
              ceil(P[g,period].x*4*G[g][2]))
    print('Total power for period {} ='.format(period),
          round(sum(P[g,period].x for g in G),2),'MW',', with a cost of $',
          ceil(sum(P[g,period].x*4*G[g][2] for g in G)))

print('Optimal cost for meeting the demand over a whole day = $'
          , ceil(m.objVal))
