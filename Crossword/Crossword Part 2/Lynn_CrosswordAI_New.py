import sys; args = sys.argv[1:]
myLines = open(args[0], 'r').read().splitlines()
args = args[1:]
import random

# twentyk.txt 4x4 0 
# twentyk.txt  ['5x5', '0', 'H0x0float']
# twentyk.txt  ['5x5', '0', 'V2x2a']
# twentyk.txt  ['4x4', '2']
# twentyk.txt  ['5x5', '2', 'h2x3N']
# twentyk.txt  ['5x5', '4', 'v2x3O']
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
            if board[index-width].isalpha() or board[index-2*width].isalpha():
                board = None
                bl = 0
                return [board, blocks-bl]
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
            if board[index-width].isalpha():
                board = None
                bl = 0
                return [board, blocks-bl]
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
            if board[index+width].isalpha() or board[index+2*width].isalpha():
                board = None
                bl = 0
                return [board, blocks-bl]
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
            if board[index+width].isalpha():
                board = None
                bl = 0
                return [board, blocks-bl]
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


def board_connected(board, width, height):
    if "-" not in board:
        return True
    else:
        index = random.randrange(0, width * height -1)
        while board[index] != "-":
            index = random.randrange(0, width * height -1)
        blocks = board.count("#")
        
            
        count = area_fill(index, list(board), width, height)
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


def check_three_index(index, board, width, height):
    x = convert_index_to_2D(index, width, height)[0]
    y = convert_index_to_2D(index, width, height)[1]

    # 1/2 SPACES BETWEEN
    # check top
    if x >= 3:
        if board[convert_2D_to_index(x-3, y, width, height)] == "#":
            if board[convert_2D_to_index(x-1, y, width, height)] != "#" or board[convert_2D_to_index(x-2, y, width, height)] != "#":
                return convert_2D_to_index(x-3, y, width, height)
    # check right
    if y < width - 3:
        if board[convert_2D_to_index(x, y+3, width, height)] == "#":
            if board[convert_2D_to_index(x, y+1, width, height)] != "#" or board[convert_2D_to_index(x, y+2, width, height)] != "#":
                return convert_2D_to_index(x, y+3, width, height)
    # check bottom
    if x < height - 3:
        if board[convert_2D_to_index(x+3, y, width, height)] == "#":
            if board[convert_2D_to_index(x+1, y, width, height)] != "#" or board[convert_2D_to_index(x+2, y, width, height)] != "#":
                return convert_2D_to_index(x+3, y, width, height)
    # check left
    if y >= 3:
        if board[convert_2D_to_index(x, y-3, width, height)] == "#":
            if board[convert_2D_to_index(x, y-1, width, height)] != "#" or board[convert_2D_to_index(x, y-2, width, height)] != "#":
                return convert_2D_to_index(x, y-3, width, height)
    
    # 1 SPACE BETWEEN
    # check top
    if x >= 2:
        if board[convert_2D_to_index(x-2, y, width, height)] == "#":
            if board[convert_2D_to_index(x-1, y, width, height)] != "#":
                return convert_2D_to_index(x-2, y, width, height)
    # check right
    if y < width - 2:
        if board[convert_2D_to_index(x, y+2, width, height)] == "#":
            if board[convert_2D_to_index(x, y+1, width, height)] != "#":
                return convert_2D_to_index(x, y+2, width, height)
    # check bottom
    if x < height - 2:
        if board[convert_2D_to_index(x+2, y, width, height)] == "#":
            if board[convert_2D_to_index(x+1, y, width, height)] != "#":
                return convert_2D_to_index(x+2, y, width, height)
    # check left
    if y >= 2:
        if board[convert_2D_to_index(x, y-2, width, height)] == "#":
            if board[convert_2D_to_index(x, y-1, width, height)] != "#":
                return convert_2D_to_index(x, y-2, width, height) 
        
    return True


