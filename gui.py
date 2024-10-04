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
        self.colors = ["blue", "red", "green", "orange", "purple", "brown"]

        # Detect the date column and convert dates to numeric
        for key, values in csv_dict.items():
            if isinstance(values[0], str) and self._is_date(values):
                self.dates_numeric[key] = self._convert_dates_to_numeric(values)

    def _is_date(self, values: List[str]) -> bool:
        try:
            for value in values:
                datetime.datetime.strptime(value, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    def _convert_dates_to_numeric(self, dates: List[str]) -> List[int]:
        base_date = datetime.datetime.strptime(dates[0], "%Y-%m-%d")
        return [(datetime.datetime.strptime(date, "%Y-%m-%d") - base_date).days for date in dates]

    def _data_to_canvas(self, data_x, data_y, x_min, x_max, y_min, y_max):
        if x_max - x_min == 0:
            scaled_x = self.margin + self.plot_width / 2
        else:
            scaled_x = ((data_x - x_min) / (x_max - x_min)) * self.plot_width + self.margin

        if y_max - y_min == 0:
            scaled_y = self.margin + self.plot_height / 2
        else:
            scaled_y = self.canvas_height - ((data_y - y_min) / (y_max - y_min)) * self.plot_height - self.margin

        return scaled_x, scaled_y

    def draw_data_points(self, x_axis_key=None):
        if x_axis_key is None:
            x_key = next(iter(self.csv_dict.keys()))
        elif x_axis_key in self.csv_dict:
            x_key = x_axis_key
        else:
            raise ValueError(f"Invalid x_axis_key: {x_axis_key}. Key not found in csv_dict.")

        x_values = self.dates_numeric.get(x_key, self.csv_dict[x_key])
        y_keys = [k for k in self.csv_dict if k != x_key]

        x_min, x_max = min(x_values), max(x_values)
        y_min, y_max = float("inf"), float("-inf")
        for y_key in y_keys:
            y_values = self.csv_dict[y_key]
            y_min = min(y_min, min(y_values))
            y_max = max(y_max, max(y_values))

        # Add some padding to y-axis
        y_padding = (y_max - y_min) * 0.1
        y_min -= y_padding
        y_max += y_padding

        for i, y_key in enumerate(y_keys):
            y_values = self.csv_dict[y_key]
            data_points = zip(x_values, y_values)
            canvas_points = [self._data_to_canvas(x, y, x_min, x_max, y_min, y_max) for x, y in data_points]

            color = self.colors[i % len(self.colors)]

            # Draw lines connecting the points
            for j in range(len(canvas_points) - 1):
                self.canvas.create_line(canvas_points[j], canvas_points[j + 1], fill=color, width=2)

            # Draw data points
            for point in canvas_points:
                self.canvas.create_oval(point[0] - 3, point[1] - 3, point[0] + 3, point[1] + 3, fill=color)

            # Add legend entry
            legend_x = self.canvas_width - self.margin + 10
            legend_y = self.margin + i * 20
            self.canvas.create_oval(legend_x, legend_y - 3, legend_x + 6, legend_y + 3, fill=color)
            self.canvas.create_text(legend_x + 15, legend_y, text=y_key, anchor="w", fill=color)

        self._draw_axis_labels(x_key, x_min, x_max, y_min, y_max)

        ## To be implemented
        # self._draw_tick_marks(x_key, x_min, x_max, y_min, y_max)

        # self._draw_title_label()

    def _draw_axis_labels(self, x_key, x_min, x_max, y_min, y_max):  # TODO: fix the label display
        # X-axis labels
        for i in range(6):
            x = x_min + (x_max - x_min) * i / 5
            canvas_x, canvas_y = self._data_to_canvas(x, y_min, x_min, x_max, y_min, y_max)

            if x_key in self.dates_numeric:
                base_date = datetime.datetime.strptime(self.csv_dict[x_key][0], "%Y-%m-%d")
                date = base_date + datetime.timedelta(days=int(x))
                label = date.strftime("%Y-%m-%d")
            else:
                label = f"{x:.1f}"

            self.canvas.create_text(canvas_x, canvas_y + 15, text=label, angle=45)
            self.canvas.create_line(canvas_x, canvas_y, canvas_x, canvas_y + 5)

        # Y-axis labels
        for i in range(6):
            y = y_min + (y_max - y_min) * i / 5
            canvas_x, canvas_y = self._data_to_canvas(x_min, y, x_min, x_max, y_min, y_max)
            self.canvas.create_text(canvas_x - 25, canvas_y, text=f"{y:.1f}")
            self.canvas.create_line(canvas_x - 5, canvas_y, canvas_x, canvas_y)

    def _draw_tick_marks(self):  # TODO: Implement the tick marks
        """displays Dynamic tick marks for the X and Y axis"""

    def _draw_title_label(self):  # TODO: Implement the title labels
        """displays Dynamic title labels for the X and Y axis"""

    def draw_axis(self):
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


def main():
    root = tk.Tk()
    root.title("Data Plotter")

    canvas_width = 1000
    canvas_height = 600
    margin = 60

    # Example data
    csv_dict: Dict[str, List[Any]] = {  # add more data types later
        "Date": ["2022-01-01", "2022-01-02", "2022-01-03", "2022-01-04", "2022-01-05"],
        "Temperature": [10, 15, 20, 25, 30],
        "Humidity": [50, 45, 40, 35, 30],
    }

    plotter = Plotter(root, canvas_width, canvas_height, margin, csv_dict)
    plotter.draw_axis()
    plotter.draw_data_points()

    root.mainloop()


if __name__ == "__main__":
    main()
