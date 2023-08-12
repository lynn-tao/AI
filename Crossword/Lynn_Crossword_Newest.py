import sys; args = sys.argv[1:]
import random
# myLines = open(args[0],'r').read().splitlines()

# Lynn_CrosswordAIP1.py 11x13 27 wordlist.txt H0x0begin V8x12end H5x8
# Lynn_CrosswordAIP1.py 8x8 64
# Lynn_CrosswordAIP1.py 7x7 0 wordlist.txt V0x0Striped V0x6Twiztid
# Lynn_CrosswordAIP1.py 11x11 20 wordlist.txt V0x1Ads

# All spaces are not part of a horizontal and vertical word
# Lynn_CrosswordAIP1.py 15x15 39 wordlist.txt H0x0Mute V0x0mule V10x13fair H7x5 V3x4 H6x7 V11x3

# A few less than three spaces
# Lynn_CrosswordAIP1.py 9x14 32 wordlist.txt V5x0 V8x3 H3x10 V0x9Precedent

# Lynn_CrosswordAIP1.py 9x9 14 wordlist.txt V0x4con V6x4ate
# Lynn_CrosswordAIP1.py 13x13 32 wordlist.txt H1x4#Toe# H9x2# V3x6# H10x0Scintillating V0x5Stirrup H4x2##Ordained V0x1Wall V0x12Ean V5x0orb
# Lynn_CrosswordAIP1.py 13x13 32 wordlist.txt V2x4# V1x9# V3x2# h8x2#moo# v5x5#two# h6x4#ten# v3x7#own# h4x6#orb# H12x4Goal
# Lynn_CrosswordAIP1.py 13x13 25 wordlist.txt H6x4no#on v5x5nor v0x0instep h0x4KNEE H0x9gait v0x12toed

# fill initial reverse needs to make it initially filled reverse
# Lynn_CrosswordAIP1.py 9x30 48 wordlist.txt h4x12q# h3x9s# h2x9# v2x0eat V5x1#i V8x26f

# recursion takes too long
# Lynn_CrosswordAIP1.py 14x15 104 wordlist.txt V3x2 h2x3 h4x4 h7x4 v5x10 h4x7##

# ------ HELPER METHODS -------
def display_board(board, height, width):
    grid = ""
    for i in range(0, height):
        for i in range(0, width):
            grid += board[i] + " "
        grid += "\n"
        board = board[width:]
    return grid


def get_height_width(hw):
    index = hw.index("x")
    height = hw[:index]
    width = hw[index+1:]
    return [height, width]


def add_word(board, height, width, word):
    direction = word[0]
    index = word.index("x")
    row = int(word[1:index])
    word = word[index+1:]
    
    i = 0
    while i < len(word) and word[i].isdigit():
        i+=1
    column = int(word[:i])
    word = word[i:]

    # place word
    if direction.upper() == "H":
        index = width * row + column
        if len(word) == 0:
            board = board[:index] + "#" + board[index+1:]
        else:
            for i in range(0, len(word)):
                board = board[:index] + word[i] + board[index+1:]
                index += 1
    else:
        index = width * row + column
        if len(word) == 0:
            board = board[:index] + "#" + board[index+1:]
        else:
            for i in range(0, len(word)):
                board = board[:index] + word[i] + board[index+1:]
                index += width
    return board

# ------ PART 1 HELPER METHODS -------
def convert_2D_to_index(x, y, width, height):
    return (x*width + y)


def convert_index_to_2D(index, width, height):
    x = (int)(index / width)
    y = index % width
    return [x,y]


