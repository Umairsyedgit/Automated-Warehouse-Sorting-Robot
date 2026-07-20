"""
generate_screenshots.py
-------------------------
Utility script (NOT part of the app) used to pre-render sample PNG images
of the grid/path visualizations for the project's screenshots/ folder and
for the short report. Run once with: python3 generate_screenshots.py
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from grid_utils import generate_warehouse, draw_grid
from algorithms import ALGORITHMS, bfs, astar
from explainer import generate_explanation

OUT = "screenshots"

grid, cost_grid, start, goal = generate_warehouse(10, 10, obstacle_density=0.22, seed=7)

# 1. Initial layout
fig = draw_grid(grid, cost_grid, start, goal, title="Warehouse Layout (10x10) - Before Run")
fig.savefig(f"{OUT}/01_initial_layout.png", dpi=130, bbox_inches="tight")
plt.close(fig)

# 2. BFS result
res_bfs = bfs(grid, start, goal, cost_grid)
fig = draw_grid(grid, cost_grid, start, goal, explored=res_bfs["explored"], path=res_bfs["path"],
                 title=f"BFS - Path Cost {res_bfs['cost']}, Expanded {res_bfs['nodes_expanded']}")
fig.savefig(f"{OUT}/02_bfs_result.png", dpi=130, bbox_inches="tight")
plt.close(fig)

# 3. A* result
res_astar = astar(grid, start, goal, cost_grid)
fig = draw_grid(grid, cost_grid, start, goal, explored=res_astar["explored"], path=res_astar["path"],
                 title=f"A* - Path Cost {res_astar['cost']}, Expanded {res_astar['nodes_expanded']}")
fig.savefig(f"{OUT}/03_astar_result.png", dpi=130, bbox_inches="tight")
plt.close(fig)

# 4. Side-by-side comparison (Evaluation Module)
fig, axes = plt.subplots(1, 2, figsize=(11, 5.5))

import numpy as np
for ax, (name, res, title) in zip(
    axes,
    [
        (axes[0], res_bfs, f"BFS\nCost={res_bfs['cost']} | Expanded={res_bfs['nodes_expanded']} | {res_bfs['runtime_ms']:.3f} ms"),
        (axes[1], res_astar, f"A*\nCost={res_astar['cost']} | Expanded={res_astar['nodes_expanded']} | {res_astar['runtime_ms']:.3f} ms"),
    ],
):
    sub = draw_grid(grid, cost_grid, start, goal, explored=res["explored"], path=res["path"], title=title)
    sub.savefig("/tmp/_tmp.png", dpi=130, bbox_inches="tight")
    plt.close(sub)
    img = plt.imread("/tmp/_tmp.png")
    ax.imshow(img)
    ax.axis("off")

fig.suptitle("Algorithm Comparison: BFS vs A* (same warehouse, same start/goal)", fontsize=13)
fig.tight_layout()
fig.savefig(f"{OUT}/04_comparison.png", dpi=130, bbox_inches="tight")
plt.close(fig)

print("Explanation sample (A*):")
print(generate_explanation("A* Search", res_astar, 100))
print("\nScreenshots generated successfully.")
