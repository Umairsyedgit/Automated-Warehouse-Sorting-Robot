"""
app.py
-------
Main Streamlit application for the "Smart Warehouse Sorting Robot" AI project.

Run with:
    streamlit run app.py

Modules implemented (per lab project requirements):
  A) Problem Setup Module   -> sidebar: choose/generate warehouse, validation
  B) Core Logic Module      -> algorithms.py (BFS / UCS / A* / Greedy)
  C) Visual UI Module        -> grid view, controls, result panel, status messages, animation
  D) Explainability Module   -> explainer.py - natural language "why this path"
  E) Evaluation Module        -> metrics + side-by-side algorithm comparison
"""

import time

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

from algorithms import ALGORITHMS
from explainer import explain_utility_function, generate_explanation
from grid_utils import draw_grid, generate_warehouse, load_warehouse, validate_grid

# ------------------------------------------------------------------
# Page setup
# ------------------------------------------------------------------
st.set_page_config(page_title="Warehouse Robot Pathfinder", layout="wide", page_icon="🤖")

st.title("🤖 Smart Warehouse Sorting Robot — AI Pathfinding Visualizer")
st.caption(
    "An autonomous warehouse robot must travel from its charging dock to a target "
    "shelf, avoiding shelving units (obstacles) and minimizing movement cost "
    "(narrow aisles cost more to cross). This demo applies **Search/Optimization "
    "AI** (BFS, UCS/Dijkstra, A*, Greedy Best-First) to that problem."
)

with st.expander("📘 PEAS Specification of this Agent (Assignment 1 reference)"):
    st.markdown(
        """
| PEAS Element | Description |
| --- | --- |
| **Performance Measure** | Minimize total movement cost; minimize number of steps; maximize success rate (path found); minimize nodes expanded (computation/efficiency) |
| **Environment** | Warehouse floor represented as a grid of aisles and shelving units; some aisles are *narrow* and cost more to traverse |
| **Actuators** | Drive motors (move Up / Down / Left / Right one cell at a time) |
| **Sensors** | Internal map/grid of the warehouse layout and the robot's current grid position |
"""
    )

# ====================================================================
# A) PROBLEM SETUP MODULE
# ====================================================================
st.sidebar.header("1️⃣ Problem Setup")

layout_choice = st.sidebar.selectbox(
    "Warehouse layout (input data)",
    ["Small (8x8)", "Medium (12x12)", "Large (15x15)", "Custom random grid"],
    help="Pick a pre-made warehouse from data/, or generate a random one.",
)

DATA_FILES = {
    "Small (8x8)": "data/warehouse_small.json",
    "Medium (12x12)": "data/warehouse_medium.json",
    "Large (15x15)": "data/warehouse_large.json",
}

if layout_choice == "Custom random grid":
    rows = st.sidebar.slider("Rows", 5, 25, 10)
    cols = st.sidebar.slider("Columns", 5, 25, 10)
    density = st.sidebar.slider("Obstacle density (shelves)", 0.0, 0.45, 0.20, 0.01)
    seed = st.sidebar.number_input("Random seed", min_value=0, max_value=9999, value=7, step=1)
    grid, cost_grid, start, goal = generate_warehouse(rows, cols, density, seed=int(seed))
else:
    grid, cost_grid, start, goal = load_warehouse(DATA_FILES[layout_choice])

# ---- Input validation ----
errors = validate_grid(grid, start, goal)
if errors:
    for e in errors:
        st.sidebar.error(e)
    st.error("⚠️ Invalid warehouse configuration. Please fix the settings in the sidebar.")
    st.stop()
else:
    st.sidebar.success(f"Grid OK ✅  ({len(grid)} x {len(grid[0])})")

st.sidebar.markdown(f"**🟢 Start (Dock):** `{start}`")
st.sidebar.markdown(f"**🔴 Goal (Target shelf):** `{goal}`")

# ====================================================================
# Algorithm selection
# ====================================================================
st.sidebar.header("2️⃣ Algorithm")
algo_name = st.sidebar.selectbox("Search algorithm", list(ALGORITHMS.keys()), index=2)

