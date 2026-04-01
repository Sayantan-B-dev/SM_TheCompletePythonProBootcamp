```py
matrix = [[' ', ' ', ' '],
          [' ', ' ', ' '],
          [' ', ' ', ' ']]

def display(m):
    for row in m:
        print("["+",".join(row)+"]")
    print()

def input_value():
    """Ask first player to choose X or O"""
    inp = ''
    while inp not in ['x', 'o']:
        inp = input("Select your symbol (X or O): ").lower()
        if inp not in ['x', 'o']:
            print("[[ Please select either X or O ]]")
    return inp

def select_position():
    """Ask player to choose position (1-9) and return (row, col)"""
    matrix_pos = {
        1:[0,0], 2:[0,1], 3:[0,2],
        4:[1,0], 5:[1,1], 6:[1,2],
        7:[2,0], 8:[2,1], 9:[2,2]
    }
    pos = ''
    while pos not in range(1,10):
        pos = input("Choose a position (1-9): ")
        try:
            pos = int(pos)
        except ValueError:
            print("[[ Please enter a number between 1-9 ]]")
            continue
        if pos not in range(1,10):
            print("[[ Invalid choice. Try again (1-9) ]]")
    return matrix_pos[pos]

def new_matrix(inp, row, col):
    """Place symbol if position is free. Return True/False"""
    if matrix[row][col] == ' ':
        matrix[row][col] = inp
        return True
    else:
        print("[[ That position is already taken! ]]")
        return False

def check_winner():
    """Check if there is a winner"""
    for i in range(3):
        # Rows
        if matrix[i][0] == matrix[i][1] == matrix[i][2] != ' ':
            return matrix[i][0]
        # Columns
        if matrix[0][i] == matrix[1][i] == matrix[2][i] != ' ':
            return matrix[0][i]
    # Diagonals
    if matrix[0][0] == matrix[1][1] == matrix[2][2] != ' ':
        return matrix[0][0]
    if matrix[0][2] == matrix[1][1] == matrix[2][0] != ' ':
        return matrix[0][2]
    return None

def is_draw():
    """Check if the game is a draw"""
    for row in matrix:
        if ' ' in row:
            return False
    return True

def reset_board():
    """Reset the board for new game"""
    global matrix
    matrix = [[' ', ' ', ' '],
              [' ', ' ', ' '],
              [' ', ' ', ' ']]

def game():
    """Main game loop"""
    reset_board()

    # Player chooses X or O
    player1 = input_value()
    player2 = 'o' if player1 == 'x' else 'x'
    current_player = player1

    print(f"Player 1 is [{player1.upper()}], Player 2 is [{player2.upper()}]")

    while True:
        print(f"Player {current_player.upper()}'s turn")
        display(matrix)

        row, col = select_position()

        if not new_matrix(current_player, row, col):
            continue  # invalid move, retry

        winner = check_winner()
        if winner:
            display(matrix)
            print(f"[[ Player {winner.upper()} wins! ]]")
            break

        if is_draw():
            display(matrix)
            print("[[ It's a draw! ]]")
            break

        # Switch turn
        current_player = player2 if current_player == player1 else player1

    # Ask if want to play again
    again = input("Do you want to play again? (y/n): ").lower()
    if again == 'y':
        game()
    else:
        print("Thanks for playing!")

# Start the game
game()
```

# Tic Tac Toe Game Documentation

This is a simple two-player console-based Tic Tac Toe game written in Python. Players take turns placing their symbols (X or O) on a 3×3 grid. The game checks for a winner or a draw after each move and offers the option to play again.