# check if it is possible to place a block at index
def check_three(index, board, width, height):
    x = convert_index_to_2D(index, width, height)[0]
    y = convert_index_to_2D(index, width, height)[1]
    

    # if (0 < x < 3 and 0 < y < 3) or (width - 3 < x < width - 1  and  0 < y < 3) or (0 < x < 3 and y > height - 3) and (x>width-3 and y > height-3):
    #     return None

    # 1/2 SPACES BETWEEN
    # check top
    if x >= 3:
        if board[convert_2D_to_index(x-3, y, width, height)] == "#":
            if board[convert_2D_to_index(x-1, y, width, height)] != "#" or board[convert_2D_to_index(x-2, y, width, height)] != "#":
                return False
    # check right
    if y < width - 3:
        if board[convert_2D_to_index(x, y+3, width, height)] == "#":
            if board[convert_2D_to_index(x, y+1, width, height)] != "#" or board[convert_2D_to_index(x, y+2, width, height)] != "#":
                return False
    # check bottom
    if x < height - 3:
        if board[convert_2D_to_index(x+3, y, width, height)] == "#":
            if board[convert_2D_to_index(x+1, y, width, height)] != "#" or board[convert_2D_to_index(x+2, y, width, height)] != "#":
                return False
    # check left
    if y >= 3:
        if board[convert_2D_to_index(x, y-3, width, height)] == "#":
            if board[convert_2D_to_index(x, y-1, width, height)] != "#" or board[convert_2D_to_index(x, y-2, width, height)] != "#":
                return False
    
    # 1 SPACE BETWEEN
    # check top
    if x >= 2:
        if board[convert_2D_to_index(x-2, y, width, height)] == "#":
            if board[convert_2D_to_index(x-1, y, width, height)] != "#":
                return False
    # check right
    if y < width - 2:
        if board[convert_2D_to_index(x, y+2, width, height)] == "#":
            if board[convert_2D_to_index(x, y+1, width, height)] != "#":
                return False
    # check bottom
    if x < height - 2:
        if board[convert_2D_to_index(x+2, y, width, height)] == "#":
            if board[convert_2D_to_index(x+1, y, width, height)] != "#":
                return False
    # check left
    if y >= 2:
        if board[convert_2D_to_index(x, y-2, width, height)] == "#":
            if board[convert_2D_to_index(x, y-1, width, height)] != "#":
                return False 
        
    return True


