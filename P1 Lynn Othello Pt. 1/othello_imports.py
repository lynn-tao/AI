#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 30 09:02:55 2021

@author: lynntao
"""
import sys


# EMPTY, BLACK, WHITE, OUTER = '.', 'x', 'o', '?'
directions = [-11, -10, -9, -1, 1, 9, 10, 11]
# {upleft, up, upright, left, right, downleft, down, downright}
    
def display_board(board, size):
    grid = ""
    for i in range(0, size):
        for i in range(0, size):
            grid += board[i] + " "
        grid += "\n"  
        board = board[size:]
    return grid


def add_border(board):
    new_board = "??????????"
    for i in range(0, 8):
        new_board += "?"
        for i in range(0, 8):
            new_board += board[i]
        new_board += "?"
        board = board[8:]
    new_board += "??????????"
    return new_board


def convert10to8(board):
    board = board[11:89]
    board8 = ""
    for item in board:
        if item != "?":
            board8 += item
    return board8

def opponent(token):
    if token == "x":
        return "o"
    else:
        return "x"  

 
def find_bracket(square, token, board, direction):
    bracket = square + direction
    if board[bracket] == token or board[bracket] == "." or board[bracket] == "?":
        return None
    opp = opponent(token)
    while board[bracket] == opp:
        bracket += direction
        if board[bracket] == ".":
            return bracket
        if board[bracket] == "?":
            return None 


def board_possible_moves(board, avail_moves):  
    for square in avail_moves:
         board = board[:square] + "!" + board[square+1:]
    return board


def convert_square(square): #34
    square8 = square-10
    row = int(square/10) - 1
    questions = 2*row + 1
    return square8 - questions
    

def convert_square10(square): #34
    square10 = square+10
    row = int(square/8)
    square10 += 2*row + 1
    return square10


def possible_moves(board, token):
    board = add_border(board)
    possible_moves = []
    for square in range(11, len(board)-10):
        if board[square] == token:
            for item in directions:
                bracket = find_bracket(square, token, board, item)
                if bracket is not None and bracket not in possible_moves:
                    possible_moves.append(bracket)
    
    for i in range(0, len(possible_moves)):
        possible_moves[i] = convert_square(possible_moves[i])
    
    return possible_moves
    

def make_move(board, token, index):
    board = add_border(board)
    index = convert_square10(index)
    board = board[:index] + token + board[index+1:]
    for item in directions: 
        bracket = index + item
        opp = opponent(token)
        
        if board[bracket] == opp:
            new_bracket = bracket
            while board[new_bracket] == opp and board[new_bracket] != "?":
                new_bracket += item
                if board[new_bracket] == token:
                    while board[bracket] == opp: 
                          board = board[:bracket] + token + board[bracket+1:]
                          bracket += item
                          
    board = convert10to8(board)       
    return board

    
  
    
#  ---- RUN CODE ----
# initial = "".join(sys.argv[1:])

# board = "...................o.......ox......xo.......oox.....x..........."
# board = "xxoo.xox.....oox......oxo..ooxooo..oox.ox.xxx..oxoox...o.....xox"
# # board = "xxoo.xox.....oox......oxo..ooxooo..oox.ox.xxx..oxoox...o.....xox"


# # print(display_board(new_board, 10))
# avail_moves = possible_moves(board, "x")
# print(avail_moves)

# print(display_board(board_possible_moves(board, avail_moves), 8))
# board = make_move(board, "x", 58)
# print(display_board(board, 8))



