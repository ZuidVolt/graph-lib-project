# gui.py
import tkinter as tk


class Plotter:
    def __init__(self, root, canvas_width, canvas_height, margin):
        self.root = root
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        self.margin = margin
        self.plot_width = canvas_width - 2 * margin
        self.plot_height = canvas_height - 2 * margin
        self.canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg="white")
        self.canvas.grid(row=0, column=0, padx=10, pady=10)

    def data_to_canvas(self, data_x, data_y):
        # Scale x and y values based on the plot dimensions
        scaled_x = (data_x / 100) * self.plot_width + self.margin
        scaled_y = self.plot_height - ((data_y / 100) * self.plot_height) + self.margin
        return scaled_x, scaled_y

    def draw_data_points(self, data_points):
        canvas_points = [self.data_to_canvas(x, y) for x, y in data_points]
        for point in canvas_points:
            self.canvas.create_oval(point[0] - 3, point[1] - 3, point[0] + 3, point[1] + 3, fill="blue")

    def draw_axis(self):
        # Drawing the X-axis (from left margin to right margin)
        self.canvas.create_line(
            self.margin,  # Start x
            self.canvas_height - self.margin,  # Start y (bottom)
            self.canvas_width - self.margin,  # End x (right)
            self.canvas_height - self.margin,  # End y (bottom)
            arrow=tk.LAST,  # Arrow at the end
            fill="black",
        )
        # Drawing the Y-axis (from bottom margin to top margin)
        self.canvas.create_line(
            self.margin,  # Start x (left)
            self.canvas_height - self.margin,  # Start y (bottom)
            self.margin,  # End x (left)
            self.margin,  # End y (top)
            arrow=tk.LAST,  # Arrow at the top
            fill="black",
        )

    def add_labels(self):
        pass


def main():
    root = tk.Tk()
    root.title("Tkinter Window with Canvas")
    root.resizable(True, True)

    canvas_width = 400
    canvas_height = 300
    margin = 40

    plotter = Plotter(root, canvas_width, canvas_height, margin)

    # Sample data points (X, Y)
    data_points = [(50, 30), (20, 70), (80, 90)]

    # Draw data points, axis, and labels
    plotter.draw_data_points(data_points)
    plotter.draw_axis()
    plotter.add_labels()

    root.mainloop()


if __name__ == "__main__":
    main()
