import streamlit as st
import random

st.set_page_config(page_title="Snake Game", page_icon="🐍")

GRID_SIZE = 12

# --- INITIALIZE SESSION STATE ---
if "snake" not in st.session_state:
    st.session_state.snake = [(5, 5)]
if "direction" not in st.session_state:
    st.session_state.direction = (0, 1)  # start moving right
if "food" not in st.session_state:
    st.session_state.food = (random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1))
if "alive" not in st.session_state:
    st.session_state.alive = True

# --- GAME LOGIC ---
def move_snake():
    if not st.session_state.alive:
        return

    head = st.session_state.snake[0]
    dx, dy = st.session_state.direction
    new_head = (head[0] + dx, head[1] + dy)

    # Check wall collision
    if not (0 <= new_head[0] < GRID_SIZE and 0 <= new_head[1] < GRID_SIZE):
        st.session_state.alive = False
        return

    # Check self collision
    if new_head in st.session_state.snake:
        st.session_state.alive = False
        return

    # Move
    st.session_state.snake = [new_head] + st.session_state.snake

    # Check if eating food
    if new_head == st.session_state.food:
        # Spawn new food
        while True:
            new_food = (random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1))
            if new_food not in st.session_state.snake:
                st.session_state.food = new_food
                break
    else:
        st.session_state.snake.pop()  # move without growing


# --- DRAW GRID ---
def draw_board():
    grid = [["⬛" for _ in range(GRID_SIZE)] for __ in range(GRID_SIZE)]

    # draw food
    fx, fy = st.session_state.food
    grid[fx][fy] = "🍎"

    # draw snake
    for i, (x, y) in enumerate(st.session_state.snake):
        grid[x][y] = "🟩" if i > 0 else "🟢"  # head is brighter

    board = "\n".join(" ".join(row) for row in grid)
    st.markdown(f"<pre style='font-size:20px'>{board}</pre>", unsafe_allow_html=True)


# --- UI ---
st.title("🐍 Snake (Turn-Based Version)")

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("⬆️ Up"):
        st.session_state.direction = (-1, 0)
with col2:
    if st.button("⬇️ Down"):
        st.session_state.direction = (1, 0)
with col3:
    if st.button("➡️ Right"):
        st.session_state.direction = (0, 1)

if st.button("⬅️ Left"):
    st.session_state.direction = (0, -1)

if st.button("Move"):
    move_snake()

draw_board()

if not st.session_state.alive:
    st.error("💀 Game Over!")
    if st.button("Restart"):
        st.session_state.snake = [(5, 5)]
        st.session_state.direction = (0, 1)
        st.session_state.food = (random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1))
        st.session_state.alive = True
