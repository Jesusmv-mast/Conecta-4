"""Orquesta las pantallas: Inicio -> Modo -> Dificultad -> Juego."""

import tkinter as tk

from controller.game_controller import GameController
from model.game_model import COLS, ROWS
from view.gui_view import GameView
from view.menu_view import (
    DIFFICULTY_DEPTHS,
    MODE_HUMAN_VS_HUMAN,
    MODE_HUMAN_VS_MINIMAX,
    DifficultyScreen,
    ModeScreen,
    StartScreen,
)


class ConnectFourApp:
    """Controla que pantalla se muestra y arranca la partida."""

    def __init__(self, root):
        self.root = root
        self.root.title('Conecta 4')
        self.root.resizable(False, False)

        self.container = tk.Frame(root)
        self.container.pack()

        self._current_frame = None
        self._chosen_mode = MODE_HUMAN_VS_HUMAN
        self.show_start()

    def _clear(self):
        if self._current_frame is not None:
            self._current_frame.destroy()
            self._current_frame = None

    def show_start(self):
        self._clear()
        self._current_frame = StartScreen(self.container, self.show_mode)
        self._current_frame.pack()

    def show_mode(self):
        self._clear()
        self._current_frame = ModeScreen(
            self.container, self._on_mode_selected, self.show_start)
        self._current_frame.pack()

    def _on_mode_selected(self, mode):
        self._chosen_mode = mode
        if mode == MODE_HUMAN_VS_MINIMAX:
            self.show_difficulty()
        else:
            self.start_game(mode, max_depth=6)

    def show_difficulty(self):
        self._clear()
        self._current_frame = DifficultyScreen(
            self.container, self._on_difficulty_selected, self.show_mode)
        self._current_frame.pack()

    def _on_difficulty_selected(self, difficulty_key):
        max_depth = DIFFICULTY_DEPTHS[difficulty_key]
        self.start_game(self._chosen_mode, max_depth)

    def start_game(self, mode, max_depth):
        self._clear()
        game_frame = tk.Frame(self.container)
        game_frame.pack()

        view = GameView(
            self.root, ROWS, COLS, container=game_frame,
            show_mode_selector=False)
        tk.Button(
            game_frame, text='Menu principal', command=self.show_start,
        ).pack(pady=(0, 10))

        GameController(view, mode=mode, max_depth=max_depth)
        self._current_frame = game_frame