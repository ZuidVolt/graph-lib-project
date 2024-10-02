# gui.py
import tkinter as tk
from typing import Dict, Any, List
import datetime
import logging

logging.basicConfig(level=logging.DEBUG)


class Plotter:
    def __init__(self, root, canvas_width, canvas_height, margin, csv_dict: Dict[str, List[Any]]):
        self.root = root
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        self.margin = margin
        self.plot_width = canvas_width - 2 * margin
        self.plot_height = canvas_height - 2 * margin
        self.canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg="white")
        self.canvas.grid(row=0, column=0, padx=10, pady=10)
        self.csv_dict = csv_dict
        self.dates_numeric = {}
        self.colors = ["blue", "red", "green", "yellow", "orange", "purple"]

        # Detect the date column and convert dates to numeric
        for key, values in csv_dict.items():
            if isinstance(values[0], str) and self._is_date(values):  # Ensure values are strings before checking
                self.dates_numeric[key] = self._convert_dates_to_numeric(values)

    def _is_date(self, values: List[str]) -> bool:
        """Check if a list of strings are date values."""
        try:
            for value in values:
                datetime.datetime.strptime(value, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    def _convert_dates_to_numeric(self, dates: List[str]) -> List[int]:
        """Convert date strings into the number of days since the first date."""
        base_date = datetime.datetime.strptime(dates[0], "%Y-%m-%d")
        return [(datetime.datetime.strptime(date, "%Y-%m-%d") - base_date).days for date in dates]

    def _data_to_canvas(self, data_x, data_y, x_min, x_max, y_min, y_max):
        """Scale x and y values based on the plot dimensions."""
        if x_max - x_min == 0:
            scaled_x = self.margin + self.plot_width / 2
        else:
            scaled_x = ((data_x - x_min) / (x_max - x_min)) * self.plot_width + self.margin

        if y_max - y_min == 0:
            scaled_y = self.margin + self.plot_height / 2
        else:
            scaled_y = self.plot_height - ((data_y - y_min) / (y_max - y_min)) * self.plot_height + self.margin

        return scaled_x, scaled_y

    def draw_data_points(self):
        # Get the first key from the dictionary as the X values
        x_key = next(iter(self.csv_dict.keys()))
        x_values = self.csv_dict[x_key]  # X-values

        # Get all other keys as Y values
        y_keys = list(self.csv_dict.keys())
        y_keys.remove(x_key)

        # Convert X values to numeric if they are dates
        if x_key in self.dates_numeric:
            x_values = self.dates_numeric[x_key]

        # Find min and max values for X and Y
        x_min, x_max = min(x_values), max(x_values)
        y_min, y_max = float("inf"), float("-inf")
        for y_key in y_keys:
            y_values = self.csv_dict[y_key]
            y_min = min(y_min, min(y_values))
            y_max = max(y_max, max(y_values))

        # Draw data points for each Y value
        for i, y_key in enumerate(y_keys):
            y_values = self.csv_dict[y_key]
            data_points = zip(x_values, y_values)
            canvas_points = [self._data_to_canvas(x, y, x_min, x_max, y_min, y_max) for x, y in data_points]

            color = self.colors[i % len(self.colors)]  # Cycle through colors

            for point in canvas_points:
                self.canvas.create_oval(point[0] - 3, point[1] - 3, point[0] + 3, point[1] + 3, fill=color)

            # Draw lines connecting the points
            for j in range(len(canvas_points) - 1):
                self.canvas.create_line(canvas_points[j], canvas_points[j + 1], fill=color, width=2)

            # Add a legend entry
            self.canvas.create_text(self.canvas_width - self.margin + 10, self.margin + i * 20, text=y_key, fill=color)

    def draw_axis(self):
        """Draw X and Y axes with arrows."""
        # X-axis
        self.canvas.create_line(
            self.margin,
            self.canvas_height - self.margin,
            self.canvas_width - self.margin,
            self.canvas_height - self.margin,
            arrow=tk.LAST,
            fill="black",
        )
        # Y-axis
        self.canvas.create_line(
            self.margin, self.canvas_height - self.margin, self.margin, self.margin, arrow=tk.LAST, fill="black"
        )

    def tick_marks(self):
        """Add tick marks on the X and Y axes."""

    def add_labels(self):
        """Add labels for X and Y axes."""


def main():
    root = tk.Tk()
    root.title("Plotter with Date and Value")
    root.resizable(True, True)

    canvas_width = 600
    canvas_height = 400
    margin = 50

    # Example CSV data (Dictionary format)
    csv_dict: Dict[str, list[Any]] = {
        "Date": ["2022-01-01", "2022-01-02", "2022-01-03", "2022-01-04", "2022-01-05"],
        "Value": [10, 15, 20, 25, 30],
    }

    plotter = Plotter(root, canvas_width, canvas_height, margin, csv_dict)

    plotter.draw_axis()
    plotter.tick_marks()
    plotter.draw_data_points()
    plotter.add_labels()
    plotter.add_legend()

    root.mainloop()


if __name__ == "__main__":
    main()
