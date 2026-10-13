"""Pruebas del controlador en modo Humano vs IA (Dia 4 y Dia 5)."""

from controller.game_controller import (
    GameController, MODE_HUMAN_VS_HUMAN, MODE_HUMAN_VS_MINIMAX,
)


class FakeView:
    """Vista falsa que registra lo que el controlador le pide."""

    def __init__(self):
        self.status = ''
        self.board = None
        self.draw_count = 0
        self.column_handler = None
        self.restart_handler = None
        self.mode_handler = None
        self.metrics = None

    def set_column_click_handler(self, handler):
        self.column_handler = handler

    def set_restart_handler(self, handler):
        self.restart_handler = handler

    def set_mode_handler(self, handler):
        self.mode_handler = handler

    def set_status(self, text):
        self.status = text

    def draw_board(self, board):
        self.board = [row[:] for row in board]
        self.draw_count += 1

    def schedule_delayed(self, delay_ms, callback):
        """En pruebas no hay reloj real: se ejecuta de inmediato."""
        callback()

    def set_metrics(self, nodes, elapsed_seconds):
        self.metrics = (nodes, elapsed_seconds)

    def clear_metrics(self):
        self.metrics = None


def make_game():
    view = FakeView()
    controller = GameController(view)
    return view, controller


def test_default_mode_is_human_vs_human():
    view, controller = make_game()
    assert controller.mode == MODE_HUMAN_VS_HUMAN
    view.column_handler(0)
    # En HvH, tras el clic de X le toca a O, y nadie juega automatico.
    assert view.status == 'Turno de O'


def test_switching_mode_restarts_the_game():
    view, controller = make_game()
    view.column_handler(0)  # X juega, tablero deja de estar vacio
    view.mode_handler(MODE_HUMAN_VS_MINIMAX)
    assert controller.mode == MODE_HUMAN_VS_MINIMAX
    assert all(cell == ' ' for row in view.board for cell in row)
    assert view.status == 'Turno de X'


def test_ai_responds_automatically_after_human_move():
    view, controller = make_game()
    view.mode_handler(MODE_HUMAN_VS_MINIMAX)
    draws_before = view.draw_count
    view.column_handler(2)  # humano (X) juega
    # Debieron dibujarse 2 veces: la jugada humana y la respuesta de la IA.
    assert view.draw_count == draws_before + 2
    # Tras la respuesta de la IA, el turno debe volver a ser de X.
    assert view.status == 'Turno de X'
    assert controller.model.current_player == 'X'


def test_clicks_during_ai_turn_are_ignored():
    view, controller = make_game()
    view.mode_handler(MODE_HUMAN_VS_MINIMAX)
    view.column_handler(2)  # termina en turno de X otra vez (IA ya jugo)
    fichas_antes = sum(row.count('O') for row in view.board)
    # Forzamos el estado a mitad de jugada humana, para simular que
    # alguien hiciera clic cuando no le toca.
    controller.model.current_player = 'O'
    view.column_handler(1)
    fichas_despues = sum(row.count('O') for row in controller.model.board)
    assert fichas_despues == fichas_antes  # el clic se ignoro


def test_human_vs_human_mode_has_no_automatic_moves():
    view, controller = make_game()
    draws_before = view.draw_count
    view.column_handler(0)
    assert view.draw_count == draws_before + 1  # solo el clic humano


def test_restart_keeps_the_current_mode():
    view, controller = make_game()
    view.mode_handler(MODE_HUMAN_VS_MINIMAX)
    view.column_handler(2)
    view.restart_handler()
    assert controller.mode == MODE_HUMAN_VS_MINIMAX
    assert all(cell == ' ' for row in view.board for cell in row)


def test_metrics_recorded_after_ai_move():
    """Tras jugar la IA, la vista debe recibir nodos y tiempo medidos."""
    view, controller = make_game()
    view.mode_handler(MODE_HUMAN_VS_MINIMAX)
    view.column_handler(2)  # humano juega, la IA responde
    assert view.metrics is not None
    nodes, elapsed = view.metrics
    assert nodes == controller.agent.nodes_evaluated
    assert nodes > 0
    assert elapsed >= 0


def test_metrics_cleared_on_restart():
    """Al reiniciar, las metricas de la jugada anterior desaparecen."""
    view, controller = make_game()
    view.mode_handler(MODE_HUMAN_VS_MINIMAX)
    view.column_handler(2)
    assert view.metrics is not None
    view.restart_handler()
    assert view.metrics is None


def test_ai_wins_when_possible():
    """La IA conectada al controlador debe tomar una victoria obvia."""
    view, controller = make_game()
    view.mode_handler(MODE_HUMAN_VS_MINIMAX)
    model = controller.model
    # O (IA) ya tiene 3 en fila (columnas 0, 1, 2); falta la columna 3.
    model.make_move(0, 'O')
    model.make_move(4, 'X')
    model.make_move(1, 'O')
    model.make_move(4, 'X')
    model.make_move(2, 'O')
    model.current_player = 'O'  # forzamos a que le toque jugar a la IA
    controller._play_ai_turn()
    assert view.status == '¡Gana O!'
    assert controller.game_over