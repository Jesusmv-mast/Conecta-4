"""Vista gráfica de Conecta 4 con Tkinter."""

import tkinter as tk

CELL_SIZE = 80
PADDING = 10
MARGIN = 6
BOARD_COLOR = '#1e4fa3'
EMPTY_COLOR = '#f0f0f0'
PLAYER_COLORS = {'X': '#d62828', 'O': '#f7b500'}


class GameView:
    """Dibuja el tablero y reporta los clics. No contiene lógica de juego."""

    def __init__(self, root, rows, cols):
        self.root = root
        self.rows = rows
        self.cols = cols
        self._column_handler = None

        self.root.title('Conecta 4')
        self.root.resizable(False, False)

        self.status_var = tk.StringVar()
        self.status_label = tk.Label(
            root, textvariable=self.status_var, font=('Arial', 14))
        self.status_label.pack(pady=5)

        width = cols * CELL_SIZE + 2 * PADDING
        height = rows * CELL_SIZE + 2 * PADDING
        self.canvas = tk.Canvas(
            root, width=width, height=height,
            bg=BOARD_COLOR, highlightthickness=0, bd=0)
        self.canvas.pack()

        self.restart_button = tk.Button(root, text='Reiniciar')
        self.restart_button.pack(pady=5)

    def set_column_click_handler(self, handler):
        """Registra la función que se llamará con el número de columna."""
        self._column_handler = handler
        self.canvas.bind('<Button-1>', self._on_click)

    def set_restart_handler(self, handler):
        self.restart_button.config(command=handler)

    def set_status(self, text):
        self.status_var.set(text)

    def draw_board(self, board):
        """Redibuja todo el tablero a partir de una matriz de fichas."""
        self.canvas.delete('all')
        for r in range(self.rows):
            for c in range(self.cols):
                x0 = PADDING + c * CELL_SIZE + MARGIN
                y0 = PADDING + r * CELL_SIZE + MARGIN
                x1 = x0 + CELL_SIZE - 2 * MARGIN
                y1 = y0 + CELL_SIZE - 2 * MARGIN
                color = PLAYER_COLORS.get(board[r][c], EMPTY_COLOR)
                self.canvas.create_oval(
                    x0, y0, x1, y1, fill=color, outline=color)

    def _on_click(self, event):
        left = PADDING + MARGIN
        right = PADDING + self.cols * CELL_SIZE - MARGIN
        top = PADDING + MARGIN
        bottom = PADDING + self.rows * CELL_SIZE - MARGIN
        if not (left <= event.x < right and top <= event.y < bottom):
            return
        col = (event.x - PADDING) // CELL_SIZE
        if self._column_handler:
            self._column_handler(col)