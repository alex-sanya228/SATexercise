from pysat.solvers import Cadical195
import numpy as np
from itertools import combinations
import time
from threading import Timer

start_time = time.time()

def k_colorability(file_name, k):

    # Read instance from a .col file. Get number of nodes, and pairs of nodes (v, u) that define edges 
    s = Cadical195()

    f = open(file_name)

    edges = []
    for line in f.readlines():
        if line[0] == 'p':
            nof_nodes = int(line.split()[2])

        if line[0] == "e":
            edge = (int(line.split()[1]), int(line.split()[2]))
            edges.append(edge)
        
    f.close()

    constraints = [] 

    clause_list = []
    pointer = 1

    # Get 1st and 2nd kinds of constraints.
    for i in range(nof_nodes):

        # Get a clause for every node. Such clause has k number of variables. This clause means "Choose at least 1 color for a given node"
        clause = list(range(pointer, pointer + k))
        clause_list.append(clause)

        # Get a clause that means "Choose at most 1 color for a given node"
        combos = list(combinations(clause, 2))
        # Negate the literals and append the formula
        neg_combos = [[- num for num in comb] for comb in combos]
        s.append_formula(neg_combos)

        pointer += k

    # Get constraints that means "Neighboring vertices must not have the same color". 
    for edge in edges:

        # Get beginning and end vertices
        first_vertex = edge[0]
        second_vertex = edge[1]

        # Get associated with the nodes clauses of the 1st kind
        first_list = clause_list[first_vertex - 1]
        second_list = clause_list[second_vertex - 1]

        # Get required clauses, again negating the literals from the first kind of constraints
        for m in range(k):
            constraint = -first_list[m], -second_list[m]
            constraints.append(constraint)

    s.append_formula(constraints)
    s.append_formula(clause_list)

    # timer = Timer(10, s.interrupt())
    # timer.start()

    res = s.solve()
    # print(s.get_model())

    s.delete()

    return res

# Call function with using file name and number of colors k
print(k_colorability("instances/anna.col", 11))

print("--- %s seconds ---" % (time.time() - start_time))