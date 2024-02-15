"""Functionality to edit existing tasks in tasks.json"""
import re
import readline
from utility_functions import color, print_line, input_with_prefill
from draw_tasks import create_task_str

def rlinput(prompt, prefill=''):
   readline.set_startup_hook(lambda: readline.insert_text(prefill))
   try:
      return input(prompt)  # or raw_input in Python 2
   finally:
      readline.set_startup_hook()

def format_task_id(task_id: str) -> str:
    """Takes a user inputted task_id and formats it so it can be found in tasks.json"""
    task_id_no_punc = re.sub(r"[^\w\s]", "", task_id)
    leading_zeros_num = 5 - len(task_id_no_punc)
    return f"{'0'* leading_zeros_num}{task_id_no_punc}"

def get_task_by_id(tasks: dict, called_from: str, curr_user: str) -> None:
    """Takes a user input, formats and then prints the associated task."""
    wait_task = True
    while wait_task is True:
        task_id = input("\nChoose a task by typing in it's ID number, or enter '-1' to go back to the main menu: ")
        print(task_id)
        if task_id == "-1":
            return
        formatted_task_id = format_task_id(task_id)
        try:
            tasks[formatted_task_id]
        except KeyError:
            print(f"\nError! {task_id} is not a valid task ID.")
        else:
            if tasks[formatted_task_id]["username"] == curr_user or called_from == "va":
                print_line()
                print(f"{'*'*30}{color.bold}Task {formatted_task_id}{color.end}{'*'*30}")
                print_line()
                print(create_task_str(formatted_task_id, tasks[formatted_task_id], "view_all"))
                amend_task(tasks, formatted_task_id)
            else:
                print(f"\n{formatted_task_id} is not assigned to you. View this task and change it's completion status from 'view all'.")

def amend_task(tasks: dict, task_id: str) -> None:
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
            print("edit task.")
            # TODO - completed tasks cannot be edited.
            user_str = input(f"""Select what you would like to edit:
t - Edit title
d - Edit description
u - Change username
a - Amend due date
""")
            if user_str == "t":
                print(tasks[task_id]["title"])
                test = rlinput("Input new title here: ", tasks[task_id]["title"])
                print(test)

        elif menu == "c":
            print("cancel and return to menu.")
            return
        else:
            print(f"{menu} is an invalid command. Please try again.")
