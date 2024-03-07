"""Functionality to edit existing tasks in tasks.json"""
import re
import json
from utility_functions import color, print_line, create_task_due_date

DATETIME_STRING_FORMAT = "%Y-%m-%d"

def format_task_id(task_id: str) -> str:
    """Takes a user inputted task_id and formats it so it can be found in tasks.json"""
    task_id_no_punc = re.sub(r"[^\w\s]", "", task_id)
    leading_zeros_num = 5 - len(task_id_no_punc)
    return f"{'0'* leading_zeros_num}{task_id_no_punc}"

def amend_task(tasks: dict, task_id: str, users: dict) -> None:
    """Edit a task or amend it's completion status."""
    while True:
        complete = "complete"
        if tasks[task_id]["completed"] is True:
            complete = "incomplete"
        menu = input(f"""\nSelect one of the following options below:
m - Mark task as {complete}
e - Edit task
c - Cancel and return to main menu
: """).lower()

        if menu == "m":
            tasks[task_id]["completed"] = not tasks[task_id]["completed"]
        elif menu == "e":
            edit_task_property(tasks, task_id, users)
        elif menu == "c":
            print("cancel and return to menu.")
            return
        else:
            print(f"{menu} is an invalid command. Please try again.")

def edit_task_property(tasks: dict, task_id: str, users: dict) -> None:
    """Edit the chosen task and write changes to file."""
    if tasks[task_id]["completed"]:
        print(f"\n{color.bold}{task_id} cannot be changed as it's completed{color.end}")
        print("If you would like to edit please change status to incomplete")
        return
    else:
        print(f"\n{color.bold}Edit Task.{color.end}")
        menu = input(f"""Select what you would like to edit:
t - Edit title
d - Edit description
u - Change assigned user
a - Amend due date
""")

        if menu == "t":
            edit_task_field(tasks, task_id, "title")
        elif menu == "d":
            edit_task_field(tasks, task_id, "description")
        elif menu == "u":
            edit_task_field(tasks, task_id, "username", users)
        elif menu == "a":
            edit_task_field(tasks, task_id, "due_date")

def edit_task_field(tasks: dict, task_id: str, field: str, users: dict = None) -> None:
    """update a given field (either title or description) with a user provided input and then write to tasks.json"""
    prev_field_str = f"\n{color.bold}Previous {field}:{color.end}{color.red} {tasks[task_id][field]}{color.end}\n"
    print(prev_field_str)

    if field == "username":
        new_value = update_username(users, task_id, new_value, field)
    elif field == "due_date":
        new_value = create_task_due_date().strftime(DATETIME_STRING_FORMAT)
    else:
        new_value = input(f"Input new {field} here: ")
    tasks[task_id][field] = new_value
    task_str = create_task_str(task_id, tasks[task_id], "view_all")

    # Print the amended task.
    print(f"\nNew {field} successfully added.\n")
    print_line()
    print(f"{'*'*30}{color.bold}Task {task_id}{color.end}{'*'*30}")
    print_line()
    print(f"\n{task_str}")

    with open("tasks.json", "w", encoding="UTF-8") as f:
        json.dump(tasks, f)
    print("User successfully added.")

def update_username(users, task_id, new_value, field):
    print("\nCan be assigned to:")
    for user in users:
            print(f" - {user}")
    
    new_value = input(f"Input new {field} here: ")
    
    username_exists = False
    while not username_exists:
        if new_value not in users:
            print(f"Error! {new_value} is not a registered user. Please try again.")
            new_value = input(f"Input new {field} here, or enter 'c' to cancel: ")
        if new_value == "c":
            return
        elif new_value in users:
            username_exists = True
            users[new_value]["tasks"].append(task_id) if task_id not in users[new_value]["tasks"] else users[new_value]["tasks"]
            with open("users.json", "w", encoding="UTF-8") as f:
                json.dump(users, f)
    
    return new_value