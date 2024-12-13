class Node:
    def __init__(self, type, text, left, center, right):
        self.type = type
        self.text = text
        self.left = left
        self.center = center
        self.right = right
    # def __str__(self):
    #     return f"{self.type}, {self.text}, {self.left}, {self.center}, {self.right}"

    def print_tree(self, level=0):
        indent = "  " * level  # Indentation based on depth level
        print(f"{indent}- {self.type}: {self.text}")

        # Helper function to recursively print child nodes
        def print_child(name, child, level):
            if child:
                print(f"{indent}  {name}:")
                if isinstance(child, list):  # If the child is a list, iterate over its elements
                    for idx, node in enumerate(child):
                        print(f"{indent}    [{idx}]")
                        node.print_tree(level + 2)
                else:  # If it's a single node, print it normally
                    child.print_tree(level + 1)
        # Print left, center, and right
        print_child("Left", self.left, level)
        print_child("Center", self.center, level)
        print_child("Right", self.right, level)

class Statement(Node):
    def __init__(self, type, text, left, center, right):
        super().__init__(type, text, left, center, right)

class Operation(Node):
    def __init__(self, text, left, right):
        super().__init__("op", text, left, None, right)

class Factor(Node):
    def __init__(self, type, text):
        super().__init__(type, text, None, None, None)
