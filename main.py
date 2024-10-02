# main.py
from csv_parsing import read_headers_from_csv_file, read_data_from_csv_file, data_list_to_dict
from gui import Plotter
import tkinter as tk


def main() -> None:
    headers_list = read_headers_from_csv_file()
    data_list = read_data_from_csv_file()
    csv_dict = data_list_to_dict(headers_list, data_list)

    root = tk.Tk()
    root.title("Data Plotter")

    canvas_width = 1000
    canvas_height = 600
    margin = 60

    plotter = Plotter(root, canvas_width, canvas_height, margin, csv_dict)
    plotter.draw_axis()
    plotter.draw_data_points()

    root.mainloop()


if __name__ == "__main__":
    main()
