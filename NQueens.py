from pysat.solvers import Cadical195
import numpy as np
from itertools import combinations
import time
from threading import Timer 

# This function creates a list of negated pairs of literals for rows, columns and diagonals. This takes care of the "at most 1" condition

def pairwise_encoding(clause):
    combos = list(combinations(clause, 2))
    neg_combos = [[- num for num in comb] for comb in combos]

    return neg_combos

def NQueens(N):

    s = Cadical195()

    # Create a 2D array that represents my literals for convenience. This is my N by N chessboard with numbers from 1 to N * N
    myArr = []
    k = 1
    for i in range(N):
        innerArr = []
        for j in range(N):
            innerArr.append(k)
            k += 1
        myArr.append(innerArr)

    # myArr = [[i + j for i in range(1, N + 1)] for j in range(0, N * N, N)]

    # Transpose my array to handle columns later
    tarray = np.array(myArr).transpose().tolist()

    # Choose at least one queen for each row
    s.append_formula(myArr)

    # Choose at most one queen for each row. Here I will use pairwise encoding for rows, columns and diagonals for simplicity
    for row in myArr:
        s.append_formula(pairwise_encoding(row))
    
    # Choose at most one queen for each column
    for col in tarray:
        s.append_formula(pairwise_encoding(col))

    # Next 4 loops take care of retrieving the diagonals and adding necessary clauses to the formula
    for i in range(2, N):
        myList = [i]
        k = N - 1
        for j in range(1, i):
            myList.append(i + k)
            k += N - 1
  
        s.append_formula(pairwise_encoding(myList))

    t = 0
    for i in range(N * (N - 1) + 1, N * N):
        myList = [i]
        k = N - 1
        
        for j in range(N, 1 + t, -1):
            myList.append(i - k)
            k += N - 1
        t += 1

        s.append_formula(pairwise_encoding(myList))

    for i in range(1, N):
        myList = [i]
        k = N + 1
        for j in range(N - i):
            myList.append(i + k)
            k += N + 1

        s.append_formula(pairwise_encoding(myList))
    
    t = 0
    for i in range(N + 1, N * (N - 1) + 1, N):
        myList = [i]
        k = N + 1
        for j in range(2, N - t):
            myList.append(i + k)
            k += N + 1
        t += 1

        s.append_formula(pairwise_encoding(myList))

    # Final part. Here I set the counter for found solutions. Then I solve the model, if the result is SAT, I append the counter and retrieve the solution. 
    # Retrieved solution is negated and added back to the formula to exclude found solution. Then the model is solved again. The process continues until model returns UNSAT. 
    counter = 0
    while True:
        if s.solve() is False:
            break

        sol = s.get_model()
        # print([l for l in sol if l > 0])

        neg_sol = [-l for l in sol if l > 0]
        s.add_clause(neg_sol) 

        counter += 1

    return counter

print(NQueens(9))