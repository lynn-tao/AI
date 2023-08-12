#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 26 11:16:23 2021

@author: lynntao
"""

# BLACK = X, WHITE = O
# from othello_imports import possible_moves, make_move
import sys
import random
import time

# HELPER METHODS
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


# ----- PART 2 ------
def game_over(board):
    return "." not in board

    
def check_ringofdeath_empty(board):
    ring = [9, 10, 11, 12, 13, 14, 49, 50, 51, 52, 53, 54, 17, 25, 33, 41, 22, 30, 38, 46]
    for item in ring:
        if board[item] != ".":
            return False
    return True


def check_outer_empty(board):
    outer = [2, 3, 4, 5, 16, 24, 32, 40, 58, 59, 60, 61, 23, 31, 39, 47, 1, 8, 9, 6, 14, 15, 57, 48, 49, 62, 54, 55, 0, 7, 56, 63]
    for item in outer:
        if board[item] != ".":
            return False
    return True 


def find_max_pos(max_posresults):
    pos =  []
    for item in max_posresults:
        pos.append(item[0])
    score = []
    for item in max_posresults:
        score.append(item[1])
     
    max_score = score.index(max(score))
    return pos[max_score]


def find_min_pos(min_posresults):
    pos =  []
    for item in min_posresults:
        pos.append(item[0])
    score = []
    for item in min_posresults:
        score.append(item[1])
     
    min_score = score.index(min(score))
    return pos[min_score]
    

def score_board(board):
    score = 0
    
    MOBILITY_COEF = 50
    DEATHSQR_COEF = -25
    EDGE_COEF = 40
    CORNER_BUDDY_COEF = -25
    CORNER_COEF = 75
    
    # ------ END GAME ------
    if game_over(board):
        if board.count("x") > board.count("o"):
            score = 100000000 + 100*(board.count("x") - board.count("o"))
        else:
            score = -100000000 + 100*(board.count("x") - board.count("o"))
    
        return score
    
    if check_ringofdeath_empty(board):
    # ------ EARLY GAME -------
    # MOBILITY
    # (# of available moves for black) – (# of available moves for white)
        MOBILITY_COEF = 200
        score = MOBILITY_COEF * (len(possible_moves(board, "x"))-len(possible_moves(board, "o")))
    else:
    # ------ MID GAME ------
    # MOBILITY
    # (# of available moves for black) – (# of available moves for white)
        MOBILITY_COEF = 100
        score = MOBILITY_COEF * (len(possible_moves(board, "x"))-len(possible_moves(board, "o")))
        
        # SQUARE OF DEATH
        DEATHSQR_COEF = -25
        deathsqr = [9, 10, 11, 12, 13, 14, 17, 25, 33, 41, 22, 30, 38, 46, 49, 50, 51, 52, 53, 54]
        for item in deathsqr:
            if board[item] == "x":
                score += DEATHSQR_COEF * 1
            if board[item] == "o":
                score -= DEATHSQR_COEF * 1
       
        if check_outer_empty(board) is not True:
            # EDGES
            EDGE_COEF = 40
            edges = [2, 3, 4, 5, 16, 24, 32, 40, 58, 59, 60, 61, 23, 31, 39, 47]
            for item in edges:
                if board[item] == "x":
                    score += EDGE_COEF * 1
                if board[item] == "o":
                    score -= EDGE_COEF * 1
            
            
            # CORNER BUDDIES OF DEATH
            # more positive if WHITE takes corner-adjacent squares, more negative if BLACK does
            CORNER_BUDDY_COEF = -25
            corner_buddy = {0: [1, 8, 9], 
                            7: [6, 14, 15],
                            56: [57, 48, 49],
                            63: [62, 54, 55]}
            for item in corner_buddy.keys():
                if board[item] != "x":
                    for buddy in corner_buddy[item]:
                       if board[buddy] == "x":
                           score += CORNER_BUDDY_COEF * 1 
                else:
                    score += EDGE_COEF * 1
                    
                if board[item] != "o":
                    for buddy in corner_buddy[item]:
                        if board[buddy] == "o":
                            score -= CORNER_BUDDY_COEF * 1
                else:
                    score -= EDGE_COEF * 1
                    
                    
            # CORNERS
            # add some number to the score for each corner captured by black and subtract for each corner captured by white
            CORNER_COEF = 500
            corners = [0, 7, 56, 63]
            for item in corners:
                if board[item] == "x":
                    score += CORNER_COEF * 1
                if board[item] == "o":
                    score -= CORNER_COEF * 1
    

    return score
    
def possible_next_boards(board, current_player):
    next_board = []
    avail_pos = possible_moves(board, current_player)
    for item in avail_pos:
        board_new = make_move(board, current_player, item)
        next_board.append(board_new)
    return next_board
        
 
# ---- ALPHA BETA PRUNING HERE ----
def minimax(board, player, depth, alpha, beta):
    if depth == 0 or game_over(board):
        return score_board(board)
    
    if player == "x":
        bestVal = float('-inf')
        boards = possible_next_boards(board, "x")
        results = list()
        if len(boards) > 0:
            for next_board in boards: 
                value = minimax(next_board, "o", depth-1, alpha, beta)
                bestVal = max(bestVal, value) 
                alpha = max(alpha, bestVal)
                results.append(bestVal)
                if beta <= alpha:
                    break
            return max(results)
        
        else:
            value = minimax(board, "o", depth-1, alpha, beta)
            return value

        
    if player == "o":
        bestVal = float('+inf')
        boards = possible_next_boards(board, "o")
        results = list()
        if len(boards) > 0:
            for next_board in boards: 
                value = minimax(next_board, "x", depth-1, alpha, beta)
                bestVal = min(bestVal, value) 
                beta = min(beta, bestVal)
                results.append(bestVal) 
                if beta <= alpha:
                    break
            return min(results)
        
        else:
            value = minimax(board, "x", depth-1, alpha, beta)
            return value
    
    
    
def find_next_move(board, player, depth):
    avail_pos = possible_moves(board, player)
    posresults = []
    for position in avail_pos:
        next_board = make_move(board, player, position)
        
        result = minimax(next_board, opponent(player), depth-1, float("-inf"), float("+inf"))
        posresults.append([position,result])
    
    if player == "x":
        return find_max_pos(posresults)
    else:
        return find_min_pos(posresults)


    
def convert(board):
    new_board = ""
    for i in range(0,len(board)):
        if board[i] == "x":
            new_board += "o" 
        elif board[i] == "o":
           new_board += "x" 
        else:
            new_board += "."
    
    return new_board



# board = sys.argv[1]
# player = sys.argv[2]
# depth = 1
# for count in range(board.count(".")):  # No need to look more spaces into the future than exist at all
#   print(find_next_move(board, player, depth))
#   depth += 1


class Strategy():
  logging = True  # Optional
  def best_strategy(self, board, player, best_move, still_running):
      depth = 1
      for count in range(board.count(".")):  # No need to look more spaces into the future than exist at all
          best_move.value = find_next_move(board, player, depth)
          depth += 1




