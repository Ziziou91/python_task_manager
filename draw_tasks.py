from datetime import datetime
from utility_functions import color, print_line, difference_between_dates

DATETIME_STRING_FORMAT = "%Y-%m-%d"

def view_all(tasks: list) -> None:
    """Reads tasks from task.txt file and prints all tasks to the console."""
    print_line()
    print(f"{'*'*31}{color.bold}All tasks{color.end}{'*'*31}")
    print_line()
    for key, task in tasks.items():
        #task_str = create_task_str(key, task, "view_all")
        #print(task_str)
        print_line()

def view_mine(tasks: dict, curr_user: str) -> None:
    """Reads tasks from task.txt file and prints only tasks assigned to user."""
    print_line()
    print(f"{'*'*31}{color.bold}My tasks{color.end}{'*'*31}")
    print_line()
    print("\n")
    for key, task in tasks.items():
        if task['username'] == curr_user:
            #task_str = create_task_str(key, task, "view_mine")
            #print(task_str)
            print_line()


