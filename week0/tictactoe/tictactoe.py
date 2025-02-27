"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


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
    X_count, O_count = 0, 0
    for row in board:
        for cell in row:
            if cell == X:
                X_count += 1
            elif cell == O:
                O_count += 1

    # X always starts             
    return O if X_count > O_count else X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = set()
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == EMPTY:
                possible_actions.add((i, j))

    return possible_actions

def result(board, action):
    if action not in actions(board):
        raise ValueError("Invalid move")
    
    board_copy = copy.deepcopy(board)
    board_copy[action[0]][action[1]] = player(board)
    return board_copy


def check_horizontals(board):
    for i in range(len(board)):
        symbol = board[i][0]
        if symbol != EMPTY:
            three_in_row = list(map(lambda x: x == symbol, board[i]))
            if all(three_in_row):
                return symbol
    return None

def check_verticals(board):
    for j in range(len(board)):
        symbol = board[0][j]
        if symbol != EMPTY:
            column = [board[i][j] for i in range(len(board))]
            three_in_column = list(map(lambda x: x == symbol, column))
            if all(three_in_column):
                return symbol
            
    return None

def check_diagonals(board):
    symbol = board[1][1]
    if symbol != EMPTY:
        # Check forward diagonal
        diagonal = [board[j][j] for j in range(len(board))]
        three_in_diagonal = list(map(lambda x: x == symbol, diagonal))
        if all(three_in_diagonal):
            return symbol
            
        # Check backward diagonal
        j = 2
        diagonal = [board[i][j - i] for i in range(len(board))]
        three_in_diagonal = list(map(lambda x: x == symbol, diagonal))
        if all(three_in_diagonal):
            return symbol
            
    return None  

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    winner = check_horizontals(board)
    if winner is not None:
        return winner
    
    winner = check_verticals(board)
    if winner is not None:
        return winner
    
    winner = check_diagonals(board)
    if winner is not None:
        return winner
    
    return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    def board_full():
        elements  = [board[i][j] for i in range(len(board)) for j in range(len(board))]
        return all(list(map(lambda x: x != EMPTY, elements)))

    return board_full() or winner(board) is not None

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    winner_ = winner(board)
    if winner_ == X:
        return 1
    elif winner_ == O:
        return -1
    else:
        return 0
    
def max_value(board):
    if terminal(board):
        return utility(board), None
    
    v = float("-inf")
    chosen_action = None
    for action in actions(board):
        v_prime = min_value(result(board, action))[0]
        if v < v_prime:
            v = v_prime
            chosen_action = action
    return v, chosen_action

def min_value(board):
    if terminal(board):
        return utility(board), None
    
    v = float("inf")
    chosen_action = None
    for action in actions(board):
        v_prime = max_value(result(board, action))[0]
        if v > v_prime:
            v = v_prime
            chosen_action = action
    return v, chosen_action


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    
    player_in_turn = player(board)
    return max_value(board)[1] if player_in_turn == X else min_value(board)[1]