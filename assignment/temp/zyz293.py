#!/usr/bin/env python
import struct, string, math

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
    #print board
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

def solve(initial_board, forward_checking, MRV, MCV, LCV):
    """Takes an initial SudokuBoard and solves it using back tracking, and zero
    or more of the heuristics and constraint propagation methods (determined by
    arguments). Returns the resulting board solution. """
    if is_complete(initial_board):
        return initial_board
    print initial_board.CurrentGameBoard
    #print initial_board.BoardSize
    for i in range(initial_board.BoardSize):
        for j in range(initial_board.BoardSize):
            if initial_board.CurrentGameBoard[i][j] == 0:
                #X = initial_board.CurrentGameBoard[i][j]
                for k in range(1, initial_board.BoardSize + 1):
                    for x in initial_board.CurrentGameBoard[i][:]:
                        if k != x:
                            for y in initial_board.CurrentGameBoard[:][j]:
                                if k != y:
                                    a = i // int(math.sqrt(initial_board.BoardSize))
                                    b = j // int(math.sqrt(initial_board.BoardSize))
                                    for m in range(a * int(math.sqrt(initial_board.BoardSize)),
                                                   (1+a) * int(math.sqrt(initial_board.BoardSize))):
                                        for n in range(b * int(math.sqrt(initial_board.BoardSize)),
                                                       (1+b) * int(math.sqrt(initial_board.BoardSize))):
                                            if (i != m) and (j != n):
                                                if k != initial_board.CurrentGameBoard[m][n]:
                                                    #board = SudokuBoard(len(initial_board), initial_board)
                                                    result = initial_board.set_value(i, j, k)
                                                    #print result
                                                    return solve(result, forward_checking, MRV, MCV, LCV)
    return False

def forward_checking(initial_board, row, col):
    value = initial_board.CurrentGameBoard[row][col]
    for i in range(initial_board.BoardSize):
        for j in range(initial_board.BoardSize):
            for x in initial_board.CurrentGameBoard[row][j]:
                x.remove(value)
            for y in initial_board.CurrentGameBoard[i][col]:
                y.remove(value)
    a = row // int(math.sqrt(initial_board.BoardSize))
    b = col // int(math.sqrt(initial_board.BoardSize))
    for m in range(a * int(math.sqrt(initial_board.BoardSize)),
                   (1+a) * int(math.sqrt(initial_board.BoardSize))):
        for n in range(b * int(math.sqrt(initial_board.BoardSize)),
                       (1+b) * int(math.sqrt(initial_board.BoardSize))):
            for z in initial_board.CurrentGameBoard[m][n]:
                z.remove(value)
    return initial_board

def MRV(initial_board):
    value = []
    s = 9
    legal_value = range(1, initial_board.BoardSize + 1)
    for i in range(initial_board.BoardSize):
        for j in range(initial_board.BoardSize):
            if initial_board.BoardSize[i][j] == 0:
                for x in initial_board.CurrentGameBoard[i][:]:
                    if x not in value:
                        value += [x]
                for y in initial_board.CurrentGameBoard[:][j]:
                    if y not in value:
                        value += [y]
                a = i // int(math.sqrt(initial_board.BoardSize))
                b = j // int(math.sqrt(initial_board.BoardSize))
                for m in range(a * int(math.sqrt(initial_board.BoardSize)),
                               (1+a) * int(math.sqrt(initial_board.BoardSize))):
                    for n in range(b * int(math.sqrt(initial_board.BoardSize)),
                                   (1+b) * int(math.sqrt(initial_board.BoardSize))):
                        if (i != m) and (j != n):
                            for z in initial_board.CurrentGameBoard[m][n]:
                                if z not in value:
                                    value += [z]
                counter = initial_board.BoardSize + 1 - len(value)
                if counter < s:
                    s = counter
                    row = i
                    col = j
                    for k in value:
                        if k in legal_value:
                            legal_value.remove(k)
    return row, col, legal_value

def MCV(initial_board):
    counter = 0
    s = 0
    for i in range(initial_board.BoardSize):
        for j in range(initial_board.BoardSize):
            if initial_board.BoardSize[i][j] == 0:
                for x in initial_board.CurrentGameBoard[i][:]:
                    if x != 0:
                        counter += 1
                for y in initial_board.CurrentGameBoard[:][j]:
                    if y != 0:
                        counter += 1
                a = i // int(math.sqrt(initial_board.BoardSize))
                b = j // int(math.sqrt(initial_board.BoardSize))
                for m in range(a * int(math.sqrt(initial_board.BoardSize)),
                               (1+a) * int(math.sqrt(initial_board.BoardSize))):
                    for n in range(b * int(math.sqrt(initial_board.BoardSize)),
                                   (1+b) * int(math.sqrt(initial_board.BoardSize))):
                        for z in initial_board.CurrentGameBoard[m][n]:
                            if z != 0:
                                counter += 1
                if counter > s:
                    s = counter
                    row = i
                    col = j
    return row, col

def LCV(initial_board, row, col):
    counter = 0
    s = (initial_board.BoardSize-1) * 2 - (int(math.sqrt(initial_board.BoardSize))-1) ^ 2
    for i in initial_board.CurrentGameBoard[row][col]:
        for j in range(initial_board.BoardSize):
            if j != col:
                for x in initial_board.CurrentGameBoard[row][j]:
                    if i == x:
                        counter += 1
        for l in range(initial_board.BoardSize):
            if l != row:
                for y in initial_board.CurrentGameBoard[l][col]:
                    if i == y:
                        counter += 1
    a = row // int(math.sqrt(initial_board.BoardSize))
    b = col // int(math.sqrt(initial_board.BoardSize))
    for m in range(a * int(math.sqrt(initial_board.BoardSize)),
                   (1+a) * int(math.sqrt(initial_board.BoardSize))):
        for n in range(b * int(math.sqrt(initial_board.BoardSize)),
                       (1+b) * int(math.sqrt(initial_board.BoardSize))):
            if (m != row) and (n != col):
                for z in initial_board.CurrentGameBoard[m][n]:
                    if i == z:
                        counter += 1
    if counter < s:
        s = counter
        value = i
    return value