def fill_initial_threes(board, width, height, blocks):
    pos_blocks = []
    for i in range(0, len(board)): 
        if board[i] == "#":
           pos_blocks.append(i) 
           
    for index in pos_blocks:   
        row = convert_index_to_2D(index, width, height)[0]
        col = convert_index_to_2D(index, width, height)[1]
        if row < 3:
            for i in range(0, row):
                if board[convert_2D_to_index(i, col, width, height)] != "#":
                    board = board[:convert_2D_to_index(i, col, width, height)] + "#" + board[convert_2D_to_index(i, col, width, height)+1:]
                    blocks = blocks-1
        if col <3:
            for i in range(0, col):
                if board[convert_2D_to_index(row, i, width, height)] != "#":
                    board = board[:convert_2D_to_index(row, i, width, height)] + "#" + board[convert_2D_to_index(row, i, width, height)+1:]
                    blocks = blocks-1
        
        if row>=height-3:
            for i in range(row, height):
                if board[convert_2D_to_index(i, col, width, height)] != "#":
                    board = board[:convert_2D_to_index(i, col, width, height)] + "#" + board[convert_2D_to_index(i, col, width, height)+1:]
                    blocks = blocks-1
        
        if col >= width-3:
            for i in range(col, width):
                if board[convert_2D_to_index(row, i, width, height)] != "#":
                    board = board[:convert_2D_to_index(row, i, width, height)] + "#" + board[convert_2D_to_index(row, i, width, height)+1:]
                    blocks = blocks-1
        
        if check_three(index, board, width, height) == False:
            index_three = check_three_index(index, board, width, height)
            if index_three!= True:
                row_reverse = convert_index_to_2D(index_three, width, height)[0]
                col_reverse = convert_index_to_2D(index_three, width, height)[1]
                if row == row_reverse and col_reverse > col:
                    for i in range(index+1, index_three):
                        if board[i] != "#":
                            board = board[:i] + "#" + board[i+1:]
                            blocks = blocks-1
                if row == row_reverse and col_reverse < col:
                    for i in range(index_three, index):
                        if board[i] != "#":
                            board = board[:i] + "#" + board[i+1:]
                            blocks = blocks-1
                if col == col_reverse and row_reverse > row:
                    for i in range(row+1, row_reverse+1):
                        if board[convert_2D_to_index(i, col, width, height)] != "#":
                            board = board[:convert_2D_to_index(i, col, width, height)] + "#" + board[convert_2D_to_index(i, col, width, height)+1:]
                            blocks = blocks-1
                if col == col_reverse and row_reverse < row:
                    for i in range(row_reverse, row+1):
                        if board[convert_2D_to_index(i, col, width, height)] != "#":
                            board = board[:convert_2D_to_index(i, col, width, height)] + "#" + board[convert_2D_to_index(i, col, width, height)+1:]
                            blocks = blocks-1                      
    
    
    if board_connected(board, width, height) == False:
        pos_blocks2 = []
        for i in range(0, len(board)): 
            if board[i] == "#":
                pos_blocks2.append(i) 

        for index in pos_blocks2:
            if index+1 < width*height:
                if board[index+1] == "-":
                    count = area_fill(index+1, list(board), width, height)
                    if count <= blocks:
                        board = initial_area_fill(index+1, list(board), width, height)[0]
                        blocks = blocks-count
            if index-1 >= 0:
                if board[index-1] == "-":
                    count = area_fill(index-1, list(board), width, height)
                    if count <= blocks:
                        board = initial_area_fill(index-1, list(board), width, height)[0]
                        blocks = blocks-count
            if index+width < width*height:
                if board[index+width] == "-":
                    count = area_fill(index+width, list(board), width, height)
                    if count <= blocks:
                        board = initial_area_fill(index+width, list(board), width, height)[0]
                        blocks = blocks-count
            if index-width >= 0:
                if board[index-width] == "-":
                    count = area_fill(index-width, list(board), width, height)
                    if count <= blocks:
                        board = initial_area_fill(index-width, list(board), width, height)[0]
                        blocks = blocks-count

    return [board, blocks]
    


def initial_area_fill(index, board, width, height):
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
        return ["".join(board), count]
    else:
        return 0


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
    if blocks < 0 or board_connected(board, width, height) == False:
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
        result = backtracking(new_board_blocks[1], new_board, width, height)
        if result is not None:
            return result
    return None


