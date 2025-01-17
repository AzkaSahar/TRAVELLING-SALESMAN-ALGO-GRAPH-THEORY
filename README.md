# Traveling Salesman Problem (TSP) Algorithms: Graph Theory Project

This repository contains the **Graph Theory** course project made by 3 members, which explores and compares three algorithms—**Nearest Neighbor**, **Nearest Insertion**, and **Brute Force**—for solving the Traveling Salesman Problem (TSP). The project includes both Python and C++ implementations, with a Python-based GUI for enhanced visualization.

---
## Group Members

1. Azka Sahar Shaikh  
2. Muhammad Sudais Katiya  
3. Sumaiya Waheed

---

## Project Overview

The Traveling Salesman Problem (TSP) is a classic optimization problem that involves finding the shortest possible route to visit a set of cities and return to the starting point. This project demonstrates three approaches to solving the TSP, highlighting their performance, efficiency, and usability.

---

## Algorithms Implemented

1. **Nearest Neighbor Algorithm**:
   - Greedy approach that iteratively selects the nearest unvisited city.
   - Fast but does not guarantee the optimal solution.

2. **Nearest Insertion Algorithm**:
   - Constructs a tour by inserting cities into positions that minimize the total distance.
   - Provides a more refined solution compared to Nearest Neighbor.

3. **Brute Force Algorithm**:
   - Exhaustively computes all possible city visit permutations to find the optimal path.
   - Guarantees the best solution but is computationally expensive for large datasets.

---

## Features

- **Python Implementation**:
  - GUI developed using `customtkinter` for visualizing TSP solutions.
  - Users can input city coordinates or generate random datasets.
  - Dynamic visualization of solution paths for all three algorithms.

- **C++ Implementation**:
  - Optimized for performance with a command-line interface.
  - Allows comparison of execution times and results across algorithms.

---

## Results and Observations

- **Nearest Neighbor**: Efficient for small datasets but less accurate for larger ones.
- **Nearest Insertion**: A balanced approach offering better solutions than Nearest Neighbor with reasonable speed.
- **Brute Force**: Accurate but impractical for datasets with more than 10-12 cities due to exponential time complexity.

### Language Comparison

- **Python**:
  - Easy to use and beginner-friendly with a user-friendly GUI.
  - Slower execution time compared to C++.
- **C++**:
  - Faster due to its compiled nature, ideal for performance-intensive tasks.
  - Lacks a graphical interface but excels in execution speed.

---

## How to Use

### Python Implementation
1. Install dependencies:
   ```bash
   pip install customtkinter

## Run the GUI application:
python tsp_gui.py

### C++ Implementation

## Compile the program:
  g++ tsp.cpp -o tsp

## Run the executable:
  ./tsp

