import tkinter as tk

from model.game_model import GameModel
from view.gui_view import GameView

root = tk.Tk()
model = GameModel()
view = GameView(root, model.rows, model.cols)

model.make_move(0, 'X')
model.make_move(0, 'O')
model.make_move(2, 'X')

view.draw_board(model.board)
view.set_status('Turno de X')
view.set_column_click_handler(lambda col: print('Columna', col))
root.mainloop()