# places a block, fills in sides if necessary
def fill_in(index, board, width, height, blocks):
    
    if board[index] == "#" or board[index].isalpha():
        return [board, blocks]
    
    x = convert_index_to_2D(index, width, height)[0]
    y = convert_index_to_2D(index, width, height)[1]
    
    if x < 3 and y < 3:
        bl = 0
        for i in range(0, x+1):
            for j in range(0, y+1):
                pos = convert_2D_to_index(i, j, width, height)
                if board[pos] == "-":
                    board_block = fill_reverse(pos, board, width, height)
                    board = board_block[0]
                    bl += board_block[1]
                    if board == None:
                        return [board, blocks-bl]
        return [board, blocks-bl]

    if x < 3 and y >= width-3:
        bl = 0
        for i in range(0, x+1):
            for j in range(y, width):
                pos = convert_2D_to_index(i, j, width, height)
                if board[pos] == "-":
                    board_block = fill_reverse(pos, board, width, height)
                    board = board_block[0]
                    bl += board_block[1]
                    if board == None:
                        return [board, blocks-bl]
        return [board, blocks-bl]
    
    if x >= height-3 and y < 3:
        bl = 0
        for i in range(x, height):
            for j in range(0, y+1):
                pos = convert_2D_to_index(i, j, width, height)
                if board[pos] == "-":
                    board_block = fill_reverse(pos, board, width, height)
                    board = board_block[0]
                    bl += board_block[1]
                    if board == None:
                        return [board, blocks-bl]
        return [board, blocks-bl]
    
    if x >= height-3 and y >= width-3:
        bl = 0
        for i in range(x, height):
            for j in range(y, width):
                pos = convert_2D_to_index(i, j, width, height)
                if board[pos] == "-":
                    board_block = fill_reverse(pos, board, width, height)
                    board = board_block[0]
                    bl += board_block[1]
                    if board == None:
                        return [board, blocks-bl]
        return [board, blocks-bl]
    
    
    board_block = fill_reverse(index, board, width, height)
    board = board_block[0]
    bl = board_block[1]
    if board == None:
        return [board, blocks-bl]
    # if index == int((width*height)/2) and width%2 != 0 and height%2 != 0:
    #     bl = 1
    
    # left border
    if y < 3 and (2 < x < height-3):
        if y == 2:
            if board[index-1] == "-":
                board_block = fill_reverse(index-1, board, width, height)
                board = board_block[0]
                bl += board_block[1]
                if board == None:
                    return [board, blocks-bl]
            if board[index-2] == "-":
                board_block = fill_reverse(index-2, board, width, height)
                board = board_block[0]
                bl += board_block[1]
                if board == None:
                    return [board, blocks-bl]
            return [board, blocks-bl]
        if y == 1:
            if board[index-1] == "-":
                board_block = fill_reverse(index-1, board, width, height)
                board = board_block[0]
                bl += board_block[1]
                if board == None:
                    return [board, blocks-bl]
            return [board, blocks-bl]
    
    # right border
    if y >= width-3 and 2 < x < height-3:
        if y == width-3:
            if board[index+1] == "-":
                board_block = fill_reverse(index+1, board, width, height)
                board = board_block[0]
                bl += board_block[1]
                if board == None:
                    return [board, blocks-bl]
            if board[index+2] == "-":
                board_block = fill_reverse(index+2, board, width, height)
                board = board_block[0]
                bl += board_block[1]
                if board == None:
                    return [board, blocks-bl]
            return [board, blocks-bl]
        if y == width-2:
            if board[index+1] == "-":
                board_block = fill_reverse(index+1, board, width, height)
                board = board_block[0]
                bl += board_block[1]
                if board == None:
                    return [board, blocks-bl]
            return [board, blocks-bl]
        
    # top border
    if x < 3 and 2 < y < width-3:
        if x == 2: 
            if board[index-width] == "-":
                board_block = fill_reverse(index-width, board, width, height)
                board = board_block[0]
                bl += board_block[1]
                if board == None:
                    return [board, blocks-bl]
            if board[index-2*width] == "-":
                board_block = fill_reverse(index-2*width, board, width, height)
                board = board_block[0]
                bl += board_block[1]
                if board == None:
                    return [board, blocks-bl]
            return [board, blocks-bl]
        if x == 1:
            if board[index-width] == "-":
                board_block = fill_reverse(index-width, board, width, height)
                board = board_block[0]
                bl += board_block[1]
                if board == None:
                    return [board, blocks-bl]
            return [board, blocks-bl]
        
    # bottom border
    if x >= height-3 and 2 < y < width-3:
        if x == height-3:
            if board[index+width] == "-":
                board_block = fill_reverse(index+width, board, width, height)
                board = board_block[0]
                bl += board_block[1]
                if board == None:
                    return [board, blocks-bl]
            if board[index+2*width] == "-":
                board_block = fill_reverse(index+2*width, board, width, height)
                board = board_block[0]
                bl += board_block[1]
                if board == None:
                    return [board, blocks-bl]
            return [board, blocks-bl]
        if x == height-2:
            if board[index+width] == "-":
                board_block = fill_reverse(index+width, board, width, height)
                board = board_block[0]
                bl += board_block[1]
                if board == None:
                    return [board, blocks-bl]
            return [board, blocks-bl]
    
    return [board, blocks-bl]


def area_fill(index, board, width, height):
    if (index < 0 or index >= width * height):
        return 0
    row = convert_index_to_2D(index, width, height)[0]
    col = convert_index_to_2D(index, width, height)[1]
    if (row < 0 or row > height):
        return 0
    if (col < 0 or col > width):
        return 0
    if (board[index] == "-" or board[index].isalpha()):
        board[index] = "#"
        # print(display_board(board, height, width))
        count = 1
        if (row > 0 and board[index - width] != "#"):
            count += area_fill(index - width, board, width, height)
        if (row < height - 1 and board[index + width] != "#"):
            count += area_fill(index + width, board, width, height)
        if (col > 0 and board[index - 1] != "#"):
            count += area_fill(index - 1, board, width, height)
        if (col < width-1 and board[index + 1] != "#"):
            count += area_fill(index + 1, board, width, height)
        return count
    else:
        return 0