compare_mode = st.sidebar.checkbox("Compare with a second algorithm")
algo_name_2 = None
if compare_mode:
    other_algos = [a for a in ALGORITHMS if a != algo_name]
    algo_name_2 = st.sidebar.selectbox("Second algorithm", other_algos, index=0)

animate = st.sidebar.checkbox("Animate exploration", value=True)
speed = st.sidebar.slider("Animation speed", 1, 10, 7) if animate else 10

run_clicked = st.sidebar.button("▶️ Run Robot", type="primary", use_container_width=True)

st.sidebar.markdown("---")
st.sidebar.markdown(
    "**Legend**  \n"
    "🟩 Start (dock)  🟥 Goal (shelf)  \n"
    "⬛ Obstacle (shelf)  🟧 Narrow aisle (cost 3)  \n"
    "🟦 Explored cells  🟨 Final path"
)

total_cells = len(grid) * len(grid[0])

# ====================================================================
# C) VISUAL UI MODULE - grid view + controls + results
# ====================================================================
grid_placeholder = st.empty()

if not run_clicked:
    fig = draw_grid(
        grid, cost_grid, start, goal,
        title=f"Warehouse Layout ({len(grid)}x{len(grid[0])}) — press 'Run Robot' to start",
    )
    grid_placeholder.pyplot(fig)
    plt.close(fig)
    st.info("👈 Configure the warehouse and algorithm in the sidebar, then click **Run Robot**.")

