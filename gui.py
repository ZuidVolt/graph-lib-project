import tkinter as tk

# Create the main window
root = tk.Tk()

# Set the title of the window
root.title("Tkinter Window with Canvas")

# Define the size of the canvas (e.g., width=400, height=300)
canvas_width = 400
canvas_height = 300

# Create a Canvas widget and add it to the window
canvas = tk.Canvas(root, width=canvas_width, height=canvas_height)

# Place the canvas in the window using grid layout management (optional but recommended)
canvas.grid(row=0, column=0, padx=10, pady=10)

# Make the window resizable (optional)
root.resizable(True, True)

# Run the application
root.mainloop()