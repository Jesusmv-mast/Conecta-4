# Conecta 4

Juego de **Conecta 4** en escritorio, escrito en Python con una arquitectura **MVC**
(Modelo–Vista–Controlador). Es una versión reducida del clásico: un tablero de
**4 filas × 5 columnas** donde gana quien consiga **4 fichas seguidas**.

![Python](https://img.shields.io/badge/python-3.14-blue?style=flat-square&logo=python&logoColor=white)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-1e4fa3?style=flat-square)
![Arquitectura](https://img.shields.io/badge/arquitectura-MVC-green?style=flat-square)

---

## ✨ Características

- Tablero compacto de **4 × 5** (fácil de probar y depurar).
- Detección de victoria en las **4 direcciones**: horizontal, vertical y las dos diagonales.
- Detección de **empate** cuando el tablero se llena.
- Fichas que **caen por gravedad** al fondo de la columna.
- Columna llena → el movimiento se rechaza con un aviso en pantalla.
- Botón **Reiniciar** para empezar una partida nueva.
- La vista no contiene lógica de juego: solo dibuja y reporta clics.

---

## 🚀 Requisitos

- **Python 3.10 o superior**
- **Tkinter** — incluido en la instalación estándar de Python en Windows y macOS.
  En Linux puede hacer falta instalarlo:

  ```bash
  # Debian / Ubuntu
  sudo apt install python3-tk
  ```

No hay dependencias externas: el juego usa solo la biblioteca estándar.

---

## ▶️ Ejecutar

Desde la raíz del proyecto:

```bash
python main.py
```

> Es importante ejecutarlo desde la raíz, porque los módulos se importan como
> `model.game_model`, `view.gui_view` y `controller.game_controller`.

---

## 🕹️ Cómo jugar

1. Haz clic en una **columna** para soltar tu ficha.
2. Las fichas caen hasta el fondo o hasta la pila de la columna.
3. Cambia de turno automáticamente: empieza **X** (rojo), luego **O** (amarillo).
4. Gana quien consiga **4 fichas en línea** (horizontal, vertical o diagonal).
5. Si el tablero se llena sin ganador, hay **empate**.
6. Pulsa **Reiniciar** para jugar otra vez.

La barra superior muestra el estado: de quién es el turno, la victoria, el empate
o el aviso de columna llena.

---

## 📁 Estructura del proyecto

```
connect4/
├── main.py                     # Punto de entrada: crea vista, controlador y bucle
├── controller/
│   └── game_controller.py      # Coordina modelo y vista, maneja los eventos
├── model/
│   └── game_model.py           # Estado y reglas de la partida
├── view/
│   └── gui_view.py             # Dibujo con Tkinter y captura de clics
├── tests/
│   └── test_game_model.py      # 10 tests de integración (modelo + controlador)
├── README.md
├── .gitignore
└── .flake8                     # Configuración de flake8
```

Cada paquete incluye su `__init__.py` para ser importado como módulo.

---

## 🧱 Arquitectura MVC

El proyecto separa las tres responsabilidades. La comunicación siempre pasa por
el controlador: la vista nunca toca el modelo directamente.

```
        ┌───────────────────────────────┐
        │            Vista              │
        │  view/gui_view.py             │
        │  dibuja el tablero            │
        │  emite clics de columna       │
        └───────────┬───────────────────┘
                    │  handler(col) / reiniciar
                    ▼
        ┌───────────────────────────────┐
        │         Controlador           │
        │  controller/game_controller.py│
        │  decide qué hacer con cada    │
        │  evento y qué mensaje mostrar │
        └───────────┬───────────────────┘
             ▲      │ make_move / check_winner
             │      ▼
        ┌───────────────────────────────┐
        │           Modelo              │
        │  model/game_model.py          │
        │  tablero, reglas, turnos      │
        └───────────────────────────────┘
```

### Flujo de un clic

1. El usuario hace clic → `GameView._on_click` valida que el clic caiga dentro
   del tablero y calcula la columna.
2. Llama al handler registrado → `GameController.on_column_click(col)`.
3. El controlador pide al modelo `make_move(col, player)`.
   - Si devuelve `False`, la columna está llena y solo se avisa.
4. Comprueba `check_winner` → `is_draw` → si no hay fin, `switch_player`.
5. El controlador llama `_update_view(mensaje)`, que redibuja el tablero y
   actualiza la barra de estado.

---

## 🗃️ Estructura de datos principal

El modelo se apoya en dos estructuras clave:

| Estructura | Definición | Para qué sirve |
|---|---|---|
| `board` | Lista de listas `board[ fila ][ columna ]` con `' '`, `'X'` u `'O'` | Representación del tablero para dibujarlo y leer líneas |
| `heights` | Lista de `cols` enteros: `heights[c]` = fichas apiladas en la columna `c` | Calcular dónde cae la siguiente ficha **en O(1)** sin recorrer la columna |

### Constantes

```python
ROWS = 4        # filas
COLS = 5        # columnas
CONNECT = 4     # fichas seguidas para ganar
EMPTY = ' '     # casilla vacía
```

Son parámetros por defecto del constructor, así que se puede jugar con otros
tamaños:

```python
model = GameModel(rows=6, cols=7, connect=4)   # Conecta 4 clásico
```

---

## 🔍 Detección de ganador

Para cada casilla del tablero se prueban **4 direcciones**:

```python
directions = ((0, 1),    # →  horizontal
              (1, 0),    # ↓  vertical
              (1, 1),    # ↘  diagonal descendente
              (1, -1))   # ↙  diagonal ascendente
```

`_line_matches` avanza `connect` pasos en esa dirección y comprueba que:

- todas las casillas quedan **dentro del tablero** (si se sale, descarta),
- todas contienen la **ficha del jugador**.

Si alguna dirección coincide, hay victoria. Coste: **O(filas × columnas × 4 × connect)**,
despreciable para tableros pequeños.

---

## 🧪 Tests

```bash
python -m pytest tests -v
```

> `pytest` está instalado en el `venv` del proyecto. Si no lo tienes:
> `pip install pytest`

**10 tests, todos pasando.** Están en `tests/test_game_model.py` y son de
**integración**: simulan partidas humanas usando una **vista falsa**
(`FakeView`), así que prueban modelo + controlador juntos **sin abrir ventanas**.

| Test | Qué verifica |
|---|---|
| `test_initial_state` | Tablero vacío y mensaje *"Turno de X"* al inicio |
| `test_turns_alternate` | Los turnos alternan X → O → X |
| `test_piece_falls_to_bottom_and_stacks` | Las fichas caen al fondo y se apilan |
| `test_vertical_win_and_game_locks` | Victoria vertical y que el juego **se bloquea** después |
| `test_full_column_keeps_turn` | Columna llena: no pierde el turno ni cambia el tablero |
| `test_restart_midgame` | Reiniciar a mitad de partida limpia todo |
| `test_restart_after_win_allows_play` | Tras ganar y reiniciar, se puede volver a jugar |
| `test_full_game_draw` | Secuencia completa de 20 movimientos → *Empate* |
| `test_view_does_not_import_model` | **Aislamiento MVC**: la vista no importa el modelo |
| `test_model_does_not_import_gui` | **Aislamiento MVC**: el modelo no usa `tkinter` |

Los dos últimos son reglas de arquitectura: garantizan que la separación MVC no
se rompa con el tiempo.

### El patrón `FakeView`

```python
class FakeView:
    """Vista falsa que registra lo que el controlador le pide."""
    def set_column_click_handler(self, handler): ...
    def set_restart_handler(self, handler): ...
    def set_status(self, text): ...
    def draw_board(self, board): ...
```

Implementa la misma interfaz que `GameView`, pero en lugar de dibujar **guarda
lo que le llega**. Así se puede escribir:

```python
view, _ = make_game()
view.column_handler(0)              # como si el usuario hiciera clic
assert view.status == 'Turno de O'  # comprobar el resultado
```

Es **pruebas de doble (*test double*)**: se testea la lógica sin depender de la
GUI. Gracias a esto los tests corren en `0.07 s` y funcionan sin pantalla
(incluso en CI).

---

## 🔧 Código de estilo

El proyecto sigue **PEP 8** con `max-line-length = 79`, configurado en `.flake8`:

```bash
python -m flake8 .
```

> `flake8` está en el `venv`. Excluye `venv`, `__pycache__` y `.git`.

**Estado actual: 10 avisos menores**, todos de formato, ninguno es un error de
lógica. Todos siguen el mismo patrón: sobran espacios en la última línea y
falta el salto de línea final del archivo.

- `W293` — línea en blanco con espacios (5 archivos)
- `W292` — falta salto de línea al final de archivo (5 archivos)

Afecta a: `main.py`, `controller/game_controller.py`, `model/game_model.py`,
`view/gui_view.py` y `tests/test_game_model.py`.

---

## 💡 Posibles mejoras

- **[ ]** IA rival con minimax y poda alfa-beta (aprovechando `undo_move`,
  que ya existe para *backtracking*).
- **[ ]** Marcar visualmente las 4 fichas ganadoras.
- **[ ]** Contador de victorias X vs. O.
- **[x]** Escribir tests del modelo → 10 tests ✔
- **[ ]** Animación de la ficha al caer.
- **[ ]** Limpiar los 10 avisos de `flake8` (espacios finales y falta de salto
  de línea al final de archivo).

---

## 📄 Licencia

Proyecto académico — *Estructura de Datos II*.