## Table of Contents
- [Global Variable](#global-variable)
- [Functions](#functions)
  - [`display(m)`](#displaym)
  - [`input_value()`](#input_value)
  - [`select_position()`](#select_position)
  - [`new_matrix(inp, row, col)`](#new_matrixinp-row-col)
  - [`check_winner()`](#check_winner)
  - [`is_draw()`](#is_draw)
  - [`reset_board()`](#reset_board)
  - [`game()`](#game)
- [How to Play](#how-to-play)
- [Example Game Flow](#example-game-flow)

---

## Global Variable
- `matrix` – A list of lists representing the 3×3 game board. Initially filled with spaces (`' '`). It is modified by `new_matrix()` and reset by `reset_board()`.

---

## Functions

### `display(m)`
**Purpose:** Prints the current state of the board in a readable format.  
**Parameters:**  
- `m` – The game board (a list of 3 lists, each containing 3 characters).  
**Returns:** Nothing.  
**Behavior:** Iterates through each row and prints it as `[x,o,x]` style.

---

### `input_value()`
**Purpose:** Asks the first player to choose their symbol (X or O).  
**Returns:** A lowercase string `'x'` or `'o'`.  
**Behavior:** Loops until a valid input (`'x'` or `'o'`) is provided. Rejects invalid entries with an error message.

---

### `select_position()`
**Purpose:** Prompts the current player to choose a position on the board (1–9) and converts it to grid coordinates.  
**Returns:** A list `[row, col]` where `row` and `col` are integers (0–2).  
**Behavior:** Uses a dictionary to map numbers 1–9 to row/column indices. Validates that the input is an integer between 1 and 9; repeats until valid.

---

### `new_matrix(inp, row, col)`
**Purpose:** Attempts to place the player's symbol at the specified position.  
**Parameters:**  
- `inp` – The symbol to place (`'x'` or `'o'`).  
- `row` – Row index (0–2).  
- `col` – Column index (0–2).  
**Returns:** `True` if placement was successful (the cell was empty); `False` otherwise.  
**Behavior:** Checks if the target cell is empty (`' '`). If yes, places the symbol and returns `True`. If not, prints an error message and returns `False`.

---

### `check_winner()`
**Purpose:** Checks if there is a winner after the latest move.  
**Returns:** The winning symbol (`'x'` or `'o'`) if a player has won; otherwise `None`.  
**Behavior:** Examines all rows, columns, and both diagonals for three identical non‑empty symbols. Returns the first winning symbol found.

---

### `is_draw()`
**Purpose:** Determines whether the game has ended in a draw (no empty cells left and no winner).  
**Returns:** `True` if the board is full (no `' '` characters); `False` otherwise.  
**Behavior:** Iterates through all rows and checks for any empty space.

---

### `reset_board()`
**Purpose:** Resets the global `matrix` to a fresh empty board.  
**Parameters:** None.  
**Returns:** Nothing.  
**Behavior:** Reassigns `matrix` to a new 3×3 list of spaces. Uses the `global` keyword because `matrix` is modified.

---

### `game()`
**Purpose:** The main game loop. Handles player turns, move validation, win/draw detection, and replay option.  
**Parameters:** None.  
**Returns:** Nothing (but may recursively call itself for a new game).  
**Behavior:**  
1. Resets the board.  
2. Asks Player 1 to choose X or O (`input_value`).  
3. Sets Player 2 to the opposite symbol.  
4. Alternates turns, displaying the board before each move.  
5. Validates moves with `new_matrix`; repeats if move is invalid.  
6. After each successful move, checks for a winner (`check_winner`) or a draw (`is_draw`).  
7. If the game ends, displays the final board and announces the result.  
8. Asks if players want another game. If yes, calls `game()` again; otherwise prints a goodbye message.

---

## How to Play
1. Run the script.  
2. Player 1 chooses either **X** or **O**.  
3. Players take turns selecting a position from **1 to 9**, where the board positions are numbered as:
   ```
   1 | 2 | 3
   ---------
   4 | 5 | 6
   ---------
   7 | 8 | 9
   ```
4. The game announces the winner or a draw when the board is full.  
5. After the game, you can choose to play again (`y`) or quit (`n`).

---

## Example Game Flow
```
Select your symbol (X or O): x
Player 1 is [X], Player 2 is [O]

Player X's turn
[ , , ]
[ , , ]
[ , , ]

Choose a position (1-9): 5

Player O's turn
[ , , ]
[ ,X, ]
[ , , ]

Choose a position (1-9): 1

Player X's turn
[O, , ]
[ ,X, ]
[ , , ]

Choose a position (1-9): 9

Player O's turn
[O, , ]
[ ,X, ]
[ , ,X]

Choose a position (1-9): 3

[O, ,O]
[ ,X, ]
[ , ,X]

Player O wins!  (three O's in the first row)
```

---

**Note:** The code uses recursion for replay, which is fine for a few games but could theoretically hit recursion depth limits if played hundreds of times. For a more robust implementation, a loop would be preferable, but for casual use it works perfectly.