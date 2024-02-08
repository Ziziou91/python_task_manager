from datetime import datetime, date
from unit_functions import color, print_line, difference_between_dates

DATETIME_STRING_FORMAT = "%Y-%m-%d"

def view_all(tasks: list) -> None:
    """Reads tasks from task.txt file and prints all to the console."""
    print_line()
    print(f"{'*'*31}{color.bold}All tasks{color.end}{'*'*31}")
    print_line()
    for key, task in tasks.items():
        task_str = create_task_str(key, task, "view_all")
        print(task_str)
        print_line()

def view_mine(tasks: dict, curr_user: str) -> None:
    """Reads tasks from task.txt file and prints tasks assigned to user."""
    print_line()
    print(f"{'*'*31}{color.bold}My tasks{color.end}{'*'*31}")
    print_line()
    print("\n")
    for key, task in tasks.items():
        if task['username'] == curr_user:
            task_str = create_task_str(key, task, "view_mine")
            print(task_str)
            print_line()

def create_task_line(title: str, num: int, length: int=70) -> str:
    num_str = str(num)
    spacing = length - (len(title) + len(num_str))
    return f"{title + (" "*spacing) + num_str}\n"

def create_task_str(key: str, task: dict, called_from: str) -> str:
    # TODO - clean up due_date logic.
    due_date = difference_between_dates(datetime.now().date(),datetime.strptime(task['due_date'], DATETIME_STRING_FORMAT).date())
    my_str= f"{color.bold}{create_task_line(task['title'], key)}{color.end}"
    my_str += f"{task['description']}\n\n"
    my_str += f"{create_task_line(f"Due: {datetime.strptime(task['due_date'], DATETIME_STRING_FORMAT).date()}", due_date, 79)}\n"
    assigned_by = f"Assigned by: {task['assigned_by']}"
    if called_from == "view_all":
        assigned_to = f"Assigned to: {task['username']}"
        my_str += f"{create_task_line(assigned_by, assigned_to)}"
    else:
        my_str += f"{assigned_by}\n"
    return my_str

