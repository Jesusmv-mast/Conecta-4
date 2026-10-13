"""Punto de entrada de Conecta 4."""

import tkinter as tk

from view.app import ConnectFourApp


def main():
    root = tk.Tk()
    ConnectFourApp(root)
    root.mainloop()


if __name__ == '__main__':
    main()