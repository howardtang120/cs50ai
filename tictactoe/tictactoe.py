"""
Tic Tac Toe Player
"""

from copy import deepcopy
X = "X"
O = "O"
EMPTY = None
INFINITE = 255

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
    count_x = 0
    count_o = 0

    for row in board:
        count_x += row.count(X)
        count_o += row.count(O)

    if count_x == count_o:
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    empty_cells = []
    for row in range(3):
        for column in range(3):
            if board[row][column] == EMPTY:
                empty_cells.append((row, column))
        
    return empty_cells


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    x, y = action
    if board[x][y] != EMPTY:
        raise ValueError
    
    # The symbol to insert (who's turn?)
    symbol = player(board)

    board_copy = deepcopy(board)
    board_copy[x][y] = symbol

    return board_copy


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Check rows
    for row in board:
        if row[0] == row[1] == row[2] and row[0] != None:
            return row[0]

    # Check columns
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] != None:
            return board[0][col]

    # Check diagonals
    if board[1][1] != None:
        if all(board[i][i] == board[0][0] for i in range(3)):
            return board[0][0]
        if all(board[i][2-i] == board[0][2] for i in range(3)):
            return board[0][2]

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) != None:
        return True
    
    for row in range(3):
        for column in range(3):
            if board[row][column] == EMPTY:
                return False
            
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    state = winner(board)
    if state == "X":
        return 1
    elif state == "O":
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None


    current_player = player(board)
    best_play = [10, 10]

    if current_player == X:
        current_value = -INFINITE
        for action in actions(board):
            new_board = result(board, action)
            score = min(new_board, current_value)
            if score > current_value:
                current_value = score
                best_play = action

    elif current_player == O:
        current_value = INFINITE
        for action in actions(board):
            new_board = result(board, action)
            score = max(new_board, current_value)
            if score < current_value:
                current_value = score
                best_play = action

    return best_play


def max(board, current_value):
    if terminal(board):
        return utility(board)
    
    #set to smallest value
    local_value = -INFINITE

    for play in actions(board):
        new_board = result(board, play)
        score = min(new_board, current_value)
        if score > current_value: # pruning
            return score
        if score > local_value:
            local_value = score

    return local_value


def min(board, current_value):
    if terminal(board):
        return utility(board)
    
    # set to largest value
    local_value = INFINITE

    for play in actions(board):
        new_board = result(board, play)
        score = max(new_board, current_value)
        if score < current_value: # pruning
            return score
        if score < local_value:
            local_value = score
        
    return local_value


    


