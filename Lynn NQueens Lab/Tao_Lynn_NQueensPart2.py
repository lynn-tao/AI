#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 23 12:52:36 2021

@author: lynntao
"""

import time
import random

def test_solution(state):
    for var in range(len(state)): 
        left = state[var]
        middle = state[var] 
        right = state[var]
        for compare in range(var + 1, len(state)): 
            left -= 1
            right += 1
            if state[compare] == middle: 
                return False
            if left >= 0 and state[compare] == left: 
                return False
            if right < len(state) and state[compare] == right: 
                return False
    return True


def count_conflicts(state):
    conflict = 0
    for i in range(0, len(state)):
        # vertical column
        position = state[i]
        for l in range(i+1, len(state)):
            if state[l] == position:
                conflict += 1
                break
        # left diagonal
        increment = 1
        for j in range(i+1, len(state)):
            if state[j] == position - increment:
                conflict += 1
                break
            increment += 1
        # right diagonal
        spacer = 1
        for k in range(i+1, len(state)):
            if state[k] == position + spacer:
                conflict += 1
                break
            spacer += 1

    return conflict
            
def constrained_queen(state, row):
    # state = [0,1,4,3,2]
    conflict = 0
    position = state[row]
    
    # column above
    for l in range(0, row):
        if state[l] == position:
            conflict += 1
            break
    
    # column below
    for l in range(row+1, len(state)):
        if state[l] == position:
            conflict += 1
            break
        
    # left diagonal above
    spacer = row
    for i in range(0, row):
        if state[i] == position-spacer:
            conflict +=1
            break
        spacer -= 1
    
    # left diagonal below
    increment = 1
    for j in range(row+1, len(state)):
        if state[j] == position - increment:
            conflict += 1
            break
        increment += 1
      
    # right diagonal above
    spacer = row 
    for i in range(0, row):
        if state[i] == position+spacer:
            conflict+=1
            break
        spacer -= 1    
        
    # right diagonal below
    spacer = 1
    for k in range(row+1, len(state)):
        if state[k] == position + spacer:
            conflict += 1
            break
        spacer += 1

    return conflict


def board_conflicts(board):
    conflicts = 0 
    for i in range(0, len(board)):
        conflicts += constrained_queen(board, i)
    return conflicts
        

def generate_board(size):
    board = []
    for i in range(0, size, 2):
        board.append(i) 
    for i in range(1, size, 2):
        board.append(i) 
    # for i in range(0, size):
    #     board.append(i) 
    return board

    
def incremental_repair(board):
    # find queen causing most conflicts 
    conflict = []
    for i in range(0, len(board)):
        conflict.append(constrained_queen(board, i))
    queen_max = max(conflict)
    index_queens = []
    for j in range(0, len(conflict)):
        if conflict[j] == queen_max:
            index_queens.append(j)    
    queen_row = random.choice(index_queens)
    
    # find space on that row that attacks fewest number of other queens
    row_conflicts = []
    for i in range(0, len(board)):
        board[queen_row] = i
        row_conflicts.append(constrained_queen(board, queen_row))
    queen_min = min(row_conflicts)
    index_q = []
    for k in range(0, len(row_conflicts)):
        if row_conflicts[k] == queen_min:
            index_q.append(k)
    queen_new = random.choice(index_q)
    board[queen_row] = queen_new
    
    return [board, board_conflicts(board)]


#  --- RUN CODE ---- 
first = time.perf_counter()
# BOARD ONE
board = generate_board(39)
conflicts = board_conflicts(board)
print("Size: " + str(len(board)) + "\nInitial State Board: " + str(board) + "\nConflicts: "+ str(conflicts))
new_board = board
while test_solution(board) != True:
    new_board = incremental_repair(board)
    board = new_board[0]
    print("Board: " + str(board) + "\nConflicts: "+ str(new_board[1]))    
print("Check Solution: " + str(test_solution(board)) + "\n\n\n")

# BOARD TWO
board = generate_board(45)
conflicts = board_conflicts(board)
print("Size: " + str(len(board)) + "\nInitial State Board: " + str(board) + "\nConflicts: "+ str(conflicts))
new_board = board
while test_solution(board) != True:
    new_board = incremental_repair(board)
    board = new_board[0]
    print("Board: " + str(board) + "\nConflicts: "+ str(new_board[1]))

print("Check Solution: " + str(test_solution(board)))
last = time.perf_counter()
print("Time Elapsed: " + str(last-first))

