import json
import readline
from typing import Any
import datetime

class color:
    purple = '\033[95m'
    cyan = '\033[96m'
    darkcyan = '\033[36m'
    blue = '\033[94m'
    green = '\033[92m'
    yellow = '\033[93m'
    red = '\033[91m'
    bold = '\033[1m'
    underline = '\033[4m'
    end = '\033[0m'

def print_line(char="-", count=70) -> None:
    """Prints a line of characters for formatting in the terminal."""
    print(f"{char*count}")

def difference_between_dates(current_date: datetime, due_date: datetime) -> str:
    """Compares current_date and due_date. Returns difference with additional context"""
    difference = (due_date - current_date)
    if difference.days > 3:
        return f"{color.green}{difference.days} days{color.end}"
    elif difference.days >= 0:
        return f"{color.yellow}{difference.days} days{color.end}"
    elif difference.days < 0:
        return f"{color.red}{abs(difference.days)} days overdue{color.end}"

def load_json(file_name: str) -> dict:
    """Opens and loads a json file then returns."""
    try:
        file = open(file_name, "r", encoding="UTF-8")
    except FileNotFoundError as exc:
        raise FileNotFoundError(f"Error! {file_name} is an invalid path.") from exc
    else:
        with file:
            data = json.load(file)
            return data

def write_json(file_name: str, data: Any) -> None:
    """Writes data to a json file at file_name."""
    with open(file_name, "w", encoding="UTF-8") as file:
        json.dump(data, file)
