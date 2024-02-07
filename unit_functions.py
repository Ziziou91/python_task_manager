import json

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

def days_hours(td):
    # TODO colour depends on how long left to complete the task. Will also add "overdue if negative"
    time_left = f"{abs(td.days)} days, {td.seconds//3600} hours"
    return f"{color.yellow}{time_left}{color.end}"
    

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