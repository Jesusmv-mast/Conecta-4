"""Script educativo: muestra la recursion y el backtracking en accion.

No es parte del juego. Se usa solo para visualizar como el arbol de
jugadas futuras se explora (bajar) y se deshace (subir).
"""

from model.game_model import GameModel

AI = 'O'
HUMAN = 'X'
MAX_DEPTH = 2  # Pequeno a proposito, solo para ver la traza completa.


def explore(board, depth, is_maximizing):
    """Recorre el arbol de jugadas futuras imprimiendo cada paso."""
    indent = '  ' * depth
    player = AI if is_maximizing else HUMAN

    if board.check_winner(AI):
        print(f'{indent}[profundidad {depth}] HOJA: gana {AI}')
        return
    if board.check_winner(HUMAN):
        print(f'{indent}[profundidad {depth}] HOJA: gana {HUMAN}')
        return
    if not board.get_available_moves() or depth == MAX_DEPTH:
        print(f'{indent}[profundidad {depth}] HOJA: limite o tablero lleno')
        return

    moves = board.get_available_moves()
    print(f'{indent}[profundidad {depth}] turno de {player}, '
        f'columnas posibles: {moves}')

    for move in moves:
        print(f'{indent}-> BAJAR: {player} juega columna {move}')
        board.make_move(move, player)          # bajar un nivel
        explore(board, depth + 1, not is_maximizing)
        board.undo_move(move)                   # BACKTRACKING: subir
        print(f'{indent}<- SUBIR: se deshace la jugada en columna {move}')


if __name__ == '__main__':
    model = GameModel()
    model.make_move(2, 'X')
    model.make_move(1, 'O')
    print('Tablero inicial: ya jugaron X en columna 2 y O en columna 1.')
    print(f'Explorando con MAX_DEPTH={MAX_DEPTH} (a proposito pequeno)\n')
    explore(model, 0, True)