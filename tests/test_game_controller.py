# Tests del modelo del juego Connect 4
"""Pruebas de integración Humano vs. Humano (sin abrir ventanas)."""

from pathlib import Path

from controller.game_controller import GameController

ROOT = Path(__file__).resolve().parent.parent


class FakeView:
    """Vista falsa que registra lo que el controlador le pide."""

    def __init__(self):
        self.status = ''
        self.board = None
        self.draw_count = 0
        self.column_handler = None
        self.restart_handler = None

    def set_column_click_handler(self, handler):
        self.column_handler = handler

    def set_restart_handler(self, handler):
        self.restart_handler = handler

    def set_status(self, text):
        self.status = text

    def draw_board(self, board):
        self.board = [row[:] for row in board]
        self.draw_count += 1


def make_game():
    view = FakeView()
    controller = GameController(view)
    return view, controller


def test_initial_state():
    view, _ = make_game()
    assert view.status == 'Turno de X'
    assert all(cell == ' ' for row in view.board for cell in row)


def test_turns_alternate():
    view, _ = make_game()
    view.column_handler(0)
    assert view.status == 'Turno de O'
    view.column_handler(1)
    assert view.status == 'Turno de X'


def test_piece_falls_to_bottom_and_stacks():
    view, _ = make_game()
    view.column_handler(2)
    view.column_handler(2)
    assert view.board[3][2] == 'X'
    assert view.board[2][2] == 'O'


def test_vertical_win_and_game_locks():
    view, _ = make_game()
    for _ in range(3):
        view.column_handler(0)
        view.column_handler(1)
    view.column_handler(0)
    assert view.status == '¡Gana X!'
    draws = view.draw_count
    view.column_handler(3)
    assert view.draw_count == draws
    assert view.status == '¡Gana X!'


def test_full_column_keeps_turn():
    view, _ = make_game()
    for _ in range(4):
        view.column_handler(0)
    view.column_handler(0)
    assert 'llena' in view.status
    assert 'Turno de X' in view.status
    view.column_handler(1)
    assert view.board[3][1] == 'X'


def test_restart_midgame():
    view, _ = make_game()
    view.column_handler(0)
    view.column_handler(1)
    view.restart_handler()
    assert view.status == 'Turno de X'
    assert all(cell == ' ' for row in view.board for cell in row)


def test_restart_after_win_allows_play():
    view, _ = make_game()
    for _ in range(3):
        view.column_handler(0)
        view.column_handler(1)
    view.column_handler(0)
    view.restart_handler()
    view.column_handler(4)
    assert view.board[3][4] == 'X'
    assert view.status == 'Turno de O'


def test_full_game_draw():
    view, _ = make_game()
    sequence = [0, 1, 0, 1, 1, 0, 1, 0,
                2, 3, 2, 3, 3, 2, 3, 2,
                4, 4, 4, 4]
    for col in sequence:
        view.column_handler(col)
    assert view.status == 'Empate'


def test_view_does_not_import_model():
    source = (ROOT / 'view' / 'gui_view.py').read_text(encoding='utf-8')
    for line in source.splitlines():
        stripped = line.strip()
        assert not stripped.startswith(('from model', 'import model'))


def test_model_does_not_import_gui():
    source = (ROOT / 'model' / 'game_model.py').read_text(encoding='utf-8')
    assert 'tkinter' not in source
