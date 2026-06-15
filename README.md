# Automated-Warehouse-Sorting-Robot

This project is a Python-based visual simulation of an autonomous warehouse sorting robot (inspired by Amazon Robotics). The robot navigates a 2D grid-based warehouse layout to find the most efficient path from its charging dock to a target item shelf. 

The application implements and compares four classic AI search algorithms: **Breadth-First Search (BFS)**, **Uniform Cost Search (UCS)**, **A* Search**, and **Greedy Best-First Search**. It visually demonstrates how each algorithm explores the task environment and evaluates their performance based on computational and operational metrics.

---

## 🚀 Features

- **Dynamic Task Environment:** A 2D grid layout containing empty paths, obstacles (shelving units), and narrow aisles with higher movement costs.
- **Multiple AI Algorithms:**
  - **BFS (Breadth-First Search):** Guarantees the shortest path in terms of steps/unweighted distance.
  - **UCS (Uniform Cost Search):** Explores paths based on movement costs (ideal for narrow aisles).
  - **Greedy Best-First Search:** Uses heuristics to head directly towards the target shelf rapidly.
  - **A* Search:** Combines path cost and heuristics to achieve optimal pathfinding efficiently.
- **Visual UI Module:** Real-time visual grid mapping showing the warehouse layout, nodes expanded during search, and the final generated path.
- **Performance Evaluation & Analytics:** Side-by-side metric comparison featuring **Path Cost**, **Nodes Expanded**, and **Runtime (Latency)**.
- **Explainability Module:** Live explanation components detailing why an algorithm behaved a certain way based on its mathematical logic.

---

## 🛠️ Tech Stack & Dependencies

- **Programming Language:** Python 3.8+
- **Framework/UI:** Streamlit (or PyQt/Tkinter depending on implementation)
- **Data & Math Processing:** Pandas, NumPy
- **Visualization:** Matplotlib / Native Grid UI Elements

---

## 📋 PEAS Specification

- **Performance Measures:** Path Cost (distance), Nodes Expanded (efficiency), Runtime (latency), Safety Compliance (collision avoidance).
- **Environment:** 2D grid warehouse floor with static shelving units and narrow aisles.
- **Actuators:** Motorized drive system for directional grid movement (Up, Down, Left, Right).
- **Sensors:** Grid state matrix, obstacle detection data, coordinate tracking.
