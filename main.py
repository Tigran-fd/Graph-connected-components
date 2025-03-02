#!/usr/bin/python3
import igraph as ig
import matplotlib.pyplot as plt
from tkinter import *
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from typing import List, Tuple


def plot_graph_with_components_on_canvas(canvas_frame: Frame,
                                         vertex_labels: List[str],
                                         edge_list: List[Tuple[str, str]]) -> None:
    g = ig.Graph()

    unique_vertex_labels = list(set(vertex_labels))
    g.add_vertices(unique_vertex_labels)

    label_to_index = {label: i for i, label in enumerate(unique_vertex_labels)}

    indexed_edges = []
    for u, v in edge_list:
        if u not in label_to_index or v not in label_to_index:
            messagebox.showerror("Input Error", f"Edge ({u}, {v}) references a non-existent vertex.")
            return
        if u == v:
            messagebox.showerror("Input Error", f"Self-loop detected: ({u}, {v})")
            return
        indexed_edges.append((label_to_index[u], label_to_index[v]))

    g.add_edges(indexed_edges)
    g.vs["label"] = unique_vertex_labels

    components = g.connected_components(mode='weak')
    membership = components.membership
    num_components = max(membership) + 1

    colors = [f"#{int(255 * i / num_components):02x}{int(255 * (num_components - i) / num_components):02x}80"
              for i in membership]

    fig, ax = plt.subplots(figsize=(10, 10))

    ig.plot(
        g,
        target=ax,
        vertex_size=48,
        vertex_label=g.vs["label"],
        vertex_color=colors,
        edge_width=2,
        layout=g.layout_fruchterman_reingold()
    )

    for widget in canvas_frame.winfo_children():
        widget.destroy()

    canvas = FigureCanvasTkAgg(fig, master=canvas_frame)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(fill=BOTH, expand=True)
    canvas.draw()


def display_graph_ui() -> None:
    def process_graph_input() -> None:
        vertex_labels = vertex_entry.get().split()
        edge_input = edge_text.get("1.0", END).strip()
        edges: List[Tuple[str, str]] = []

        for line in edge_input.split("\n"):
            try:
                u, v = line.split()
                edges.append((u, v))
            except ValueError:
                messagebox.showerror("Input Error", f"Invalid edge format: {line}")
                return

        if len(set(vertex_labels)) != len(vertex_labels):
            messagebox.showerror("Input Error", "Duplicate vertex labels found.")
            return

        if not vertex_labels or not edges:
            messagebox.showerror("Input Error", "Please enter both vertices and edges!")
            return

        plot_graph_with_components_on_canvas(canvas_frame, vertex_labels, edges)

    graph_window = Tk()
    graph_window.title("Graph Connected Components")
    graph_window.geometry("1920x1080")

    input_frame = Frame(graph_window)
    input_frame.pack(side=TOP, fill=X, padx=10, pady=10)

    Label(input_frame, text="Enter vertex labels (space-separated):").pack(pady=5)
    vertex_entry = Entry(input_frame, width=50)
    vertex_entry.pack(pady=5)

    Label(input_frame, text="Enter edges (one per line, format: u v):").pack(pady=5)
    edge_text = Text(input_frame, height=10, width=50)
    edge_text.pack(pady=5)

    ttk.Button(input_frame, text="View Connected Components", command=process_graph_input).pack(pady=10)

    canvas_frame = Frame(graph_window, bd=2, relief=SUNKEN)
    canvas_frame.pack(side=BOTTOM, fill=BOTH, expand=True, padx=10, pady=10)

    graph_window.mainloop()


if __name__ == "__main__":
    display_graph_ui()
