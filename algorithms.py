"""
algorithms.py
--------------
Core Logic Module for the Warehouse Robot Pathfinder.

Implements four classic search algorithms used by an autonomous warehouse
robot to navigate from its charging dock (start) to a target shelf (goal)
on a 2D grid while avoiding obstacles (shelving units).

Each algorithm returns a dictionary with:
    - path           : list of (row, col) cells from start to goal (empty if no path found)
    - explored       : list of (row, col) cells in the order they were expanded
                        (used for step-by-step "intermediate steps" visualization)
    - cost           : total movement cost of the returned path
    - nodes_expanded : number of cells expanded/visited during search
    - runtime_ms     : wall-clock time taken by the algorithm, in milliseconds
"""

import heapq
import time
from collections import deque


def get_neighbors(pos, grid):
    """Return walkable 4-directional neighbors of pos (up, down, left, right)."""
    rows, cols = len(grid), len(grid[0])
    r, c = pos
    neighbors = []
    for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != 1:
            neighbors.append((nr, nc))
    return neighbors


def manhattan(a, b):
    """Manhattan distance heuristic between two grid cells."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def _reconstruct_path(came_from, current, start):
    """Walk backwards through came_from to rebuild the path from start to current."""
    path = [current]
    while current != start:
        current = came_from[current]
        path.append(current)
    path.reverse()
    return path


def _path_cost(path, cost_grid):
    """Sum of movement costs for entering each cell along the path (excluding start)."""
    total = 0
    for cell in path[1:]:
        total += cost_grid[cell[0]][cell[1]]
    return total


def _empty_result(explored, runtime_ms):
    return {
        "path": [],
        "explored": explored,
        "cost": float("inf"),
        "nodes_expanded": len(explored),
        "runtime_ms": runtime_ms,
    }


# ---------------------------------------------------------------------------
# 1) Breadth-First Search
#    Ignores cost differences -> guarantees the path with the FEWEST STEPS.
# ---------------------------------------------------------------------------
def bfs(grid, start, goal, cost_grid):
    t0 = time.perf_counter()
    frontier = deque([start])
    came_from = {start: None}
    explored = []

    while frontier:
        current = frontier.popleft()
        explored.append(current)

        if current == goal:
            break

        for nxt in get_neighbors(current, grid):
            if nxt not in came_from:
                came_from[nxt] = current
                frontier.append(nxt)

    runtime_ms = (time.perf_counter() - t0) * 1000

    if goal not in came_from:
        return _empty_result(explored, runtime_ms)

    path = _reconstruct_path(came_from, goal, start)
    return {
        "path": path,
        "explored": explored,
        "cost": _path_cost(path, cost_grid),
        "nodes_expanded": len(explored),
        "runtime_ms": runtime_ms,
    }


# ---------------------------------------------------------------------------
# 2) Uniform Cost Search (Dijkstra)
#    Expands the cheapest-so-far cell first -> guarantees the LOWEST-COST path.
# ---------------------------------------------------------------------------
def ucs(grid, start, goal, cost_grid):
    t0 = time.perf_counter()
    counter = 0  # tie-breaker so the heap never compares tuples element-by-element ambiguously
    frontier = [(0, counter, start)]
    came_from = {start: None}
    cost_so_far = {start: 0}
    explored = []
    visited = set()

    while frontier:
        current_cost, _, current = heapq.heappop(frontier)
        if current in visited:
            continue
        visited.add(current)
        explored.append(current)

        if current == goal:
            break

        for nxt in get_neighbors(current, grid):
            new_cost = current_cost + cost_grid[nxt[0]][nxt[1]]
            if nxt not in cost_so_far or new_cost < cost_so_far[nxt]:
                cost_so_far[nxt] = new_cost
                came_from[nxt] = current
                counter += 1
                heapq.heappush(frontier, (new_cost, counter, nxt))

    runtime_ms = (time.perf_counter() - t0) * 1000

    if goal not in came_from:
        return _empty_result(explored, runtime_ms)

    path = _reconstruct_path(came_from, goal, start)
    return {
        "path": path,
        "explored": explored,
        "cost": cost_so_far[goal],
        "nodes_expanded": len(explored),
        "runtime_ms": runtime_ms,
    }


# ---------------------------------------------------------------------------
# 3) A* Search
#    Priority = cost_so_far (g) + Manhattan heuristic (h) -> optimal AND usually
#    expands fewer nodes than UCS/BFS because it is guided toward the goal.
# ---------------------------------------------------------------------------
def astar(grid, start, goal, cost_grid):
    t0 = time.perf_counter()
    counter = 0
    frontier = [(manhattan(start, goal), counter, start)]
    came_from = {start: None}
    cost_so_far = {start: 0}
    explored = []
    visited = set()

    while frontier:
        _, _, current = heapq.heappop(frontier)
        if current in visited:
            continue
        visited.add(current)
        explored.append(current)

        if current == goal:
            break

        for nxt in get_neighbors(current, grid):
            new_cost = cost_so_far[current] + cost_grid[nxt[0]][nxt[1]]
            if nxt not in cost_so_far or new_cost < cost_so_far[nxt]:
                cost_so_far[nxt] = new_cost
                priority = new_cost + manhattan(nxt, goal)
                came_from[nxt] = current
                counter += 1
                heapq.heappush(frontier, (priority, counter, nxt))

    runtime_ms = (time.perf_counter() - t0) * 1000

    if goal not in came_from:
        return _empty_result(explored, runtime_ms)

    path = _reconstruct_path(came_from, goal, start)
    return {
        "path": path,
        "explored": explored,
        "cost": cost_so_far[goal],
        "nodes_expanded": len(explored),
        "runtime_ms": runtime_ms,
    }


# ---------------------------------------------------------------------------
# 4) Greedy Best-First Search
#    Priority = Manhattan heuristic (h) ONLY -> fast, but can be tricked into
#    a more expensive path because it ignores accumulated cost.
# ---------------------------------------------------------------------------
def greedy(grid, start, goal, cost_grid):
    t0 = time.perf_counter()
    counter = 0
    frontier = [(manhattan(start, goal), counter, start)]
    came_from = {start: None}
    explored = []
    visited = set()

    while frontier:
        _, _, current = heapq.heappop(frontier)
        if current in visited:
            continue
        visited.add(current)
        explored.append(current)

        if current == goal:
            break

        for nxt in get_neighbors(current, grid):
            if nxt not in visited and nxt not in came_from:
                came_from[nxt] = current
                counter += 1
                heapq.heappush(frontier, (manhattan(nxt, goal), counter, nxt))

    runtime_ms = (time.perf_counter() - t0) * 1000

    if goal not in came_from:
        return _empty_result(explored, runtime_ms)

    path = _reconstruct_path(came_from, goal, start)
    return {
        "path": path,
        "explored": explored,
        "cost": _path_cost(path, cost_grid),
        "nodes_expanded": len(explored),
        "runtime_ms": runtime_ms,
    }


ALGORITHMS = {
    "BFS (Breadth-First Search)": bfs,
    "UCS / Dijkstra (Uniform Cost Search)": ucs,
    "A* Search": astar,
    "Greedy Best-First Search": greedy,
}
