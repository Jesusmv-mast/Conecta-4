"""Pruebas del modelo de Conecta 4."""

import copy

from model.game_model import GameModel


def test_vertical_win():
    model = GameModel()
    for _ in range(4):
        model.make_move(0, 'X')
    assert model.check_winner('X')


def test_horizontal_win():
    model = GameModel()
    for col in range(4):
        model.make_move(col, 'X')
    assert model.check_winner('X')


def test_diagonal_win_ascending():
    model = GameModel()
    model.make_move(0, 'X')
    model.make_move(1, 'O')
    model.make_move(1, 'X')
    model.make_move(2, 'O')
    model.make_move(2, 'O')
    model.make_move(2, 'X')
    model.make_move(3, 'O')
    model.make_move(3, 'O')
    model.make_move(3, 'O')
    model.make_move(3, 'X')
    assert model.check_winner('X')


def test_diagonal_win_descending():
    model = GameModel()
    model.make_move(3, 'X')
    model.make_move(2, 'O')
    model.make_move(2, 'X')
    model.make_move(1, 'O')
    model.make_move(1, 'O')
    model.make_move(1, 'X')
    model.make_move(0, 'O')
    model.make_move(0, 'O')
    model.make_move(0, 'O')
    model.make_move(0, 'X')
    assert model.check_winner('X')


def test_no_winner_on_empty_board():
    model = GameModel()
    assert not model.check_winner('X')
    assert not model.check_winner('O')


def test_full_column_rejects_move():
    model = GameModel()
    for _ in range(4):
        assert model.make_move(2, 'X')
    assert not model.make_move(2, 'O')
    assert 2 not in model.get_available_moves()


def test_draw():
    model = GameModel()
    patterns = ('XXOO', 'OOXX', 'XXOO', 'OOXX', 'XXOO')
    for col, pattern in enumerate(patterns):
        for symbol in pattern:
            model.make_move(col, symbol)
    assert model.is_draw()
    assert not model.check_winner('X')
    assert not model.check_winner('O')


def test_undo_restores_board():
    model = GameModel()
    model.make_move(1, 'X')
    model.make_move(1, 'O')
    board_before = copy.deepcopy(model.board)
    heights_before = list(model.heights)
    model.make_move(3, 'X')
    model.undo_move(3)
    assert model.board == board_before
    assert model.heights == heights_before
