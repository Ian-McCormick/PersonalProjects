import time
import pygame as pg
import random

SIZE = 200
RES = 1000


def update(org_board):
    board = [[0 for i in range(SIZE)] for j in range(SIZE)]
    #check corners
    numN = org_board[0][1] + org_board[1][1] + org_board[1][0]
    if (numN < 2) or (numN >3):
        board[0][0] = 0
    elif numN == 3:
        board[0][0] = 1
    
    numN = org_board[0][SIZE-2] + org_board[1][SIZE-2] + org_board[1][SIZE-1]
    if (numN < 2) or (numN >3):
        board[0][SIZE-1] = 0
    elif numN == 3:
        board[0][SIZE-1] = 1
    
    numN = org_board[SIZE-2][0] + org_board[SIZE-2][1] + org_board[SIZE-1][1]
    if (numN < 2) or (numN >3):
        board[SIZE-1][0] = 0
    elif numN == 3:
        board[SIZE-1][0] = 1
    
    numN = org_board[SIZE-1][SIZE-2] + org_board[SIZE-2][SIZE-2] + org_board[SIZE-2][SIZE-1]
    if (numN < 2) or (numN >3):
        board[SIZE-1][SIZE-1] = 0
    elif numN == 3:
        board[SIZE-1][SIZE-1] = 1

    #check edges
    for i in range(1,SIZE-1):
        numN = org_board[0][i-1] + org_board[1][i-1] + org_board[1][i] + org_board[1][i+1] + org_board[0][i+1]
        if (numN < 2) or (numN >3):
            board[0][i] = 0
        elif numN == 3:
            board[0][i] = 1

        numN = org_board[SIZE-1][i-1] + org_board[SIZE-2][i-1] + org_board[SIZE-2][i] + org_board[SIZE-2][i+1] + org_board[SIZE-1][i+1]
        if (numN < 2) or (numN >3):
            board[SIZE-1][i] = 0
        elif numN == 3:
            board[SIZE-1][i] = 1
        
        numN = org_board[i-1][0] + org_board[i-1][1] + org_board[i][1] + org_board[i+1][1] + org_board[i+1][0]
        if (numN < 2) or (numN >3):
            board[i][0] = 0
        elif numN == 3:
            board[i][0] = 1

        numN = org_board[SIZE-1][i+1] + org_board[SIZE-2][i-1] + org_board[SIZE-2][i] + org_board[SIZE-2][i+1] + org_board[SIZE-1][i+1]
        if (numN < 2) or (numN >3):
            board[SIZE-1][i] = 0
        elif numN == 3:
            board[SIZE-1][i] = 1
    
    #check center
    for row in range(1, SIZE-1):
        for col in range (1, SIZE-1):
            numN = org_board[row-1][col-1] + org_board[row-1][col] + org_board[row-1][col+1] + org_board[row][col-1] + org_board[row][col+1] + org_board[row+1][col-1] + org_board[row+1][col] + org_board[row+1][col+1]
            if (numN < 2) or (numN >3):
                board[row][col] = 0
            elif numN == 3:
                board[row][col] = 1
            else:
                board[row][col] = org_board[row][col]

    return board

def print_board(board):
    for row in range(SIZE):
        for col in range (SIZE):
            print(board[row][col], end = " ")
        print()
    print("-" * 2 * SIZE)

def draw_board(board, screen, sc_size):
    for row in range(SIZE):
        for col in range(SIZE):
            cell = board[row][col]
            color = (255*cell, 255*cell, 255*cell)
            pg.draw.rect(screen, color, [sc_size*row, sc_size*col, sc_size, sc_size])
    pg.display.update()

def rand_board():
    board = [[0 for i in range(SIZE)] for j in range(SIZE)]
    for row in range(SIZE):
        for col in range(SIZE):
            board[row][col] = random.randint(0, 1)
    return board



def main():
    pg.init()
    sc_size = RES/SIZE
    screen = pg.display.set_mode((RES, RES))
    board = rand_board()
    draw_board(board, screen, sc_size)
    board = update(board)
    for i in range(500):
        board = update(board)
        draw_board(board, screen, sc_size)
        #time.sleep(.1)
    

main()
