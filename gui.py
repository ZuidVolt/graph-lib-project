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
        scaled_x = ((data_x - x_min) / (x_max - x_min)) * self.plot_width + self.margin
        scaled_y = self.plot_height - ((data_y - y_min) / (y_max - y_min)) * self.plot_height + self.margin
        return scaled_x, scaled_y

    def draw_data_points(self):
        # Get the first date key from the converted numeric dates
        date_key = next(iter(self.dates_numeric.keys()))
        x_values = self.dates_numeric[date_key]  # Numeric X-values for dates
        y_values = self.csv_dict["Value"]  # Y-values

        x_min, x_max = min(x_values), max(x_values)
        y_min, y_max = min(y_values), max(y_values)

        data_points = zip(x_values, y_values)
        canvas_points = [self._data_to_canvas(x, y, x_min, x_max, y_min, y_max) for x, y in data_points]

        for point in canvas_points:
            self.canvas.create_oval(point[0] - 3, point[1] - 3, point[0] + 3, point[1] + 3, fill="blue")

        # Draw lines connecting the points
        for i in range(len(canvas_points) - 1):
            self.canvas.create_line(canvas_points[i], canvas_points[i + 1], fill="blue", width=2)

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

    def add_legend(self):
        """Add a legend for the plotted data."""


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
