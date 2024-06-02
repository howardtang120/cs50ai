
x = "X"
o = "o"
         
board =  [[None, o, x],
        [None, o, x],
        [None, None, x]]

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

print(winner(board))

