import tkinter as tk
from tkinter import ttk
from custom_parser import NonTerminals

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


    def draw_tree(self, root, start_x=800, start_y=50, node_size=60, y_spread=120, gap=35):
        """Recursively draw a syntax tree with dynamic spacing."""
        def calculate_width(node):
            """Recursively calculate the width of a subtree."""
            if not node:  # If node is None, width is 0
                return 0

            # If a child is a list, calculate the combined width of the list
            def list_width(children):
                return sum(calculate_width(child) - 2 * gap for child in children) + (len(children) + 1) * gap

            left_width = gap + list_width(node.left) if isinstance(node.left, list) else calculate_width(node.left)
            center_width = list_width(node.center) if isinstance(node.center, list) else calculate_width(node.center)
            right_width = gap + list_width(node.right) if isinstance(node.right, list) else calculate_width(node.right)

            # Total width: at least the size of the node, plus space for children
            return max(node_size + gap * 2, left_width + center_width + right_width)

        def calculate_width_general(node):
            return calculate_width(node) if not isinstance(node, list) else sum(calculate_width(child) - gap * 2 for child in node) + gap * (len(node) + 1)


        def draw_subtree(node, x, y, total_width):
            """Helper function to draw the tree and return its center position."""
            if not node:  # Base case: empty node
                return x

            # Draw the current node
            if (node.type):
                node_id = self.draw_node_shape(x, y, node.type, size=node_size)
                self.canvas.create_text(x, y, text=str(node), font=("Arial", 12))
            left_width = calculate_width_general(node.left)
            center_width = calculate_width_general(node.center)
            right_width = calculate_width_general(node.right)

            child_y = y + y_spread

            # Helper to draw lists of children
            def draw_child_list(child_list, child_x, child_y):
                """Draw a list of children horizontally starting from start_x."""
                prev_x = child_x
                for idx, child in enumerate(child_list):
                    child_width = calculate_width(child)
                    child_right_width = calculate_width_general(child.right)
                    child_center_width = calculate_width_general(child.center)
                    draw_subtree(child, prev_x, child_y, child_width)
                    if idx < len(child_list) - 1:
                        next_left_width = calculate_width_general(child_list[idx + 1].left)
                        self.canvas.create_line(prev_x + node_size // 2, child_y, prev_x + (child_right_width + child_center_width) + max(next_left_width, node_size + 2 * gap) - node_size // 2 - gap, child_y, arrow="last")
                        prev_x += max(next_left_width, node_size + 2 * gap)
                    prev_x += (child_right_width + child_center_width) - gap

            # Handle left child
            if node.left:
                if isinstance(node.left, list) and len(node.left) >= 2:
                    child_x = x - left_width + calculate_width_general(node.left[0]) // 2 #current_x + left_width // 2
                    draw_child_list(node.left, child_x, child_y)
                    if node.type:
                        self.canvas.create_line(x, y + node_size // 2, child_x, child_y - node_size // 2, arrow="last")
                else:
                    if isinstance(node.left, list):
                        node.left = node.left[0]
                    child_x = x - left_width // 2 #current_x + left_width // 2
                    draw_subtree(node.left, child_x, child_y, left_width)
                    if node.type:
                        self.canvas.create_line(x, y + node_size // 2, child_x, child_y - node_size // 2, arrow="last")

            # Handle center child
            if node.center:
                child_x = x #current_x + left_width // 2
                if isinstance(node.center, list) and len(node.center) >= 2:
                    draw_child_list(node.center, child_x, child_y)
                    if node.type:
                        self.canvas.create_line(x, y + node_size // 2, child_x, child_y - node_size // 2, arrow="last")
                else:
                    if isinstance(node.center, list):
                        node.center = node.center[0]
                    draw_subtree(node.center, child_x, child_y, center_width)
                    if node.type:
                        self.canvas.create_line(x, y + node_size // 2, child_x, child_y - node_size // 2, arrow="last")

            # Handle right child
            if node.right:
                if isinstance(node.right, list) and len(node.right) >= 2:
                    child_x = x + center_width #current_x + left_width // 2
                    if node.type:
                        self.canvas.create_line(x, y + node_size // 2, child_x, child_y - node_size // 2, arrow="last")
                    draw_child_list(node.right, child_x, child_y)
                else:
                    if isinstance(node.right, list):
                        node.right = node.right[0]
                    child_x = x + center_width + right_width // 2#current_x + left_width // 2
                    draw_subtree(node.right, child_x, child_y, right_width)
                    if node.type:
                        self.canvas.create_line(x, y + node_size // 2, child_x, child_y - node_size // 2, arrow="last")

            return x

        tree_width = calculate_width(root)
        draw_subtree(root, start_x, start_y, tree_width)

        # Update scroll region to fit the entire tree
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def visualize_tree(self, root):
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
