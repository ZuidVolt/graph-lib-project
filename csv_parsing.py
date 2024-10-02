# csv_parsing.py
import csv
from pathlib import Path
from typing import Dict, Any, List

DATA_FILE_PATH = Path("data.csv")


def read_data_from_csv_file(data_file_path: Path) -> list:
    try:
        with Path.open(data_file_path, newline="") as data_file:
            data_reader = csv.reader(data_file)
            headers = next(data_reader)  # Remove the header row  # noqa: F841
            return list(data_reader)  # Return the remaining rows
    except FileNotFoundError:
        print(f"Error: {data_file_path} not found.")
        exit(1)


def read_headers_from_csv_file(data_file_path: Path) -> list:
    try:
        with Path.open(data_file_path, newline="") as data_file:
            data_reader = csv.reader(data_file)
            return next(data_reader)  # Get the first row which contains the headers
    except FileNotFoundError:
        print(f"Error: {data_file_path} not found.")
        exit(1)


def is_numeric(value: str) -> bool:
    value = value.strip()
    return value.replace(".", "", 1).replace("-", "", 1).isdigit()


def is_whole_number(value: str) -> bool:
    value = value.strip()
    return value.replace("-", "", 1).isdigit()


# function time complexity of O(n*m) and with constant it is O(2*n*m)
def data_list_to_dict(headers_list: List[str], data_list: List[List[str]]) -> Dict[str, List[Any]]:
    csv_dict: Dict[str, List[Any]] = {header: [] for header in headers_list}

    for row in data_list:
        for header, value in zip(headers_list, row):
            csv_dict[header].append(value)

    for header, values in csv_dict.items():
        if all(is_numeric(value) for value in values):
            if all(is_whole_number(value) for value in values):
                csv_dict[header] = [int(value) for value in values]
            else:
                csv_dict[header] = [float(value) for value in values]
        # # Check for non-numeric values in the column and print a warning message
        # else:
        #     non_numeric_values = [value for value in values if not is_numeric(value)]
        #     print(f"Warning: Non-numeric values found in column '{header}': {non_numeric_values}")

    return csv_dict


def print_csv_dict(csv_dict: Dict[str, List[Any]]) -> None:
    for header, values in csv_dict.items():
        print(f"{header}: {values}")


def print_data_rows(data_list) -> None:
    for row in data_list:
        date = str(row[0])
        values = float(row[1])
        print(f"{date}, {values}")


def main() -> None:
    headers_list = read_headers_from_csv_file(DATA_FILE_PATH)
    data_list = read_data_from_csv_file(DATA_FILE_PATH)
    csv_dict = data_list_to_dict(headers_list, data_list)
    # print the csv dict and the data row list to compare the results

    print("\nData Rows from CSV file:")
    print_data_rows(data_list)
    print("\nCSV Dictionary:")
    print_csv_dict(csv_dict)
    print()


if __name__ == "__main__":
    main()
