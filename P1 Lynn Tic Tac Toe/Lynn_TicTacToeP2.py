#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 25 08:49:11 2021

@author: lynntao
"""

import sys

def game_status(board):
    # rows
    if board[0] == board[1] == board[2] == "X":
        return [True, 1]
    if board[0] == board[1] == board[2] == "O":
        return [True, -1]
    if board[3] == board[4] == board[5] == "X":
        return [True, 1]
    if board[3] == board[4] == board[5] == "O":
        return [True, -1]
    if board[6] == board[7] == board[8] == "X":
        return [True, 1]
    if board[6] == board[7] == board[8] == "O":
        return [True, -1]
    # columns
    if board[0] == board[3] == board[6] == "X":
        return [True, 1]
    if board[0] == board[3] == board[6] == "O":
        return [True, -1]
    if board[1] == board[4] == board[7] == "X":
        return [True, 1]
    if board[1] == board[4] == board[7] == "O":
        return [True, -1]
    if board[2] == board[5] == board[8] == "X":
        return [True, 1]
    if board[2] == board[5] == board[8] == "O":
        return [True, -1]
    # diagonals
    if board[0] == board[4] == board[8] == "X":
        return [True, 1]
    if board[0] == board[4] == board[8] == "O":
        return [True, -1]
    if board[2] == board[4] == board[6] == "X":
        return [True, 1]
    if board[2] == board[4] == board[6] == "O":
        return [True, -1]
    
    if "." not in board:
        return [True, 0]
    
    return [False]

def avail_pos(board):    
    avail = set()
    for i in range(0, len(board)):
        if board[i] == ".":
            avail.add(i)
    return avail
    
def board_empty(board):
    return "X" not in board and "O" not in board

def computer_char(board):
    xcount = 0
    for i in range(0, len(board)):
        if board[i] == "X":
            xcount += 1
    ocount = 0
    for i in range(0, len(board)):
        if board[i] == "O":
            ocount += 1
    
    if xcount == ocount:
        return "X"
    else:
        return "O"
        
def display_board(board):
    grid = ""
    for i in range(0, 3):
        for i in range(0, 3):
            grid += board[i] + " "
        grid += "\n"  
        board = board[3:]
    return grid
    
def possible_next_boards(board, current_player):
    pos = avail_pos(board)
    list_boards = []
    for item in pos:
        new_board = board[0:item] + current_player + board[item+1:]
        list_boards.append(new_board)
    return list_boards


def max_step(board, current_player): 
    if game_status(board)[0] == True:
        return game_status(board)[1] 
    results = list()
    boards = possible_next_boards(board, current_player)
    for next_board in boards: 
        results.append(min_step(next_board, next_player))
    return max(results)

def min_step(board, next_player): 
    if game_status(board)[0] == True:
        return game_status(board)[1]  
    results = list()
    boards = possible_next_boards(board, next_player)
    for next_board in boards: 
        results.append(max_step(next_board, current_player))
    return min(results)


def move_max(board, position, current_player):
    if game_status(board)[0] == True:
        return game_status(board)[1] 
    results = list()
    next_board = board[:position] + current_player + board[position+1:]
    results.append(min_step(next_board, next_player))
    return max(results)
    
def move_min(board, position, next_player):
    if game_status(board)[0] == True:
        return game_status(board)[1] 
    results = list()
    next_board = board[:position] + next_player + board[position+1:]
    results.append(max_step(next_board, current_player))
    return min(results)

def nega_max(board, current_player): 
    if game_status(board)[0] == True:
         win = game_status(board)[1] 
         if current_player != first_token:    
             return -1 * win
         else:
            return win
    if current_player == "X":
        next_player = "O"
    else:
        next_player = "X"
    results = list()
    boards = possible_next_boards(board, current_player)
    for next_board in boards: 
        results.append(-1 * nega_max(next_board, next_player))
    return max(results)

def nega_max_move(board, position, current_player):
    if game_status(board)[0] == True:
         win = game_status(board)[1] 
         if current_player != first_token:    
             return -1 * win
         else:
            return win
    if current_player == "X":
        next_player = "O"
    else:
        next_player = "X"
    results = list()
    next_board = board[:position] + current_player + board[position+1:]
    results.append(-1 * nega_max(next_board, next_player))
    return max(results)


# ----- RUN CODE -----

initial = "".join(sys.argv[1:])
# initial = "......XOX"

# DECIDE PLAYER/COMPUTER TOKENS
if board_empty(initial) == True:
    computer_token = input("Should I (computer) be X or O?  ")
else:
    computer_token = computer_char(initial)
    
if computer_token == "X":
    player_token = "O"
    current_player = computer_token
    next_player = player_token
    first_token = current_player

else:
    player_token = "X"
    next_player = computer_token
    current_player = player_token
    first_token = next_player

    
print("Computer: " + computer_token + "    Player: " + player_token + "\n")

# START GAME
# IF BOARD BLANK
if computer_token == "O" and board_empty(initial) == True:
    # PLAYER GOES
    print("Current Board:")  
    print(display_board(initial))
    print(display_board("012345678")) 
    print("\nYou can move to any of these spaces: " + str(avail_pos(initial)))
    position = int(input("Your choice? "))
    print("\n")
    initial = initial[0:position] + player_token + initial[position+1:]

while game_status(initial)[0] != True:
    # COMPUTER GOES FIRST
    print("Current Board:")  
    print(display_board(initial))
    print(display_board("012345678")) 
    if computer_token == "X":
        available_pos = avail_pos(initial)
        # FIND STATUS OF EACH POSITION
        pos_status = []
        pos_space = []
        for pos in available_pos:
            status = nega_max_move(initial, pos, current_player)
            pos_status.append(status)
            pos_space.append(pos)
            if status == 1:
                status = "win."
            if status == 0:
                status = "tie."
            if status == -1:
                status = "loss."
            print("Position " + str(pos) + " returns a " + status)
        # COMPUTER CHOOSES BEST POSITION
        max_status = max(pos_status)
        max_pos = pos_status.index(max_status)
        position = pos_space[max_pos]
        print("\nComputer chooses " + str(pos_space[max_pos]) + "\n")
        # DISPLAYS UPDATED BOARD
        initial = initial[0:position] + computer_token + initial[position+1:]
        print("Current Board:")  
        print(display_board(initial))
        print(display_board("012345678")) 
        
        # PLAYER GOES
        if game_status(initial)[0] != True:
            print("\nYou can move to any of these spaces: " + str(avail_pos(initial)))
            position = int(input("Your choice? "))
            initial = initial[0:position] + player_token + initial[position+1:]
        else:
            break
 
    if computer_token == "O":    
        available_pos = avail_pos(initial)
        # FIND STATUS OF EACH POSITION
        pos_status = []
        pos_space = []
        for pos in available_pos:
            status = move_min(initial, pos, next_player)
            pos_status.append(status)
            pos_space.append(pos)
            if status == -1:
                status = "win."
            if status == 0:
                status = "tie."
            if status == 1:
                status = "loss."
            print("Position " + str(pos) + " returns a " + status)
            
        # COMPUTER CHOOSES BEST POSITION
        min_status = min(pos_status)
        min_pos = pos_status.index(min_status)
        position = pos_space[min_pos]
        print("\nComputer chooses " + str(pos_space[min_pos]) + "\n")
        # DISPLAYS UPDATED BOARD
        initial = initial[0:position] + computer_token + initial[position+1:]
        print("Current Board:")  
        print(display_board(initial))
        print(display_board("012345678")) 
        # PLAYER GOES
        if game_status(initial)[0] != True:
            print("\nYou can move to any of these spaces: " + str(avail_pos(initial)))
            position = int(input("Your choice? "))
            print("\n")
            initial = initial[0:position] + player_token + initial[position+1:]
        else:
            break
 
# # # ONCE GAME IS OVER
print("Current Board:")  
print(display_board(initial))   
final_status = game_status(initial)[1] 

if computer_token == "X":
    if final_status == 1:
        print("Computer wins!")
    if final_status == 0:
        print("Tie!")
    if final_status == -1:
        print("You win!")
else:
    if final_status == 1:
        print("You win!")
    if final_status == 0:
        print("Tie!")
    if final_status == -1:
        print("Computer wins!")
    
