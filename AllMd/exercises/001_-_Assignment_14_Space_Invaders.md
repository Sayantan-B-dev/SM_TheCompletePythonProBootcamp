# Space Invaders – Multiplayer Web Game Documentation

## Table of Contents

1. [Introduction](#introduction)  
2. [Technology Stack](#technology-stack)  
3. [Project Structure](#project-structure)  
4. [Detailed Component Explanation](#detailed-component-explanation)  
    - 4.1 Backend – Flask Application (`__init__.py`, `run.py`)  
    - 4.2 Socket.IO Events and Game Management (`routes.py`)  
    - 4.3 Core Game Logic (`game_logic.py`)  
    - 4.4 Frontend – HTML Templates (`base.html`, `index.html`)  
    - 4.5 Frontend – Client-Side JavaScript (`game.js`)  
5. [Gameplay Mechanics](#gameplay-mechanics)  
6. [Communication Flow](#communication-flow)  
7. [Execution Flow](#execution-flow)  
8. [Diagrams](#diagrams)  
    - 8.1 System Architecture Diagram (Component View)  
    - 8.2 Data Flow Sequence Diagram  
9. [Setup and Running Instructions](#setup-and-running-instructions)  
10. [Conclusion](#conclusion)  

---

## 1. Introduction

This project implements a classic **Space Invaders** arcade game as a real‑time web application.  
It uses a **Flask** backend with **Flask‑SocketIO** to handle multiple concurrent players, each with their own isolated game instance.  
The frontend is a single‑page HTML5 canvas game that communicates with the server via WebSockets, ensuring smooth, low‑latency gameplay.

The game supports:
- Player movement (left/right) and shooting.
- Waves of aliens that move and drop.
- Collision detection (player bullets vs aliens, enemy bullets vs player, barriers).
- Score, level, and lives tracking.
- Game over and restart functionality.

The architecture is designed for clarity and educational purposes, with a clear separation between game logic, network handling, and presentation.

---

## 2. Technology Stack

| Component        | Technology                          | Purpose                                                  |
|------------------|-------------------------------------|----------------------------------------------------------|
| Backend          | Python 3.13+                        | Application logic and game state management              |
| Web Framework    | Flask 2.3.3                         | HTTP server, routing, template rendering                 |
| Real‑time        | Flask‑SocketIO 5.3.6                | WebSocket communication between server and clients       |
| Frontend         | HTML5, Tailwind CSS                  | Structure and styling of the game page                   |
| Graphics         | Canvas API                           | Drawing game elements (player, aliens, bullets, barriers)|
| Communication    | Socket.IO client library (v4.7.5)    | Client‑side WebSocket handling                           |

---

## 3. Project Structure

```
space_invaders/
├── app/
│   ├── __init__.py           # Flask application factory, SocketIO initialization
│   ├── game_logic.py         # Core game classes and constants
│   ├── routes.py             # Blueprint for HTTP routes and SocketIO event handlers
│   ├── static/
│   │   └── js/
│   │       └── game.js       # Client‑side JavaScript (canvas rendering, input)
│   └── templates/
│       ├── base.html         # Base template with Tailwind CSS
│       └── index.html        # Main game page (extends base)
├── requirements.txt          # Python dependencies
└── run.py                    # Entry point to start the server
```

---

## 4. Detailed Component Explanation

### 4.1 Backend – Flask Application (`__init__.py`, `run.py`)

**`app/__init__.py`**  
This file follows the **application factory pattern**.

- `socketio = SocketIO()` – creates a global SocketIO instance.
- `create_app()` – function that:
  - Creates a Flask app instance.
  - Sets a secret key (required for session management with SocketIO).
  - Registers the blueprint from `routes.py`.
  - Initialises `socketio` with the app using **threading mode** (`async_mode='threading'`). This mode uses Python threads, which is compatible with all environments (including Python 3.13) and avoids the need for eventlet or gevent.

**`run.py`**  
- Imports `create_app` and `socketio` from the app package.
- Creates the app.
- Calls `socketio.run(app, debug=True)` to start the development server with WebSocket support. The `debug=True` enables auto‑reloading on code changes.

### 4.2 Socket.IO Events and Game Management (`routes.py`)

This file defines a Flask **Blueprint** (`bp`) and all SocketIO event handlers.

- **`games` dictionary**: Maps a socket session ID (`sid`) to a `SpaceInvadersGame` instance. Each connected client gets its own isolated game.
- **`game_tasks` dictionary**: Stores the background thread (task) for each client, allowing the server to run the game loop independently per client.

#### HTTP Route
- `@bp.route('/')` – serves the main `index.html` page.

#### SocketIO Event Handlers

- **`handle_connect`** – triggered when a client connects.
  - Creates a new `SpaceInvadersGame` and stores it in `games[sid]`.
  - Starts a background task (`game_loop`) for that client and stores the task reference.
  - Emits a `'connected'` event back to the client.

- **`handle_disconnect`** – triggered on client disconnect.
  - Removes the game instance from `games`.
  - The background task will detect that the game is gone and terminate on its next iteration.

- **`handle_input`** – receives player input from the client.
  - Expects a JSON object with optional boolean fields: `left`, `right`, `shoot`.
  - Retrieves the game instance for the current socket and calls its `handle_input` method with those values.

- **`handle_reset`** – resets the game for the current client by calling `game.reset()`.

#### Background Game Loop (`game_loop`)

- Runs at approximately **60 frames per second**.
- While the client’s game still exists:
  - Records start time.
  - Calls `game.update()` – advances the game state by one tick.
  - Emits the serialised game state (`game.to_dict()`) to the client via `socketio.emit('game_state', ..., room=sid)`.
  - Calculates elapsed time and sleeps for the remainder of the frame (target 1/60 sec) to maintain a consistent tick rate.

### 4.3 Core Game Logic (`game_logic.py`)

This file contains all constants, the main `SpaceInvadersGame` class, and collision detection utilities.

#### Constants

All gameplay parameters are defined as uppercase constants for easy tweaking:

- `SCREEN_WIDTH`, `SCREEN_HEIGHT` – canvas dimensions (800x600).
- `PLAYER_WIDTH`, `PLAYER_HEIGHT`, `PLAYER_SPEED` – player dimensions and movement speed.
- `BULLET_WIDTH`, `BULLET_HEIGHT` – bullet size.
- `PLAYER_BULLET_SPEED`, `ENEMY_BULLET_SPEED` – bullet velocities (negative for upward).
- `MAX_PLAYER_BULLETS` – limits simultaneous shots from player.
- `ALIEN_ROWS`, `ALIEN_COLS`, `ALIEN_WIDTH`, `ALIEN_HEIGHT`, `ALIEN_SPACING` – alien grid layout.
- `ALIEN_BASE_SPEED`, `ALIEN_DROP_STEP`, `ALIEN_SHOOT_BASE_PROB` – movement and shooting probabilities.
- `USE_BARRIERS`, `BARRIER_COUNT`, `BARRIER_WIDTH`, `BARRIER_HEIGHT`, `BARRIER_Y`, `BARRIER_COLOR` – barrier configuration.
- `PLAYER_HITBOX_EXPANSION` – extra collision padding for the player (makes hit detection slightly more generous).

#### Class `SpaceInvadersGame`

**Attributes** (all initialised in `reset()`):

- `player` – dictionary with `x`, `y`, `width`, `height`.
- `aliens` – list of alien dictionaries, each with `x`, `y`, `width`, `height`, `active` flag, `row`, `col`, `color`.
- `player_bullets`, `enemy_bullets` – lists of bullet dictionaries.
- `barriers` – list of barrier block lists (each block is a dict with `x`, `y`, `width`, `height`, `active`).
- `score`, `level`, `lives` – game status.
- `game_over`, `game_win` – flags.
- `alien_direction`, `alien_move_counter`, `alien_move_delay` – for controlling alien movement pacing.
- `left_pressed`, `right_pressed` – current input states.

**Key Methods**:

- `reset()` – sets the game to initial state, creates aliens and barriers.
- `_create_aliens()` – populates the alien grid with rows and columns, assigning colours.
- `_create_barriers()` – builds barriers as 3×3 block matrices.
- `_player_hitbox()` – returns an expanded rectangle for player collision detection (using `PLAYER_HITBOX_EXPANSION`).
- `handle_input(left, right, shoot)` – updates input flags; if `shoot` is `True` and below bullet limit, adds a new player bullet.
- `update()` – called every game tick:
  - Moves player based on input.
  - Moves player bullets upward and removes off‑screen ones.
  - Moves aliens (only when move counter reaches delay, speed increases with level). Changes direction and drops aliens when edge is hit.
  - Alien shooting: random chance per alien to add an enemy bullet.
  - Moves enemy bullets downward, removes off‑screen.
  - Calls `_check_collisions()` to handle all collisions.
- `_check_collisions()` – handles:
  - Player bullets vs aliens (score +10).
  - Player bullets vs barrier blocks.
  - Enemy bullets vs player (hitbox, lose life, game over if lives = 0).
  - Enemy bullets vs barrier blocks.
  - Alien vs player (game over).
  - Aliens reaching the player’s y‑level (game over).
  - If all aliens destroyed, increases level and creates new aliens.
- `_rect_collide(r1, r2)` – static method for rectangle collision.
- `to_dict()` – returns a dictionary with only active game objects for JSON serialisation (used to send state to client).

### 4.4 Frontend – HTML Templates (`base.html`, `index.html`)

**`base.html`**  
- Base template with Tailwind CSS CDN.
- Defines a basic structure with a `<main>` block for content.

**`index.html`**  
- Extends `base.html`.
- Includes Socket.IO client library (`socket.io.min.js`).
- Adds custom styling for the canvas and game info.
- Displays score, level, lives in a retro‑style bar.
- Contains the `<canvas>` element (800×600) where the game is drawn.
- Provides keyboard/control hints.
- Includes the `game.js` script at the bottom.

### 4.5 Frontend – Client-Side JavaScript (`game.js`)

This script manages the client‑side experience.

**Global Variables**:
- `canvas`, `ctx` – canvas and 2D context.
- `gameState` – object mirroring the structure from the server (populated via socket updates).
- `leftPressed`, `rightPressed` – booleans tracking key states.

**Socket Event Handlers**:
- `socket.on('game_state', ...)` – updates `gameState` and refreshes the score display.
- `socket.on('connected', ...)` – logs connection and sends initial input.

**Input Handling**:
- `keydown` / `keyup` listeners for arrow keys, A/D (movement), Space (shoot), R (reset).
- Calls `sendInput()` after movement key changes to emit the current state of movement keys.
- Shoot key (Space) and mouse click on canvas emit an `'input'` event with `{ shoot: true }`.
- `sendInput()` emits `{ left: leftPressed, right: rightPressed }` (shoot is handled separately).

**Rendering** (`draw()`):
- Clears canvas with black background.
- Draws a starfield effect (random dots).
- Draws player (green rectangle with a small “cannon”).
- Draws player bullets (yellow) and enemy bullets (red).
- Draws each active alien with its assigned colour and two black “eyes”.
- Draws barrier blocks if active.
- If `gameOver` is true, overlays a translucent black layer and displays “GAME OVER” and restart hint.

**Game Loop**:
- `gameLoop()` calls `draw()` and requests the next animation frame.

---

## 5. Gameplay Mechanics

- **Player Movement**: Left/right arrow keys or A/D. Speed constant `PLAYER_SPEED`.
- **Shooting**: Space bar or mouse click. Limited to `MAX_PLAYER_BULLETS` simultaneous bullets. Bullets move upward at `PLAYER_BULLET_SPEED`.
- **Aliens**: Arranged in a grid. They move horizontally, change direction when hitting screen edge, and drop down. Movement speed increases with level (`ALIEN_BASE_SPEED * level`). Alien shooting probability also scales with level.
- **Collisions**:
  - Player bullet hits alien → alien disappears, +10 score.
  - Player bullet hits barrier block → block disappears.
  - Enemy bullet hits player → life lost, bullet removed.
  - Enemy bullet hits barrier block → block disappears.
  - Alien collides with player (using expanded hitbox) → game over.
  - Alien reaches player’s y‑level → game over.
- **Barriers**: Four barriers, each made of 3×3 blocks. They protect the player from enemy bullets but degrade over time.
- **Level Progression**: When all aliens are destroyed, `level` increments and a new wave is created. Alien speed and firing probability increase.
- **Game Over**: Triggered when lives reach zero or alien reaches player.
- **Reset**: Press ‘R’ to restart the current game (calls `socket.emit('reset')`).

---

## 6. Communication Flow

The communication between client and server is entirely event‑based via Socket.IO.

1. **Client connects** → server creates a game and starts a background loop.
2. **Client sends input** (movement, shoot) → server updates the game instance.
3. **Server game loop** updates the game state at ~60 Hz and emits `game_state` to the client.
4. **Client receives `game_state`**, updates its local copy, and redraws the canvas.
5. **Client disconnects** → server removes the game instance and the loop terminates.

This ensures that all game logic runs on the server, preventing cheating and keeping the client lightweight.

---

## 7. Execution Flow

1. User runs `python run.py`.
2. Flask development server starts, listening on `http://localhost:5000`.
3. User opens browser to that address.
4. Server serves `index.html` and `game.js`.
5. Client JavaScript establishes a WebSocket connection to the server.
6. Server’s `handle_connect` creates a game and starts the background loop.
7. Client sends input events as the user plays.
8. Server processes input and updates the game state.
9. Server pushes state updates to the client.
10. Client renders each frame.
11. On disconnect, server cleans up resources.

---

## 8. Diagrams

- **Corrected System Architecture Diagram**

```mermaid
graph TD
    subgraph Client [Browser]
        A["HTML Templates (base.html / index.html)"]
        B[Canvas Rendering Layer]
        C[game.js - Socket.IO Client]
    end

    subgraph Server [Flask + Socket.IO Server]
        D[Flask App Factory (__init__.py)]
        E[SocketIO Event Handlers (routes.py)]
        F[SpaceInvadersGame (game_logic.py)]
        G[Background Game Loop per Session]
    end

    C -- "WebSocket (input/reset)" --> E
    E -- "handle_input()" --> F
    E -- "reset()" --> F
    G -- "update() tick (~60 FPS)" --> F
    F -- "to_dict()" --> G
    G -- "emit('game_state')" --> C
    C -- "update local state" --> B
    B -- "render frame" --> A
    A -- "user interaction" --> C
```

- **Corrected Data Flow Sequence Diagram**

```mermaid
sequenceDiagram
    participant User
    participant Browser as Client (game.js)
    participant Server as Flask-SocketIO (routes.py)
    participant GameLogic as SpaceInvadersGame (game_logic.py)
    participant GameLoop as Background Game Loop

    User->>Browser: Press left arrow key
    Browser->>Server: emit("input", { left: true })
    Server->>GameLogic: handle_input(left=True)

    Note right of GameLogic: Sets left_pressed flag

    GameLoop->>GameLogic: update()
    GameLogic->>GameLogic: Apply movement using left_pressed
    GameLogic-->>GameLoop: Updated state via to_dict()

    GameLoop->>Server: emit("game_state", state, room=sid)
    Server->>Browser: game_state event
    Browser->>Browser: Replace gameState and draw()
    Browser->>User: Visual feedback rendered on canvas
```
---

## 9. Setup and Running Instructions

### Prerequisites
- Python 3.13 or later (any Python 3.8+ should work, but threading mode is compatible with 3.13).
- `pip` (Python package installer).

### Installation
1. Clone or download the project files.
2. Open a terminal in the project root.
3. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Server
```bash
python run.py
```
The server will start on `http://127.0.0.1:5000`. Open this URL in a web browser.

### Playing
- Use **Arrow keys** or **A/D** to move.
- Press **Space** or **click** on the canvas to shoot.
- Press **R** to restart the game.

---

## 10. Conclusion

This Space Invaders implementation demonstrates a clean, real‑time multiplayer architecture using Flask and Socket.IO.  
The separation of concerns (game logic, network layer, presentation) makes the code easy to maintain and extend.  
Potential enhancements could include:
- Adding sound effects.
- Storing high scores in a database.
- Adding power‑ups.
- Supporting multiple simultaneous players in a shared arena.

The documentation provided here covers every aspect of the system, from the low‑level collision detection to the high‑level communication patterns, making it suitable for both learning and production reference.