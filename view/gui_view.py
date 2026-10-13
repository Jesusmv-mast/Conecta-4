"""Vista grafica de Conecta 4 con Tkinter."""

import tkinter as tk

CELL_SIZE = 80
PADDING = 10
MARGIN = 6
BOARD_COLOR = '#1e4fa3'
EMPTY_COLOR = '#f0f0f0'
PLAYER_COLORS = {'X': '#d62828', 'O': '#f7b500'}

MODE_LABELS = {
    'hvh': 'Humano vs Humano',
    'hvm': 'Humano vs IA (Minimax)',
}


class GameView:
    """Dibuja el tablero y reporta clics, modo y reinicio."""

    def __init__(self, root, rows, cols, container=None,
                 show_mode_selector=True):
        self.root = root
        self.rows = rows
        self.cols = cols
        self._column_handler = None
        self._mode_handler = None
        parent = container if container is not None else root

        if container is None:
            self.root.title('Conecta 4')
            self.root.resizable(False, False)

        if show_mode_selector:
            self.mode_var = tk.StringVar(value='hvh')
            self._build_mode_selector(parent)

        self.status_var = tk.StringVar()
        self.status_label = tk.Label(
            parent, textvariable=self.status_var, font=('Arial', 14))
        self.status_label.pack(pady=5)

        width = cols * CELL_SIZE + 2 * PADDING
        height = rows * CELL_SIZE + 2 * PADDING
        self.canvas = tk.Canvas(
            parent, width=width, height=height,
            bg=BOARD_COLOR, highlightthickness=0, bd=0)
        self.canvas.pack()

        self.restart_button = tk.Button(parent, text='Reiniciar')
        self.restart_button.pack(pady=5)

        self.metrics_var = tk.StringVar(value='')
        self.metrics_label = tk.Label(
            parent, textvariable=self.metrics_var,
            font=('Arial', 10), fg='#555555')
        self.metrics_label.pack(pady=(0, 5))

    def _build_mode_selector(self, parent):
        frame = tk.Frame(parent)
        frame.pack(pady=5)
        tk.Label(frame, text='Modo:').pack(side=tk.LEFT)
        for mode_key, label in MODE_LABELS.items():
            tk.Radiobutton(
                frame, text=label, variable=self.mode_var,
                value=mode_key, command=self._on_mode_change,
            ).pack(side=tk.LEFT, padx=5)

    def _on_mode_change(self):
        if self._mode_handler:
            self._mode_handler(self.mode_var.get())

    def set_column_click_handler(self, handler):
        self._column_handler = handler
        self.canvas.bind('<Button-1>', self._on_click)

    def set_restart_handler(self, handler):
        self.restart_button.config(command=handler)

    def set_mode_handler(self, handler):
        self._mode_handler = handler

    def set_status(self, text):
        self.status_var.set(text)

    def set_metrics(self, nodes, elapsed_seconds):
        """Muestra nodos explorados y tiempo de la ultima jugada de la IA."""
        self.metrics_var.set(
            f'Minimax: {nodes} nodos explorados, '
            f'{elapsed_seconds:.3f}s de respuesta')

    def clear_metrics(self):
        self.metrics_var.set('')

    def schedule_delayed(self, delay_ms, callback):
        """Ejecuta callback despues de delay_ms, sin congelar la ventana."""
        self.root.after(delay_ms, callback)

    def draw_board(self, board):
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