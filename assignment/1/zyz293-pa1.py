# name: Zijiang Yang
# netID: zyz293
def twoToTheN(n):
    """
    Calculate 2^n in log(n) time.
    :param n: the power of 2
    :return: return the result of 2^n
    """
    if n == 1: # for the case when n is 1
        return 2
    elif n == 0: # for the case when n is 0
        return 1
    elif n % 2 == 0: # for the case when n is even
        n = n / 2
        return twoToTheN(n) ** 2
    elif n % 2 ==1: # for the case when n is odd
        n = (n-1)/2
        return 2 * twoToTheN(n) ** 2

def mean(L):
    """
    the average of a list of numbers
    :param L: the list of numbers
    :return: return the average of L
    """
    a = 0
    for i in L:
        a += i   # calculate the sum of the list L
    return (a/float(len(L))) # calculate the average of the list L

def median(L):
    """
    the median of a list of numbers
    :param L: a list of numbers
    :return: return the median of L
    """
    L.sort()  # rearrange elements of L from smallest to biggest
    if len(L)%2 == 1:  # the median for a list of odd number of elements
        return L[(len(L)-1)/2]
    elif len(L)%2 ==0: # the median for a list of even number of elements
        return ((L[len(L)/2]+L[(len(L)/2-1)])/float(2))

def bfs(tree, elem):
    """
    perform a breadth first search
    :param tree: the list that will be searched
    :param elem: the element that search for
    :return: if the elem is in the tree return True. Otherwise, return False.
    """
    def copy(tree, treec):  #  copy tree to treec and use treec to search for elem
        for k in tree:
            if type(k) == int: #  add element in this layer to the treec
                treec.append(k)
            else:
                treec.append([])  #  add element in deeper layer to the treec
                copy(k, treec[-1])
    treec = []
    copy(tree, treec)
    a = []  # a is a list used to store the elements in tree arranged by the order of breadth first search
    a.append(treec[0]) # put the element of first layer in the first place of a
    treec.pop(0) # then delete the element of first layer of tree
    while True:
    #for each loop, extract elements of next layer of tree, then according to the order from left to right add them in a
        a.append(treec[0][0])
        b = treec[0] # b is a list used to store the first element in tree temporarily
        b.pop(0)
        treec.pop(0) # delete the first element in tree
        for i in range(0, len(b)): # put the children for the first element(the next layer) in the back of tree
            treec.append(b[i])
        if len(treec) == 0: # when tree is empty, which means all elements are already put in a according to the order of breadth first search
            break
    for j in range(0, len(a)): # search elem in a. if elem exist, return True. Otherwise return False
        print a[j]
        if a[j] == elem:
            return True
    return False

def dfs(tree, elem):
    """
    perform a depth first search
    :param tree: the list that will be searched
    :param elem: the element that search for
    :return: if the elem is in the tree return True. Otherwise, return False
    """
    def copy(tree, treec):  #  copy tree to treec and use treec to search for elem
        for k in tree:
            if type(k) == int: #  add element in this layer to the treec
                treec.append(k)
            else:
                treec.append([])  #  add element in deeper layer to the treec
                copy(k, treec[-1])
    treec = []
    copy(tree, treec)
    a = []  # a is a list used to store the elements in tree arranged by the order of depth first search
    a.append(treec[0])  # put the element of first layer in the first place of a
    treec.pop(0)  # then delete the element of first layer of tree
    while True:
    # put the rest elements in tree in a according to the order from left to right, which is the same as the order of depth first search
        a.append(treec[0][0])
        b = treec[0]  # b is a list used to store the first element in tree temporarily
        b.pop(0)
        treec.pop(0)  # delete the first element in tree
        c = 0
        if len(b) != 0:
            for j in range(0, len(b)):
                treec.insert(c, b[j])
                c += 1
        if len(treec) == 0:# when tree is empty, which means all elements are already put in a according to the order of depth first search
            break
    for j in range(0, len(a)):  # search elem in a. if elem exist, return True. Otherwise return False
        print a[j]
        if a[j] == elem:
            return True
    return False

class TTTBoard:
    """
    Tic Tac Toe game
    """
    def __init__(self):
        """
        initialize a tic tac toe board
        """
        self.a = ['*', '*', '*', '*', '*', '*', '*', '*', '*']
        return
    def __str__(self):
        """
        display a tring representation of the board
        """
        self.b = self.a[0]+' '+self.a[1]+' '+self.a[2]+'\n'+\
        self.a[3]+' '+self.a[4]+' '+self.a[5]+'\n'+\
        self.a[6]+' '+self.a[7]+' '+self.a[8]+'\n'
        return self.b
    def makeMove(self, player, pos):
        """
        Places a move for player in the position pos
        :param player: could be 'X' or 'O', which represents two players
        :param pos: the position players put 'X' or 'O' in
        :return: if move is valid, return True. Otherwise, return False
        """
        if player == 'X' or player == 'O':
            if self.a[pos] == '*':
                self.a[pos] = player
                return True
            else:
                return False
    def hasWon(self, player):
        """
        Test whether one of the players wins the game
        :param player: could be 'X' or 'O', which represents two players
        :return: if one of the players wins the game, return True. Otherwise return False
        """
        #  just list all the wining states
        for i in [0, 3, 6]:
            if self.a[i] == player and self.a[i+1] == player and self.a[i+2] == player:
                return True
        for j in [0, 1, 2]:
            if self.a[j] == player and self.a[j+3] == player and self.a[j+6] == player:
                return True
        if self.a[0] == player and self.a[4] == player and self.a[8] == player:
            return True
        elif self.a[2] == player and self.a[4] == player and self.a[6] == player:
            return True
        return False
    def gameOver(self):
        """
        Test whether someone has won of whether the board is full
        :return: if game is over, return True. Otherwise, return False
        """
        if self.hasWon('X') or self.hasWon('O') or ('*' not in self.a):
            return True
        else:
            return False
    def clear(self):
        """
        clears the board to reset the game
        """
        self.__init__()
        return