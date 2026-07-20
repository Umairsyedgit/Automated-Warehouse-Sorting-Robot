# Short Report — Smart Warehouse Sorting Robot (AI Pathfinding Visualizer)

## 1. Problem

Automated warehouses (e.g., Amazon Robotics) use mobile robots to move between
a charging dock and shelf locations to pick/sort packages. The robot must
navigate a grid-like floor plan, avoiding shelving units (obstacles) and
minimizing travel cost — some aisles are narrow and slower/riskier to
traverse, so they are modeled with a higher movement cost.

**Goal:** Given a warehouse grid (free aisles, obstacles, and "narrow" higher-
cost aisles), a start cell (dock) and a goal cell (target shelf), find a route
for the robot that is efficient in terms of steps, total cost, and computation.

This maps directly onto Option A ("Automated Warehouse Sorting Robot") from
Assignment 1, and onto **Option 2: Search/Optimization AI** from the lab
project guide.

## 2. Method

- **Input/Data:** Warehouse layouts are stored as JSON grids
  (`data/warehouse_small.json`, `_medium.json`, `_large.json`), each
  containing a 0/1 obstacle grid, a per-cell movement-cost grid, a start
  position, and a goal position. Custom random layouts can also be generated
  and are automatically checked for solvability.
- **Algorithms implemented (`algorithms.py`):**
  - **BFS** (uninformed) — fewest-steps path, ignores movement cost.
  - **UCS / Dijkstra** (uninformed) — cheapest-cost path.
  - **A\*** (informed, Manhattan heuristic) — cheapest-cost path, fewer
    expansions than UCS.
  - **Greedy Best-First Search** (informed, cost-blind) — fast but not
    cost-optimal.
- **Visualization (`grid_utils.py`):** Each cell is color-coded — free, narrow
  aisle, obstacle, explored, final path, start, goal — and rendered with
  matplotlib inside the Streamlit UI, including a step-by-step animation of
  the exploration order.
- **Explainability (`explainer.py`):** After a run, a natural-language summary
  explains how the chosen algorithm works, how many cells it explored (and
  what % of the grid that represents), and why its path has the cost/length
  it has.
- **Evaluation:** The app reports path steps, path cost, nodes expanded, and
  runtime (ms) for the selected algorithm, and can run a **second algorithm on
  the same grid** for a direct side-by-side comparison (table + bar chart +
  two grid views).

## 3. AI Used

Rule-based / classical **Search & Optimization AI** — no external AI APIs,
no model training, no internet connection required. This keeps the project
fully reproducible and instantly explainable, which fits the
"Explainability Module" requirement directly.

## 4. Results (example run — 10x10 random grid, seed = 7)

| Algorithm | Path Steps | Path Cost | Nodes Expanded | Runtime (ms) |
|---|---|---|---|---|
| BFS | 18 | 24 | 80 | ~0.09 |
| UCS / Dijkstra | 18 | **18** | 80 | ~0.15 |
| **A\*** | 18 | **18** | **39** | ~0.08 |
| Greedy | 18 | 24 | **24** | ~0.04 |

**Observations:**
- BFS and Greedy both found 18-step paths but with cost 24 — they walked
  through narrow (cost-3) aisles because they don't track accumulated cost.
- UCS and A\* both found the optimal cost-18 path, but **A\* expanded under
  half as many cells as UCS** (39 vs 80) because its heuristic focuses the
  search toward the goal.
- Greedy was the fastest and expanded the fewest cells overall, but its path
  is *not* guaranteed to be the cheapest — a real trade-off between speed and
  optimality.

## 5. Critical Analysis (Assignment 1, Task 3)

**Hardest dimension to handle:** *Static vs. Dynamic* / *Deterministic vs.
Stochastic* are the most challenging in a real deployment — a real warehouse
has other moving robots and people, so the "grid" the robot planned for can
change mid-execution, forcing re-planning. This project's grid is static
during a single run, which is a simplification of the real environment.

**Utility function example (Speed vs Safety):**
```
U = (w_speed × 1/steps) − (w_safety × extra_cost)
extra_cost = path_cost − steps   (i.e., how much extra cost came from narrow aisles)
```
With a low `w_safety`, the agent is indifferent between BFS/Greedy and
A*/UCS — speed dominates. If `w_safety` is **doubled**, routes through narrow
aisles become heavily penalized, so the agent's preferred algorithm shifts
toward **A\*/UCS** (cost-aware), and even within A\*, the chosen path would
shift to avoid narrow-aisle cells even if that means a few extra steps.

## 6. Limitations & Future Improvements

- Only 4-directional (no diagonal) movement is modeled.
- The environment is static during a run (no dynamic obstacles / other robots
  — i.e., single-agent, not multi-agent).
- Future work: add diagonal movement, multiple robots (multi-agent
  coordination), dynamic re-planning when obstacles appear, and local search
  (e.g., simulated annealing) for continuous re-optimization.
