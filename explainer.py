"""
explainer.py
-------------
Explainability Module.

Given the result of a search algorithm, produce a short natural-language
explanation of WHY the robot chose this path, HOW the algorithm works,
and what its strengths/weaknesses are. This is shown to the user in the
"Why this path?" panel of the UI.
"""

ALGO_DESCRIPTIONS = {
    "BFS (Breadth-First Search)": (
        "BFS explores the warehouse layer by layer (all cells 1 step away, then all "
        "cells 2 steps away, and so on). It guarantees the path with the FEWEST "
        "MOVES, but it completely ignores the fact that narrow aisles cost more "
        "to traverse - so the 'shortest' path is not always the 'cheapest' path."
    ),
    "UCS / Dijkstra (Uniform Cost Search)": (
        "UCS always expands the cell with the lowest accumulated movement cost so "
        "far. It guarantees the CHEAPEST possible path (accounting for narrow-aisle "
        "penalties), but - like BFS - it has no sense of direction toward the goal, "
        "so it tends to expand cells in every direction equally."
    ),
    "A* Search": (
        "A* combines the actual cost-so-far (g) with an estimate of the remaining "
        "distance to the goal (Manhattan-distance heuristic, h). This pulls the "
        "search toward the goal, so A* usually expands far fewer cells than UCS or "
        "BFS while STILL guaranteeing the cheapest path - making it the most "
        "efficient choice for this warehouse robot."
    ),
    "Greedy Best-First Search": (
        "Greedy search only looks at the estimated distance to the goal (h) and "
        "ignores accumulated cost entirely. It is usually very fast and expands few "
        "cells, but because it ignores cost it can walk straight through expensive "
        "narrow aisles, so the path it returns is not guaranteed to be the cheapest."
    ),
}


def generate_explanation(algo_name, result, total_cells):
    """Return a short natural-language explanation string for the result panel."""
    path = result["path"]
    explored = result["explored"]
    nodes = result["nodes_expanded"]
    cost = result["cost"]

    if not path:
        return (
            f"{algo_name} expanded {nodes} cell(s) but could NOT find a path from the "
            f"dock to the target shelf. This means the goal is completely sealed off "
            f"by obstacles (shelving units) - the robot would need a human to clear "
            f"a route, or the warehouse layout needs to be redesigned."
        )

    pct_explored = (nodes / total_cells) * 100 if total_cells else 0
    steps = len(path) - 1

    intro = ALGO_DESCRIPTIONS.get(algo_name, "")

    summary = (
        f"\n\nFor this warehouse, {algo_name} expanded **{nodes} of {total_cells} cells "
        f"({pct_explored:.1f}%)** before reaching the target shelf, and found a route "
        f"that takes **{steps} step(s)** with a total movement cost of **{cost}**."
    )

    return intro + summary


def explain_utility_function(weight_safety):
    """
    Explanation tied to Assignment 1 / Task 3.2 (Utility Function: Speed vs Safety).

    utility = (1 / cost) * speed_weight  -  cost * safety_weight   [conceptual form]

    Here we use a simplified, intuitive framing: as `weight_safety` increases,
    the agent should prefer UCS/A* (cost-aware, avoids narrow/expensive aisles)
    over BFS/Greedy (which can ignore real movement cost).
    """
    if weight_safety <= 1:
        return (
            "Low safety weight: the robot prioritizes SPEED (fewest steps). "
            "Algorithms like BFS or Greedy, which ignore aisle-cost penalties, "
            "are acceptable - the robot may cut through narrow aisles."
        )
    elif weight_safety <= 3:
        return (
            "Balanced weight: the robot balances speed and safety. A* is ideal here, "
            "since it finds the cheapest (safest) path while still being efficient."
        )
    else:
        return (
            "High safety weight: the robot strongly avoids narrow/expensive aisles, "
            "even if it means more steps. UCS (Dijkstra) or A* with cost-aware "
            "planning should be used; BFS/Greedy become unsuitable because they "
            "can route the robot through high-risk narrow aisles."
        )
