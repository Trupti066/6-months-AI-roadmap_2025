import streamlit as st
import random
import time
from dataclasses import dataclass
from typing import List, Tuple, Set
import numpy as np

# Grid settings
GRID_ROWS = 20
GRID_COLS = 20
CELL_SIZE_PX = 24

# Directions
UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)
OPPOSITE = {UP: DOWN, DOWN: UP, LEFT: RIGHT, RIGHT: LEFT}

@dataclass
class SnakeState:
    snake: List[Tuple[int, int]]
    direction: Tuple[int, int]
    food: Tuple[int, int]
    score: int
    speed_ms: int
    alive: bool
    paused: bool


def new_food(occupied: Set[Tuple[int, int]]) -> Tuple[int, int]:
    free = [
        (r, c)
        for r in range(GRID_ROWS)
        for c in range(GRID_COLS)
        if (r, c) not in occupied
    ]
    return random.choice(free) if free else (-1, -1)


def init_game() -> SnakeState:
    mid_r, mid_c = GRID_ROWS // 2, GRID_COLS // 2
    snake = [(mid_r, mid_c - 1), (mid_r, mid_c), (mid_r, mid_c + 1)]  # horizontal start
    direction = LEFT
    occupied = set(snake)
    food = new_food(occupied)
    return SnakeState(
        snake=snake,
        direction=direction,
        food=food,
        score=0,
        speed_ms=140,
        alive=True,
        paused=False,
    )


def move_snake(state: SnakeState) -> SnakeState:
    if not state.alive or state.paused:
        return state

    head_r, head_c = state.snake[0]
    dr, dc = state.direction
    new_head = (head_r + dr, head_c + dc)

    # Wall collision
    if not (0 <= new_head[0] < GRID_ROWS and 0 <= new_head[1] < GRID_COLS):
        state.alive = False
        return state

    # Self collision (allow tail cell only if not growing)
    will_grow = new_head == state.food
    body_cells = set(state.snake[:-1] if not will_grow else state.snake)
    if new_head in body_cells:
        state.alive = False
        return state

    state.snake.insert(0, new_head)

    if will_grow:
        state.score += 1
        occupied = set(state.snake)
        state.food = new_food(occupied)
    else:
        state.snake.pop()  # move forward

    return state


def change_direction(state: SnakeState, new_dir: Tuple[int, int]):
    if OPPOSITE.get(new_dir) == state.direction:
        return
    state.direction = new_dir


def draw_board(state: SnakeState):
    # Classic snake grid using a colored image
    cell = CELL_SIZE_PX
    height = GRID_ROWS * cell
    width = GRID_COLS * cell
    # Background
    img = np.zeros((height, width, 3), dtype=np.uint8)
    bg_light = np.array([30, 30, 30], dtype=np.uint8)
    bg_dark = np.array([38, 38, 38], dtype=np.uint8)
    # Checkerboard background for subtle grid effect
    for r in range(GRID_ROWS):
        for c in range(GRID_COLS):
            color = bg_light if (r + c) % 2 == 0 else bg_dark
            img[r*cell:(r+1)*cell, c*cell:(c+1)*cell] = color

    # Food
    fr, fc = state.food
    food_color = np.array([220, 60, 60], dtype=np.uint8)  # red
    img[fr*cell:(fr+1)*cell, fc*cell:(fc+1)*cell] = food_color

    # Snake body
    body_color = np.array([60, 200, 100], dtype=np.uint8)  # green
    for (r, c) in state.snake[1:]:
        img[r*cell:(r+1)*cell, c*cell:(c+1)*cell] = body_color

    # Snake head
    hr, hc = state.snake[0]
    head_color = np.array([250, 210, 70], dtype=np.uint8)  # yellow
    img[hr*cell:(hr+1)*cell, hc*cell:(hc+1)*cell] = head_color

    # Optional grid lines overlay
    line_color = (50, 50, 50)
    for r in range(GRID_ROWS + 1):
        img[min(r*cell, height-1), :, :] = line_color
    for c in range(GRID_COLS + 1):
        img[:, min(c*cell, width-1), :] = line_color

    st.image(img, caption=f"Score: {state.score}", use_container_width=False)


def main():
    st.set_page_config(page_title="Snake", page_icon="🐍", layout="centered")
    st.title("🐍 Snake")

    # Session state
    if "snake_state" not in st.session_state:
        st.session_state.snake_state = init_game()
    if "high_score" not in st.session_state:
        st.session_state.high_score = 0
    if "key_input" not in st.session_state:
        st.session_state.key_input = ""

    state: SnakeState = st.session_state.snake_state

    # Sidebar controls
    with st.sidebar:
        st.header("Controls")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("⬆️ Up"):
                change_direction(state, UP)
            if st.button("⬅️ Left"):
                change_direction(state, LEFT)
        with col2:
            if st.button("⬇️ Down"):
                change_direction(state, DOWN)
            if st.button("➡️ Right"):
                change_direction(state, RIGHT)
        st.markdown("---")
        state.paused = st.toggle("Pause", value=state.paused)
        speed = st.slider("Speed (ms/step)", 60, 300, state.speed_ms, 10)
        state.speed_ms = speed
        if st.button("Reset Game"):
            st.session_state.snake_state = init_game()
            st.rerun()

    # Keyboard input (focus this box and press W/A/S/D)
    def _on_key_change():
        key = (st.session_state.key_input or "").strip()
        if not key:
            return
        k = key.lower()
        if k in ("w", "arrowup", "up"):
            change_direction(state, UP)
        elif k in ("s", "arrowdown", "down"):
            change_direction(state, DOWN)
        elif k in ("a", "arrowleft", "left"):
            change_direction(state, LEFT)
        elif k in ("d", "arrowright", "right"):
            change_direction(state, RIGHT)
        st.session_state.key_input = ""

    st.text_input(
        "Keyboard (focus here; use W/A/S/D or type 'up/down/left/right')",
        key="key_input",
        on_change=_on_key_change,
        placeholder="Press keys while this box is focused",
    )

    # Stats
    cols = st.columns(3)
    cols[0].metric("Score", state.score)
    cols[1].metric("High Score", st.session_state.high_score)
    cols[2].metric("Status", "Alive" if state.alive else "Game Over")

    draw_board(state)

    # Auto tick
    if state.alive and not state.paused:
        time.sleep(state.speed_ms / 1000.0)
        st.session_state.snake_state = move_snake(state)
        st.session_state.high_score = max(st.session_state.high_score, state.score)
        st.rerun()
    elif not state.alive:
        st.success(f"Final score: {state.score}")
        if st.button("Play Again"):
            st.session_state.snake_state = init_game()
            st.rerun()


if __name__ == "__main__":
    main()
