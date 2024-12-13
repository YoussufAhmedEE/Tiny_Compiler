import customtkinter
from tkinter import filedialog
from tkinter import Tk
from FileHandler import FileHandler
from scanner import Scanner
from parser_tree import ScrollableCanvas
# Global variable to store the file path after upload
file_path = ""
file_content = ""

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

parse_button = customtkinter.CTkButton(action_frame, text="Parse")  # Call parse_file function
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
output_label3 = customtkinter.CTkLabel(output_frame, text="Parse Results:")
output_label3.grid(row=0, column=1, padx=10, pady=10, sticky="e")  # "e" aligns it to the right

output_box3 = ScrollableCanvas(output_frame, width=800, height=250)
output_box3.grid(row=1, column=1, padx=10, pady=10, sticky="e")

#################### TEST ########################
# Draw shapes on the canvas
output_box3.draw_square(100, 100, 50)
output_box3.draw_square(300, 300, 80)
output_box3.draw_circle(500, 150, 30)
output_box3.draw_circle(700, 400, 40)


# Update scroll region based on the drawn shapes
output_box3.set_scroll_region()
##################################################

# Run the app
app.mainloop()
