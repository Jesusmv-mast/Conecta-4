"""Pruebas del agente Minimax (Dia 3)."""

from model.game_model import GameModel
from model.minimax_agent import MinimaxAgent


def test_takes_immediate_win():
    """Si la IA puede ganar en esta jugada, debe tomarla."""
    model = GameModel()
    model.make_move(0, 'O')
    model.make_move(4, 'X')
    model.make_move(1, 'O')
    model.make_move(4, 'X')
    model.make_move(2, 'O')
    model.make_move(4, 'X')
    agent = MinimaxAgent(max_depth=6)
    move, score = agent.get_best_move(model)
    assert move == 3
    assert score > 9000


def test_blocks_opponent_win():
    """Si el humano puede ganar en su siguiente jugada, la IA bloquea."""
    model = GameModel()
    model.make_move(0, 'X')
    model.make_move(4, 'O')
    model.make_move(1, 'X')
    model.make_move(4, 'O')
    model.make_move(2, 'X')
    agent = MinimaxAgent(max_depth=6)
    move, _ = agent.get_best_move(model)
    assert move == 3


def test_board_unchanged_after_search():
    """La busqueda no debe dejar el tablero modificado (backtracking)."""
    model = GameModel()
    model.make_move(2, 'X')
    model.make_move(1, 'O')
    board_before = [row[:] for row in model.board]
    heights_before = list(model.heights)
    agent = MinimaxAgent(max_depth=6)
    agent.get_best_move(model)
    assert model.board == board_before
    assert model.heights == heights_before


def test_nodes_evaluated_increases_with_depth():
    """Mas profundidad debe explorar mas nodos (prueba de Backtracking)."""
    shallow = MinimaxAgent(max_depth=2)
    deep = MinimaxAgent(max_depth=6)
    shallow.get_best_move(GameModel())
    deep.get_best_move(GameModel())
    assert deep.nodes_evaluated > shallow.nodes_evaluated


def test_nodes_evaluated_resets_each_call():
    """El contador no debe acumularse entre jugadas distintas."""
    agent = MinimaxAgent(max_depth=4)
    model = GameModel()
    agent.get_best_move(model)
    first_count = agent.nodes_evaluated
    agent.get_best_move(model)
    second_count = agent.nodes_evaluated
    assert first_count == second_count


def test_evaluate_terminal_prefers_faster_win():
    """Ganar en menos jugadas debe puntuar mas alto."""
    agent = MinimaxAgent()
    model = GameModel()
    for _ in range(4):
        model.make_move(0, 'O')
    score_fast = agent.evaluate_terminal(model, depth=1)
    score_slow = agent.evaluate_terminal(model, depth=5)
    assert score_fast > score_slow


def test_heuristic_prefers_three_in_a_row_over_empty():
    """Una ventana con 3 fichas propias debe puntuar mejor que vacia."""
    agent = MinimaxAgent(ai_player='O', human_player='X')
    strong = GameModel()
    for col in range(3):
        strong.make_move(col, 'O')
    empty = GameModel()
    assert agent.evaluate_heuristic(strong) > agent.evaluate_heuristic(empty)


def test_heuristic_ignores_mixed_window():
    """Una ventana con fichas de ambos jugadores no suma ni resta."""
    agent = MinimaxAgent(ai_player='O', human_player='X')
    model = GameModel()
    model.make_move(0, 'O')
    model.make_move(1, 'X')
    model.make_move(2, 'O')
    model.make_move(3, 'X')
    # La fila de abajo completa (O X O X) es una ventana mezclada.
    row_window = [model.board[3][c] for c in range(4)]
    assert agent._score_window(row_window) == 0
