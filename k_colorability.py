from pysat.solvers import Cadical195
import numpy as np
from itertools import combinations
import time
from threading import Timer

start_time = time.time()

def k_colorability(file_name, k):
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

    combos = []

    constraints = [] 

    pointer = 1
    clause_list = []
    for i in range(nof_nodes):
        arr = list(range(pointer, pointer + k))

        clause_list.append(arr)

        combos = list(combinations(arr, 2))
        neg_combos = [[- num for num in comb] for comb in combos]

        s.append_formula(neg_combos)

        pointer += k

    for edge in edges:
        first_vertex = edge[0]
        second_vertex = edge[1]

        first_list = clause_list[first_vertex - 1]
        second_list = clause_list[second_vertex - 1]

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

print(k_colorability("instances/anna.col", 11))

print("--- %s seconds ---" % (time.time() - start_time))