def board_connected(board, width, height, letters):
    if "-" not in board:
        return True
    else:
        index = random.randrange(0, width * height -1)
        while board[index] != "-":
            index = random.randrange(0, width * height -1)
        blocks = board.count("#")
        
            
        count = area_fill(index, list(board), width, height)
        # return count == width*height - blocks - letters
        return count == width*height - blocks 


def fill_reverse(index, board, width, height):
    blocks = 0
    if check_three(width*height - index - 1, board, width, height) == False or board[width*height - index - 1].isalpha():
        board = None
        # FILL IN BLOCKS IN BETWEEN IF TOO CLOSE 
    else:
        if board[width*height - index - 1] == "-":
            board = board[:index] + "#" + board[index+1:]
            board = board[:width*height - index - 1] + "#" + board[width*height - index:]
            if index == width*height - index - 1:
                blocks += 1
            else:
                blocks += 2
        
        
    return [board, blocks]
        

def initial_fill_reverse(board, width, height, blocks):
    for index in range(0, len(board)):
        if board[index] == "#":
            # if check_three(width*height - index - 1, board, width, height) == False or board[width*height - index - 1].isalpha():
            if board[width*height - index - 1].isalpha():
                None
                # row = convert_index_to_2D(index, width, height)[0]
                # col = convert_index_to_2D(index, width, height)[1]
                # row_reverse = convert_index_to_2D(width*height - index - 1, width, height)[0]
                # col_reverse = convert_index_to_2D(width*height - index - 1, width, height)[1]
                # if row == row_reverse and col_reverse > col:
                #     for i in range(index+1, width*height - index):
                #         board = board[:i] + "#" + board[i+1:]
                #         blocks = blocks-1
                #         print(display_board(board, height, width))
                # if row == row_reverse and col_reverse < col:
                #     for i in range(width*height - index-1, index):
                #         board = board[:i] + "#" + board[i+1:]
                #         blocks = blocks-1
                #         print(display_board(board, height, width))
                # if col == col_reverse and row_reverse > row:
                #     for i in range(row+1, row_reverse+1):
                #         board = board[:convert_2D_to_index(i, col, width, height)] + "#" + board[convert_2D_to_index(i, col, width, height)+1:]
                #         blocks = blocks-1
                #         print(display_board(board, height, width))
                # if col == col_reverse and row_reverse < row:
                #     for i in range(row_reverse, row+1):
                #         board = board[:convert_2D_to_index(i, col, width, height)] + "#" + board[convert_2D_to_index(i, col, width, height)+1:]
                #         blocks = blocks-1
                #         print(display_board(board, height, width))
                      
            else:
                if board[width*height - index - 1] != "#":
                    blocks = blocks-2
                else:
                    blocks = blocks-1
                    
    for index in range(0, len(board)):
        if board[index] == "#":
            if board[width*height - index - 1] != "#":
                board = board[:width*height - index - 1] + "#" + board[width*height - index:]

            
            
    return [board, blocks]
    

# --- BACKTRACKING ----
def heuristic(index, board, width, height):
    row = convert_index_to_2D(index, width, height)[0]
    col = convert_index_to_2D(index, width, height)[1]

    hx = abs((height-row-1) - row)
    hy = abs((width -col-1) - col)

    heuristic =  height * width - (hx + hy)
    return heuristic


def Sort(pos_heuristic):
    pos_heuristic.sort(key = lambda x: x[1], reverse = True )
    return pos_heuristic


def get_avail_pos_constrained(board, width, height, blocks):
    pos = []
    # odd board
    
    count_blocks = 0
    
    for i in range(0, len(board)):
        if board[i] == "-" and check_three(i, board, width, height) == True and check_three(width*height - i - 1, board, width, height) == True:
            new_board = board[:i] + "#" + board[i+1:]
            if check_three(width*height - i - 1, new_board, width, height) == True:
                pos.append([i, heuristic(i, board, width, height)])
        if board[i] == "#":
            count_blocks +=1
    
    if width%2 != 0 and height%2 != 0 and (blocks+count_blocks)%2 == 0:
        i = int((width*height)/2)
        if [i, heuristic(i, board, width, height)] in pos:
            pos.remove([i, heuristic(i, board, width, height)]) 
        
    return Sort(pos)


