from functools import reduce

def print_board(board, p1_turn):
    if p1_turn:
        for i in range(11, 5, -1):
            print(f'{board[i]}|', end="", flush=True)
        print("")
        for i in range(6):
            print(f'{board[i]}|', end="", flush=True)
        print("")
    else:
        for i in range(5, -1, -1):
            print(f'{board[i]}|', end="", flush=True)
        print("")
        for i in range(6, 12):
            print(f'{board[i]}|', end="", flush=True)
        print("")

def legal_moves(board, p1_turn):
    moves = []
    if p1_turn:
        for i in range(6):
            if board[i] > 0:
                moves.append(i)
    else:
        for i in range(6, 12):
            if board[i] > 0:
                moves.append(i)

    return moves

def game_over(board):
    s = reduce((lambda x, y: x + y), board[:6])
    if s == 0:
        return True
    s = reduce((lambda x, y: x + y), board[6:])
    if s == 0:
        return True
    return False