from datetime import datetime, date
from unit_functions import color, print_line, days_hours, load_json

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

def create_task_str(key: str, task: dict, called_from: str) -> str:
    my_str= create_task_num_line(task['title'], key)
    my_str += f"{task['description']}\n\n"
    # TODO - date logic needs putting in a function.
    my_str += f"Due: {datetime.strptime(task['due_date'], DATETIME_STRING_FORMAT).date()} \t \n\n"
    my_str += f"Assigned by: {task['assigned_by']}\n"
    if called_from == "view_all":
        my_str += f"Assigned to: {task['username']}\n"
    return my_str


def create_task(task: list, called_from: str) -> str:
    my_str= create_task_num_line(task['title'], task['task_id'])
    my_str += f"{task['description']}\n\n"
    my_str += f"Due: {task['due_date'].strftime(DATETIME_STRING_FORMAT)} \t {days_hours(task['due_date'] - datetime.now())}\n\n"
    my_str += f"Assigned by: {task['assigned_by']}\n"
    if called_from == "view_all":
        my_str += f"Assigned to: {task['username']}\n"
    return my_str



def create_task_num_line(title: str, num: int, length: int=70) -> str:
    num_str = str(num)
    spacing = length - (len(title) + len(num_str))
    return f"{color.bold + title + (" "*spacing) + num_str + color.end}\n"