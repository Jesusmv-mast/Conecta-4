# Punto de entrada del juego Connect 4
"""Punto de entrada de Conecta 4."""

import tkinter as tk

from controller.game_controller import GameController
from model.game_model import COLS, ROWS
from view.gui_view import GameView


def main():
    root = tk.Tk()
    view = GameView(root, ROWS, COLS)
    GameController(view)
    root.mainloop()


if __name__ == '__main__':
    main()