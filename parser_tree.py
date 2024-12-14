import tkinter as tk
from tkinter import ttk
from parser import NonTerminals

class ScrollableCanvas(tk.Frame):
    def __init__(self, parent, width=1600, height=1000, scrollregion=(0, 0, 3000, 3000)):
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

    def draw_node_shape(self, x, y, node_type, size=60):
        """Draw appropriate shape based on node type"""
        colors = {
            "op": "lightblue",
            "factor": "lightgreen",
            "const": "lightgreen",
            "id": "lightgreen",
            "assign": "lightsalmon",
            "if": "lightcoral",
            "repeat": "lightseagreen",
            "read": "lightskyblue",
            "write": "lightskyblue",
            "stmt_sequence": "lightpink"
        }
        fill_color = colors.get(node_type, "lightyellow")
        
        if node_type in ["op", "factor"]:
            return self.canvas.create_oval(x - size//2, y - size//2, 
                                           x + size//2, y + size//2, 
                                           fill=fill_color, outline="black")
        else:
            return self.canvas.create_rectangle(x - size//2, y - size//2, 
                                                x + size//2, y + size//2, 
                                                fill=fill_color, outline="black")

    def draw_tree(self, root, start_x=800, start_y=50, x_spread=600, y_spread=120):
        """Recursively draw the entire tree with comprehensive child handling"""
        def _draw_tree(node, x, y, x_spread, level=0):
            if not node:
                return None

            # Draw the current node
            node_shape = self.draw_node_shape(x, y, node.type)
            
            # Prepare node text (type: text)
            display_text = f"{node.type or ''}"
            if node.text:
                display_text += f": {node.text}"
            
            # Create text for the node
            self.canvas.create_text(x, y, text=display_text, font=('Arial', 10))

            # Comprehensive child collection
            children = []
            child_names = []

            # Helper to add children safely
            def add_child(name, child_node):
                if child_node:
                    if isinstance(child_node, list):
                        for i, sub_node in enumerate(child_node):
                            children.append(sub_node)
                            child_names.append(f"{name}[{i}]")
                    else:
                        children.append(child_node)
                        child_names.append(name)

            # Add children from different attributes
            add_child("Left", node.left)
            add_child("Center", node.center)
            add_child("Right", node.right)

            # Calculate child positions
            num_children = len(children)
            child_x_spread = max(x_spread // (num_children + 1), 200)

            # Draw children
            for i, (child, child_name) in enumerate(zip(children, child_names)):
                # Calculate child x position
                child_x = x + (i - num_children//2) * child_x_spread

                # Draw connection line
                self.canvas.create_line(x, y+30, child_x, y+y_spread-30, arrow=tk.LAST)
                
                # Recursively draw child
                _draw_tree(child, child_x, y+y_spread, child_x_spread, level+1)

            return node_shape

        # Start drawing from the given start position
        _draw_tree(root, start_x, start_y, x_spread)
        
        # Update scroll region to fit the entire tree
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def visualize_tree(root):
        """Create a window to visualize the tree"""
        root_window = tk.Tk()
        root_window.title("Parse Tree Visualization")
        
        # Create scrollable canvas
        canvas_frame = ScrollableCanvas(root_window, width=1600, height=1000)
        canvas_frame.pack(fill=tk.BOTH, expand=True)
        
        # Draw the tree
        canvas_frame.draw_tree(root)
        
        root_window.mainloop()
    

    
    
# parser = NonTerminals("scanner.txt")
# parser.parse()
# visualize_tree(parser.root)