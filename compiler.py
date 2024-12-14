import customtkinter
from tkinter import filedialog
from tkinter import Tk
from FileHandler import FileHandler
from scanner import Scanner
from parser_tree import ScrollableCanvas
from  parser import NonTerminals  # Assuming you'll rename the parser file
# Global variable to store the file path after upload
file_path = ""
file_content = ""


def parse_file():
    global file_path
    global file_content
    global output_box3  # Reference to the scrollable canvas for tree visualization

    if file_path:
        try:
            # Initialize the NonTerminals class and parse the file
            parser = NonTerminals(file_path)
            parser.parse()

            # Clear previous tree visualization
            output_box3.canvas.delete("all")

            # Visualize the parse tree
            def draw_parse_tree(canvas, node, x=400, y=50, x_spread=200):
                """Recursively draw the parse tree"""
                if not node:
                    return

                # Draw the current node
                node_shape = canvas.draw_node_shape(x, y, node.type or 'Root')
                
                # Display node type and text
                type_text = str(node.type or 'Root')
                value_text = str(node.text or '')
                
                # Combine type and text if text is not None
                display_text = type_text if not value_text else f"{type_text}: {value_text}"
                canvas.canvas.create_text(x, y, text=display_text, font=('Arial', 10))

                # Recursive drawing of children
                def draw_children(children, start_x, y_offset):
                    if not children:
                        return
                    
                    # If children is a list (like in stmt_sequence)
                    if isinstance(children, list):
                        child_spread = max(100, x_spread // (len(children) + 1))
                        for i, child in enumerate(children):
                            child_x = start_x + (i - len(children)//2) * child_spread
                            
                            # Draw connection line
                            canvas.canvas.create_line(x, y+25, child_x, y+y_offset-25, arrow=tk.LAST)
                            
                            # Recursively draw child
                            draw_parse_tree(canvas, child, child_x, y+y_offset, child_spread)
                    
                    # If children is a single node
                    else:
                        # Draw connection line
                        canvas.canvas.create_line(x, y+25, start_x, y+y_offset-25, arrow=tk.LAST)
                        
                        # Recursively draw child
                        draw_parse_tree(canvas, children, start_x, y+y_offset, x_spread//2)

                # Draw left, center, and right children
                draw_children(node.left, x - x_spread, 100)
                draw_children(node.center, x, 100)
                draw_children(node.right, x + x_spread, 100)

            # Start drawing from the root
            draw_parse_tree(output_box3, parser.root)
            
            # Update scroll region
            output_box3.canvas.config(scrollregion=output_box3.canvas.bbox("all"))

            # Optional: print the tree structure to output box for additional information
            output_box2.delete(1.0, "end")
            
            # Capture print_tree output
            import io
            import sys
            
            # Redirect stdout to capture print_tree output
            old_stdout = sys.stdout
            result = io.StringIO()
            sys.stdout = result
            
            parser.root.print_tree()
            
            # Restore stdout and get output
            sys.stdout = old_stdout
            tree_structure = result.getvalue()
            
            output_box2.insert("end", "Parse Tree Structure:\n")
            output_box2.insert("end", tree_structure)

        except Exception as e:
            output_box2.delete(1.0, "end")
            output_box2.insert("end", f"Parse Error: {str(e)}")


def parse_file2():  
    parser = NonTerminals(file_path)
    parser.parse()
    ScrollableCanvas.visualize_tree(parser.root)


# Function to handle file browsing
def browse_file():
    global file_path  # Use the global file_path variable
    global file_content # Use the global file_content variable
    # Open a file dialog to browse files
    file_path = filedialog.askopenfilename(
        title="Select a File",
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
    )
    if file_path:
        print(f"File selected: {file_path}")
        input_label.configure(text=f"Selected: {file_path.split('/')[-1]}")  # Update label to show file name

        # Use FileHandler to read the file content
        try:
            file_content = FileHandler.read_file(file_path)
            # Display the file content in the output box
            output_box.delete(1.0, "end")  # Clear the previous content
            output_box.insert("end", file_content)  # Insert the new file content
        except Exception as e:
            output_box.delete(1.0, "end")  # Clear the output box in case of error
            output_box.insert("end", f"Error: {str(e)}")  # Display error message in output box


# Function to handle scanning the file
def scan_file():
    global file_path  # Access the global file_path variable
    global file_content
    if file_path:
        try:
            # Initialize the Scanner class and call the scan method
            scanner = Scanner(file_content)
            output_box2.delete(1.0, "end")  # Clear previous scan result
            output_box2.insert("end", str(scanner))  # Insert the scan result
        except Exception as e:
            output_box2.delete(1.0, "end")  # Clear the output box in case of error
            output_box2.insert("end", f"Error: {str(e)}")  # Display error message in output box


# Function to reset the interface
def reset_interface():
    global file_path  # Access the global file_path variable
    global file_content  # Access the global file_content variable

    # Reset global variables
    file_path = ""
    file_content = ""

    # Clear the output boxes
    output_box.delete(1.0, "end")  # Clear file content box
    output_box2.delete(1.0, "end")  # Clear scan result box

    output_box3.canvas.delete("all") # Clear tree
    # Reset the input label text
    input_label.configure(text="Input")  # Reset input label to default text

    print("Reset clicked")  # Optionally log the reset action for debugging purposes




# Initialize the app
app = customtkinter.CTk()
app.title("Parser Application")
app.geometry("1200x800")

# Input Section
input_frame = customtkinter.CTkFrame(app)
input_frame.pack(pady=30, fill="x")

# Configure grid layout for input_frame
input_frame.grid_columnconfigure(0, weight=1)

# Inner Frame for Centering Label and Button
center_frame = customtkinter.CTkFrame(input_frame)
center_frame.grid(row=0, column=0)

# Input Label
input_label = customtkinter.CTkLabel(center_frame, text="Input")
input_label.grid(row=0, column=0, padx=10)

# Upload Button
upload_button = customtkinter.CTkButton(center_frame, text="Upload", command=browse_file)
upload_button.grid(row=0, column=1, padx=10)


# Action Section
action_frame = customtkinter.CTkFrame(app)
action_frame.pack(pady=10, fill="x")

# Scan Button
scan_button = customtkinter.CTkButton(action_frame, text="Scan", command=scan_file)  # Call scan_file function
scan_button.pack(side="left", padx=10)

parse_button = customtkinter.CTkButton(action_frame, text="Parse",command= parse_file2)
parse_button.pack(side="left", padx=10)

# Reset Button with functionality to call the reset_interface function
reset_button = customtkinter.CTkButton(action_frame, text="Reset", command=reset_interface)
reset_button.pack(side="right", padx=10)

# Output Section
output_label = customtkinter.CTkLabel(app, text="File Content:")
output_label.pack(pady=10)

output_box = customtkinter.CTkTextbox(app, width=500, height=100)
output_box.pack(pady=40)

# Output Section for Scan Results and Parse Results
output_frame = customtkinter.CTkFrame(app)
output_frame.pack(pady=10, fill="x")

# Configure the grid layout to have two columns
output_frame.grid_columnconfigure(0, weight=1, minsize=250)  # Left column for Scan Results
output_frame.grid_columnconfigure(1, weight=1, minsize=800)  # Right column for Parse Results

# Output Section for Scan Results (Left Side)
output_label2 = customtkinter.CTkLabel(output_frame, text="Scan Results:")
output_label2.grid(row=0, column=0, padx=10, pady=10, sticky="w")  # "w" aligns it to the left

output_box2 = customtkinter.CTkTextbox(output_frame, width=250, height=250)  # Increased size
output_box2.grid(row=1, column=0, padx=10, pady=10, sticky="w")  # Align text box to the left

# Output Section for Parse Results (Right Side)
# output_label3 = customtkinter.CTkLabel(output_frame, text="Parse Results:")
# output_label3.grid(row=0, column=1, padx=10, pady=10, sticky="e")  # "e" aligns it to the right

# output_box3 = ScrollableCanvas(output_frame, width=800, height=250)
# output_box3.grid(row=1, column=1, padx=10, pady=10, sticky="e")

#################### TEST ########################
# Draw shapes on the canvas
# output_box3.draw_square(100, 100, 50)
# output_box3.draw_square(300, 300, 80)
# output_box3.draw_circle(500, 150, 30)
# output_box3.draw_circle(700, 400, 40)


# Update scroll region based on the drawn shapes
# output_box3.set_scroll_region()
##################################################

# Run the app
app.mainloop()
