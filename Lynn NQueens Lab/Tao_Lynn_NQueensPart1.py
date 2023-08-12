#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 22 09:48:07 2021

@author: lynntao
"""

import time


def goal_test(board):
    for i in range(0, len(board)):
        if board[i] == -1:
            return False
    return True     


def get_next_unassigned_var(board):
    for i in range(0, len(board)):
        if board[i] == -1:
            return i
  
    
def get_sorted_values(board, row):
    open_pos = []
    if row == 0:
        for i in range(0, len(board)):
            open_pos.append(i)
        return open_pos      
    else:
        flag = True
        for position in range(0, len(board)):
            # check column above
            for i in range(0, row):
                if board[i] == position:
                    flag = False
                    break
            # check left diagonal above
            if flag == True:
                spacer = row
                for i in range(0, row):
                    if board[i] == position-spacer:
                        flag = False
                        break
                    spacer -= 1
            # check right diagonal above
            if flag == True:
                spacer = row 
                for i in range(0, row):
                    if board[i] == position+spacer:
                        flag = False
                        break
                    spacer -= 1
            if flag == True:
                 open_pos.append(position)
            flag = True
        return open_pos        
    
def csp_backtracking(state):
    if goal_test(state): 
        return state
    var = get_next_unassigned_var(state)
    avail_pos = get_sorted_values(state, var)
    if len(avail_pos) != 0:
        avail_pos = avail_pos[int(len(avail_pos)/2):len(avail_pos)] + avail_pos[0:int(len(avail_pos)/2)] 
        failure = 0
        for val in avail_pos:
            new_state = state
            new_state[var] = val
            result = csp_backtracking(new_state)   
            if result == None:
                failure += 1      
            if failure == len(avail_pos):
                new_state[var] = -1   
            if result is not None:
                return result    
    return None


def test_solution(state):
    for var in range(len(state)): 
        left = state[var]
        middle = state[var] 
        right = state[var]
        for compare in range(var + 1, len(state)): 
            left -= 1
            right += 1
            if state[compare] == middle: 
                print(var, "middle", compare) 
                return False
            if left >= 0 and state[compare] == left: 
                print(var, "left", compare)
                return False
            if right < len(state) and state[compare] == right: 
                print(var, "right", compare)
                return False
    return True


# ---- RUN CODE ----
# BOARD 1
size = 31
board = []
for i in range(0,size):
    board.append(-1)

first = time.perf_counter()
nqueens1 = csp_backtracking(board)
last = time.perf_counter()

print("Size: " + str(size))
print("Solution: " + str(nqueens1))
print("Solution Check: " + str(test_solution(board)) + "\n")

time1 = last-first

# BOARD 2
size = 34
board2 = []
for i in range(0,size):
    board2.append(-1)

begin = time.perf_counter()
nqueens2 = csp_backtracking(board2)
end = time.perf_counter()

print("Size: " + str(size))
print("Solution: " + str(nqueens2))
time2 = end-begin
print("Solution Check: " + str(test_solution(board2)))
print("Total time: " + str(time1+time2))




