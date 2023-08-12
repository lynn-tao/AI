#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  3 09:03:15 2021

@author: lynntao
"""
import sys
import math
import time
import pprint

N = 0
subblock_height = 0
subblock_width = 0
symbol_set = set()
constraint_list = []
constraint_neigh = {}


def puzzle_information(puzzle):
    global N
    global subblock_height
    global subblock_width
    global symbol_set
    N = int(math.sqrt(len(puzzle)))
    subblock_height = int(math.sqrt(N))
    for i in range(subblock_height, 0, -1):
        if N % i == 0:
            subblock_height = i
            break
    subblock_width = int(math.sqrt(N))
    for i in range(subblock_width+1, N):
        if N % i == 0:
            subblock_width = i
            break
    symbol_set = set()
    for item in puzzle:
        if item != ".":
            symbol_set.add(item)
    return [N, subblock_width, subblock_height, symbol_set]

def format_puzzle(puzzle):
    puzzle_information(puzzle)
    grid = ""
    for i in range(0, N):
        for i in range(0, N):
            grid += puzzle[i] + " "
        grid += "\n"  
        puzzle = puzzle[N:]
    return grid

def constraint_sets(N):
    global constraint_list
    constraint_list = []
    subblock_height = int(math.sqrt(N))
    for i in range(subblock_height, 0, -1):
        if N % i == 0:
            subblock_height = i
            break
    subblock_width = int(math.sqrt(N))
    for i in range(subblock_width+1, N):
        if N % i == 0:
            subblock_width = i
            break
    constraint_row = set()
    constraint_column = set()
    constraint_block = set()
    
    for i in range(0, N*N, N):
        for j in range(0, N):
            constraint_row.add(i+j)
        constraint_list.append(constraint_row)
        constraint_row = set()
    
    counter = 0
    for i in range(0, N):
        for j in range(0, N):
            constraint_column.add(i+N*counter)
            counter += 1
        constraint_list.append(constraint_column)
        constraint_column = set()
        counter = 0
    
    counter = 0
    for i in range(0,int(N/subblock_height)):
        for j in range(0, N, subblock_width):
            for k in range(j+subblock_height*N*i, j+subblock_height*N*i+subblock_width):
                counter = 0
                for l in range(0, subblock_height):     
                    constraint_block.add(k+N*counter)
                    counter += 1
            constraint_list.append(constraint_block)
            constraint_block = set()
    return constraint_list


def neighbor_list(N):
    global constraint_neigh
    constraint_sets(N)
    for i in range(0, N*N):
        constraint_neigh[i] = set()
    
    for i in range(0, N*N):
        for item in constraint_list:
            if i in item:
                constraint_neigh[i].update(item)
                constraint_neigh[i].remove(i)
        
    return constraint_neigh
    

def symbol_test(puzzle):
    puzzle_information(puzzle)
    symbol_count = {}
    for symbol in symbol_set:
        symbol_count[symbol] = 0
    for item in puzzle:
        if item in symbol_count.keys():
            symbol_count[item] += 1
    return symbol_count
            
   
def goal_test(board):
    for i in range(0, len(board)):
        if board[i] == ".":
            return False
    return True 

def get_next_unassigned_var(board):
    for i in range(0, len(board)):
        if board[i] == ".":
            return i
        
def get_sorted_values(puzzle, index, constraint_neigh):
    N = int(math.sqrt(len(puzzle)))
    constr_index = constraint_neigh[index]
    used_values = set()
    avail_pos = []
    for item in constr_index:
        if puzzle[item] != ".":
            used_values.add(puzzle[item])
    
    alphabet = ["A", "B", "C", "D", "E"]
    for i in range(1, N+1):
        if i >= 10:
            i = alphabet[i-10]
        if str(i) not in used_values:
            avail_pos.append(i)
    return avail_pos
    
    
def sudoku_solution(puzzle):
    if goal_test(puzzle): 
        return puzzle
    var = get_next_unassigned_var(puzzle)
    avail_pos = get_sorted_values(puzzle, var, constraint_neigh)
    if len(avail_pos) != 0:
        failure = 0
        for val in avail_pos:
            new_state = puzzle
            new_state = new_state[:var] + str(val) + new_state[var + 1:]
            # print(format_puzzle(new_state))
            result = sudoku_solution(new_state)   
            if result is not None:
                return result    
    return None
    

# ---- RUN CODE ----
initial = "".join(sys.argv[1:])
# "puzzles_1_standard_easy.txt"
# "puzzles_2_variety_easy.txt"
# puzzles_3_standard_medium_more.txt


with open(initial, encoding='utf-8-sig') as f:
    f = f.read().split("\n")
    for i in range(0,len(f)):
        puzzle_information(f[i])
        constraint_neigh = neighbor_list(N)
        solution = sudoku_solution(f[i])
        print(solution)
        # print("Line: " + str(i+1) + " " + solution)
        # print("Check Solution: " + str(symbol_test(solution)))
   

# ---- TEST CODE ----
# print(constraint_sets(16))
# print(neighbor_list(8))

# first = time.perf_counter()
# puzzle = ".7..23....2....1.147.......81......68.......326.6....8....53..1."
# puzzle_information(puzzle)
# print(format_puzzle(puzzle))
# constraint_neigh = neighbor_list(N)
# solution = sudoku_solution(puzzle)
# print(format_puzzle(solution))
# last = time.perf_counter()
# print(last-first)

# print(symbol_test(solution))

