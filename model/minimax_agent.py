"""Agente Minimax con poda Alfa-Beta y profundidad limitada.

El tablero reducido (5x4) es demasiado grande para explorarlo completo
en el primer movimiento (medido: mas de 60s sin poda, mas de 30s con
poda pero sin limite). Por eso se usa un limite de profundidad mas una
heuristica para los nodos donde la busqueda se corta antes de llegar
a un final real de partida.
"""

WINDOW_LENGTH = 4


class MinimaxAgent:
    """Decide la mejor jugada explorando el arbol de jugadas futuras."""

    def __init__(self, ai_player='O', human_player='X', max_depth=6):
        self.ai_player = ai_player
        self.human_player = human_player
        self.max_depth = max_depth
        self.nodes_evaluated = 0

    def evaluate_terminal(self, board, depth):
        """Puntua un estado terminal (victoria, derrota o empate)."""
        if board.check_winner(self.ai_player):
            return 10000 - depth
        if board.check_winner(self.human_player):
            return -10000 + depth
        return 0

    def evaluate_heuristic(self, board):
        """Puntua un estado NO terminal, cuando se corta por profundidad.

        Recorre todas las ventanas de 4 casillas en linea (horizontal,
        vertical y ambas diagonales) y suma puntos segun cuantas fichas
        de cada jugador contiene una ventana que no esta mezclada.
        """
        score = 0
        directions = ((0, 1), (1, 0), (1, 1), (1, -1))
        for r in range(board.rows):
            for c in range(board.cols):
                for dr, dc in directions:
                    window = self._window(board, r, c, dr, dc)
                    if window is not None:
                        score += self._score_window(window)
        return score

    def _window(self, board, row, col, d_row, d_col):
        cells = []
        for i in range(WINDOW_LENGTH):
            r = row + d_row * i
            c = col + d_col * i
            if not (0 <= r < board.rows and 0 <= c < board.cols):
                return None
            cells.append(board.board[r][c])
        return cells

    def _score_window(self, window):
        ai_count = window.count(self.ai_player)
        human_count = window.count(self.human_player)
        if ai_count > 0 and human_count > 0:
            return 0  # ventana mezclada, no la puede ganar nadie
        if ai_count == 3:
            return 5
        if ai_count == 2:
            return 2
        if human_count == 3:
            return -5
        if human_count == 2:
            return -2
        return 0

    def get_best_move(self, board):
        """Devuelve la mejor columna para la IA en el estado actual."""
        self.nodes_evaluated = 0
        best_score = -float('inf')
        best_move = None
        alpha, beta = -float('inf'), float('inf')
        for move in board.get_available_moves():
            board.make_move(move, self.ai_player)
            score = self._minimax(board, 1, alpha, beta, False)
            board.undo_move(move)
            if score > best_score:
                best_score = score
                best_move = move
            alpha = max(alpha, best_score)
        return best_move, best_score

    def _minimax(self, board, depth, alpha, beta, is_maximizing):
        self.nodes_evaluated += 1

        score = self.evaluate_terminal(board, depth)
        if score >= 9000 or score <= -9000:
            return score
        if not board.get_available_moves():
            return 0
        if depth >= self.max_depth:
            return self.evaluate_heuristic(board)

        if is_maximizing:
            best_score = -float('inf')
            for move in board.get_available_moves():
                board.make_move(move, self.ai_player)
                current = self._minimax(board, depth + 1, alpha, beta, False)
                board.undo_move(move)
                best_score = max(best_score, current)
                alpha = max(alpha, best_score)
                if beta <= alpha:
                    break
            return best_score
        else:
            best_score = float('inf')
            for move in board.get_available_moves():
                board.make_move(move, self.human_player)
                current = self._minimax(board, depth + 1, alpha, beta, True)
                board.undo_move(move)
                best_score = min(best_score, current)
                beta = min(beta, best_score)
                if beta <= alpha:
                    break
            return best_score
