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
            repeat_turn = True
        if move_index == 0 and not p1_turn:
            stones -= 1
            scores['p2'] += 1
            repeat_turn = True

        if stones > 0:
            board[move_index % 12] += 1
            stones -= 1
            move_index += 1

    return board, repeat_turn

def move(board, p1_score, p2_score):
    temp_board = copy.deepcopy(board)
    scores = {'p1': p1_score, 'p2': p2_score}
    iters = 0
    p1_turn = False
    path = []

    for move in utils.legal_moves(board, p1_turn):
        scores[move] = 0

    while iters < 10:
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
            path.clear()

    print(f'scores {scores}')

    print('game over')