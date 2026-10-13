"""Controlador de Conecta 4: coordina modelo, vista y agentes de IA."""

import time

from model.game_model import GameModel
from model.minimax_agent import MinimaxAgent

MODE_HUMAN_VS_HUMAN = 'hvh'
MODE_HUMAN_VS_MINIMAX = 'hvm'
AI_THINK_DELAY_MS = 500


class GameController:
    """Recibe los eventos de la vista y actualiza el modelo."""

    def __init__(self, view, ai_player='O', human_player='X',
            mode=MODE_HUMAN_VS_HUMAN, max_depth=6):
        self.view = view
        self.ai_player = ai_player
        self.human_player = human_player
        self.mode = mode
        self.agent = MinimaxAgent(
            ai_player=ai_player, human_player=human_player,
            max_depth=max_depth)
        self.model = GameModel()
        self.game_over = False

        self.view.set_column_click_handler(self.on_column_click)
        self.view.set_restart_handler(self.restart)
        self.view.set_mode_handler(self.set_mode)
        self._update_view(f'Turno de {self.model.current_player}')

    def set_mode(self, mode):
        """Cambia de modo (Humano vs Humano / Humano vs IA) y reinicia."""
        self.mode = mode
        self.restart()

    def on_column_click(self, col):
        """Procesa el clic en una columna."""
        if self.game_over:
            return
        if self.mode == MODE_HUMAN_VS_MINIMAX:
            if self.model.current_player != self.human_player:
                return  # es turno de la IA, se ignora el clic

        self._play_move(col, self.model.current_player)

        if (not self.game_over
                and self.mode == MODE_HUMAN_VS_MINIMAX
                and self.model.current_player == self.ai_player):
            self.view.set_status('La IA está pensando...')
            self.view.schedule_delayed(AI_THINK_DELAY_MS, self._play_ai_turn)

    def _play_move(self, col, player):
        """Aplica una jugada (de humano o de IA) y actualiza la vista."""
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

    def _play_ai_turn(self):
        """Pide al agente su jugada, mide sus metricas y la aplica."""
        start = time.time()
        move, _ = self.agent.get_best_move(self.model)
        elapsed = time.time() - start
        self.view.set_metrics(self.agent.nodes_evaluated, elapsed)
        self._play_move(move, self.ai_player)

    def restart(self):
        """Inicia una partida nueva, conservando el modo actual."""
        self.model = GameModel()
        self.game_over = False
        self.view.clear_metrics()
        self._update_view(f'Turno de {self.model.current_player}')

    def _update_view(self, message):
        self.view.draw_board(self.model.board)
        self.view.set_status(message)