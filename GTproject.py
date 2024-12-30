import tkinter as tk
from tkinter import IntVar
import random
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from customtkinter import CTk, CTkFrame, CTkButton, CTkLabel
from itertools import permutations


class App(CTk):
    def __init__(self):
        super().__init__()
        self.title("Algorithm Visualizer")
        self.geometry("800x600")
        self.attributes('-fullscreen', True)
        self.configure(bg="black")
        self.bind("<Escape>", self.toggle_fullscreen)

        # Sidebar
        self.sidebar_frame = CTkFrame(self, fg_color="#1a1a1a", border_color="#ff0000", border_width=2)
        self.sidebar_frame.pack(side="left", fill="y", padx=0, pady=10)

        # Prevent the sidebar from resizing according to its contents
        self.sidebar_frame.pack_propagate(0)

        # Add a function to dynamically adjust the width of the sidebar on window resize
        self.bind("<Configure>", self.adjust_sidebar_width)

        # Plot area
        self.plot_frame = CTkFrame(self, fg_color="black")
        self.plot_frame.pack(expand=True, fill="both", pady=10)

        # Algorithm selection
        self.algo_var = IntVar(value=1)

        # Buttons for each algorithm
        self.nearest_neighbor_button = CTkButton(
            self.sidebar_frame, text="Nearest Neighbor", command=self.run_nearest_neighbor,
            fg_color="black", text_color="#ff0000", hover_color="#990000", font=("Consolas", 12, "bold"),
            border_color="#ff0000", border_width=2
        )
        self.nearest_neighbor_button.pack(pady=(100, 5))

        self.nearest_insertion_button = CTkButton(
            self.sidebar_frame, text="Nearest Insertion", command=self.run_nearest_insertion,
            fg_color="black", text_color="#ff0000", hover_color="#990000", font=("Consolas", 12, "bold"),
            border_color="#ff0000", border_width=2
        )
        self.nearest_insertion_button.pack(pady=5)

        self.brute_force_button = CTkButton(
            self.sidebar_frame, text="Brute Force", command=self.run_brute_force,
            fg_color="black", text_color="#ff0000", hover_color="#990000", font=("Consolas", 12, "bold"),
            border_color="#ff0000", border_width=2
        )
        self.brute_force_button.pack(pady=5)

        self.exit_button = CTkButton(
            self.sidebar_frame, text="Exit", command=self.quit,
            fg_color="black", text_color="#ff0000", hover_color="#990000",
            corner_radius=5, font=("Consolas", 12, "bold"), border_color="#ff0000", border_width=2
        )
        self.exit_button.pack(pady=5)

        # Result text
        self.result_text = CTkLabel(
            self.sidebar_frame, text="Result: N/A",
            text_color="#ff0000", font=("Consolas", 13, "bold")
        )
        self.result_text.pack(pady=(30, 10))

        # Initialize random points
        self.num_vertices = 10
        self.points = [(random.randint(50, 750), random.randint(50, 550)) for _ in range(self.num_vertices)]
        self.x, self.y = zip(*self.points)

        # Initial graph plot
        self.fig, self.ax = plt.subplots(figsize=(40, 16), facecolor="black")
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.plot_graph()
        self.canvas.draw()

    def toggle_fullscreen(self, event=None):
        """Toggle fullscreen mode."""
        current_state = self.attributes('-fullscreen')
        self.attributes('-fullscreen', not current_state)

    def plot_graph(self):
        """Initial graph setup with labeled edges."""
        self.ax.clear()  # Clear previous plot
        self.ax.set_facecolor("black")

        # Plot vertices
        for i, (x, y) in enumerate(zip(self.x, self.y)):
            self.ax.scatter(x, y, color="#ff0000", s=200)
            self.ax.text(x, y, str(i), color="white", fontsize=14, ha="center", va="center")

        # Draw all edges and label their weights
        for i in range(self.num_vertices):
            for j in range(i + 1, self.num_vertices):
                self.ax.plot([self.x[i], self.x[j]], [self.y[i], self.y[j]], color="gray", lw=0.5, alpha=1)
                weight = self.distance(self.points[i], self.points[j])
                mid_x, mid_y = (self.x[i] + self.x[j]) / 2, (self.y[i] + self.y[j]) / 2
                self.ax.text(mid_x, mid_y, f"{weight:.1f}", color="yellow", fontsize=15, ha="center", va="center")

        self.ax.set_xlim(0, 800)
        self.ax.set_ylim(0, 600)
        self.fig.tight_layout()

        self.canvas.draw()

    def distance(self, p1, p2):
        """Calculate Euclidean distance."""
        return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5

    def run_nearest_neighbor(self):
        """Nearest Neighbor Algorithm."""
        self.result_text.configure(text="Running...")
        self.update_idletasks()
        start_time = time.time()
    

        start = random.randint(0, self.num_vertices - 1)
        visited = [start]
        total_weight = 0

        while len(visited) < self.num_vertices:
            current = visited[-1]
            nearest = None
            nearest_distance = float("inf")

            for i in range(self.num_vertices):
                if i not in visited:
                    dist = self.distance(self.points[current], self.points[i])
                    if dist < nearest_distance:
                        nearest_distance = dist
                        nearest = i

            visited.append(nearest)
            total_weight += nearest_distance

        visited.append(start)
        total_weight += self.distance(self.points[visited[-2]], self.points[start])
        
        elapsed_time = time.time() - start_time

        self.visualize_path(visited, total_weight, elapsed_time,start)

    def run_nearest_insertion(self):
        """Nearest Insertion Algorithm."""
        self.result_text.configure(text="Running...")
        self.update_idletasks()
        
        edges = []
        total_weight = 0
        start_time = time.time()
        # Step 1: Pick the smallest edge
        all_edges = [(i, j, self.distance(self.points[i], self.points[j]))
                     for i in range(self.num_vertices) for j in range(i + 1, self.num_vertices)]
        all_edges.sort(key=lambda x: x[2])
        start_edge = all_edges[0]
        edges.append(start_edge)
        total_weight += start_edge[2]

        visited = {start_edge[0], start_edge[1]}
        cycle = [start_edge[0], start_edge[1], start_edge[0]]

        while len(visited) < self.num_vertices:
            nearest_vertex = None
            min_increase = float('inf')
            insert_position = None

            for vertex in range(self.num_vertices):
                if vertex not in visited:
                    for i in range(len(cycle) - 1):
                        increase = (self.distance(self.points[cycle[i]], self.points[vertex]) +
                                    self.distance(self.points[vertex], self.points[cycle[i + 1]]) - 
                                    self.distance(self.points[cycle[i]], self.points[cycle[i + 1]]))
                        if increase < min_increase:
                            min_increase = increase
                            nearest_vertex = vertex
                            insert_position = i

            cycle.insert(insert_position + 1, nearest_vertex)
            visited.add(nearest_vertex)
            total_weight += min_increase
        
        elapsed_time = time.time() - start_time
        self.result_text.configure(text=f"Total Weight: {total_weight:.2f}")
        self.visualize_path(cycle, total_weight, elapsed_time,start=-1)

    def run_brute_force(self):
        """Brute Force Algorithm."""
        self.result_text.configure(text="Running...")
        self.update_idletasks()

        min_weight = float("inf")
        best_path = None
        start_vertex = 0
        start_time = time.time()

        # Generate all permutations of the vertices (excluding the starting point)
        vertices = list(range(self.num_vertices))
        vertices.remove(start_vertex)
        all_permutations = permutations(vertices)

        for perm in all_permutations:
            # Add start and end vertex to the permutation path
            path = [start_vertex] + list(perm) + [start_vertex]
            total_weight = 0

            # Calculate the total weight for the current permutation path
            for i in range(len(path) - 1):
                total_weight += self.distance(self.points[path[i]], self.points[path[i + 1]])

            if total_weight < min_weight:
                min_weight = total_weight
                best_path = path
   
        elapsed_time = time.time() - start_time
        self.visualize_path(best_path, min_weight, elapsed_time, start=start_vertex)

    def visualize_path(self, path, total_weight,elapsed_time, start=-1):
        """Visualize the path taken by the algorithm."""
        self.ax.clear()
        self.ax.set_facecolor("black")
        self.plot_graph()  # Replot the graph with vertices and edges

        # Plot the selected path
        for i in range(len(path) - 1):
            self.ax.plot([self.x[path[i]], self.x[path[i + 1]]], [self.y[path[i]], self.y[path[i + 1]]],
                         color="green", lw=2)

        if start != -1:
            self.ax.text(self.x[start], self.y[start], f"Start", color="Red", fontsize=14, ha="center")

    
        path_str = "\n".join(f"Vertex {v}" for v in path)  # Create a string of vertices with each on a new line
        self.result_text.configure(text=f"Result:\n{path_str} \n\nTotal Weight: {total_weight:.2f}\n\nTime : {elapsed_time:.6f}")
        self.canvas.draw()

    def adjust_sidebar_width(self, event):
        """Adjust sidebar width based on window size."""
        width = event.width  # Get the current window width
        sidebar_width = max(200, int(width * 0.2))  # Set sidebar width to 20% of window width, but no less than 150px
        self.sidebar_frame.configure(width=sidebar_width)


if __name__ == "__main__":
    app = App()
    app.mainloop()