# PART 2 CODE

def contains_word(board, width, height, word_place):
    words = []
    for i in range(0, height):
        word = ""
        for j in range(0, width):
            word += board[i*width+j]
        if "-" not in word:
            words.append(word)
    for i in range(0, width):
        word = ""
        for j in range(0, height):
            word += board[j*width+i]
        if "-" not in word:
            words.append(word)
    return word_place in words
    
   

def horizontal_possible_words(board, dictionary, index, width, height):
    row = convert_index_to_2D(index, width, height)[0]
    col = convert_index_to_2D(index, width, height)[1]
    length = width - col
    if board[index] == "-":
        if len(dictionary[length]) == 0:
            return []
        else:
            return dictionary[length]
            
    else:
        begin = ""
        while col < width:
            if board[convert_2D_to_index(row, col, width, height)].isalpha():
                begin += board[convert_2D_to_index(row, col, width, height)] 
            col += 1
        
        avail_words = []
        for item in dictionary[length]:
            if item.startswith(begin) and contains_word(board, width, height, item) == False:
                avail_words.append(item)
        
        if len(avail_words) == 0:
            return []
            
        else:
            return avail_words


def add_horizontal_word(board, word, index, width, height):
    # row = convert_index_to_2D(index, width, height)[0]
    # col = convert_index_to_2D(index, width, height)[1]

    if contains_word(board, width, height, word) == False:
        for i in range(0, len(word)):
            board = board[:index] + word[i] + board[index+1:]
            index += 1 
        
    return board


def vertical_possible_words(board, dictionary, index, width, height):
    row = convert_index_to_2D(index, width, height)[0]
    col = convert_index_to_2D(index, width, height)[1]
    length = height - row
    if board[index] == "-":
        if len(dictionary[length]) == 0:
            return []
        else:
            return dictionary[length]

    else:
        begin = ""
        while row < height:
            if board[convert_2D_to_index(row, col, width, height)].isalpha():
                begin += board[convert_2D_to_index(row, col, width, height)] 
            row += 1
        
        avail_words = []
        for item in dictionary[length]:
            if item.startswith(begin) and contains_word(board, width, height, item) == False:
                avail_words.append(item)
        
        if len(avail_words) == 0:
            return []
        else:
            return avail_words
        
        
def add_vertical_word(board, word, index, width, height):
    
    if contains_word(board, width, height, word) == False:
        for i in range(0, len(word)):
            board = board[:index] + word[i] + board[index+1:]
            index += width
        
    return board
    

def Sort_min(pos_heuristic):
    pos_heuristic.sort(key = lambda x: x[1])
    return pos_heuristic


def word_get_avail_pos(board, width, height):
    # fix, prioritize words with least blank spaces left
    pos_vertical = list()
    pos_horizontal = list()
    for index in range(0, width):
        blanks = 0
        flag = False
        for i in range(0, height):
            if board[convert_2D_to_index(i, index, width, height)] == "-":
                flag = True
                blanks += 1
        if flag == True:
            pos_vertical.append([index, blanks])
        
    for index in range(0, height):
        blanks = 0
        flag = False
        for i in range(0, width):
            if board[convert_2D_to_index(index, i, width, height)] == "-":
                flag = True
                blanks += 1
        if flag == True:
            pos_horizontal.append([index*width, blanks])
         
    pos = pos_horizontal + pos_vertical
    pos = Sort_min(pos)
    
    return pos
    

def check_board(dict_copy, board, width, height):
    words = []
    for i in range(0, height):
        word = ""
        for j in range(0, width):
            word += board[i*width+j]
        flag = False
        for i in word:
            if i.isalpha():
                flag = True
        if flag == True:
            words.append(word)
    for i in range(0, width):
        word = ""
        for j in range(0, height):
            word += board[j*width+i]
        flag = False
        for i in word:
            if i.isalpha():
                flag = True
        if flag == True:
            words.append(word)
    for item in words:
        if "-" not in item:
            if item not in dict_copy[len(item)]:
                return False
        else:
            begin = item[:item.index("-")]
            flag = False
            for option in dict_copy[len(item)]:
                if option.startswith(begin):
                    flag = True
            if flag == False:
                return False
    return True
        

    
