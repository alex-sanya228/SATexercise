from pysat.solvers import Cadical195
import numpy as np
from itertools import combinations
import time
from threading import Timer 

def NQueens(N):

    s = Cadical195()

    # Create a 2D array that represents my literals for convenience. This is my N by N chessboard
    myArr = []
    k = 1
    for i in range(N):
        innerArr = []
        for j in range(N):
            innerArr.append(k)
            k += 1
        myArr.append(innerArr)

    # Create a trasnposed array for retrieving clauses for columns
    tarray = np.array(myArr).transpose().tolist()

    # Choose at least one queen for each row
    s.append_formula(myArr)

    # Choose at most one queen for each row. Here I will use pairwise encoding for rows, columns and diagonols for simplicity
    for clause in myArr:

        # Get pairs and negate them. Then append the formula
        combos = list(combinations(clause, 2))
        neg_combos = [[- num for num in comb] for comb in combos]

        s.append_formula(neg_combos)
    
    # Choose at most one queen for each column
    for clause in tarray:

        combos = list(combinations(clause, 2))
        neg_combos = [[- num for num in comb] for comb in combos]

        s.append_formula(neg_combos)

    
    for i in range(2, N):
        myList = [i]
        k = N - 1
        for j in range(1, i):
            myList.append(i + k)
            k += N - 1
        # print(myList)
        combos = list(combinations(myList, 2))
        neg_combos = [[- num for num in comb] for comb in combos]
        s.append_formula(neg_combos)

    # Next 4 loops take care of retrieving the diagonals and adding them to the formula
    t = 0
    for i in range(N * (N - 1) + 1, N * N):
        myList = [i]
        k = N - 1
        
        for j in range(N, 1 + t, -1):
            myList.append(i - k)
            k += N - 1
        t += 1

        combos = list(combinations(myList, 2))
        neg_combos = [[- num for num in comb] for comb in combos]
        s.append_formula(neg_combos)

    for i in range(1, N):
        myList = [i]
        k = N + 1
        for j in range(N - i):
            myList.append(i + k)
            k += N + 1

        combos = list(combinations(myList, 2))
        neg_combos = [[- num for num in comb] for comb in combos]
        s.append_formula(neg_combos)
    

    t = 0
    for i in range(N + 1, N * (N - 1) + 1, N):
        myList = [i]
        k = N + 1
        for j in range(2, N - t):
            myList.append(i + k)
            k += N + 1
        t += 1
        combos = list(combinations(myList, 2))
        neg_combos = [[- num for num in comb] for comb in combos]
        s.append_formula(neg_combos)

    # Final part. Here I set the counter for found solutions. Then I solve the model, if the result is SAT, I append the counter and retrieve the solution. 
    # Retrieved solution is negated and added back to the formula. Then the model is solved again. The process continues untill model returns UNSAT. 
    counter = 0
    while True:
        res = s.solve()
        if res is False:
            break

        sol = s.get_model()
        print([l for l in sol if l > 0])

        neg_sol = [-l for l in sol if l > 0]
        s.add_clause(neg_sol) 

        counter += 1

    return counter



print(NQueens(6))