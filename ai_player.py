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
    last_move_index = -1

    while stones > 0:
        # jugador 1 paso por su mancala, sumarle punto
        if move_index == 6 and p1_turn:
            stones -= 1
            scores['p1'] += 1
            # ends turn in mancala
            if stones == 0:
                another_turn = True
                break

        # AI paso por su mancala, sumarle punto
        if move_index == 0 and not p1_turn:
            stones -= 1
            scores['p2'] += 1
            # ends turn in mancala
            if stones == 0:
                another_turn = True
                break

        # agregar una piedra en la casilla actual y restar la cantidad
        # de piedras restantes en la mano del jugador; por ultimo,
        # avanzar una casilla
        board[move_index] += 1
        stones -= 1
        if stones == 0:
            last_move_index = move_index
            break
        move_index = (move_index + 1) % 12

    # jugador deja ultima piedra en un espacio vacio propio, captura su piedra
    # y las de enfrente del otro jugador
    if last_move_index >= 0 and board[last_move_index] == 1:
        if p1_turn and last_move_index < 6:
            scores['p1'] += (board[11 - last_move_index] + 1)
            board[last_move_index] = 0
            board[11 - last_move_index] = 0
        elif not p1_turn and last_move_index >= 6:
            scores['p2'] += (board[11 - last_move_index] + 1)
            board[last_move_index] = 0
            board[11 - last_move_index] = 0

    return board, repeat_turn

def board_move(board, p1_score, p2_score, limit = 10):
    temp_board = copy.deepcopy(board)
    scores = {
        'p1': p1_score, 
        'p2': p2_score,
        6: 0,
        7: 0,
        8: 0,
        9: 0,
        10: 0,
        11: 0
    }
    iters = 0
    p1_turn = False
    path = []

    while iters < limit:
        moves = utils.legal_moves(temp_board, p1_turn)
        move = random.choice(moves)
        
        # se guarda el tiro solo si es el turno del AI
        if not p1_turn:
            path.append(move)
        
        # bla bla
        temp_board, repeat_turn = apply_move(temp_board, move, p1_turn, scores)
        if not repeat_turn:
            p1_turn = not p1_turn
        
        # bla bla
        if utils.game_over(temp_board):
            p1_l, p2_l = utils.leftovers(temp_board)
            scores['p1'] += p1_l
            scores['p2'] += p2_l
            
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

    legal_moves = utils.legal_moves(board, False)
    score_max = -float('inf')
    score_max_index = legal_moves[0]
    for i in legal_moves:
        if i in scores:
            if scores[i] > score_max:
                score_max = scores[i]
                score_max_index = i
    
    return score_max_index