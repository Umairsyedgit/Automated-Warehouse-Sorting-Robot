# 🤖 Smart Warehouse Sorting Robot — AI Pathfinding Visualizer

The **Smart Warehouse Sorting Robot** is an interactive Streamlit application that shows how an autonomous robot can navigate through a warehouse.

The robot starts from its charging dock and searches for the best route to a target shelf while avoiding obstacles and considering different movement costs.

The application includes four common AI search algorithms:

- Breadth-First Search (BFS)
- Uniform Cost Search (UCS / Dijkstra)
- A* Search
- Greedy Best-First Search

This project was created for an Introduction to Artificial Intelligence course lab. It is based on the **Automated Warehouse Sorting Robot** scenario introduced in Assignment 1 through the PEAS framework.

## Features

With this application, you can:

- Choose between small, medium, and large warehouse layouts.
- Generate a custom warehouse layout with random obstacles.
- Select one search algorithm or compare two algorithms side by side.
- Watch the robot explore the warehouse step by step.
- See the final route from the starting point to the goal.
- Compare algorithms using path length, movement cost, expanded nodes, and runtime.
- Read a simple explanation of why an algorithm selected a particular route.
- Experiment with the trade-off between speed and safety through a utility function demonstration.

## 📁 Project Structure

```text
WarehouseRobotPathfinder/
│
├── app.py
│   └── Main Streamlit application and user interface
│
├── algorithms.py
│   └── Implementations of BFS, UCS, A*, and Greedy Best-First Search
│
├── grid_utils.py
│   └── Warehouse loading, generation, validation, and visualization utilities
│
├── explainer.py
│   └── Generates simple explanations for algorithm results
│
├── generate_screenshots.py
│   └── Helper script for generating sample screenshots
│
├── requirements.txt
│   └── Python dependencies required to run the project
│
├── README.md
│   └── Project setup and usage guide
│
├── REPORT.md
│   └── Detailed technical report
│
├── data/
│   ├── warehouse_small.json
│   ├── warehouse_medium.json
│   └── warehouse_large.json
│
└── screenshots/
    ├── 01_initial_layout.png
    ├── 02_bfs_result.png
    ├── 03_astar_result.png
    └── 04_comparison.png
```