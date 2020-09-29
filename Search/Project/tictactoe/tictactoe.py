"""
Tic Tac Toe Player
"""

import math
from copy import copy, deepcopy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[X, O, X],
            [O, X, EMPTY],
            [O, EMPTY, O]]


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
    Winner = winner(board)
    if(Winner == X):
        return 1
    if(Winner == O):
        return -1
    return 0
        
    # raise NotImplementedError

def maxValue(board):
    choice  = (-math.inf, None)
    if(terminal(board)):
        return utility(board)
    for action in actions(board):
        v = (max(v,minValue(result(board, action))), action)
    
    print("MaxValue Function")
    print("V : " + str(v))
    print(board)
    input()
    return v

def minValue(board):
    v = (math.inf, None)
    if(terminal(board)):
        return utility(board)
    for action in actions(board):
        v = (min(v,maxValue(result(board, action))), action)

    print("MinValue Function")
    print("V : " + str(v))
    print(board)
    input()
    return v

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    currentPlayer = player(board) #if X maximize; if O minimize
    if(currentPlayer == X):
        v = maxValue(board)
    else:
        v = minValue(board)
    print("Current player is : " + str(currentPlayer))
    print("V : " + str(v))
    # start = Node(state=board, parent=None, action=None)
    # frontier = QueueFrontier() #Find a win in the least number of moves from the current board.
    # frontier.add(start)

    # terminalNodes = set()
    # loopcnt = 0
    # while True:
    #     print("Loop Count = " + str(loopcnt))
    #     loopcnt = loopcnt + 1
    #     print("Frontier Empty = " + str(frontier.empty()))
    #     print("Frontier Length = " + str(len(frontier.frontier)))
    #     if(frontier.empty()):
    #         print("Frontier Empty")
    #         Actions = actions(board)
    #         return list(Actions)[0]
    #         #find a node in terminalNodes that has a value of 0, no winning game was found
        
    #     node = frontier.remove()
    #     currentPlayer = player(node.state) #if X maximize; if O minimize
    #     if(terminal(node.state)):
    #         print("Location Test : terminal(node.state)")
    #         playerUtility = utility(node.state)
    #         #If player X found a winning board return the required action, No need to continue searching
    #         if(currentPlayer == X):
    #             if(playerUtility == 1):
    #                 bestAction = node.action
    #                 print("Player X Optimal Action")
    #                 return bestAction
            
    #         #If player O found a winning board return the required action, No need to continue searching
    #         if(currentPlayer == O):
    #             if(playerUtility == -1):
    #                 bestAction = node.action
    #                 print("Player O Optimal Action")
    #                 return bestAction

    #         #If no winning board is found add the terminal node to a list. We will want to find boards that are 0 if we don't find any winners.
    #         #Because of breath first searching a winner that is found will be an optimal path, no need to store winning boards
    #         terminalNodes.add(node)

    #     else:
    #         #if the game isn't over...            
    #         #What turns are available? 
    #         availableActions = actions(node.state)
    #         #add the nodes to the frontier
    #         for action in availableActions:
    #             print("ACTION :")
    #             print(action)
    #             newBoard = result(node.state, action)
    #             print("NEW BOARD :")
    #             print(newBoard)
    #             frontier.add(Node(state=newBoard, parent=node, action=action))
                

    Actions = actions(board)
    print("Just got to a weird spot?")
    return list(Actions)[0]
    # raise NotImplementedError
