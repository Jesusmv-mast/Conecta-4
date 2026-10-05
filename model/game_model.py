# Modelo del juego Connect 4
"""Modelo del juego Conecta 4 reducido."""

ROWS = 4
COLS = 5
CONNECT = 4
EMPTY = ' '


class GameModel:
    """Estado y reglas de la partida."""

    def __init__(self, rows=ROWS, cols=COLS, connect=CONNECT):
        self.rows = rows
        self.cols = cols
        self.connect = connect
        self.board = [[EMPTY] * cols for _ in range(rows)]
        self.heights = [0] * cols
        self.current_player = 'X'

    def get_available_moves(self):
        """Devuelve las columnas que aún tienen espacio."""
        return [c for c in range(self.cols) if self.heights[c] < self.rows]

    def make_move(self, col, player):
        """Coloca una ficha en la columna. Devuelve False si es inválido."""
        if col not in self.get_available_moves():
            return False
        row = self.rows - 1 - self.heights[col]
        self.board[row][col] = player
        self.heights[col] += 1
        return True

    def undo_move(self, col):
        """Retira la ficha superior de la columna (backtracking)."""
        self.heights[col] -= 1
        row = self.rows - 1 - self.heights[col]
        self.board[row][col] = EMPTY

    def switch_player(self):
        self.current_player = 'O' if self.current_player == 'X' else 'X'

    def check_winner(self, player):
        directions = ((0, 1), (1, 0), (1, 1), (1, -1))
        for r in range(self.rows):
            for c in range(self.cols):
                for dr, dc in directions:
                    if self._line_matches(r, c, dr, dc, player):
                        return True
        return False

    def is_draw(self):
        return not self.get_available_moves()

    def _line_matches(self, row, col, d_row, d_col, player):
        for i in range(self.connect):
            r = row + d_row * i
            c = col + d_col * i
            if not (0 <= r < self.rows and 0 <= c < self.cols):
                return False
            if self.board[r][c] != player:
                return False
        return True
    