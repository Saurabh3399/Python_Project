"""
Tic Tac Toe Player
"""
import copy
from math import inf

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    count = [0, 0]
    for i in range(3):
        for j in range(3):
            if board[i][j] == "X":
                count[0] = count[0] + 1
            elif board[i][j] == "O":
                count[1] = count[1] + 1

    if count[0] > count[1]:
        return O
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_action = []
    for i in range(3):
        for j in range(3):
            if board[i][j] == None:
                possible_action.append((i, j))

    return possible_action


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    copy_board = copy.deepcopy(board)

    if copy_board[action[0]][action[1]] is None:
        a = player(copy_board)
        copy_board[action[0]][action[1]] = a
        return copy_board
    else:
        raise "eror"


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for i in range(3):
        if (
            board[i][0] == board[i][1]
            and board[i][0] == board[i][2]
            and board[i][0] != None
        ):
            if board[i][0] == "X":
                return X
            elif board[i][0] == "O":
                return O
            else:
                return None

    for i in range(3):
        if (
            board[0][i] == board[1][i]
            and board[1][i] == board[2][i]
            and board[0][i] != None
        ):
            if board[0][i] == "X":
                return X
            elif board[0][i] == "O":
                return O
            else:
                return None

    if (
        board[0][0] == board[1][1]
        and board[1][1] == board[2][2]
        and board[0][0] != None
    ):
        if board[0][0] == "X":
            return X
        elif board[0][0] == "O":
            return O
        else:
            return None

    if (
        board[2][0] == board[1][1]
        and board[1][1] == board[0][2]
        and board[2][0] != None
    ):
        if board[2][0] == "X":
            return X
        elif board[2][0] == "O":
            return O
        else:
            return None

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) == "X":
        return True
    elif winner(board) == "O":
        return True

    for i in range(3):
        for j in range(3):
            if board[i][j] == None:
                return False
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == "X":
        return 1
    elif winner(board) == "O":
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal move for the current player on the board.
    """
    # Check for terminal state
    if terminal(board):
        return None

    # If X's turn
    elif player(board) == X:
        options = []
        for action in actions(board):
            score = min_value(result(board, action))
            # Store options in list
            options.append([score, action])
        # Return highest value action
        return sorted(options, reverse=True)[0][1]

    # If O's turn
    else:
        options = []
        for action in actions(board):
            score = max_value(result(board, action))
            # Store options in list
            options.append([score, action])
        # Return lowest value action
        return sorted(options)[0][1]


def max_value(board):
    """
    Returns the highest value option of a min-value result
    """
    # Check for terminal state
    if terminal(board):
        return utility(board)

    # Loop through possible steps
    v = -inf
    for action in actions(board):
        v = max(v, min_value(result(board, action)))
    return v


def min_value(board):
    """
    Returns the smallest value option of a max-value result
    """
    # Check for terminal state
    if terminal(board):
        return utility(board)

    # Loop through possible steps
    v = inf
    for action in actions(board):
        v = min(v, max_value(result(board, action)))
    return v