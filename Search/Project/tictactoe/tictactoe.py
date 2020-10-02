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
iterMax = 100
iterCount = 0

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
        return 100 # 9 because 3 in a row squared 
    if(Winner == O):
        return -100
    # return 0

    rowCount = len(board)
    colCount = len(board[0])
    utility = 0
    laneUtility = [] #Lane utility gives a score to each lane : Utility = sum(X^2) - sum(O^2)
    # Checking Rows
    # printBoard(board)
    for rows in board:
        sumX = 0
        sumO = 0
        for ele in rows:
            if(ele == X):
                sumX = sumX+1
            if(ele == O):
                sumO = sumO+1
        
        # print("SumX : " + str(sumX))
        # print("SumO : " + str(sumO))
        if(sumX != 0 and sumO == 0 ):
            # print("SumX_row = " + str(sumX))
            laneUtility.append(pow(sumX,2))
        if(sumX == 0 and sumO != 0 ):
            # print("SumO_row = " + str(sumO))
            laneUtility.append(-pow(sumO,2)) #NOTE THE NEGITIVE SIGN... this is gonna get me somehow

    # print("Checking Lane Utilities ROWS!!!!!")
    # print(laneUtility)   
    # Checking Cols
    for j in range(colCount):
        cols = [board[0][j], board[1][j], board[2][j]]
        # print("cols")
        # print(cols)
        sumX = 0
        sumO = 0
        for ele in cols:
            if(ele == X):
                sumX = sumX+1
            if(ele == O):
                sumO = sumO+1
        if(sumX != 0 and sumO == 0 ):
            # print("SumX_col = " + str(sumX))
            laneUtility.append(pow(sumX,2))
        if(sumX == 0 and sumO != 0 ):
            # print("SumO_col = " + str(sumO))
            laneUtility.append(-pow(sumO,2))

    # print("Checking Lane Utilities COLS!!!!!")
    # print(laneUtility)   

    # Check Diags
    diagDown = [board[0][0], board[1][1], board[2][2]]
    # print("Diag Down")
    # print(diagDown)
    sumX = 0
    sumO = 0
    for ele in diagDown:
        if(ele == X):
            sumX = sumX+1
        if(ele == O):
            sumO = sumO+1
    if(sumX != 0 and sumO == 0 ):
        # print("SumX_diagd = " + str(sumX))
        laneUtility.append(pow(sumX,2))
    if(sumX == 0 and sumO != 0 ):
        # print("SumO_diagd = " + str(sumO))
        laneUtility.append(-pow(sumO,2))

    diagUp = [board[2][0], board[1][1], board[0][2]]
    # print("Diag Up")
    # print(diagUp)
    sumX = 0
    sumO = 0
    for ele in diagUp:
        if(ele == X):
            sumX = sumX+1
        if(ele == O):
            sumO = sumO+1
    if(sumX != 0 and sumO == 0 ):
        # print("SumX_diagu = " + str(sumX))
        laneUtility.append(pow(sumX,2))
    if(sumX == 0 and sumO != 0 ):
        # print("SumO_diagu = " + str(sumO))
        laneUtility.append(-pow(sumO,2))

    # print("Checking Lane Utilities Diags!!!!!")
    # print(laneUtility)
    
    boardUtility = 0
    for ele in laneUtility:
        boardUtility += ele
    # print("Checking Board Utilities!!!!!")
    # print(boardUtility)
    # input()
    return boardUtility


    # raise NotImplementedError

