"""
MODELACION Y SIMULACION
MINI PROYECTO 4

INTEGRANTES
Sebastian Arriola
Rodrigo Zea
"""
import ai_player as ai
import utils as utils

BOARD_SIZE = 12

# puntaje
p1, p2 = 0, 0

# llevar control de turnos
p1_turn = True
another_turn = False

# inicializar tablero, por ahora solo con una piedra en cada casilla
board = [4 for _ in range(BOARD_SIZE)]

def main():
    global p1, p2, p1_turn
    print("""
    ¡Bienvenido al juego de Mancala
    Los niveles de computadora disponibles son:
    1. Noob
    2. Avanzado
    3. Pro
    """)

    cpu_lvl = 0
    while cpu_lvl not in ['1', '2', '3']:
        cpu_lvl = input("Escoga el nivel de la computadora: ")
    
    if cpu_lvl == '1':
        cpu_lvl = 1
    elif cpu_lvl == '2':
        cpu_lvl = 100
    elif cpu_lvl == '3':
        cpu_lvl = 10000

    # loop de juego para probar
    while not utils.game_over(board):
        another_turn = False

        print(f'points: p1 {p1}, p2 {p2}')
        print(f'\n\nit is player {"1" if p1_turn else "AI"} turn')
        if p1_turn:
            utils.print_board(board, True)
        
        if p1_turn:
            i = int(input("choose your move index: "))
            board_move(board, i)
            print('board after your move:')
            utils.print_board(board, True)
            print('########################################')
        else:
            ai_move = ai.board_move(board, p1, p2, limit=cpu_lvl)
            board_move(board, ai_move)
            print(f'AI moved {ai_move}')
        
        print("")
        if not another_turn:
            p1_turn = not p1_turn

    # sumar las piedras restantes en el tablero para puntaje final
    p1_l, p2_l = utils.leftovers(board)
    p1 += p1_l
    p2 += p2_l

    print('############################################')
    if p1 > p2:
        print('LE GANASTE A NUESTRO SUPER AI :(')
    elif p2 > p1:
        print('AI TE GANO XDXDXDXD')
    else:
        print('EMPATE, QUE NOOBSTER')
    print('************* PUNTAJE FINAL ****************')
    print(f'Player: {p1}, AI: {p2}')
    print('############################################')

def board_move(board, move):
    global p1, p2, another_turn

    stones = board[move]
    board[move] = 0
    move_index = (move + 1) % BOARD_SIZE
    last_move_index = -1

    while stones > 0:
        # jugador 1 paso por su mancala, sumarle punto
        if move_index == 6 and p1_turn:
            stones -= 1
            p1 += 1
            # ends turn in mancala
            if stones == 0:
                another_turn = True
                break

        # AI paso por su mancala, sumarle punto
        if move_index == 0 and not p1_turn:
            stones -= 1
            p2 += 1
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
        move_index = (move_index + 1) % BOARD_SIZE

    # jugador deja ultima piedra en un espacio vacio propio, captura su piedra
    # y las de enfrente del otro jugador
    if last_move_index >= 0 and board[last_move_index] == 1:
        if p1_turn and last_move_index < 6:
            p1 += (board[11 - last_move_index] + 1)
            board[last_move_index] = 0
            board[11 - last_move_index] = 0
        elif not p1_turn and last_move_index >= 6:
            p2 += (board[11 - last_move_index] + 1)
            board[last_move_index] = 0
            board[11 - last_move_index] = 0

main()