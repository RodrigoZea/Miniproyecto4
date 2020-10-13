"""
MODELACION Y SIMULACION
MINI PROYECTO 4

INTEGRANTES
Sebastian Arriola
Rodrigo Zea
"""
import ai_player as ai
import utils as utils

# puntaje
p1, p2 = 0, 0

# llevar control de turnos
p1_turn = True
another_turn = False

# inicializar tablero, por ahora solo con una piedra en cada casilla
board = [1 for _ in range(12)]

def main():
    global p1_turn
    print("""
    ¡Bienvenido al juego de Mancala
    Los niveles de computadora disponibles son:
    1. Noob
    2. Avanzado
    3. Pro
    """)

    cpu_lvl = input("Escoga el nivel de la computadora: ")

    # loop de juego para probar
    while not utils.game_over(board):
        another_turn = False

        print(f'points: p1 {p1}, p2 {p2}')
        utils.print_board(board, p1_turn)
        print(f'\n\nit is player {"1" if p1_turn else "AI"} turn')
        
        if p1_turn:
            i = int(input("choose your move index: "))
            board_move(board, i)
        else:
            ai.board_move(board, p1, p2)
        
        print("")
        if not another_turn:
            p1_turn = not p1_turn
            
def board_move(board, move):
    global p1, p2, another_turn

    stones = board[move]
    board[move] = 0
    move = (move + 1) % 12

    while stones > 0:
        if move == 6 and p1_turn:
            stones -= 1
            p1 += 1
            # ends turn in mancala
            if stones == 0:
                another_turn = True
        if move == 0 and not p1_turn:
            stones -= 1
            p2 += 1
            # ends turn in mancala
            if stones == 0:
                another_turn = True

        if stones > 0:
            board[move % 12] += 1
            stones -= 1
            move += 1

    # player drops a stone on last slot visited
    if board[move-1] == 1:
        # apply score
        # since move ends in offset +2, 13 is mirror slot
        p1 += board[13 - move]
        # remove stones from mirror slot
        board[13 - move] = 0

main()