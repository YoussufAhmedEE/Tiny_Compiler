import customtkinter
from tkinter import filedialog
from tkinter import Tk
from FileHandler import FileHandler
from scanner import Scanner
from parser_tree import ScrollableCanvas
from custom_parser import NonTerminals  # Assuming you'll rename the parser file
# Global variable to store the file path after upload
file_path = ""
file_content = ""


def parse_input():
    global input_box
    global syntax_tree_canvas  # Reference to the scrollable canvas for tree visualization

    file_content = input_box.get("0.0", "end").strip()
    if file_content:
        try:
            parser = NonTerminals(file_content)
            parser.parse()

            # Clear previous tree visualization
            print(parser.root.print_tree())
            output_box.delete(1.0, "end")
            output_box.insert("end", "Parse Tree Structure:\n")
            output_box.insert("end", parser.root.print_tree())

            syntax_tree_canvas.canvas.delete("all")
            syntax_tree_canvas.visualize_tree(parser.root)


        except Exception as e:
            output_box.delete(1.0, "end")
            output_box.insert("end", f"Parse Error: {str(e)}")

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
        upload_label.configure(text=f"Selected: {file_path.split('/')[-1]}")  # Update label to show file name

        # Use FileHandler to read the file content
        try:
            file_content = FileHandler.read_file(file_path)
            # Display the file content in the output box
            input_box.delete(1.0, "end")  # Clear the previous content
            input_box.insert("end", file_content)  # Insert the new file content
        except Exception as e:
            input_box.delete(1.0, "end")  # Clear the output box in case of error
            input_box.insert("end", f"Error: {str(e)}")  # Display error message in output box


# Function to handle scanning the file
def scan_input():
    global input_box
    file_content = input_box.get("0.0", "end").strip()
    if file_content:
        try:
            # Initialize the Scanner class and call the scan method
            scanner = Scanner(file_content)
            output_box.delete(1.0, "end")  # Clear previous scan result
            output_box.insert("end", str(scanner))  # Insert the scan result
        except Exception as e:
            output_box.delete(1.0, "end")  # Clear the output box in case of error
            output_box.insert("end", f"Error: {str(e)}")  # Display error message in output box


# Function to reset the interface
def reset_interface():
    global file_path  # Access the global file_path variable
    global file_content  # Access the global file_content variable

    # Reset global variables
    file_path = ""
    file_content = ""

    # Clear the output boxes
    input_box.delete(1.0, "end")  # Clear file content box
    output_box2.delete(1.0, "end")  # Clear scan result box
    syntax_tree_canvas.canvas.delete("all") # Clear tree
    upload_label.configure(text="Upload input:")  # Reset input label to default text


# Initialize the app
app = customtkinter.CTk()
app.title("Parser Application")
app.geometry("1200x500")

# ================= Layout Structure =================

# Configure main grid layout (3 columns: buttons, output_box, output_box2)
app.grid_columnconfigure(0, weight=1)  # Left section for buttons
app.grid_columnconfigure(1, weight=2)  # Center section for output_box
app.grid_columnconfigure(2, weight=2)  # Right section for output_box2

# ================= Left Section: Buttons =================
button_frame = customtkinter.CTkFrame(app)
button_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsw")

# Buttons inside button_frame
upload_label = customtkinter.CTkLabel(button_frame, text="Upload input:")
upload_label.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="nsw")

upload_button = customtkinter.CTkButton(button_frame, text="Upload", command=browse_file)
upload_button.grid(row=1, column=0, padx=0, pady=(0, 50), sticky="nsw")

scan_button = customtkinter.CTkButton(button_frame, text="Scan", command=scan_input)
scan_button.grid(row=2, column=0, padx=0, pady=(10, 10), sticky="nsw")

parse_button = customtkinter.CTkButton(button_frame, text="Parse", command=parse_input)
parse_button.grid(row=3, column=0, padx=0, pady=(10, 10), sticky="nsw")

reset_button = customtkinter.CTkButton(button_frame, text="Reset", command=reset_interface)
reset_button.grid(row=4, column=0, padx=0, pady=(220, 10), sticky="nsw")

# ================= Center Section: Output Box =================
center_frame = customtkinter.CTkFrame(app)
center_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

input_label = customtkinter.CTkLabel(center_frame, text="File Content: Start typing in TINY, or upload a file.")
input_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

input_box = customtkinter.CTkTextbox(center_frame, width=500, height=400)
input_box.grid(row=1, column=0, padx=10, pady=10, sticky="w")

# ================= Right Section: Output Box 2 =================
output_frame = customtkinter.CTkFrame(app)
output_frame.grid(row=0, column=2, padx=20, pady=20, sticky="nse")

output_label = customtkinter.CTkLabel(output_frame, text="Scan/Parse Results:")
output_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

output_box = customtkinter.CTkTextbox(output_frame, width=400, height=400)
output_box.grid(row=1, column=0, padx=10, pady=10, sticky="w")

syntax_tree_canvas = ScrollableCanvas(output_frame)
# ================= Start the Application =================# Run the app
app.mainloop()
