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
    # {days_left} days, {hours_left} hour
    time_left = f"{abs(td.days)} days, {td.seconds//3600} hours"
    return f"{color.yellow}{time_left}{color.end}"
    