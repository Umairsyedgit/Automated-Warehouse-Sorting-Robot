# 🤖 Smart Warehouse Sorting Robot — AI Pathfinding Visualizer

An interactive Streamlit app that demonstrates an autonomous warehouse robot
finding the best route from its charging dock (Start) to a target shelf (Goal)
using classic **Search/Optimization AI** algorithms: **BFS, UCS (Dijkstra),
A\*, and Greedy Best-First Search**.

This project was built for an Introduction to AI course lab, based on the
**"Automated Warehouse Sorting Robot"** topic from Assignment 1 (PEAS Framework).

---

## 1. What this project does

- Lets you pick a warehouse layout (small/medium/large sample grids, or
  generate a custom random one).
- Lets you pick a search algorithm (or two, to compare side-by-side).
- **Visualizes** the search step-by-step (which cells the robot "thinks about")
  and the final path it takes.
- **Explains** in plain English *why* that path/algorithm behaved the way it did.
- Shows **evaluation metrics**: path length, total movement cost, number of
  nodes expanded, and runtime — and compares two algorithms head-to-head.

---

## 2. Project Structure

```
WarehouseRobotPathfinder/
├── app.py                  # Streamlit UI (run this)
├── algorithms.py           # Core Logic: BFS, UCS, A*, Greedy
├── grid_utils.py           # Data loading/generation, validation, grid drawing
├── explainer.py            # Explainability module (natural-language explanations)
├── generate_screenshots.py # Helper script used to create sample screenshots
├── requirements.txt
├── README.md
├── REPORT.md
├── data/                    # Sample warehouse layouts (datasets)
│   ├── warehouse_small.json
│   ├── warehouse_medium.json
│   └── warehouse_large.json
└── screenshots/             # Sample output images
    ├── 01_initial_layout.png
    ├── 02_bfs_result.png
    ├── 03_astar_result.png
    └── 04_comparison.png
```

---

## 3. How to run it

### Step 1 — Install Python
Make sure you have **Python 3.9+** installed. Check with:
```bash
python3 --version
```

### Step 2 — Open a terminal in the project folder
```bash
cd WarehouseRobotPathfinder
```

### Step 3 — (Recommended) create a virtual environment
```bash
python3 -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```

### Step 4 — Install dependencies
```bash
pip install -r requirements.txt
```

### Step 5 — Run the app
```bash
streamlit run app.py
```

Streamlit will print a local URL, e.g.:
```
Local URL: http://localhost:8501
```
It should also open automatically in your default browser. If not, copy the
URL into your browser manually.

---

## 4. How to use the app

1. **Sidebar → Problem Setup**: pick a warehouse layout (Small / Medium /
   Large / Custom random grid). For a custom grid, adjust rows, columns,
   obstacle density, and seed.
2. **Sidebar → Algorithm**: pick a search algorithm. Optionally tick "Compare
   with a second algorithm" to see two algorithms side-by-side.
3. Tick/untick **"Animate exploration"** and adjust the speed slider if you
   want to see the search happen step-by-step.
4. Click **▶️ Run Robot**.
5. Read the **Result Panel** (success/failure, metrics), the
   **🧠 Why this path?** explanation, and (if comparing) the
   **📊 Evaluation** section.
6. Expand **⚖️ Utility Function Demo** to explore the Speed-vs-Safety
   trade-off discussed in Assignment 1, Task 3.2.

---

## 5. Running on Google Colab (optional, like your previous project)

Streamlit apps don't render directly inside a Colab cell, but you can still
run it there using a tunnel:

```python
!pip install -r requirements.txt -q
!streamlit run app.py &>/content/log.txt &
!npx localtunnel --port 8501
```
Then open the URL printed by `localtunnel`.

---

## 6. AI Component Used

This project uses **rule-based Search/Optimization AI** (no external AI
APIs, no internet connection required):
- **BFS** — uninformed, finds the path with the fewest steps.
- **UCS (Dijkstra)** — uninformed, finds the cheapest-cost path.
- **A\*** — informed (Manhattan-distance heuristic), finds the cheapest path
  while expanding far fewer nodes.
- **Greedy Best-First Search** — informed but cost-blind; fast but not always
  cost-optimal.

---

## 7. Troubleshooting

- **`ModuleNotFoundError: No module named 'streamlit'`** → run
  `pip install -r requirements.txt` again, and make sure your virtual
  environment is activated.
- **Port already in use** → run `streamlit run app.py --server.port 8502`.
- **Blank/old UI after editing code** → Streamlit hot-reloads automatically;
  if it doesn't, press `R` in the browser tab or refresh the page.
