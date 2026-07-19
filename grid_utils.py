"""
grid_utils.py
--------------
Helper functions for the Warehouse Robot Pathfinder.

Covers:
  - load_data()        : load a warehouse layout from a JSON file (sample dataset)
  - generate_warehouse(): create a random warehouse layout (custom input)
  - validate_grid()    : Problem Setup Module input validation
  - draw_grid()        : Visual UI Module - render the warehouse grid + path/exploration
"""

import json
import random

import matplotlib.pyplot as plt
import numpy as np


# ---------------------------------------------------------------------------
# Data loading (load_data)
# ---------------------------------------------------------------------------
def load_warehouse(path):
    """Load a warehouse layout from a JSON file.

    Expected JSON structure:
        {
            "grid": [[0,1,0,...], ...],       # 0 = free, 1 = obstacle (shelf)
            "cost_grid": [[1,1,3,...], ...],  # movement cost to ENTER each cell
            "start": [row, col],              # robot's charging dock
            "goal": [row, col]                # target shelf location
        }
    """
    with open(path, "r") as f:
        data = json.load(f)
    grid = data["grid"]
    cost_grid = data["cost_grid"]
    start = tuple(data["start"])
    goal = tuple(data["goal"])
    return grid, cost_grid, start, goal


# ---------------------------------------------------------------------------
# Random warehouse generation (Problem Setup - custom input)
# ---------------------------------------------------------------------------
def generate_warehouse(rows, cols, obstacle_density=0.2, narrow_aisle_prob=0.15, seed=42):
    """Generate a random warehouse grid.

    - 0           : free aisle (cost 1)
    - 1           : obstacle / shelving unit (impassable)
    - cost_grid=3 : narrow aisle (passable, but costs more to traverse -
                    represents the robot slowing down for safety)

    The function guarantees that the start (top-left) and goal (bottom-right)
    cells are always free, and re-rolls the random grid (up to 50 times) until
    a path between them exists, so the user never gets an unsolvable random map.
    """
    start = (0, 0)
    goal = (rows - 1, cols - 1)

    for attempt in range(50):
        rng = random.Random(seed + attempt)
        grid = [[0] * cols for _ in range(rows)]
        cost_grid = [[1] * cols for _ in range(rows)]

        for r in range(rows):
            for c in range(cols):
                if rng.random() < obstacle_density:
                    grid[r][c] = 1
                elif rng.random() < narrow_aisle_prob:
                    cost_grid[r][c] = 3

        grid[start[0]][start[1]] = 0
        grid[goal[0]][goal[1]] = 0
        cost_grid[start[0]][start[1]] = 1
        cost_grid[goal[0]][goal[1]] = 1

        if _has_path(grid, start, goal):
            return grid, cost_grid, start, goal

    # Fallback: completely empty grid (always solvable)
    grid = [[0] * cols for _ in range(rows)]
    cost_grid = [[1] * cols for _ in range(rows)]
    return grid, cost_grid, start, goal


def _has_path(grid, start, goal):
    """Quick BFS reachability check used while generating random grids."""
    from collections import deque

    rows, cols = len(grid), len(grid[0])
    seen = {start}
    q = deque([start])
    while q:
        r, c = q.popleft()
        if (r, c) == goal:
            return True
        for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != 1 and (nr, nc) not in seen:
                seen.add((nr, nc))
                q.append((nr, nc))
    return False


# ---------------------------------------------------------------------------
# Input validation (Problem Setup Module)
# ---------------------------------------------------------------------------
def validate_grid(grid, start, goal):
    """Return a list of human-readable error strings (empty list = valid)."""
    errors = []
    rows, cols = len(grid), len(grid[0])

    def in_bounds(pos):
        return 0 <= pos[0] < rows and 0 <= pos[1] < cols

    if not in_bounds(start):
        errors.append(f"Start position {start} is outside the grid ({rows}x{cols}).")
    elif grid[start[0]][start[1]] == 1:
        errors.append(f"Start position {start} sits on an obstacle (shelf). Pick a free cell.")

    if not in_bounds(goal):
        errors.append(f"Goal position {goal} is outside the grid ({rows}x{cols}).")
    elif grid[goal[0]][goal[1]] == 1:
        errors.append(f"Goal position {goal} sits on an obstacle (shelf). Pick a free cell.")

    if not errors and start == goal:
        errors.append("Start and Goal cannot be the same cell.")

    if not errors and not _has_path(grid, start, goal):
        errors.append("No possible path exists between Start and Goal on this grid (goal is fully enclosed by shelves).")

    return errors


# ---------------------------------------------------------------------------
# Visualization (Visual UI Module)
# ---------------------------------------------------------------------------
def draw_grid(grid, cost_grid, start, goal, explored=None, path=None, title=""):
    """Render the warehouse grid as a matplotlib figure.

    Color key:
        white        -> free aisle (cost 1)
        light orange -> narrow aisle (cost 3)
        dark gray    -> obstacle / shelf
        light blue   -> explored cell (search frontier history)
        yellow       -> final path
        green        -> start (charging dock)
        red          -> goal (target shelf)
    """
    rows, cols = len(grid), len(grid[0])
    color_grid = np.ones((rows, cols, 3))

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 1:
                color_grid[r, c] = (0.25, 0.25, 0.25)        # obstacle
            elif cost_grid[r][c] > 1:
                color_grid[r, c] = (1.0, 0.80, 0.55)         # narrow aisle
            else:
                color_grid[r, c] = (1.0, 1.0, 1.0)           # free

    if explored:
        for cell in explored:
            if cell != start and cell != goal:
                r, c = cell
                color_grid[r, c] = (0.65, 0.82, 1.0)         # explored

    if path:
        for cell in path:
            if cell != start and cell != goal:
                r, c = cell
                color_grid[r, c] = (1.0, 0.85, 0.15)         # final path

    color_grid[start[0], start[1]] = (0.25, 0.75, 0.30)       # start
    color_grid[goal[0], goal[1]] = (0.85, 0.15, 0.15)         # goal

    fig_w = max(3.5, min(cols * 0.55, 9))
    fig_h = max(3.5, min(rows * 0.55, 9))
    fig, ax = plt.subplots(figsize=(fig_w, fig_h))
    ax.imshow(color_grid, interpolation="nearest")

    ax.set_xticks(np.arange(-0.5, cols, 1), minor=True)
    ax.set_yticks(np.arange(-0.5, rows, 1), minor=True)
    ax.grid(which="minor", color="gray", linewidth=0.5)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title(title, fontsize=11)

    fig.tight_layout()
    return fig
