class Node:
    def __init__(self, type, text, left, center, right):
        self.type = type
        self.text = text
        self.left = left
        self.center = center
        self.right = right
    def __str__(self):
        if self.text:
            return f"{self.type}\n({self.text})"
        else:
            return str(self.type)

    def print_tree(self, level=0):
        final_str = []
        indent = "  " * level  # Indentation based on depth level
        final_str.append(f"{indent}- {self.type}: {self.text}\n")
        # Helper function to recursively print child nodes
        def print_child(name, child, level):
            minor_str = []
            if child:
                minor_str.append(f"{indent}  {name}:\n")
                if isinstance(child, list):  # If the child is a list, iterate over its elements
                    for idx, node in enumerate(child):
                        minor_str.append(f"{indent}    [{idx}]\n")
                        minor_str.append(node.print_tree(level + 2))
                else:  # If it's a single node, print it normally
                    minor_str.append(child.print_tree(level + 1))
            return "".join(st for st in minor_str)
        # Print left, center, and right
        final_str.append(print_child("Left", self.left, level))
        final_str.append(print_child("Center", self.center, level))
        final_str.append(print_child("Right", self.right, level))

        return "".join(st for st in final_str)

class Statement(Node):
    def __init__(self, type, text, left, center, right):
        super().__init__(type, text, left, center, right)

class Operation(Node):
    def __init__(self, text, left, right):
        super().__init__("op", text, left, None, right)

class Factor(Node):
    def __init__(self, type, text):
        super().__init__(type, text, None, None, None)