def empty_right(board, index, width, height):
    row = convert_index_to_2D(index, width, height)[0]
    col = convert_index_to_2D(index, width, height)[1]
    for i in range(col+1, width):
        if board[convert_2D_to_index(row, i, width, height)] == "-":
            return True
    return False


def empty_down(board, index, width, height):
    row = convert_index_to_2D(index, width, height)[0]
    col = convert_index_to_2D(index, width, height)[1]
    for i in range(row+1, height):
        if board[convert_2D_to_index(i, col, width, height)] == "-":
            return True
    return False
    

# sys.setrecursionlimit(10**6)
def word_backtracking(dictionary, copy, board, width, height):
    if board == None:
        return None
    if check_board(copy, board, width, height) == False:
        return None
    if "-" not in board:
        return board

    avail_pos = word_get_avail_pos(board, width, height)
    for item in avail_pos:
        val = item[0]
        # copy to new board
        new_board = board
        
        # fill in a word
        if empty_right(board, val, width, height) and (val > width-1 or val == 0):
            h_words = horizontal_possible_words(board, dictionary, val, width, height)
            for word_choice in h_words:
                new_board  = add_horizontal_word(board, word_choice, val, width, height)
                # if new_board != None:
                #     print(display_board(new_board, height, width))
                result = word_backtracking(dictionary, copy, new_board, width, height)
                if result is not None:
                    return result
        elif empty_down(board, val, width, height) and (0 <= val < width):
            v_words = vertical_possible_words(board, dictionary, val, width, height)
            for word_choice in v_words:
                new_board = add_vertical_word(board, word_choice, val, width, height)
                # if new_board != None:
                #     print(display_board(new_board, height, width))
                result = word_backtracking(dictionary, copy, new_board, width, height)
                if result is not None:
                    return result
        else:
            None
        
        result = word_backtracking(dictionary, copy, new_board, width, height)
        if result is not None:
            return result


        
    return None
    
    
#  ------ RUN CODE ------

# GET BOARD PARAMETERS
hw = get_height_width(args[0])
height = int(hw[0])
width = int(hw[1])
blocks = int(args[1])

# SET UP BOARD
board = ""
for i in range(0, height*width):
    board += "-"

# ADD WORDS
for i in range(2, len(args)):
    board = add_word(board, height, width, args[i])

# place reverse of initial blocks
board_blocks = initial_fill_reverse(board, width, height, blocks)
board = board_blocks[0]
blocks = board_blocks[1]

# fill in initial check threes
# board_blocks = fill_initial_threes(board, width, height, blocks)
# board = board_blocks[0]
# blocks = board_blocks[1]

if board_connected(board, width, height) == False:
    board = None
    print(board)
else:
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
        # print(board)
        # print(display_board(board, height, width))
    
    # print(board.count("#"))

# PART 2
dict_word = {}
dict_copy = {}

for item in myLines:
    flag = True
    for i in range(0, len(item)):
        if not item[i].isalpha():
            flag = False
    if flag == True and len(item) > 2:
        if len(item) in dict_word.keys():
            dict_word[len(item)].append(item)
            dict_copy[len(item)].append(item)
        else:
            dict_word[len(item)] = [item]
            dict_copy[len(item)] = [item]
      
 
# print(dict_word)
# dict_word[3].remove("odd")
# print("caa" in dict_copy[3])
# board = "sourlensa-d-m-o-"
# print(display_board(board, height, width))
# print(check_board(dict_copy, board, width, height))
# print(contains_word(board, width, height, "rs--"))

# print(add_horizontal_word(board, dict_word, 0, width, height))
# r p g 
# m o p 
# s d l 

# c d p 
# a d p 
# a s c 

# s o u r 
# l e n s 
# a - d - 
# m - o - 

board = word_backtracking(dict_word, dict_copy, board, width, height)
if board!= None:
    print(board)
else:
    print("None")



# Lynn Tao, 1, 2023

