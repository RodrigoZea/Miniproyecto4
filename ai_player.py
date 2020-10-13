import utils
import random
import hashlib
import copy

random.seed(69)

def apply_move(board, move, p1_turn, scores):
    board = copy.deepcopy(board)
    stones = board[move]
    board[move] = 0
    move_index = (move + 1) % 12
    repeat_turn = False

    while stones > 0:
        if move_index == 6 and p1_turn:
            stones -= 1
            scores['p1'] += 1
            # ends turn in mancala
            if stones == 0:
                another_turn = True
        if move_index == 0 and not p1_turn:
            stones -= 1
            scores['p2'] += 1
            # ends turn in mancala
            if stones == 0:
                another_turn = True

        if stones > 0:
            board[move_index % 12] += 1
            stones -= 1
            move_index += 1

    # player drops a stone on last slot visited
    if board[move] == 1:
        # apply score
        p1 += board[13 - move]
        # remove stones from mirror
        board[13 - move] = 0

    return board, repeat_turn

def board_move(board, p1_score, p2_score, limit = 10):
    temp_board = copy.deepcopy(board)
    scores = {'p1': p1_score, 'p2': p2_score}
    iters = 0
    p1_turn = False
    path = []

    for move in utils.legal_moves(board, p1_turn):
        scores[move] = 0

    while iters < limit:
        moves = utils.legal_moves(temp_board, p1_turn)
        move = random.choice(moves)
        path.append(move)
        temp_board, repeat_turn = apply_move(temp_board, move, p1_turn, scores)
        if not repeat_turn:
            p1_turn = not p1_turn
        if utils.game_over(temp_board):
            print(f'iteration {iters} done...')
            print(f'path {path}')
            print(f'scores  {scores}')
            
            if scores['p1'] > scores['p2']:
                scores[path[0]] -= 1
            else:
                scores[path[0]] += 1

            p1_turn = False
            iters += 1
            temp_board = copy.copy(board)
            scores['p1'] = 0
            scores['p2'] = 0
            path.clear()

    print(f'scores {scores}')

    print('game over')