def backtracking(blocks, board, width, height):
    if board == None:
        return None
    if blocks < 0 or board_connected(board, width, height, count) == False:
        return None
    if blocks == 0:
        return board
    avail_pos = get_avail_pos_constrained(board, width, height, blocks)
    for val in avail_pos:
        # copy to new board
        new_board = board
        # fill in blocks
        new_board_blocks = fill_in(val[0], board, width, height, blocks)
        new_board = new_board_blocks[0]
        
        # print(display_board(new_board, height, width))
        bl1 = new_board_blocks[1]
                    
        result = backtracking(new_board_blocks[1], new_board, width, height)
        if result is not None:
            return result
    return None


#  ------ RUN CODE ------

# GET BOARD PARAMETERS
hw = get_height_width(args[1])
height = int(hw[0])
width = int(hw[1])
blocks = int(args[2])

# SET UP BOARD
board = ""
for i in range(0, height*width):
    board += "-"

# ADD WORDS
for i in range(4, len(args)):
    board = add_word(board, height, width, args[i])

# print(display_board(board, height, width))
print(display_board(board, height, width))

board_blocks = initial_fill_reverse(board, width, height, blocks)
board = board_blocks[0]
blocks = board_blocks[1]
print(display_board(board, height, width))

# PLACE BLOCKS
# count letters
count = 0
for item in board:
    if item.isalpha():
        count += 1
        
# if blocks cover entire board
if blocks == width * height:
    for i in range(0, len(board)):
        if board[i] == "-":
            board = board[:i] + "#" + board[i+1:]
    print(display_board(board, height, width))
    
else: 
    # if odd board, odd blocks
    if width%2 != 0 and height%2 != 0 and blocks%2!=0:
        i = int((width*height)/2)
        board = board[:i] + "#" + board[i+1:]
        blocks = blocks-1
    
    # run backtracking
    board = backtracking(blocks, board, width, height)
    print(display_board(board, height, width))

print(board.count("#"))



# ------ TESTING CODE ------
# board = ""
# for i in range(0, height*width):
#     board += "-"

# board = "------------------------------"
# width = 5
# height = 6
# blocks = 14

# board = "------"
# width = 2
# height = 3
# blocks = 2

# board = "S-----Tt-----wr-----ii-----zp-----te-----id-----d"
# width = 11 
# height = 11
# blocks = 10
# board = "-A----------d---#------s------------------#----------------#-------------------------------------------------------------"
# print(display_board(board, height, width))
# print(initial_fill_reverse(board, width, height, blocks))

# width = 14
# height = 9
# blocks = 32
# board = "---------P-------------r-------------e-------------c#------------e-------------d-------------e-------------n-------#-----t----"
# count = 0
# for item in board:
#     if item.isalpha():
#         count += 1

# print(display_board(board, height, width))
# board = backtracking(blocks, board, width, height)
# print(display_board(board, height, width))

# print(area_fill(13, list(board), width, height))

  # CHECK FILL IN
# index = 23
# blocks = 2
# bb = fill_in(index, board, width, height, blocks)
# print(display_board(bb[0], height, width))
# print(bb[1])

#  CHECK CHECK-THREE
# index = 31
# print(convert_index_to_2D(index, 5, 6))
# board = board[:index] + "#" + board[index+1:]
# print(display_board(board, height, width))
# print(check_three(index, board, width, height))

#  CHECK HEURISTIC
# index = 1
# print(heuristic(index, board, width, height))
# board = board[:index] + "#" + board[index+1:]
# print(display_board(board, height, width))

# print(board_connected(board, width, height, count))

# 1 - FIX HEURISTIC FUNCTION 
# 2 - if in fill in function, the reverse space is a letter, you can't fill it in  
# 3 - check three function, should be != "# in case there is a letter in between, not just a space
# 4 - should be 180 degrees symmetric (put down symmetric blocks first) - fix fill in - fill reverse



# Lynn Tao, 1, 2023
