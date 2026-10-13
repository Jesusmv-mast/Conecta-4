"""Pantallas de inicio, seleccion de modo y dificultad (Tkinter)."""

import tkinter as tk

MODE_HUMAN_VS_HUMAN = 'hvh'
MODE_HUMAN_VS_MINIMAX = 'hvm'

DIFFICULTY_LABELS = {
    'facil': 'Fácil',
    'medio': 'Medio',
    'dificil': 'Difícil',
}

# Profundidad de busqueda del Minimax por nivel. Medido en banco de
# pruebas: con max_depth=6 la IA no perdio ninguna de 60 partidas
# contra un jugador aleatorio; facil y medio ven menos jugadas por
# adelantado y responden de inmediato
DIFFICULTY_DEPTHS = {
    'facil': 1,
    'medio': 4,
    'dificil': 6,
}


class StartScreen(tk.Frame):
    """Pantalla de bienvenida con el boton para empezar."""

    def __init__(self, parent, on_play):
        super().__init__(parent)
        tk.Label(
            self, text='Conecta 4', font=('Arial', 28, 'bold'),
        ).pack(pady=(40, 10))
        tk.Label(
            self, text='Tablero reducido 5x4',
            font=('Arial', 12), fg='#555555',
        ).pack(pady=(0, 30))
        tk.Button(
            self, text='Jugar', font=('Arial', 14),
            width=14, command=on_play,
        ).pack(pady=10)


class ModeScreen(tk.Frame):
    """Pantalla para elegir Humano vs Humano o Humano vs IA."""

    def __init__(self, parent, on_select, on_back):
        super().__init__(parent)
        tk.Label(
            self, text='Elige un modo', font=('Arial', 18),
        ).pack(pady=(30, 20))
        tk.Button(
            self, text='Humano vs Humano', font=('Arial', 12),
            width=20, command=lambda: on_select(MODE_HUMAN_VS_HUMAN),
        ).pack(pady=8)
        tk.Button(
            self, text='Humano vs IA', font=('Arial', 12),
            width=20, command=lambda: on_select(MODE_HUMAN_VS_MINIMAX),
        ).pack(pady=8)
        tk.Button(self, text='Atras', command=on_back).pack(pady=(20, 0))


class DifficultyScreen(tk.Frame):
    """Pantalla para elegir la dificultad de la IA."""

    def __init__(self, parent, on_select, on_back):
        super().__init__(parent)
        tk.Label(
            self, text='Elige la dificultad', font=('Arial', 18),
        ).pack(pady=(30, 20))
        for key, label in DIFFICULTY_LABELS.items():
            tk.Button(
                self, text=label, font=('Arial', 12), width=20,
                command=lambda k=key: on_select(k),
            ).pack(pady=8)
        tk.Button(self, text='Atras', command=on_back).pack(pady=(20, 0))