<div align="center">

# DSA Collection

_A suite of my data structures and algorithms solutions and visualizations._

[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](#)
[![NumPy](https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white)](#)
[![ModernGL](https://img.shields.io/badge/ModernGL-2D3436?style=for-the-badge&logo=opengl&logoColor=white)](#)
[![Pygame](https://img.shields.io/badge/Pygame-6af02a?style=for-the-badge)](#)

</div>

## Overview

This repository is a comprehensive collection of my Data Structures and Algorithms work, featuring optimized solutions to the NeetCode 250, a professional-grade testing engine, and a suite of interactive visualizers.

## Key Features

- **Optimized Solutions:** Solutions to the NeetCode 250, meticulously optimized for both time and space complexity, categorized by algorithmic pattern (e.g., Two Pointers, Slidng Window, Backtracking).
- **Robust Testing Engine:** A custom-built Tester class that manages execution environment state, enforces strict time and memory limits, and provides formatted, diff-based validation for algorithmic correctness.
- **Visual Debugging Suite:** Specialized helpers in Helper.py for transforming complex data structures (Binary Trees, Tries, Linked Lists, Graphs, etc.) into human-readable, printable formats for complex state debugging.
- **Algorithmic Visualizers:** Interactive, hardware-accelerated visualizations for sorting and pathfinding algorithms. Famous algorithms like Merge Sort, Quick Sort, Dijkstra, and A\*, featured with real-time audio-visual feedback.

## System Architecture

The DSA Collection follows a utility-first architecture, separating algorithmic logic from visualization and testing instrumentation.

1. **Problem Solutions (`solutions/`):** An organized repository of Python implementations for DSA problems, each leveraging the utility layer for verification.
2. **Utility Layer (`Helper.py`):** The core engine providing data structure nodes, processing helpers, and the `Tester` framework. It uses `signal` and `resource` for sandbox-like execution limits.
3. **Visualization Layer (`sort.py`, `find.py`):**
   - `sort.py` uses **ModernGL** for hardware-accelerated rendering of large datasets.
   - `find.py` uses **Pygame** to create an interactive grid-based environment for pathfinding exploration.

## Trade-offs & Design Decisions

- **Custom Tester over Pytest:** While Pytest is standard, a bespoke `Tester` was implemented to handle specific competitive programming needs: strict per-test timing, memory heap limits via `setrlimit`, and custom object-aware comparison (e.g., handling cyclic Linked Lists or Tree equality). This allows for a more integrated "Submit -> Test -> Debug" loop.
- **ModernGL for Sorting Visuals:** Standard plotting libraries (like Matplotlib) or even Pygame struggle with rendering 10,000+ elements at 60FPS while updating in real-time. ModernGL leverages GPU shaders to ensure perfectly fluid visualizations regardless of array size.
- **Utility-Heavy Approach:** Rather than writing standalone solutions, every problem uses common helper classes and nodes. **Trade-off:** This introduces an internal dependency, but guarantees that every solution benefits from the same robust visual debugging and testing infrastructure.

## Images

#### Solution Passes:

![Solution Passes](./public/Image%201%20-%20Solution%20Passes.png)

#### Time Limit Exceeded:

![Time Limit Exceeded](./public/Image%202%20-%20Time%20Limit%20Exceeded.png)

#### Binary Tree Helper:

![Binary Tree Helper](./public/Image%203%20-%20Binary%20Tree%20Helper.png)

#### Merge Sort Visualized:

![Merge Sort Visualized](./public/Image%204%20-%20Merge%20Sort%20Visualized.png)

#### DFS Pathfinding:

![DFS Pathfinding](./public/Image%205%20-%20DFS%20Pathfinding.png)

## Installation & Setup

1. Clone the repository with `git clone https://github.com/BryanWieschenberg/DSA-Collection.git`, enter the directory with `cd DSA-Collection`, and install dependencies with `pip -r requirements.txt`
2. Test a solution with `python3 test.py <problem_number>`. A map with problems and their corresponding numbers can be found in [docs/problems.md](/docs/problems.md)
3. See sorting algorithms visualized with `python3 sort.py <algorithm> <size: int ?? 128> <speed: Speed ?? m>`
   - **Algorithms:** `selection`, `insertion`, `bubble`, `bogo`, `merge`, `quick`, `radix`, `tim`, `heap`, `bitonic`, `comb`, `cycle`, `pancake`, `cocktail_shaker`, `shell`, `gravity`, `odd_even`, `flash`
   - **Speed:** `xxs`, `xs`, `s`, `m`, `f`, `u`
4. See pathfinding algorithms visualized with `python3 find.py <maze_height: int ?? 20> <slow_ratio: 0-1 ?? 0.1> <wall_prob: 0-1 ?? 0.5> <delay_ms: int ?? 50>`
