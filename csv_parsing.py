import csv
from pathlib import Path
from typing import Dict, Any, List

DATA_FILE_PATH = Path("data.csv")


def read_data_from_csv_file() -> list:
    try:
        with Path.open(DATA_FILE_PATH, newline="") as data_file:
            data_reader = csv.reader(data_file)
            headers = next(data_reader)  # Remove the header row  # noqa: F841
            return list(data_reader)  # Return the remaining rows
    except FileNotFoundError:
        print(f"Error: {DATA_FILE_PATH} not found.")
        exit(1)


def read_headers_from_csv_file() -> list:
    try:
        with Path.open(DATA_FILE_PATH, newline="") as data_file:
            data_reader = csv.reader(data_file)
            return next(data_reader)  # Get the first row which contains the headers
    except FileNotFoundError:
        print(f"Error: {DATA_FILE_PATH} not found.")
        exit(1)


def data_list_to_dict(headers_list: list, data_list: list) -> Dict:
    csv_dict: Dict[str, List[Any]] = {header: [] for header in headers_list}
    for row in data_list:
        for header, value in zip(headers_list, row):
            if header == "Value":
                try:
                    value = float(value)
                except ValueError:
                    print(f"Error: {value} is not a float.")
                    exit(1)
            csv_dict[header].append(value)

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
    headers_list = read_headers_from_csv_file()
    data_list = read_data_from_csv_file()
    csv_dict = data_list_to_dict(headers_list, data_list)
    # print the csv dict and the data row list to compare the results
    print_csv_dict(csv_dict)
    print_data_rows(data_list)


if __name__ == "__main__":
    print()
    main()
