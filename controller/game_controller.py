# Controlador del juego Connect 4
"""Controlador de Conecta 4: coordina modelo y vista."""

from model.game_model import GameModel


class GameController:
    """Recibe los eventos de la vista y actualiza el modelo."""

    def __init__(self, view):
        self.view = view
        self.model = GameModel()
        self.game_over = False

        self.view.set_column_click_handler(self.on_column_click)
        self.view.set_restart_handler(self.restart)
        self._update_view(f'Turno de {self.model.current_player}')

    def on_column_click(self, col):
        """Procesa el clic en una columna."""
        if self.game_over:
            return

        player = self.model.current_player
        if not self.model.make_move(col, player):
            self.view.set_status(
                f'Columna {col + 1} llena. Turno de {player}')
            return

        if self.model.check_winner(player):
            self.game_over = True
            message = f'¡Gana {player}!'
        elif self.model.is_draw():
            self.game_over = True
            message = 'Empate'
        else:
            self.model.switch_player()
            message = f'Turno de {self.model.current_player}'
        self._update_view(message)

    def restart(self):
        """Inicia una partida nueva."""
        self.model = GameModel()
        self.game_over = False
        self._update_view(f'Turno de {self.model.current_player}')

    def _update_view(self, message):
        self.view.draw_board(self.model.board)
        self.view.set_status(message)
        