else:
    # ---- B) CORE LOGIC MODULE ----
    result = ALGORITHMS[algo_name](grid, start, goal, cost_grid)

    # ---- Animation of intermediate exploration steps ----
    if animate and result["explored"]:
        n = len(result["explored"])
        step = max(1, n // 25)
        for i in range(0, n + 1, step):
            fig = draw_grid(
                grid, cost_grid, start, goal,
                explored=result["explored"][:i],
                title=f"{algo_name} — exploring... ({min(i, n)}/{n} cells)",
            )
            grid_placeholder.pyplot(fig)
            plt.close(fig)
            time.sleep((11 - speed) * 0.012)

    fig = draw_grid(
        grid, cost_grid, start, goal,
        explored=result["explored"], path=result["path"],
        title=f"{algo_name} — Final Result",
    )
    grid_placeholder.pyplot(fig)
    plt.close(fig)

    # ---- Result panel / status messages ----
    st.subheader("📋 Result Panel")
    if result["path"]:
        st.success(
            f"✅ Robot reached the target shelf! "
            f"{len(result['path']) - 1} step(s), total movement cost = {result['cost']}."
        )
    else:
        st.error("❌ No path found — the target shelf is completely blocked by shelving units.")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Path Steps", len(result["path"]) - 1 if result["path"] else "N/A")
    c2.metric("Path Cost", result["cost"] if result["path"] else "N/A")
    c3.metric("Nodes Expanded", result["nodes_expanded"])
    c4.metric("Runtime (ms)", f"{result['runtime_ms']:.3f}")

    # ====================================================================
    # D) EXPLAINABILITY MODULE
    # ====================================================================
    st.subheader("🧠 Why this path? (Explainability)")
    st.markdown(generate_explanation(algo_name, result, total_cells))

    # ====================================================================
    # E) EVALUATION MODULE - comparison
    # ====================================================================
    if compare_mode:
        st.markdown("---")
        st.subheader("📊 Evaluation: Algorithm Comparison")

        result2 = ALGORITHMS[algo_name_2](grid, start, goal, cost_grid)

        df = pd.DataFrame(
            {
                "Metric": ["Path Steps", "Path Cost", "Nodes Expanded", "Runtime (ms)"],
                algo_name: [
                    len(result["path"]) - 1 if result["path"] else "N/A",
                    result["cost"] if result["path"] else "N/A",
                    result["nodes_expanded"],
                    round(result["runtime_ms"], 4),
                ],
                algo_name_2: [
                    len(result2["path"]) - 1 if result2["path"] else "N/A",
                    result2["cost"] if result2["path"] else "N/A",
                    result2["nodes_expanded"],
                    round(result2["runtime_ms"], 4),
                ],
            }
        )
        st.dataframe(df, use_container_width=True, hide_index=True)

        col_chart, col_grids = st.columns([1, 2])

        with col_chart:
            fig2, ax2 = plt.subplots(figsize=(4, 3.5))
            ax2.bar(
                [algo_name.split(" ")[0], algo_name_2.split(" ")[0]],
                [result["nodes_expanded"], result2["nodes_expanded"]],
                color=["#4C72B0", "#DD8452"],
            )
            ax2.set_ylabel("Nodes Expanded")
            ax2.set_title("Search Efficiency")
            fig2.tight_layout()
            st.pyplot(fig2)
            plt.close(fig2)

        with col_grids:
            g1, g2 = st.columns(2)
            fig_a = draw_grid(grid, cost_grid, start, goal, explored=result["explored"], path=result["path"], title=algo_name)
            fig_b = draw_grid(grid, cost_grid, start, goal, explored=result2["explored"], path=result2["path"], title=algo_name_2)
            g1.pyplot(fig_a)
            g2.pyplot(fig_b)
            plt.close(fig_a)
            plt.close(fig_b)

        st.markdown(f"**{algo_name_2} explanation:**")
        st.markdown(generate_explanation(algo_name_2, result2, total_cells))

    # ====================================================================
    # Utility Function demo - Assignment 1, Task 3 (Speed vs Safety)
    # ====================================================================
    st.markdown("---")
    with st.expander("⚖️ Utility Function Demo: Speed vs Safety (Assignment 1, Task 3.2)"):
        st.markdown(
            "A simple utility function for this agent could be:\n\n"
            "`U = (w_speed × 1/steps) − (w_safety × extra_cost)`\n\n"
            "where `extra_cost = path_cost − steps` measures how much *additional* "
            "cost came from passing through narrow (riskier) aisles. "
            "Increasing `w_safety` makes the utility function penalize routes through "
            "narrow aisles more heavily, pushing the agent toward cost-aware "
            "algorithms (UCS / A*) instead of cost-blind ones (BFS / Greedy)."
        )
        safety_weight = st.slider("Safety weight (w_safety)", 1, 5, 2)
        st.info(explain_utility_function(safety_weight))

# ====================================================================
# About / Viva prep section
# ====================================================================
st.markdown("---")
with st.expander("ℹ️ About this AI system (viva prep)"):
    st.markdown(
        """
**Why this problem is relevant:** Warehouse robots (e.g., Amazon Robotics) must
constantly re-plan routes around shelves and congestion - an ideal, intuitive
showcase of classic AI search.

**Why these algorithms:** BFS and UCS are *uninformed* search (no domain
knowledge); A* and Greedy are *informed* search using the Manhattan-distance
heuristic. Together they demonstrate the full spectrum from Chapter 2/3 of
Russell & Norvig.

**Data used:** Sample warehouse grids (`data/*.json`) — 0 = free aisle,
1 = shelf/obstacle, and a separate cost grid where some free cells cost 3
(narrow aisle) instead of 1. Custom random grids can also be generated and are
checked for solvability before use.

**How the UI helps understand the result:** The grid view shows every cell the
algorithm *considered* (blue) versus the *final path* (yellow), the metrics
panel quantifies cost/efficiency, and the explanation panel translates the
algorithm's behavior into plain English.

**AI component:** Rule-based / Search & Optimization AI (BFS, UCS/Dijkstra, A*,
Greedy Best-First Search) — no external AI APIs are used.

**Limitations & future improvements:** Only 4-directional movement is modeled
(no diagonals); the warehouse is static during a run (no moving obstacles /
other robots); a future version could add dynamic obstacles (multi-agent),
diagonal movement, or local-search algorithms (e.g., simulated annealing) for
re-routing.
"""
    )

st.caption("AI Lab Project — Warehouse Sorting Robot (PEAS / Search & Optimization AI)")
