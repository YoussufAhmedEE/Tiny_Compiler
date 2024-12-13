import tkinter as tk
from tkinter import ttk

class ScrollableCanvas(tk.Frame):
    def __init__(self, parent, width=800, height=600, scrollregion=(0, 0, 1000, 1000)):
        super().__init__(parent)

        # Create a canvas widget
        self.canvas = tk.Canvas(self, bg="white", width=width, height=height, scrollregion=scrollregion)
        self.canvas.grid(row=0, column=0, sticky="nsew")

        # Create horizontal and vertical scrollbars
        self.h_scroll = tk.Scrollbar(self, orient="horizontal", command=self.canvas.xview)
        self.h_scroll.grid(row=1, column=0, sticky="ew")
        self.v_scroll = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.v_scroll.grid(row=0, column=1, sticky="ns")

        # Configure the canvas to work with the scrollbars
        self.canvas.config(xscrollcommand=self.h_scroll.set, yscrollcommand=self.v_scroll.set)

        # Make the frame expand to fill available space
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def draw_square(self, x, y, size=50):
        """Draw a square at specific coordinates"""
        return self.canvas.create_rectangle(x, y, x + size, y + size, fill="blue", outline="black")

    def draw_circle(self, x, y, radius=25):
        """Draw a circle at specific coordinates"""
        return self.canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill="red", outline="black")

    def set_scroll_region(self):
        """Update scroll region based on canvas items"""
        self.canvas.config(scrollregion=self.canvas.bbox("all"))
