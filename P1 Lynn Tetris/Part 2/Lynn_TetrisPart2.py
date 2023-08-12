#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 14 09:28:31 2022

@author: lynntao
"""
import sys
import random

row_1 = 40 
row_2 = 100 
row_3 = 300 
row_4 = 1200 

pieces = {
    "I0": [0, 0, 0, 0], 
    "I1": [0],
    "O0": [0, 0],
    "T0": [0, 0, 0],
    "T1": [0, -1],
    "T2": [0, 1, 0],
    "T3": [0, 1],
    "S0": [0, 0, -1],
    "S1": [0, 1],
    "Z0": [0, 1, 1],
    "Z1": [0, -1],
    "J0": [0, 0, 0],
    "J1": [0, -2],
    "J2": [0, 0, 1],
    "J3": [0, 0],
    "L0": [0, 0, 0],
    "L1": [0, 0],
    "L2": [0, -1, -1],
    "L3": [0, 2],
    }

pieces_index = {
    "I0": [0, 1, 2, 3], 
    "I1": [0, -10, -20, -30],
    "O0": [0, 1, -10, -9],
    "T0": [0, 1, 2, -9],
    "T1": [0, -10, -9, -20],
    "T2": [0, 1, 2, 11],
    "T3": [0, 1, 11, -9],
    "S0": [0, 1, -9, -8],
    "S1": [0, 1, 11, -10],
    "Z0": [0, 1, 11, 12],
    "Z1": [0, -10, -9, -19],
    "J0": [0, 1, 2, -10],
    "J1": [0, -10, -20, -19],
    "J2": [0, 1, 2, 12],
    "J3": [0, 1, -9, -19],
    "L0": [0, 1, 2, -8],
    "L1": [0, 1, -10, -20],
    "L2": [0, -10, -9, -8],
    "L3": [0, 1, 11, 21],
    }


def display_board(board):
    grid = ""
    for i in range(0, 20):
        for i in range(0, 10):
            grid += board[i] + " "
        grid += "\n"
        board = board[10:]
    return grid


def convert_2D_to_index(x, y):
    return 200 - ((10-x) + y*10)

def convert_index_to_2D(index):
    x = (index % 10)
    y = 19-(int)(index / 10)
    return [x,y]


def is_filled(board):
    for i in range(0, 20):
        i = i*10
        if board[i: i+10] == "##########":
            return True
    return False


def line_filled(board):
    count = 0
    for i in range(0, 20):
        i = i*10
        if board[i: i+10] == "##########":
            count += 1
            board = "          " + board[:i] + board[i+10:]
    if count == 1:
        score = 40
    if count == 2:
        score = 100
    if count == 3:
        score = 300
    if count == 4:
        score = 1200
    else:
        score = 0
    return [board, score]


def board_col(board):
    height = []
    for i in range(0, 10):
        for j in range(0, 19):
            if board[i+10*j] == "#":
                if (i+10*j-10) >= 0:
                    height.append(20-j)
                break
    return height
    

def place_piece(board, piece, i, row):
    boards = []
    index = convert_2D_to_index(i, row)
    placement = pieces_index[piece]
    new_board = board
    for i in range(0, len(placement)):
        if index+placement[i] < 0:
            new_board = "GAME OVER"
        else:
            new_board = new_board[:index+placement[i]] + "#" + new_board[index+placement[i]+1:]
    
    # REMOVE FILLED LINES 
    if is_filled(new_board) == True:
        new_board = line_filled(new_board)[0]
        # UPDATE THE BOARD COLUMN PARAMETERS
        col = board_col(board) 
    
    # PRINT BOARDS
    # if new_board != "GAME OVER":
    #     print(display_board(new_board))
    # else:
    #     print(new_board)
    
    boards.append(new_board)
    return boards
    

def all_pieces(board):
    col = board_col(board)
    final_boards = []
    for piece in pieces.keys():
        offsets = pieces[piece]
        for i in range(0, 10-len(offsets)+1):
            if len(offsets) == 1:
                row = col[i]+offsets[0]
                boards1 = place_piece(board, piece, i, row)
                final_boards.extend(boards1)
            if len(offsets) == 2:
                row1 = col[i]+offsets[0]
                row2 = col[i+1]+offsets[1]
                row = max(row1, row2)
                boards2 = place_piece(board, piece, i, row)
                final_boards.extend(boards2)
            if len(offsets) == 3:
                row1 = col[i]+offsets[0]
                row2 = col[i+1]+offsets[1]
                row3 = col[i+2]+offsets[2]
                row = max(row1, row2, row3)
                boards3 = place_piece(board, piece, i, row)
                final_boards.extend(boards3)
            if len(offsets) == 4:
                row1 = col[i]+offsets[0]
                row2 = col[i+1]+offsets[1]
                row3 = col[i+2]+offsets[2]
                row4 = col[i+3]+offsets[3]
                row = max(row1, row2, row3, row4)
                boards4 = place_piece(board, piece, i, row)
                final_boards.extend(boards4)
                
    return final_boards

# ------ PART 2 ------
def play_game(strategy): 
    board  =  make_new_board() 
    points  =  0
    while  game  is  not  over:
        piece  =  randomly  chosen  piece for  each  orientation  of  piece:
            for  each  column  on  the  board  where  this  orientation  will  fit: poss_board  =  place(piece,  orientation,  location,  board) poss_score  =  heuristic(poss_board,  strategy)
            #  Keep  track  of  the  board  with  the  highest  heuristic  score  however  you  like! board  =  (the  board  with  the  highest  heuristic  score)
                if  any  lines  were  cleared:
                    points  +=  new_points	#reminder:  1  row  cleared  -->  40  points,  2  -->  100,  3  -->  300,  4  -->  1200 return  points


def  heuristic(board,  strategy):
    a,  b,  c  =  strategy    #  As  many  variables  as  you  want! value  =  0
    value  +=  a  *  (perhaps  highest  column  height?) value  +=  b  *  (perhaps  deepest  well  depth?)
    value  +=  c  *  (perhaps  number  of  holes  in  board,  ie  empty  spaces  with  a  filled  space  above?)
    value  +=  d  *  (perhaps  the  number  of  lines  that  were  just  cleared,  in  the  move  that  made  this  board?) #  add  as  many  variables  as  you  want  -  whatever  you  think  might  be  relevant!
    return  value


def fitness_function(strategy): 
    game_scores = []
    for count in range(num_trials): 
        game_scores.append(play_game(strategy))
    return average(game_scores)


def Sort(pos_heuristic):
    pos_heuristic.sort(key = lambda x: x[1], reverse = True)
    return pos_heuristic


def selection(population, coded_text, NUM_CLONES, TOURNAMENT_SIZE, TOURNAMENT_WIN_PROBABILITY, CROSSOVER_LOCATIONS, MUTATION_RATE):
    next_gen = []
    rank_current = []
    rank_dict = dict()
    for item in population:
        score = fitness_function(4, coded_text, item, n_gram_eng)
        rank_current.append([item, score])
        rank_dict[item] = score
    rank_current = Sort(rank_current)
    for i in range(0, NUM_CLONES):
        next_gen.append(rank_current[i][0])
    
    print(decode(coded_text, rank_current[i][0]))
      
    
    while len(next_gen) < 500:
        parents = random.sample(population, 2*TOURNAMENT_SIZE)
        tourn1 = parents[:TOURNAMENT_SIZE]
        tourn2 = parents[TOURNAMENT_SIZE:]
        parent1 = tournament(tourn1, rank_dict, TOURNAMENT_WIN_PROBABILITY)
        parent2 = tournament(tourn2, rank_dict, TOURNAMENT_WIN_PROBABILITY)
        
        child = breed(parent1, parent2, CROSSOVER_LOCATIONS)
        child = mutation(child, MUTATION_RATE)
    
        if child not in next_gen:
            next_gen.append(child)
        
    return next_gen
    
    
def tournament(tourn, rank_dict, TOURNAMENT_WIN_PROBABILITY):
    rank_tourn = []
    for item in tourn:
        rank_tourn.append([item, rank_dict[item]])
    rank_tourn = Sort(rank_tourn)
    
    for cipher in rank_tourn:
        if random.random() < TOURNAMENT_WIN_PROBABILITY:
            return cipher[0]
    

def breed(parent1, parent2, CROSSOVER_LOCATIONS):
    child = []
    for i in range(0, 26): 
        child.append(0)
    locations = random.sample(range(0, 26),  CROSSOVER_LOCATIONS)
    for pos in locations:
        child[pos] = parent1[pos]
    
    for j in range(0, 26):
        if parent2[j] not in child:
            index = child.index(0)
            child[index] = parent2[j]
        
    if all_letters(child):
        return "".join(child)


def mutation(child, MUTATION_RATE):
    if random.random() < MUTATION_RATE:
        child = swap_letters(child)
    return child


# RUN CODE
# test = "          #         #         #      #  #      #  #      #  #     ##  #     ##  #     ## ##     ## #####  ########  ######### ######### ######### ######### ########## #### # # # # ##### ###   ########"
board = "".join(sys.argv[1:])
# print("Board:\n" + display_board(board))

# MODELING
# col = board_col(board)
# print(col)
all_boards = all_pieces(board)

with open('tetrisout.txt', 'w') as f:
    for item in all_boards:
        f.write(item + "\n")
    

