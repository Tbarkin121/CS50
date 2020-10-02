"""
Tic Tac Toe Player
"""

import math
from copy import copy, deepcopy
from util import Node

X = "X"
O = "O"
EMPTY = None
Debug = False

def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    pieces = 0
    for row in board:
        for element in row:
            if element != EMPTY:
                pieces = pieces + 1
    if(pieces%2):
        return O
    else:
        return X
        
    # raise NotImplementedError


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    movelist = set()
    rowCount = len(board)
    colCount = len(board[0])
    # print("board size  :  " + str(rowCount) + " x " + str(colCount))
    for row in range(rowCount):
        # print("i" + str(i))
        for col in range(colCount):
            if(board[row][col] == EMPTY):
                movelist.add((row,col))
    
    # print("Move List:")
    # for x in movelist:
    #     print(x)
    
    return movelist
    # raise NotImplementedError


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    class NotValidMove(BaseException):
        pass

    newBoard = deepcopy(board)
    if board[action[0]][action[1]] != EMPTY:
        raise NotValidMove
    else:
        newBoard[action[0]][action[1]] = player(board)
    # print(board)
    # print(newBoard)
    return newBoard


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    rowCount = len(board)
    colCount = len(board[0])
    # Checking Rows
    for rows in board:
        res = all(ele == rows[0] for ele in rows)
        if(res and rows[0] != None):
            return rows[0]
        
    # Checking Cols
    for j in range(colCount):
        cols = [board[0][j], board[1][j], board[2][j]]
        res = all(ele == cols[0] for ele in cols)
        if(res and cols[0] != None):
            return cols[0]
    # Check Diags
    diagDown = [board[0][0], board[1][1], board[2][2]]
    res = all(ele == diagDown[0] for ele in diagDown)
    if(res and diagDown[0] != None):
        return diagDown[0]

    diagUp = [board[2][0], board[1][1], board[0][2]]
    res = all(ele == diagUp[0] for ele in diagUp)
    if(res and diagUp[0] != None):
        return diagUp[0]

    return None
    # raise NotImplementedError


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # Check For Winner
    Winner = winner(board)
    if(Winner != None):
        return True

    # Check for Actions
    Actions = actions(board)
    if(len(Actions) <= 0):
        return True
    return False
    # raise NotImplementedError


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    #if we have a winning board there is no reason to do the other stuff
    Winner = winner(board)
    if(Winner == X):
        return 1 # 9 because 3 in a row squared 
    if(Winner == O):
        return -1
    return 0

    # rowCount = len(board)
    # colCount = len(board[0])
    # utility = 0
    # laneUtility = set() #Lane utility gives a score to each lane : Utility = sum(X^2) - sum(O^2)
    # # Checking Rows
    # for rows in board:
    #     sumX = 0
    #     sumO = 0
    #     for ele in rows:
    #         if(ele == X):
    #             sumX = sumX+1
    #         if(ele == O):
    #             sumO = sumO+1
    #     printBoard(board)
    #     print("SumX : " + str(sumX))
    #     print("SumO : " + str(sumO))
    #     if(sumX != 0 and sumO == 0 ):
    #         laneUtility.add(sumX^2)
    #     if(sumX == 0 and sumO != 0 ):
    #         laneUtility.add(-(sumO^2)) #NOTE THE NEGITIVE SIGN... this is gonna get me somehow

        
    # # Checking Cols
    # for j in range(colCount):
    #     cols = [board[0][j], board[1][j], board[2][j]]
    #     sumX = 0
    #     sumO = 0
    #     for ele in cols:
    #         if(ele == X):
    #             sumX = sumX+1
    #         if(ele == O):
    #             sumO = sumO+1
    #     if(sumX != 0 and sumO == 0 ):
    #         laneUtility.add(sumX^2)
    #     if(sumX == 0 and sumO != 0 ):
    #         laneUtility.add(-(sumO^2)) 

    # # Check Diags
    # diagDown = [board[0][0], board[1][1], board[2][2]]
    # for ele in diagDown:
    #     if(ele == X):
    #         sumX = sumX+1
    #     if(ele == O):
    #         sumO = sumO+1
    # if(sumX != 0 and sumO == 0 ):
    #     laneUtility.add(sumX^2)
    # if(sumX == 0 and sumO != 0 ):
    #     laneUtility.add(-(sumO^2)) 

    # diagUp = [board[2][0], board[1][1], board[0][2]]
    # for ele in diagUp:
    #     if(ele == X):
    #         sumX = sumX+1
    #     if(ele == O):
    #         sumO = sumO+1
    # if(sumX != 0 and sumO == 0 ):
    #     laneUtility.add(sumX^2)
    # if(sumX == 0 and sumO != 0 ):
    #     laneUtility.add(-(sumO^2)) 
    # print("Checking Lane Utilities!!!!!")
    # print(laneUtility)
    # boardUtility = 0
    # for ele in laneUtility:
    #     boardUtility = boardUtility + ele
    # print("Checking Board Utilities!!!!!")
    # print(boardUtility)
    # input()
    # return boardUtility

    
    
        
    # raise NotImplementedError

def maxValue(board):

    v = (-math.inf, None) #value and action

    if(terminal(board)):
        return (utility(board), v[1])


    #if the center is open take it. I just feel like this is a good strat since board score is trinary
    if (1,1) in actions(board):
        v_new = (max(v[0],minValue(result(board, (1,1)))[0]), (1,1))

        if (v_new[0] > v[0]):
            v = v_new

        if(v[0] == 1): #Stop at first win condition
            return v

    for action in actions(board):
        v_new = (max(v[0],minValue(result(board, action))[0]), action)

        if (v_new[0] > v[0]):
            v = v_new

        if(v[0] == 1): #Stop at first win condition
            return v

    return v

def minValue(board):
    v = (math.inf, None) #value and action

    if(terminal(board)):
        return (utility(board), v[1])

    
    #if the center is open take it. I just feel like this is a good strat since board score is trinary
    if (1,1) in actions(board):

        v_new = (min(v[0],maxValue(result(board, (1,1)))[0]), (1,1))

        if (v_new[0] < v[0]):
            v = v_new

        if(v[0] == -1): #Stop at first win condition
            return v

    for action in actions(board):
        v_new = (min(v[0],maxValue(result(board, action))[0]), action)

        if (v_new[0] < v[0]):
            v = v_new

        if(v[0] == -1): #Stop at first win condition
            return v

    return v

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    currentPlayer = player(board) #if X maximize; if O minimize

    print("Current player is : " + str(currentPlayer) + " : : " + str(currentPlayer == X))

    if(currentPlayer == X):
        v = maxValue(board)
    else:
        v = minValue(board)
    print("V : " + str(v))

    return v[1]
    # raise NotImplementedError

def printBoard(board):
    print(board[0])
    print(board[1])
    print(board[2])