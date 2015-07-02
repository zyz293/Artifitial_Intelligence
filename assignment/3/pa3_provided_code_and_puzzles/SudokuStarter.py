#!/usr/bin/env python
import struct, string, math
from copy import *

class SudokuBoard:
    """This will be the sudoku board game object your player will manipulate."""
  
    def __init__(self, size, board):
      """the constructor for the SudokuBoard"""
      self.BoardSize = size #the size of the board
      self.CurrentGameBoard= board #the current state of the game board

    def set_value(self, row, col, value):
        """This function will create a new sudoku board object with the input
        value placed on the GameBoard row and col are both zero-indexed"""

        #add the value to the appropriate position on the board
        self.CurrentGameBoard[row][col]=value
        #return a new board of the same size with the value added
        return SudokuBoard(self.BoardSize, self.CurrentGameBoard)
                                                                  
                                                                  
    def print_board(self):
        """Prints the current game board. Leaves unassigned spots blank."""
        div = int(math.sqrt(self.BoardSize))
        dash = ""
        space = ""
        line = "+"
        sep = "|"
        for i in range(div):
            dash += "----"
            space += "    "
        for i in range(div):
            line += dash + "+"
            sep += space + "|"
        for i in range(-1, self.BoardSize):
            if i != -1:
                print "|",
                for j in range(self.BoardSize):
                    if self.CurrentGameBoard[i][j] > 9:
                        print self.CurrentGameBoard[i][j],
                    elif self.CurrentGameBoard[i][j] > 0:
                        print "", self.CurrentGameBoard[i][j],
                    else:
                        print "  ",
                    if (j+1 != self.BoardSize):
                        if ((j+1)//div != j/div):
                            print "|",
                        else:
                            print "",
                    else:
                        print "|"
            if ((i+1)//div != i/div):
                print line
            else:
                print sep

def parse_file(filename):
    """Parses a sudoku text file into a BoardSize, and a 2d array which holds
    the value of each cell. Array elements holding a 0 are considered to be
    empty."""

    f = open(filename, 'r')
    BoardSize = int( f.readline())
    NumVals = int(f.readline())

    #initialize a blank board
    board= [ [ 0 for i in range(BoardSize) ] for j in range(BoardSize) ]

    #populate the board with initial values
    for i in range(NumVals):
        line = f.readline()
        chars = line.split()
        row = int(chars[0])
        col = int(chars[1])
        val = int(chars[2])
        board[row-1][col-1]=val
    
    return board
    
def is_complete(sudoku_board):
    """Takes in a sudoku board and tests to see if it has been filled in
    correctly."""
    BoardArray = sudoku_board.CurrentGameBoard
    size = len(BoardArray)
    subsquare = int(math.sqrt(size))

    #check each cell on the board for a 0, or if the value of the cell
    #is present elsewhere within the same row, column, or square
    for row in range(size):
        for col in range(size):
            if BoardArray[row][col]==0:
                return False
            for i in range(size):
                if ((BoardArray[row][i] == BoardArray[row][col]) and i != col):
                    return False
                if ((BoardArray[i][col] == BoardArray[row][col]) and i != row):
                    return False
            #determine which square the cell is in
            SquareRow = row // subsquare
            SquareCol = col // subsquare
            for i in range(subsquare):
                for j in range(subsquare):
                    if((BoardArray[SquareRow*subsquare+i][SquareCol*subsquare+j]
                            == BoardArray[row][col])
                        and (SquareRow*subsquare + i != row)
                        and (SquareCol*subsquare + j != col)):
                            return False
    return True

def init_board(file_name):
    """Creates a SudokuBoard object initialized with values from a text file"""
    board = parse_file(file_name)
    return SudokuBoard(len(board), board)

def select_variable(initial_board):
    for i in range(initial_board.BoardSize):
        for j in range(initial_board.BoardSize):
            if initial_board.CurrentGameBoard[i][j] == 0:
                return i, j

def solve(initial_board, forward_checking, MRV, MCV, LCV):
    """Takes an initial SudokuBoard and solves it using back tracking, and zero
    or more of the heuristics and constraint propagation methods (determined by
    arguments). Returns the resulting board solution. """
    legal_value = deepcopy(initial_board.CurrentGameBoard)
    for i in range(len(legal_value)):
        for j in range(len(legal_value)):
            if legal_value[i][j] == 0:
                legal_value[i][j] = range(1, len(legal_value) + 1)
    if is_complete(initial_board):
        return initial_board
    candidate = []
    legal_value_candidate = []
    if MRV:
        [row, col] = MRV(legal_value)
    elif MCV:
        [row, col] = MRV(initial_board)
    else:
        row, col = select_variable(initial_board)
    if LCV:
            value_order = LCV(legal_value, row, col)
            while len(value_order) != 0:
                k = value_order.pop()
                nb = deepcopy(initial_board.CurrentGameBoard)
                nb[row][col] = k
                candidate += [nb]
                legal_value2 = deepcopy(legal_value)
                legal_value2[row][col] = k
                legal_value_candidate += [legal_value2]
    else:
        for k in legal_value[row][col]:
            assigned_value = []
            for i in legal_value[row]:
                if type(i) == int:
                    assigned_value.append(i)
            for y in range(len(legal_value)):
                if type(legal_value[y][col]) == int:
                    assigned_value.append(legal_value[y][col])
            a = row // int(math.sqrt(len(legal_value)))
            b = col // int(math.sqrt(len(legal_value)))
            for m in range(a * int(math.sqrt(len(legal_value))),
                           (1+a) * int(math.sqrt(len(legal_value)))):
                for n in range(b * int(math.sqrt(len(legal_value))),
                               (1+b) * int(math.sqrt(len(legal_value)))):
                    if type(legal_value[m][n]) == int:
                        assigned_value.append(legal_value[m][n])
            if k not in assigned_value:
                nb = deepcopy(initial_board.CurrentGameBoard)
                nb[row][col] = k
                candidate += [nb]
                legal_value2 = deepcopy(legal_value)
                legal_value2[row][col] = k
                legal_value_candidate += [legal_value2]
    if forward_checking:
        return Forward_checking(forward_checking, row, col, candidate, legal_value_candidate)
    else:
        return solve2(forward_checking, MRV, MCV, LCV, candidate, legal_value_candidate)

def solve2(forward_checking, MRV, MCV, LCV, candidate, legal_value_candidate):
    temp = candidate.pop()
    value_temp = legal_value_candidate.pop()
    initial_board = SudokuBoard(len(temp), temp)
    if is_complete(initial_board):
        return initial_board
    if MRV:
        [row, col] = MRV(value_temp)
    elif MCV:
        row, col = MCV(initial_board)
    else:
        row, col = select_variable(initial_board)
    if LCV:
            value_order = LCV(value_temp, row, col)
            while len(value_order) != 0:
                k = value_order.pop()
                nb = deepcopy(initial_board.CurrentGameBoard)
                nb[row][col] = k
                candidate += [nb]
                nv = deepcopy(value_temp)
                nv[row][col] = k
                legal_value_candidate += [nv]
    else:
        for k in value_temp[row][col]:
            assigned_value = []
            for i in value_temp[row]:
                if type(i) == int:
                    assigned_value.append(i)
            for y in range(len(value_temp)):
                if type(value_temp[y][col]) == int:
                    assigned_value.append(value_temp[y][col])
            a = row // int(math.sqrt(len(value_temp)))
            b = col // int(math.sqrt(len(value_temp)))
            for m in range(a * int(math.sqrt(len(value_temp))),
                           (1+a) * int(math.sqrt(len(value_temp)))):
                for n in range(b * int(math.sqrt(len(value_temp))),
                               (1+b) * int(math.sqrt(len(value_temp)))):
                    if type(value_temp[m][n]) == int:
                        assigned_value.append(value_temp[m][n])
            if k not in assigned_value:
                nb = deepcopy(initial_board.CurrentGameBoard)
                nb[row][col] = k
                candidate += [nb]
                nv = deepcopy(value_temp)
                nv[row][col] = k
                legal_value_candidate += [nv]
    if forward_checking:
        return Forward_checking(forward_checking, row, col, candidate, legal_value_candidate)
    else:
        return solve2(forward_checking, MRV, MCV, LCV, candidate, legal_value_candidate)

def Forward_checking(forward_checking, row, col, candidate, legal_value_candidate):
    temp = candidate[-1]
    value_temp = legal_value_candidate[-1]
    initial_board = SudokuBoard(len(temp), temp)
    value = value_temp[row][col]
    for k in range(initial_board.BoardSize):
        if type(value_temp[row][k]) != int:
            if value in value_temp[row][k]:
                value_temp[row][k].remove(value)
        if type(value_temp[k][col]) != int:
            if value in value_temp[k][col]:
                value_temp[k][col].remove(value)
    a = row // int(math.sqrt(initial_board.BoardSize))
    b = col // int(math.sqrt(initial_board.BoardSize))
    for m in range(a * int(math.sqrt(initial_board.BoardSize)),
                   (1+a) * int(math.sqrt(initial_board.BoardSize))):
        for n in range(b * int(math.sqrt(initial_board.BoardSize)),
                       (1+b) * int(math.sqrt(initial_board.BoardSize))):
            if type(value_temp[m][n]) != int:
                if value in value_temp[m][n]:
                    value_temp[m][n].remove(value)
    return solve2(forward_checking, MRV, MCV, LCV, candidate, legal_value_candidate)

def MRV(legal_value):
    size = len(legal_value)
    pos = [0, 0]
    s = 0
    for i in range(size):
        for j in range(size):
            if type(legal_value[i][j]) != int:
                value = []
                for k in legal_value[i]:
                    if type(k) == int:
                        if k not in value:
                            value.append(k)
                for y in range(size):
                    if type(legal_value[y][j]) == int:
                        if y not in value:
                            value.append(legal_value[y][j])
                a = i // int(math.sqrt(size))
                b = j // int(math.sqrt(size))
                for m in range(a * int(math.sqrt(size)),
                               (1+a) * int(math.sqrt(size))):
                    for n in range(b * int(math.sqrt(size)),
                                   (1+b) * int(math.sqrt(size))):
                        if type(legal_value[m][n]) == int:
                            if legal_value[m][n] not in value:
                                value.append(legal_value[m][n])
                counter = len(value)
                if counter > s:
                    s = counter
                    pos = [i, j]
    return pos

def MCV(initial_board):
    pos = []
    s = initial_board.BoardSize * 3 - 3
    for i in range(initial_board.BoardSize):
        for j in range(initial_board.BoardSize):
            if initial_board.BoardSize[i][j] == 0:
                counter = 0
                for x in initial_board.CurrentGameBoard[i]:
                    if x == 0:
                        counter += 1
                for y in range(len(initial_board.CurrentGameBoard)):
                    if initial_board.CurrentGameBoard[y][j] == 0:
                        counter += 1
                a = i // int(math.sqrt(initial_board.BoardSize))
                b = j // int(math.sqrt(initial_board.BoardSize))
                for m in range(a * int(math.sqrt(initial_board.BoardSize)),
                               (1+a) * int(math.sqrt(initial_board.BoardSize))):
                    for n in range(b * int(math.sqrt(initial_board.BoardSize)),
                                   (1+b) * int(math.sqrt(initial_board.BoardSize))):
                        for z in initial_board.CurrentGameBoard[m][n]:
                            if z == 0:
                                counter += 1
                counter += -3
                if counter < s:
                    s = counter
                    pos = [i, j]
    return pos

def LCV(legal_value, row, col):
    value_order = {}
    order = []
    for k in legal_value[row][col]:
        counter = 0
        for j in range(len(legal_value)):
            if type(legal_value[row][j]) != int:
                if k in legal_value[row][j]:
                    counter += 1
            if type(legal_value[j][col]) != int:
                if k in legal_value[j][col]:
                    counter += 1
            a = row // int(math.sqrt(len(legal_value)))
            b = col // int(math.sqrt(len(legal_value)))
            for m in range(a * int(math.sqrt(len(legal_value))),
                           (1+a) * int(math.sqrt(len(legal_value)))):
                for n in range(b * int(math.sqrt(len(legal_value))),
                               (1+b) * int(math.sqrt(len(legal_value)))):
                    if type(legal_value[m][n]) != int:
                        if k in legal_value[m][n]:
                            counter += 1
        value_order[counter] = k
    for i in value_order:
        order.append(value_order[i])
    return order