def maxValue(board):
    global iterCount
    print("Board :")
    printBoard(board)

    v = Node(-math.inf, None, -math.inf, None) #value, est_value, action

    #If we hit a terminal board return the actual values
    if(terminal(board)):
        print("Max Term Board End")
        return Node(utility(board), v.action, None, None)
    #If we hit a depth limit return the estimated values
    if(iterCount >= iterMax):
        print("Max Iter Count End  " + str(iterCount))
        return Node(None, None, utility(board), v.action)
    iterCount += 1
    
    # #if the center is open take it. I just feel like this is a good strat since board score is trinary
    # if (1,1) in actions(board):
    #     v_new = maxValue(result(board, (1,1)))

    #     if (v_new.value is not None and v.value is not None):
    #         if (v_new.value > v.value):
    #             v = v_new
    #             v.action = (1,1)
    #     elif (v_new.estvalue is not None and v.estvalue is not None):
    #         if ( (v_new.estvalue > v.estvalue)):
    #             v = v_new
    #             v.estaction = (1,1)
    #     if(v.value == 100): #Stop at first win condition
    #         return v

    for action in actions(board):
        v_new = minValue(result(board, action))
        
        #If we are here we've hit a return by either terminal or iterCount. If terminal then we should have a valid v_new.value. If not we can check the estimated board value next
        # print("Max")
        # print("Board :")
        # printBoard(board)
        # print("Action :")
        # print(action)
        # print("v_new      " + str(v_new.value))
        # print("v          " + str(v.value))
        # print("v_new est  " + str(v_new.estvalue))
        # print("v est      " + str(v.estvalue))
        # input()
        # print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        if (v_new.value is not None and v.value is not None):
            if (v_new.value > v.value):
                v = v_new
                v.action = action
        if (v_new.estvalue is not None and v.estvalue is not None):
            if ( (v_new.estvalue > v.estvalue) and v_new.estvalue > v.value):
                print("Are we ever here?")
                v.estvalue = v_new.estvalue
                v.estaction = action
        # if(v.value == 100): #Stop at first win condition
        #     print("Found a Winning Game X")
        #     print(v.value)
        #     print(" ")
        #     return v

    return v


def minValue(board):
    global iterCount
    print("Board :")
    printBoard(board)

    v = Node(math.inf, None, math.inf, None) #value, est_value, action

    #If we hit a terminal board return the actual values
    if(terminal(board)):
        print("Min Term Board End")
        return Node(utility(board), v.action, None, None)
    #If we hit a depth limit return the estimated values
    if(iterCount >= iterMax):
        print("Min Iter Count End " + str(iterCount))
        return Node(None, None, utility(board), v.action)
    iterCount += 1
    
    # #if the center is open take it. I just feel like this is a good strat since board score is trinary
    # if (1,1) in actions(board):
    #     v_new = maxValue(result(board, (1,1))) #This is the recursive part of the function
        

    #     #If we are here we've hit a return by either terminal or iterCount. If terminal then we should have a valid v_new.value. If not we can check the estimated board value next
    #     if (v_new.value is not None and v.value is not None):
    #         if (v_new.value < v.value): #This is the min part of the function
    #             v = v_new
    #             v.action = (1,1)
    #     elif (v_new.estvalue is not None and v.estvalue is not None):
    #         if ( (v_new.estvalue < v.estvalue)):
    #             v = v_new
    #             v.estaction = (1,1)
    #     if(v.value == -100): #Stop at first win condition
    #         return v

    for action in actions(board):
        v_new = maxValue(result(board, action))
        
        #If we are here we've hit a return by either terminal or iterCount. If terminal then we should have a valid v_new.value. If not we can check the estimated board value next
        # print("min")
        # print("Board :")
        # printBoard(board)
        # print("Action :")
        # print(action)
        # print("v_new      " + str(v_new.value))
        # print("v          " + str(v.value))
        # print("v_new est  " + str(v_new.estvalue))
        # print("v est      " + str(v.estvalue))
        # input()
        # print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        if (v_new.value is not None and v.value is not None):
            if (v_new.value < v.value):
                v = v_new
                v.action = action
        if (v_new.estvalue is not None and v.estvalue is not None):
            if ( (v_new.estvalue < v.estvalue) and v_new.estvalue < v.value):
                print("Are we ever here?")
                v.estvalue = v_new.estvalue
                v.estaction = action
        # if(v.value == -100): #Stop at first win condition
        #     print("Found a Winning Game O")
        #     return v

    return v

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    global iterCount
    iterCount = 0
    currentPlayer = player(board) #if X maximize; if O minimize
    print("Current player is : " + str(currentPlayer))

    if(currentPlayer == X):
        v = maxValue(board)
    else:
        v = minValue(board)
    print("v.value " + str(v.value))
    print("v.action " + str(v.action))
    print("v.estvalue " + str(v.estvalue))
    print("v.estaction " + str(v.estaction))

    if(v.action is not None):
        print("Using Term Value")
        return v.action
    else:
        print("Using Est Value")
        return v.estaction
    # raise NotImplementedError

def printBoard(board):
    print(board[0])
    print(board[1])
    print(board[2])